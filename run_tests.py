#!/usr/bin/env python3
"""
Run tests for scenarios listed in scenarios.json.

Modes (per scenario):
  none    - skip
  update  - run only models that do not already have a result file
  refresh - rerun every model in models.json (overwrite those result files)

System prompt:
  - If test.json "system_prompt" is false, no system message is used.
  - Otherwise use scenarios/<name>/system.md if it exists,
    else fall back to root system.md if it exists.

run_tests.py
version 0.5.2
"""

import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
import requests

# ==========================================
# CONFIGURATION
# ==========================================
CHAT_TIMEOUT = 900   # seconds (15 minutes)
CONFIG_PATH = "config.json"
MODELS_PATH = "models.json"
SCENARIOS_PATH = "scenarios.json"
SCENARIOS_DIR = "scenarios"
RESULTS_DIR = "results"
ROOT_SYSTEM_PROMPT = "system.md"

DRY_RUN = False
FORCE_MODE = None          # None | "update" | "refresh" | "none"

# Helper model prompt (optional, used only if model is set and reachable)
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
    """Return a friendly duration string."""
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

def load_model(base_url, headers, model_key):
    url = f"{base_url}/api/v1/models/load"
    payload = {"model": model_key, "echo_load_config": True}
    print(f"  Loading {model_key} ...")
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
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

def chat(base_url, headers, model_key, messages):
    url = f"{base_url}/api/v0/chat/completions"
    payload = {
        "model": model_key,
        "messages": messages,
        "stream": False,
        "max_tokens": -1
    }
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
    """Build stats.md entirely from the stats.json content (all models)."""
    models = stats.get("models", []) if isinstance(stats, dict) else []
    if not models:
        return "# Stats\n\nNo models were run.\n"

    # Determine max questions from any model
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

def merge_stats(existing_stats, new_model_stats, scenario_name, created_str):
    """Keep old model entries; update or add the ones just tested.
    overall_seconds is recalculated from all models in the file.
    """
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

def run_one_model(base_url, headers, model, questions, system_prompt):
    """Run the full conversation for one model. Returns turns + stats dict."""
    model_key = model.get("key")
    instance_id = None
    turns = []
    question_times = []
    tps_values = []

    try:
        instance_id, context_length = load_model(base_url, headers, model_key)
        context_str = format_context(context_length)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        for q in questions:
            messages.append({"role": "user", "content": q})
            start = time.time()
            response = chat(base_url, headers, model_key, messages)
            elapsed = time.time() - start

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
            "question_times": question_times
        }
        return turns, model_stat, context_str

    except Exception as e:
        print(f"  Error with {model_key}: {e}")
        return [], {"key": model_key, "error": str(e)}, "unknown"
    finally:
        unload_model(base_url, headers, instance_id)

def run_scenario(scenario, models, base_url, headers, config, dry_run=False):
    name = scenario["scenario"]
    mode = FORCE_MODE or scenario.get("mode", "none")

    if mode == "none":
        print(f"Skipping {name} (mode=none)")
        return
    if not scenario.get("ready", False):
        print(f"Skipping {name} (not ready)")
        return

    scenario_path = Path(SCENARIOS_DIR) / name
    results_path = Path(RESULTS_DIR) / name
    results_path.mkdir(parents=True, exist_ok=True)

    test_json_path = scenario_path / "test.json"
    test_info = load_json(test_json_path, required=False) or {}

    questions = load_questions(scenario_path)
    if not questions:
        print(f"  No questions found in {name}, skipping")
        return

    system_prompt = load_system_prompt(scenario_path, test_info)

    print(f"\n=== {name}  mode={mode}  questions={len(questions)}  system={'yes' if system_prompt else 'no'} ===")

    to_run = []
    for model in models:
        rfile = result_file_for_model(results_path, model)
        if mode == "update" and rfile.exists():
            continue
        to_run.append(model)

    if not to_run:
        print("  Nothing to run")
        return

    if dry_run:
        print(f"  Would run {len(to_run)} models:")
        for m in to_run:
            print(f"    - {m.get('key')}")
        return

    shutil.copy(MODELS_PATH, results_path / "models.json")

    created_str = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    model_stats = []
    scenario_start = time.time()

    for model in to_run:
        print(f"Testing {model.get('key')}")
        turns, model_stat, context_str = run_one_model(
            base_url, headers, model, questions, system_prompt
        )

        if turns:
            md = build_result_markdown(model, created_str, context_str, turns, test_info)
            out_file = result_file_for_model(results_path, model)
            out_file.write_text(md, encoding="utf-8")
            print(f"  Wrote {out_file.name}")
            model_stat["file"] = out_file.name

        model_stats.append(model_stat)

    overall_seconds = time.time() - scenario_start

    # Write test.md
    test_md = build_test_md(test_info, name, created_str, model_stats)
    (results_path / "test.md").write_text(test_md, encoding="utf-8")

    # Merge with existing stats so removed models are kept
    # overall_seconds is recalculated from all models in the file
    stats_path = results_path / "stats.json"
    existing = load_json(stats_path, required=False) if stats_path.exists() else None
    merged = merge_stats(existing, model_stats, name, created_str)

    # Write stats.md entirely from the merged stats.json content
    stats_md = build_stats_md(merged)
    helper = try_helper_summary(config, merged.get("models", []))
    if stats_md.startswith("# Stats"):
        stats_md = f"# Stats\n\n{helper}\n\n" + "\n".join(stats_md.split("\n")[2:])
    (results_path / "stats.md").write_text(stats_md, encoding="utf-8")

    (results_path / "stats.json").write_text(json.dumps(merged, indent=2), encoding="utf-8")

    # Ensure results.md exists for cloud evaluation
    results_md = results_path / "results.md"
    if not results_md.exists():
        results_md.write_text("# Evaluation Results\n\nPaste the cloud model evaluation here.\n", encoding="utf-8")

    print(f"  Finished {name}")

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
    if DRY_RUN:
        print("DRY RUN — no models will be loaded\n")

    for scenario in scenarios:
        run_scenario(scenario, models, base_url, headers, config, dry_run=DRY_RUN)

    elapsed = time.time() - start
    print(f"\nDone in {format_duration(elapsed)}")

if __name__ == "__main__":
    main()
