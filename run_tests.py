#!/usr/bin/env python3
"""
Run tests for scenarios listed in scenarios.json.

Models are loaded once and walked through every scenario that needs them.
The model is reloaded only when the requested context length changes.
Other inference settings are sent per request.

Modes (per scenario):
  none    - skip
  update  - run only models that do not already have a result file
  refresh - rerun every model in models.json (overwrite those result files)

System prompt:
  - If test.json "system_prompt" is false, no system message is used.
  - If test.json "system" is set, use that for the system prompt.
  - Otherwise use scenarios/<relative-path>/system.md if it exists,
    else fall back to root system.md if it exists.

Scenarios:
  - The "scenario" field in scenarios.json may be a top-level folder name
    (e.g. "weather app") or a nested relative path (e.g. "bug/null pointer").
  - Both styles are supported. Results are written under the matching
    relative path under results/.

Inference:
  - USE_CUSTOM_INFER = False: do not send inference settings; LM Studio defaults are used.
  - USE_CUSTOM_INFER = True: use inference.json from the scenario folder if present,
    otherwise use the root inference.json. Missing file = LM Studio defaults.
  - Only context_length causes a model reload. Other settings are applied per chat call.

run_tests.py
version 0.9.0
"""

import json
import os
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

# ==========================================
# CONFIGURATION
# ==========================================
CONFIG_PATH = "config.json"         # LM Studio connection settings (base_url, api_token, optional helper model)
TEST_PATH = "test.json"             # Per scenario metadata (name, description, system_prompt flag, notes)
MODELS_PATH = "models.json"         # Master list of models to test (created by get_models.py)
SCENARIOS_PATH = "scenarios.json"   # List of scenarios with ready/status/mode (created by get_scenarios.py)
INFERENCE_PATH = "inference.json"   # Optional inference settings (context, temperature, top_p, etc.) used when USE_CUSTOM_INFER is True
HARDWARE_PATH = "hardware.json"     # Static hardware snapshot written at the start of each run
ROOT_STATS_PATH = "stats.json"      # System-wide model stats (VRAM/spill, times, scenarios)
ROOT_STATS_MD = "stats.md"          # Readable system-wide stats
ROOT_SYSTEM_PROMPT = "system.md"    # Fallback system prompt used if a scenario does not have its own system.md
SCENARIOS_DIR = "scenarios"         # Folder containing one subfolder per test scenario
RESULTS_DIR = "results"             # Folder where per-scenario results, stats, and snapshots are written

DRY_RUN = False                     # Set to true to print what would run without loading models or writing results
FORCE_MODE = None                   # Overrides the mode in scenarios.json: None | "update" | "refresh" | "none"
USE_CUSTOM_INFER = True             # Set to true to use inference settings from inference.json (or scenario override), set to false to use LM Studio defaults

CHAT_TIMEOUT = 900                  # Max seconds to wait for a single chat response before timing out (default is 900 seconds, which is 15 minutes)

# Hardware spill detection
INSTALLED_RAM_GB = 32               # Total system RAM in GB (used to calculate spill threshold)
INSTALLED_VRAM_GB = 16              # Total GPU VRAM in GB (reference only)
RAM_SPILL_THRESHOLD_PERCENT = 25    # If RAM usage rises by this percent during a test, then let's assume the model spilled into VRAM

# Helper model prompt (optional, used only if a helper model is set and available)
# Helper summaries are generated at the end of the full run, after all test models are unloaded.
HELPER_PROMPT = """Write a short 2-3 sentence summary of these test results. Mention overall speed and any notable differences. Keep it plain."""

def load_json(path, required=True):
    if not os.path.exists(path):
        if required:
            print(f"Missing required file: {path}")
            raise SystemExit(1)
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_headers(token):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def safe_filename(name):
    keep = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_ ."
    cleaned = "".join(c if c in keep else "-" for c in name)
    return cleaned.strip().replace("  ", " ")[:100]

def format_context(context_length):
    if not context_length:
        return "unknown"
    if context_length >= 1024 and context_length % 1024 == 0:
        return f"{context_length // 1024}K"
    return str(context_length)

