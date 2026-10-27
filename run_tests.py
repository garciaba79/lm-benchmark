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
version 0.5.1
"""

import json
import os
import re
import shutil
import time
from datetime import datetime
from pathlib import Path
import requests

# ==========================================
# CONFIGURATION
# ==========================================
CONFIG_PATH = "config.json"
MODELS_PATH = "models.json"
SCENARIOS_PATH = "scenarios.json"
SCENARIOS_DIR = "scenarios"
RESULTS_DIR = "results"
ROOT_SYSTEM_PROMPT = "system.md"

# Command-line style overrides (set here or pass via env later)
DRY_RUN = False
FORCE_MODE = None          # None | "update" | "refresh" | "none"  (overrides scenarios.json)

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

def load_questions(scenario_path):
    questions = []
    i = 1
    while True:
        qfile = scenario_path / f"question{i}.md"
        if not qfile.exists():
            # also accept Question1.md etc.
            qfile = scenario_path / f"Question{i}.md"
            if not qfile.exists():
                break
        questions.append(qfile.read_text(encoding="utf-8").strip())
        i += 1
    return questions

def load_system_prompt(scenario_path, test_info):
    # Explicit disable
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
    resp = requests.post(url, headers=headers, json=payload, timeout=300)
    resp.raise_for_status()
    return resp.json()

def build_markdown(model_info, created_str, context_str, turns, test_info):
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
        lines.append("### User")
        lines.append("")
        lines.append(turn["user"])
        lines.append("")
        lines.append("### Assistant")
        lines.append("")
        lines.append(turn["assistant"])
        lines.append("")
        if turn.get("stats_line"):
            lines.append(turn["stats_line"])
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"

def run_scenario(scenario, models, base_url, headers, dry_run=False):
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

    # Load test.json
    test_json_path = scenario_path / "test.json"
    test_info = {}
    if test_json_path.exists():
        try:
            test_info = json.loads(test_json_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  Warning: could not read test.json: {e}")

    questions = load_questions(scenario_path)
    if not questions:
        print(f"  No questions found in {name}, skipping")
        return

    system_prompt = load_system_prompt(scenario_path, test_info)

    print(f"\n=== {name}  mode={mode}  questions={len(questions)}  system={'yes' if system_prompt else 'no'} ===")

    # Decide which models to run
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

    # Snapshot models.json
    shutil.copy(MODELS_PATH, results_path / "models.json")

    created_str = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    summary_models = []

    for model in to_run:
        model_key = model.get("key")
        if not model_key:
            continue

        print(f"Testing {model_key}")
        instance_id = None
        turns = []

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

            md = build_markdown(model, created_str, context_str, turns, test_info)
            out_file = result_file_for_model(results_path, model)
            out_file.write_text(md, encoding="utf-8")
            print(f"  Wrote {out_file.name}")

            summary_models.append({
                "key": model_key,
                "display_name": model.get("display_name"),
                "params": model.get("params"),
                "quant": model.get("quant"),
                "size_gb": model.get("size_gb"),
                "context": context_str,
                "file": out_file.name
            })

        except Exception as e:
            print(f"  Error with {model_key}: {e}")
            summary_models.append({"key": model_key, "error": str(e)})
        finally:
            unload_model(base_url, headers, instance_id)

    # Write summary and empty results.md
    summary_lines = [
        f"# Test Summary: {test_info.get('name', name)}",
        "",
        f"**Description:** {test_info.get('description', '')}",
        "",
        f"**Scenario folder:** {name}",
        f"**Run time:** {created_str}",
        f"**Models in this run:** {len(summary_models)}",
        "",
        "## Models",
        ""
    ]
    for sm in summary_models:
        if "error" in sm:
            summary_lines.append(f"- {sm['key']} — ERROR: {sm['error']}")
        else:
            summary_lines.append(
                f"- {sm.get('display_name') or sm['key']} "
                f"({sm.get('params') or '?'} / {sm.get('quant') or '?'} / {sm.get('size_gb')} GB) "
                f"Context: {sm.get('context')} → `{sm.get('file')}`"
            )

    (results_path / "test_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    results_md = results_path / "results.md"
    if not results_md.exists():
        results_md.write_text("# Evaluation Results\n\nPaste the cloud model evaluation here.\n", encoding="utf-8")

    print(f"  Finished {name}")

def main():
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
        run_scenario(scenario, models, base_url, headers, dry_run=DRY_RUN)

    print("\nDone.")

if __name__ == "__main__":
    main()
