#!/usr/bin/env python3
"""
Scan the scenarios folder and write scenarios.json and scenarios.md.
Overwrites both files each run. Default mode is "none".

Supports both top-level scenario folders and nested category folders.
Any folder that contains a test.json is treated as a scenario.
The "scenario" field stores the relative path (e.g. "weather app" or "bug/null pointer").

get_scenarios.py
version 0.6.0
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
import requests

# ==========================================
# CONFIGURATION
# ==========================================
SCENARIOS_DIR = "scenarios"
RESULTS_DIR = "results"
MODELS_PATH = "models.json"
OUTPUT_JSON = "scenarios.json"
OUTPUT_MD = "scenarios.md"
CONFIG_PATH = "config.json"
DEFAULT_MODE = "update"                 # Set the mode for updating the tests: "update" | "refresh" | "none"
REQUIRE_TEST_JSON = True
REQUIRE_AT_LEAST_ONE_QUESTION = True

# Helper model prompt (used only if model is set in config.json and reachable)
HELPER_PROMPT = """Summarize the current state of these test scenarios in 2-3 short sentences. Mention how many are complete, partial, or not started. Keep it plain and useful."""

def load_json(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def load_models():
    data = load_json(MODELS_PATH)
    return data if isinstance(data, list) else []

def find_scenario_dirs(base: Path):
    """Return sorted list of (relative_path, full_path) for every folder that has a test.json."""
    found = []
    for p in base.rglob("*"):
        if not p.is_dir():
            continue
        if (p / "test.json").exists():
            rel = p.relative_to(base).as_posix()
            found.append((rel, p))
    return sorted(found, key=lambda x: x[0].lower())

def has_questions(scenario_path):
    for p in scenario_path.glob("question*.md"):
        if re.match(r"question\d+\.md$", p.name, re.IGNORECASE):
            return True
    return False

def get_display_name(test_data: dict, fallback_name: str) -> str:
    name = test_data.get("name", "")
    if name and len(name) > 0:
        return name

    test_field = test_data.get("test", "")
    if test_field:
        return test_field.title()

    return fallback_name

def get_result_status(scenario_rel, models):
    results_path = Path(RESULTS_DIR) / scenario_rel
    if not results_path.exists():
        return "none", None

    result_files = [p for p in results_path.glob("*.md")
                    if p.name.lower() not in ("test.md", "results.md", "stats.md")]

    if not result_files:
        return "none", None

    if models and len(result_files) >= len(models):
        status = "complete"
    elif result_files:
        status = "partial"
    else:
        status = "none"

    newest = max(result_files, key=lambda p: p.stat().st_mtime)
    last_run = datetime.fromtimestamp(newest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    return status, last_run

def try_helper_summary(config, scenarios):
    model = config.get("model") if config else None
    if not model:
        return "Here is the summary results."

    base_url = config.get("base_url", "http://localhost:1234").rstrip("/")
    token = config.get("api_token", "")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Build a short context for the model
    lines = [f"- {s['scenario']} ({s['status']})" for s in scenarios]
    context = "Scenarios:\n" + "\n".join(lines)

    try:
        resp = requests.post(
            f"{base_url}/api/v0/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": HELPER_PROMPT},
                    {"role": "user", "content": context}
                ],
                "stream": False,
                "max_tokens": 200
            },
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return text or "Here is the summary results."
    except Exception:
        return "Here is the summary results."

def build_scenarios_md(scenarios, summary):
    complete = [s for s in scenarios if s["status"] == "complete"]
    partial = [s for s in scenarios if s["status"] == "partial"]
    none = [s for s in scenarios if s["status"] == "none"]

    lines = [
        "# Scenarios",
        "",
        "## Summary",
        "",
        summary,
        "",
        f"## Scenarios",
        "",
        f"There are {len(scenarios)} scenarios.",
        ""
    ]
    for s in scenarios:
        lines.append(f"- {s['scenario']} ({s['status']})")

    if none:
        lines.extend(["", "## Uncompleted Scenarios", ""])
        for s in none:
            lines.append(f"- {s['scenario']}")

    if partial:
        lines.extend(["", "## Partially Completed Scenarios", ""])
        for s in partial:
            lines.append(f"- {s['scenario']}")

    if complete:
        lines.extend(["", "## Completed Scenarios", ""])
        for s in complete:
            lines.append(f"- {s['scenario']}")

    lines.extend([
        "",
        "## Suggestions",
        "",
        "Set modes in scenarios.json and run the tests to complete remaining scenarios."
    ])

    return "\n".join(lines) + "\n"

def main():
    scenarios_path = Path(SCENARIOS_DIR)
    if not scenarios_path.exists():
        print(f"No {SCENARIOS_DIR}/ folder found.")
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
        return

    models = load_models()
    config = load_json(CONFIG_PATH) or {}
    scenarios = []

    for rel_path, item in find_scenario_dirs(scenarios_path):
        test_json_path = item / "test.json"
        has_test = True  # we only reach here if test.json exists
        has_q = has_questions(item)

        ready = True
        if REQUIRE_TEST_JSON and not has_test:
            ready = False
        if REQUIRE_AT_LEAST_ONE_QUESTION and not has_q:
            ready = False

        status, last_run = get_result_status(rel_path, models)

        display_name = rel_path
        description = ""
        if has_test:
            t = load_json(test_json_path) or {}
            display_name = get_display_name(t, rel_path)
            description = t.get("description", "")

        scenarios.append({
            "scenario": rel_path,
            "name": display_name,
            "description": description,
            "ready": ready,
            "status": status,
            "mode": DEFAULT_MODE,
            "last_run": last_run
        })

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2)

    summary = try_helper_summary(config, scenarios)
    md = build_scenarios_md(scenarios, summary)
    Path(OUTPUT_MD).write_text(md, encoding="utf-8")

    print(f"Wrote {len(scenarios)} scenarios to {OUTPUT_JSON}")
    print(f"Wrote {OUTPUT_MD}")
    print(f"Default mode: {DEFAULT_MODE}")

if __name__ == "__main__":
    main()