def format_duration(seconds):
    if seconds is None or seconds < 0:
        return "0 s"
    total = int(round(seconds))
    if total < 60:
        return f"{total} s"
    minutes = total // 60
    secs = total % 60
    if minutes < 60:
        return f"{minutes}:{secs:02d} minutes"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}:{mins:02d} hours"

def get_ram_used_gb():
    if psutil is None:
        return None
    try:
        return psutil.virtual_memory().used / (1024 ** 3)
    except Exception:
        return None

def get_fits_memory(base_ram_gb, current_ram_gb):
    """Return True if the model appears to have spilled into RAM."""
    if base_ram_gb is None or current_ram_gb is None:
        return False
    increase = current_ram_gb - base_ram_gb
    threshold = INSTALLED_RAM_GB * (RAM_SPILL_THRESHOLD_PERCENT / 100.0)
    return increase >= threshold

def load_inference(scenario_path):
    if not USE_CUSTOM_INFER:
        return {}
    scenario_inf = scenario_path / "inference.json"
    if scenario_inf.exists():
        return load_json(scenario_inf, required=False) or {}
    root_inf = Path(INFERENCE_PATH)
    if root_inf.exists():
        return load_json(root_inf, required=False) or {}
    return {}

def unload_models(base_url, headers):
    """Unload every currently loaded model. Call this immediately before any load."""
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

def load_system_prompt(scenario_path, test_info):
    if test_info.get("system_prompt") is False:
        return None
    inline = test_info.get("system")
    if inline and str(inline).strip():
        return str(inline).strip()
    scenario_system = scenario_path / "system.md"
    if scenario_system.exists():
        return scenario_system.read_text(encoding="utf-8").strip()
    root_system = Path(ROOT_SYSTEM_PROMPT)
    if root_system.exists():
        return root_system.read_text(encoding="utf-8").strip()
    return None

def result_file_for_model(results_path, model):
    key = model.get("key") or model.get("display_name") or "unknown"
    return results_path / f"{safe_filename(key)}.md"

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
    resp = requests.post(url, headers=headers, json=payload, timeout=CHAT_TIMEOUT)
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

def build_test_md(test_info, name, created_str, summary_models):
    lines = [
        f"# Test: {test_info.get('name', name)}",
        "",
        f"**Description:** {test_info.get('description', '')}",
        "",
        f"Scenario folder: {name}  ",
        "",
        f"Run time: {created_str}  ",
        "",
        f"Models in this run: {len(summary_models)}  ",
        "",
        "## Models",
        ""
    ]
    for sm in summary_models:
        if "error" in sm:
            lines.append(f"- {sm['key']} — ERROR: {sm['error']}")
        else:
            lines.append(
                f"- {sm.get('display_name') or sm['key']} "
                f"({sm.get('params') or '?'} / {sm.get('quant') or '?'} / {sm.get('size_gb')} GB) "
                f"Context: {sm.get('context')} → `{sm.get('file')}`"
            )
    return "\n".join(lines) + "\n"

def build_stats_md(stats):
    models = stats.get("models", []) if isinstance(stats, dict) else []
    if not models:
        return "# Stats\n\nNo models were run.\n"

    question_count = 0
    for m in models:
        qtimes = m.get("question_times") or []
        question_count = max(question_count, len(qtimes))

    rows = []
    for ms in models:
        if "error" in ms:
            continue
        name = ms.get("display_name") or ms.get("key") or "-"
        avg = f"{ms.get('avg_tps', 0):.0f}" if ms.get("avg_tps") is not None else "-"
        total = format_duration(ms.get("total_seconds")) if ms.get("total_seconds") is not None else "-"
        qtimes = ms.get("question_times") or []
        q_cells = []
        for i in range(question_count):
            if i < len(qtimes) and qtimes[i] is not None:
                q_cells.append(format_duration(qtimes[i]))
            else:
                q_cells.append("-")
        rows.append([name, avg, total] + q_cells)

    if not rows:
        return "# Stats\n\nNo successful model runs.\n"

    headers = ["Model", "Avg t/s", "Total time"] + [f"Q{i+1}" for i in range(question_count)]

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def pad_row(cells):
        return "| " + " | ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(cells)) + " |"

    lines = ["# Stats", ""]
    overall = stats.get("overall_seconds")
    if overall is not None:
        lines.append(f"Overall time (all models): {format_duration(overall)}")
        lines.append("")
    lines.append(pad_row(headers))
    lines.append("| " + " | ".join("-" * col_widths[i] for i in range(len(headers))) + " |")
    for row in rows:
        lines.append(pad_row(row))

    return "\n".join(lines) + "\n"

