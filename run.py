#!/usr/bin/env python3
"""
Run tests for scenarios listed in scenarios/scenarios.json.

Models are loaded once and walked through every scenario that needs them.
The model is reloaded only when the requested context length changes.
Other inference settings are sent per request.

Modes (per scenario):
  none    - skip
  update  - run only models that do not already have a result file
  refresh - rerun every model in models.json (overwrite those result files)

System prompt and inference:
  Look for system.md / inference.json starting at the scenario folder,
  then each parent group folder, then scenarios/ root. Highest precedence first.
  test.json can still override the system prompt directly.

scenarios/models.json is the active list and is not modified.
results/<scenario>/models.json is the historic record. A successful test
updates that model key and leaves every other model in place.

run.py
version 0.12.0
"""

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

try:
    import psutil
except ImportError:
    psutil = None

import config
import utils


def get_ram_used_gb():
    if psutil is None:
        return None
    try:
        return psutil.virtual_memory().used / (1024 ** 3)
    except Exception:
        return None


def spilled_to_ram(base_ram_gb, current_ram_gb):
    """True when system RAM rose enough that the model spilled out of VRAM."""
    if base_ram_gb is None or current_ram_gb is None:
        return False
    increase = current_ram_gb - base_ram_gb
    threshold = config.INSTALLED_RAM_GB * (config.RAM_SPILL_THRESHOLD_PERCENT / 100.0)
    return increase >= threshold


def context_length_from(value):
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)) and value > 0:
        return int(value)
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if text.isdigit():
            number = int(text)
            return number if number > 0 else None
    return None


def resolve_context_length(loaded_context, inference):
    """Loaded LM Studio context, then inference.json, then 16K."""
    loaded = context_length_from(loaded_context)
    if loaded:
        return loaded
    configured = context_length_from((inference or {}).get("context_length"))
    if configured:
        return configured
    return config.DEFAULT_CONTEXT_LENGTH


