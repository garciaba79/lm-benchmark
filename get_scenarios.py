#!/usr/bin/env python3
"""
Scan the scenarios folder and write scenarios.json.
Overwrites the file each run.
Default mode is "none".

get_scenarios.py
version 0.5.1
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
SCENARIOS_DIR = "scenarios"
RESULTS_DIR = "results"
MODELS_PATH = "models.json"
OUTPUT_PATH = "scenarios.json"
DEFAULT_MODE = "update"          # none | update | refresh
REQUIRE_TEST_JSON = True
REQUIRE_AT_LEAST_ONE_QUESTION = True

def load_models():
    if not os.path.exists(MODELS_PATH):
        return []
    try:
        with open(MODELS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def has_questions(scenario_path):
    for p in scenario_path.glob("question*.md"):
        if re.match(r"question\d+\.md$", p.name, re.IGNORECASE):
            return True
    return False

def get_result_status(scenario_name, models):
    results_path = Path(RESULTS_DIR) / scenario_name
    if not results_path.exists():
        return "none", None

    # Look for any .md result files (ignore test_summary.md and results.md)
    result_files = [p for p in results_path.glob("*.md")
                    if p.name.lower() not in ("test_summary.md", "results.md")]

    if not result_files:
        return "none", None

    # Simple check: if we have at least as many result files as models, call it complete
    # (more precise matching can be added later)
    if models and len(result_files) >= len(models):
        status = "complete"
    elif result_files:
        status = "partial"
    else:
        status = "none"

    # Best-effort last run date from newest file
    newest = max(result_files, key=lambda p: p.stat().st_mtime)
    last_run = datetime.fromtimestamp(newest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")

    return status, last_run

def main():
    scenarios_path = Path(SCENARIOS_DIR)
    if not scenarios_path.exists():
        print(f"No {SCENARIOS_DIR}/ folder found. Creating empty scenarios.json")
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
        return

    models = load_models()
    scenarios = []

    for item in sorted(scenarios_path.iterdir()):
        if not item.is_dir():
            continue

        name = item.name
        test_json_path = item / "test.json"
        has_test = test_json_path.exists()
        has_q = has_questions(item)

        ready = True
        if REQUIRE_TEST_JSON and not has_test:
            ready = False
        if REQUIRE_AT_LEAST_ONE_QUESTION and not has_q:
            ready = False

        status, last_run = get_result_status(name, models)

        # Load name/description from test.json if present
        display_name = name
        description = ""
        if has_test:
            try:
                with open(test_json_path, "r", encoding="utf-8") as f:
                    t = json.load(f)
                    display_name = t.get("name", name)
                    description = t.get("description", "")
            except Exception:
                pass

        scenarios.append({
            "scenario": name,
            "name": display_name,
            "description": description,
            "ready": ready,
            "status": status,
            "mode": DEFAULT_MODE,
            "last_run": last_run
        })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2)

    print(f"Wrote {len(scenarios)} scenarios to {OUTPUT_PATH}")
    print(f"Default mode: {DEFAULT_MODE}")
    print("Edit modes in scenarios.json if needed, then run run_tests.py")

if __name__ == "__main__":
    main()