def build_root_stats_md(system_stats, overall_seconds):
    if not system_stats:
        return "# System Stats\n\nNo models were run.\n"

    rows = []
    for ms in system_stats:
        name = ms.get("display_name") or ms.get("key") or "-"
        avg = f"{ms.get('avg_tps', 0):.0f}" if ms.get("avg_tps") is not None else "-"
        total = format_duration(ms.get("total_seconds")) if ms.get("total_seconds") is not None else "-"
        used = "yes" if ms.get("used_ram") else "no"
        peak = f"{ms.get('peak_ram_gb')} GB" if ms.get("peak_ram_gb") is not None else "-"
        scen_count = len(ms.get("scenarios") or [])
        rows.append([name, avg, total, used, peak, str(scen_count)])

    headers = ["Model", "Avg t/s", "Total time", "Used RAM", "Peak RAM", "Scenarios"]

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def pad_row(cells):
        return "| " + " | ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(cells)) + " |"

    lines = ["# System Stats", ""]
    if overall_seconds is not None:
        lines.append(f"Overall time (all models): {format_duration(overall_seconds)}")
        lines.append("")
    lines.append(pad_row(headers))
    lines.append("| " + " | ".join("-" * col_widths[i] for i in range(len(headers))) + " |")
    for row in rows:
        lines.append(pad_row(row))

    return "\n".join(lines) + "\n"

def merge_stats(existing_stats, new_model_stats, scenario_name, created_str):
    if not existing_stats or not isinstance(existing_stats, dict):
        existing_stats = {"models": []}

    old_models = {m.get("key"): m for m in existing_stats.get("models", []) if m.get("key")}
    for ms in new_model_stats:
        key = ms.get("key")
        if key:
            old_models[key] = ms

    ordered = []
    seen = set()
    for m in existing_stats.get("models", []):
        key = m.get("key")
        if key and key in old_models and key not in seen:
            ordered.append(old_models[key])
            seen.add(key)
    for key, ms in old_models.items():
        if key not in seen:
            ordered.append(ms)

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

def try_helper_summary(config, model_stats):
    model = config.get("model") if config else None
    if not model or not model_stats:
        return "Here is the summary results."

    base_url = config.get("base_url", "http://localhost:1234").rstrip("/")
    token = config.get("api_token", "")
    headers = get_headers(token)

    brief = []
    for ms in model_stats:
        if "error" not in ms:
            brief.append(f"{ms.get('display_name') or ms['key']}: {ms.get('avg_tps', 0):.0f} t/s")

    try:
        resp = requests.post(
            f"{base_url}/api/v0/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": HELPER_PROMPT},
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
        return text or "Here is the summary results."
    except Exception:
        return "Here is the summary results."

def run_questions_for_scenario(base_url, headers, model, item, peak_ram, base_ram_gb):
    """Run all questions for one scenario while the model is already loaded.
    Returns turns, model_stat (no RAM fields), updated peak_ram, context_str.
    """
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

        context_length = inference.get("context_length")
        context_str = format_context(context_length)

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
            "avg_tps": avg_tps,
            "total_seconds": total_seconds,
            "question_times": question_times,
            "scenario": item["name"]
        }
        return turns, model_stat, peak_ram, context_str

    except Exception as e:
        print(f"  Error with {model_key} on {item['name']}: {e}")
        return [], {"key": model_key, "error": str(e), "scenario": item["name"]}, peak_ram, "unknown"