def unload_models(base_url, headers):
    try:
        resp = requests.get(f"{base_url}/api/v1/models", headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        instances = []
        for m in data.get("models", []):
            for inst in m.get("loaded_instances", []):
                iid = inst.get("id")
                if iid:
                    instances.append(iid)
        if not instances:
            print("No models currently loaded.")
            return
        print(f"Unloading {len(instances)} loaded model(s)...")
        for iid in instances:
            unload_model(base_url, headers, iid)
    except Exception as e:
        print(f"Warning: could not unload existing models: {e}")


def load_questions(scenario_path):
    questions = []
    i = 1
    while True:
        qfile = scenario_path / f"question{i}.md"
        if not qfile.exists():
            qfile = scenario_path / f"Question{i}.md"
            if not qfile.exists():
                break
        questions.append(qfile.read_text(encoding="utf-8").strip())
        i += 1
    return questions


def load_model(base_url, headers, model_key, inference):
    url = f"{base_url}/api/v1/models/load"
    payload = {"model": model_key, "echo_load_config": True}
    if inference.get("context_length"):
        payload["context_length"] = inference["context_length"]
    print(f"  Loading {model_key} ...")
    resp = requests.post(url, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    data = resp.json()
    context = None
    if data.get("load_config"):
        context = data["load_config"].get("context_length")
    return data.get("instance_id"), context


def unload_model(base_url, headers, instance_id):
    if not instance_id:
        return
    url = f"{base_url}/api/v1/models/unload"
    try:
        requests.post(url, headers=headers, json={"instance_id": instance_id}, timeout=30)
        print(f"  Unloaded {instance_id}")
    except Exception as e:
        print(f"  Warning: could not unload {instance_id}: {e}")


def chat(base_url, headers, model_key, messages, inference):
    url = f"{base_url}/api/v0/chat/completions"
    payload = {
        "model": model_key,
        "messages": messages,
        "stream": False,
        "max_tokens": -1
    }
    for key in ("temperature", "top_p", "top_k", "repeat_penalty", "reasoning_effort"):
        if key in inference and inference[key] is not None:
            payload[key] = inference[key]
    resp = requests.post(url, headers=headers, json=payload, timeout=config.CHAT_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def build_result_markdown(model_info, created_str, context_str, turns, test_info):
    lines = []
    name = model_info.get("display_name") or model_info.get("key")
    lines.append(f"# {name}")
    lines.append(f"Model: {model_info.get('key')}")
    lines.append(f"Test: {test_info.get('name', '')}")
    lines.append(f"Created: {created_str}")
    lines.append("Exported from: LM Studio (via test script)")
    lines.append(f"Context {context_str}")
    lines.append("")
    for turn in turns:
        lines.append("> #### 💬 User")
        lines.append("")
        lines.append(turn["user"])
        lines.append("")
        lines.append("> #### 🤖 Assistant")
        lines.append("")
        lines.append(turn["assistant"])
        lines.append("")
        if turn.get("stats_line"):
            lines.append(turn["stats_line"])
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def merge_stats(existing_stats, new_model_stats, scenario_name, created_str):
    if not existing_stats or not isinstance(existing_stats, dict):
        existing_stats = {"models": []}
    ordered = utils.keyed_records(existing_stats.get("models"))
    for ms in new_model_stats:
        if not isinstance(ms, dict) or not ms.get("key") or "error" in ms:
            continue
        ordered = utils.upsert_record(ordered, ms)
    total_seconds = sum(
        m.get("total_seconds", 0) or 0
        for m in ordered
        if "error" not in m
    )
    return {
        "scenario": scenario_name,
        "run_time": created_str,
        "overall_seconds": total_seconds,
        "models": ordered
    }


def try_helper_summary(model_stats):
    if not config.HELPER_MODEL or not model_stats:
        return None
    brief = []
    for ms in model_stats:
        if "error" not in ms and ms.get("key"):
            brief.append(f"{ms.get('display_name') or ms['key']}: {ms.get('avg_tps', 0):.0f} t/s")
    if not brief:
        return None
    try:
        resp = requests.post(
            f"{config.BASE_URL.rstrip('/')}/api/v0/chat/completions",
            headers=utils.get_headers(),
            json={
                "model": config.HELPER_MODEL,
                "messages": [
                    {"role": "system", "content": config.RUN_SUMMARY_PROMPT},
                    {"role": "user", "content": "\n".join(brief)}
                ],
                "stream": False,
                "max_tokens": 150
            },
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return text or None
    except Exception:
        return None


def run_questions_for_scenario(base_url, headers, model, item, peak_ram, base_ram_gb, context_length):
    model_key = model.get("key")
    questions = item["questions"]
    system_prompt = item["system_prompt"]
    inference = item["inference"]
    turns = []
    question_times = []
    tps_values = []
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        context_str = utils.format_context(context_length)
        for q in questions:
            messages.append({"role": "user", "content": q})
            start = time.time()
            response = chat(base_url, headers, model_key, messages, inference)
            elapsed = time.time() - start
            current_ram = get_ram_used_gb()
            if current_ram and (peak_ram is None or current_ram > peak_ram):
                peak_ram = current_ram
            choice = response.get("choices", [{}])[0]
            assistant_text = choice.get("message", {}).get("content", "").strip()
            messages.append({"role": "assistant", "content": assistant_text})
            usage = response.get("usage", {})
            stats = response.get("stats", {})
            completion_tokens = usage.get("completion_tokens", 0)
            gen_time = stats.get("generation_time", elapsed)
            tps = stats.get("tokens_per_second")
            if tps is None and gen_time and completion_tokens:
                tps = completion_tokens / gen_time
            if tps is not None:
                tps_values.append(tps)
            question_times.append(gen_time)
            context_used = usage.get("total_tokens", 0)
            pct = 0
            if context_length and context_used:
                pct = round((context_used / context_length) * 100)
            stats_parts = []
            if tps is not None:
                stats_parts.append(f"{tps:.0f} t/s")
            if completion_tokens:
                stats_parts.append(f"{completion_tokens} tokens")
            stats_parts.append(f"{gen_time:.0f}s")
            if pct:
                stats_parts.append(f"{pct}%")
            turns.append({
                "user": q,
                "assistant": assistant_text,
                "stats_line": ", ".join(stats_parts) if stats_parts else None
            })
        avg_tps = sum(tps_values) / len(tps_values) if tps_values else 0
        total_seconds = sum(question_times)
        model_stat = {
            "key": model_key,
            "display_name": model.get("display_name"),
            "params": model.get("params"),
            "quant": model.get("quant"),
            "size_gb": model.get("size_gb"),
            "context": context_str,
            "context_length": context_length,
            "avg_tps": avg_tps,
            "total_seconds": total_seconds,
            "question_times": question_times,
            "scenario": item["name"]
        }
        return turns, model_stat, peak_ram, context_str
    except Exception as e:
        print(f"  Error with {model_key} on {item['name']}: {e}")
        return [], {"key": model_key, "error": str(e), "scenario": item["name"]}, peak_ram, "unknown"


def write_transcript_json(path, model, name, test_info, created_str, context_length, system_prompt, turns):
    """Chat transcript for reconstruction. system_prompt is a field, not a message."""
    messages = []
    for turn in turns:
        messages.append({"role": "user", "content": turn["user"]})
        assistant = {"role": "assistant", "content": turn["assistant"]}
        if turn.get("stats_line"):
            assistant["stats_line"] = turn["stats_line"]
        messages.append(assistant)
    record = {
        "key": model.get("key"),
        "display_name": model.get("display_name"),
        "scenario": name,
        "test": test_info.get("name") or "",
        "created": created_str,
        "context_length": context_length,
        "system_prompt": system_prompt or None,
        "messages": messages,
    }
    utils.save_json(path, record)


def update_scenario_files(results_path, test_info, name, model, model_stat, turns, context_str, context_length, system_prompt):
    results_path.mkdir(parents=True, exist_ok=True)
    created_str = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    if turns:
        md = build_result_markdown(model, created_str, context_str, turns, test_info)
        out_file = utils.result_file_for_model(results_path, model)
        out_file.write_text(md, encoding="utf-8")
        json_file = utils.transcript_json_for_model(results_path, model)
        write_transcript_json(
            json_file, model, name, test_info, created_str,
            context_length, system_prompt, turns,
        )
        print(f"  Wrote {out_file.name}")
        model_stat["file"] = out_file.name

    models_snapshot_path = results_path / "models.json"
    existing_models = utils.load_json(models_snapshot_path, required=False) if models_snapshot_path.exists() else []
    if model.get("key"):
        existing_models = utils.upsert_record(existing_models, model)
        utils.save_json(models_snapshot_path, existing_models)

    stats_path = results_path / "stats.json"
    existing = utils.load_json(stats_path, required=False) if stats_path.exists() else None
    merged = merge_stats(existing, [model_stat], name, created_str)
    utils.save_json(stats_path, merged)

    (results_path / "stats.md").write_text(utils.build_stats_md(merged), encoding="utf-8")

    # Keep the evaluation block as it was written. evaluate.py owns that section.
    existing_test = results_path / "test.md"
    eval_section = ""
    if existing_test.exists():
        eval_section = utils.evaluation_section(existing_test.read_text(encoding="utf-8"))

    test_md = utils.build_test_md(test_info, name, created_str, merged.get("models", []))
    (results_path / "test.md").write_text(utils.append_evaluation_section(test_md, eval_section), encoding="utf-8")

    results_md = results_path / "results.md"
    if not results_md.exists():
        results_md.write_text("# Evaluation Results\n\nPaste the cloud model evaluation here.\n", encoding="utf-8")


def get_work_for_model(model, scenarios):
    work = []
    for scenario in scenarios:
        name = scenario["scenario"]
        mode = config.FORCE_MODE or scenario.get("mode") or config.DEFAULT_MODE
        if mode == "none" or not scenario.get("ready", False):
            continue
        scenario_path = config.SCENARIOS_DIR / name
        results_path = config.RESULTS_DIR / name
        questions = load_questions(scenario_path)
        if not questions:
            continue
        rfile = utils.result_file_for_model(results_path, model)
        if mode == "update" and rfile.exists():
            continue
        test_json_path = scenario_path / config.TEST_JSON
        test_info = utils.load_json(test_json_path, required=False) or {}
        system_prompt = utils.load_system_prompt(scenario_path, test_info)
        inference = utils.load_inference(scenario_path)
        context = inference.get("context_length")
        work.append({
            "name": name,
            "scenario_path": scenario_path,
            "results_path": results_path,
            "questions": questions,
            "system_prompt": system_prompt,
            "inference": inference,
            "context": context,
            "test_info": test_info,
            "mode": mode
        })
    return work


def backfill_historic_models(models, scenarios):
    """
    If a result file exists for an active model and that key is missing from the
    scenario's historic models.json, add the record. Existing records are not replaced.
    """
    added = 0
    for scenario in scenarios:
        mode = config.FORCE_MODE or scenario.get("mode") or config.DEFAULT_MODE
        if mode == "none" or not scenario.get("ready", False):
            continue
        name = scenario.get("scenario")
        if not name:
            continue
        results_path = config.RESULTS_DIR / name
        models_path = results_path / "models.json"
        existing = utils.keyed_records(utils.load_json(models_path, required=False) if models_path.exists() else [])
        have = {record["key"] for record in existing}
        changed = False
        for model in models:
            key = model.get("key")
            if not key or key in have:
                continue
            if not utils.result_file_for_model(results_path, model).exists():
                continue
            existing = utils.upsert_record(existing, model)
            have.add(key)
            changed = True
            added += 1
        if changed:
            utils.save_json(models_path, existing)
    return added


def write_hardware_json():
    hw = {
        "installed_ram_gb": config.INSTALLED_RAM_GB,
        "installed_vram_gb": config.INSTALLED_VRAM_GB,
        "ram_spill_threshold_percent": config.RAM_SPILL_THRESHOLD_PERCENT,
        "base_ram_gb": get_ram_used_gb(),
        "collected_at": datetime.now().isoformat()
    }
    utils.save_json(config.HARDWARE_PATH, hw)


def main():
    start = time.time()
    models = utils.keyed_records(utils.load_json(config.MODELS_PATH))
    scenarios_raw = utils.load_json(config.SCENARIOS_JSON)
    if isinstance(scenarios_raw, list) or (
        isinstance(scenarios_raw, dict)
        and all(isinstance(value, dict) for value in scenarios_raw.values())
    ):
        scenarios = utils.keyed_records(scenarios_raw, "scenario")
    else:
        print("scenarios.json must be a list of scenario records")
        raise SystemExit(1)

    base_url = config.BASE_URL.rstrip("/")
    headers = utils.get_headers()

    print(f"Models available: {len(models)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Custom inference: {'on' if config.USE_CUSTOM_INFER else 'off (LMS defaults)'}")

    base_ram_gb = get_ram_used_gb()
    if base_ram_gb:
        print(f"Base RAM used: {base_ram_gb:.1f} GB")

    if config.DRY_RUN:
        print("DRY RUN — no models will be loaded and no result files will be written\n")
    else:
        write_hardware_json()
        added = backfill_historic_models(models, scenarios)
        if added:
            print(f"Added {added} missing historic model record(s) for result files that already exist.")

    touched_scenarios = set()
    ram_updates = {}

    try:
        for model in models:
            model_key = model.get("key")
            if not model_key:
                continue
            work = get_work_for_model(model, scenarios)
            if not work:
                continue
            work.sort(key=lambda s: s["context"] if s["context"] is not None else -1, reverse=True)
            print(f"\n=== Model {model_key}  scenarios={len(work)} ===")
            if config.DRY_RUN:
                for item in work:
                    ctx = utils.format_context(item["context"]) if item["context"] else "LMS"
                    print(f"  Would run {item['name']} (context {ctx})")
                continue

            current_context = object()
            loaded_context = None
            peak_ram = base_ram_gb
            model_scenario_stats = []

            for item in work:
                print(f"  Running {item['name']}")

                needed = item["context"]
                if needed != current_context:
                    unload_models(base_url, headers)
                    try:
                        instance_id, loaded_context = load_model(base_url, headers, model_key, item["inference"])
                        current_context = needed
                    except Exception as e:
                        print(f"  Failed to load {model_key}: {e}")
                        print("  Left existing results for this scenario unchanged.")
                        continue

                context_length = resolve_context_length(loaded_context, item["inference"])
                print(f"  Context {utils.format_context(context_length)}")

                turns, scen_stat, peak_ram, context_str = run_questions_for_scenario(
                    base_url, headers, model, item, peak_ram, base_ram_gb, context_length
                )
                if "error" in scen_stat or not turns:
                    print("  Left existing results for this scenario unchanged.")
                    continue
                update_scenario_files(
                    item["results_path"], item["test_info"], item["name"],
                    model, scen_stat, turns, context_str, context_length,
                    item["system_prompt"],
                )
                touched_scenarios.add(item["name"])
                model_scenario_stats.append(scen_stat)

            unload_models(base_url, headers)

            if model_scenario_stats:
                ram_updates[model_key] = {
                    "used_ram": spilled_to_ram(base_ram_gb, peak_ram),
                    "peak_ram_gb": round(peak_ram, 1) if peak_ram else None,
                }

        elapsed = time.time() - start

        if not config.DRY_RUN and touched_scenarios:
            previous_root = utils.load_json(config.ROOT_STATS_JSON, required=False)
            previous_models = previous_root.get("models") if isinstance(previous_root, dict) else []
            root_models = utils.aggregate_root_models(previous_models, ram_updates)
            root_stats = {
                "run_time": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
                "overall_seconds": elapsed,
                "models": root_models
            }
            utils.save_json(config.ROOT_STATS_JSON, root_stats)
            config.ROOT_STATS_MD.write_text(utils.build_root_stats_md(root_models, elapsed), encoding="utf-8")
            print(f"\nUpdated {config.ROOT_STATS_JSON} and {config.ROOT_STATS_MD}")

            if config.HELPER_MODEL:
                print("\nGenerating helper summaries...")
                unload_models(base_url, headers)
                for name in sorted(touched_scenarios):
                    results_path = config.RESULTS_DIR / name
                    stats_path = results_path / "stats.json"
                    if not stats_path.exists():
                        continue
                    stats = utils.load_json(stats_path, required=False)
                    info_path = utils.write_info_md(results_path / "info.md", try_helper_summary(stats.get("models", [])))
                    if info_path:
                        print(f"  Wrote {info_path}")
                    else:
                        print(f"  Helper summary skipped for {name}")

        if not config.DRY_RUN:
            scenarios_script = Path("scenarios.py")
            if scenarios_script.exists():
                print("\nUpdating scenario status...")
                try:
                    subprocess.run([sys.executable, str(scenarios_script)], check=False)
                except Exception as e:
                    print(f"Warning: could not run scenarios.py: {e}")
            else:
                print("\nNote: scenarios.py not found, scenario status not refreshed.")

        print(f"\nDone in {utils.format_duration(elapsed)}")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user (Ctrl-C).")
        print("Unloading any loaded models...")
        try:
            unload_models(base_url, headers)
        except Exception:
            pass
        print("Shutdown complete.")
        sys.exit(130)


if __name__ == "__main__":
    main()