def update_scenario_files(results_path, test_info, name, model, model_stat, turns, context_str):
    """Write the result markdown and merge stats / models snapshot / test.md for one scenario."""
    results_path.mkdir(parents=True, exist_ok=True)
    created_str = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")

    if turns:
        md = build_result_markdown(model, created_str, context_str, turns, test_info)
        out_file = result_file_for_model(results_path, model)
        out_file.write_text(md, encoding="utf-8")
        print(f"  Wrote {out_file.name}")
        model_stat["file"] = out_file.name

    # Merge models.json snapshot
    models_snapshot_path = results_path / "models.json"
    existing_models = load_json(models_snapshot_path, required=False) if models_snapshot_path.exists() else []
    if not isinstance(existing_models, list):
        existing_models = []
    model_map = {m.get("key"): m for m in existing_models if m.get("key")}
    if model.get("key"):
        model_map[model["key"]] = model
    merged_models = list(model_map.values())
    models_snapshot_path.write_text(json.dumps(merged_models, indent=2), encoding="utf-8")

    # Merge stats
    stats_path = results_path / "stats.json"
    existing = load_json(stats_path, required=False) if stats_path.exists() else None
    merged = merge_stats(existing, [model_stat], name, created_str)
    (results_path / "stats.json").write_text(json.dumps(merged, indent=2), encoding="utf-8")

    # Write stats.md without helper (helper is added at the very end)
    stats_md = build_stats_md(merged)
    (results_path / "stats.md").write_text(stats_md, encoding="utf-8")

    # Rebuild test.md from current merged models
    test_md = build_test_md(test_info, name, created_str, merged.get("models", []))
    (results_path / "test.md").write_text(test_md, encoding="utf-8")

    # Ensure results.md exists
    results_md = results_path / "results.md"
    if not results_md.exists():
        results_md.write_text("# Evaluation Results\n\nPaste the cloud model evaluation here.\n", encoding="utf-8")

def get_work_for_model(model, scenarios):
    """Return list of scenario work items this model still needs to run."""
    work = []
    for scenario in scenarios:
        name = scenario["scenario"]
        mode = FORCE_MODE or scenario.get("mode", "none")
        if mode == "none" or not scenario.get("ready", False):
            continue

        scenario_path = Path(SCENARIOS_DIR) / name
        results_path = Path(RESULTS_DIR) / name

        questions = load_questions(scenario_path)
        if not questions:
            continue

        rfile = result_file_for_model(results_path, model)
        if mode == "update" and rfile.exists():
            continue

        test_json_path = scenario_path / "test.json"
        test_info = load_json(test_json_path, required=False) or {}
        system_prompt = load_system_prompt(scenario_path, test_info)
        inference = load_inference(scenario_path)
        context = inference.get("context_length")  # None means LMS default

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

def write_hardware_json():
    hw = {
        "installed_ram_gb": INSTALLED_RAM_GB,
        "installed_vram_gb": INSTALLED_VRAM_GB,
        "ram_spill_threshold_percent": RAM_SPILL_THRESHOLD_PERCENT,
        "base_ram_gb": get_ram_used_gb(),
        "collected_at": datetime.now().isoformat()
    }
    Path(HARDWARE_PATH).write_text(json.dumps(hw, indent=2), encoding="utf-8")

def main():
    start = time.time()
    config = load_json(CONFIG_PATH)
    models = load_json(MODELS_PATH)
    scenarios = load_json(SCENARIOS_PATH)

    if not isinstance(scenarios, list):
        print("scenarios.json must be a list")
        raise SystemExit(1)

    base_url = config.get("base_url", "http://localhost:1234").rstrip("/")
    token = config.get("api_token", "")
    headers = get_headers(token)

    print(f"Models available: {len(models)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Custom inference: {'on' if USE_CUSTOM_INFER else 'off (LMS defaults)'}")

    base_ram_gb = get_ram_used_gb()
    write_hardware_json()
    if base_ram_gb:
        print(f"Base RAM used: {base_ram_gb:.1f} GB")

    if DRY_RUN:
        print("DRY RUN — no models will be loaded\n")

    system_model_stats = []
    touched_scenarios = set()

    try:
        for model in models:
            model_key = model.get("key")
            work = get_work_for_model(model, scenarios)
            if not work:
                continue

            # Sort by context length descending (None / LMS default last)
            work.sort(key=lambda s: s["context"] if s["context"] is not None else -1, reverse=True)

            print(f"\n=== Model {model_key}  scenarios={len(work)} ===")
            if DRY_RUN:
                for item in work:
                    ctx = format_context(item["context"]) if item["context"] else "LMS"
                    print(f"  Would run {item['name']} (context {ctx})")
                continue

            current_context = object()  # sentinel, different from any real value including None
            peak_ram = base_ram_gb
            model_scenario_stats = []

            for item in work:
                needed = item["context"]
                if needed != current_context:
                    unload_models(base_url, headers)
                    try:
                        instance_id, loaded_context = load_model(base_url, headers, model_key, item["inference"])
                        current_context = needed
                        print(f"  Loaded with context {format_context(loaded_context or needed)}")
                    except Exception as e:
                        print(f"  Failed to load {model_key}: {e}")
                        # Record error for this scenario and continue
                        err_stat = {"key": model_key, "error": str(e), "scenario": item["name"]}
                        update_scenario_files(
                            item["results_path"], item["test_info"], item["name"],
                            model, err_stat, [], "unknown"
                        )
                        touched_scenarios.add(item["name"])
                        continue

                turns, scen_stat, peak_ram, context_str = run_questions_for_scenario(
                    base_url, headers, model, item, peak_ram, base_ram_gb
                )
                update_scenario_files(
                    item["results_path"], item["test_info"], item["name"],
                    model, scen_stat, turns, context_str
                )
                touched_scenarios.add(item["name"])
                if "error" not in scen_stat:
                    model_scenario_stats.append(scen_stat)

            unload_models(base_url, headers)

            # System-wide stats for this model
            if model_scenario_stats or peak_ram != base_ram_gb:
                total_sec = sum(s.get("total_seconds", 0) or 0 for s in model_scenario_stats)
                avgs = [s.get("avg_tps") for s in model_scenario_stats if s.get("avg_tps") is not None]
                avg_tps = sum(avgs) / len(avgs) if avgs else 0
                used_ram = get_fits_memory(base_ram_gb, peak_ram)
                system_model_stats.append({
                    "key": model_key,
                    "display_name": model.get("display_name"),
                    "params": model.get("params"),
                    "quant": model.get("quant"),
                    "size_gb": model.get("size_gb"),
                    "avg_tps": avg_tps,
                    "total_seconds": total_sec,
                    "used_ram": used_ram,
                    "peak_ram_gb": round(peak_ram, 1) if peak_ram else None,
                    "scenarios": [s.get("scenario") for s in model_scenario_stats]
                })

        elapsed = time.time() - start

        if not DRY_RUN:
            # Write root-level system stats
            root_stats = {
                "run_time": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
                "overall_seconds": elapsed,
                "models": system_model_stats
            }
            Path(ROOT_STATS_PATH).write_text(json.dumps(root_stats, indent=2), encoding="utf-8")
            root_md = build_root_stats_md(system_model_stats, elapsed)
            Path(ROOT_STATS_MD).write_text(root_md, encoding="utf-8")
            print(f"\nWrote {ROOT_STATS_PATH} and {ROOT_STATS_MD}")

            # Helper summaries at the end (after all test models are unloaded)
            if config.get("model") and touched_scenarios:
                print("\nGenerating helper summaries...")
                unload_models(base_url, headers)
                for name in sorted(touched_scenarios):
                    results_path = Path(RESULTS_DIR) / name
                    stats_path = results_path / "stats.json"
                    if not stats_path.exists():
                        continue
                    stats = load_json(stats_path, required=False)
                    helper = try_helper_summary(config, stats.get("models", []))
                    stats_md = build_stats_md(stats)
                    if stats_md.startswith("# Stats"):
                        stats_md = f"# Stats\n\n{helper}\n\n" + "\n".join(stats_md.split("\n")[2:])
                    (results_path / "stats.md").write_text(stats_md, encoding="utf-8")
                    print(f"  Updated summary for {name}")

        # Refresh scenario status files so scenarios.json and scenarios.md match the run
        if not DRY_RUN:
            scenarios_script = Path("get_scenarios.py")
            if scenarios_script.exists():
                print("\nUpdating scenario status...")
                try:
                    subprocess.run([sys.executable, str(scenarios_script)], check=False)
                except Exception as e:
                    print(f"Warning: could not run get_scenarios.py: {e}")
            else:
                print("\nNote: get_scenarios.py not found, scenario status not refreshed.")

        print(f"\nDone in {format_duration(elapsed)}")

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
