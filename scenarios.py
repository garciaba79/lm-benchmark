#!/usr/bin/env python3
"""
Scan the scenarios folder and write scenarios/scenarios.json and scenarios.md.

Existing scenario modes are kept. New scenarios get config.DEFAULT_MODE.
Status is complete, partial, or none based on active model keys that have a result file.

Supports nested group folders. Any folder containing test.json is a scenario.
The "scenario" field stores the relative path (e.g. "function/test1").

scenarios.py
version 0.8.0
"""

import re
from pathlib import Path

import requests

import config
import utils


def find_scenario_dirs(base: Path):
    found = []
    for p in base.rglob("*"):
        if not p.is_dir():
            continue
        if (p / config.TEST_JSON).exists():
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
    if name:
        return name
    test_field = test_data.get("test", "")
    if test_field:
        return test_field.title()
    return fallback_name


def load_saved_modes():
    """Keep hand-set modes. The rest of each scenario record is refreshed from disk."""
    saved = utils.load_json(config.SCENARIOS_JSON, required=False)
    modes = {}
    for record in utils.keyed_records(saved, "scenario"):
        mode = record.get("mode")
        if mode:
            modes[record["scenario"]] = mode
    return modes


def try_helper_summary(scenarios):
    """Return helper prose, or None when the helper is unset or unreachable."""
    if not config.HELPER_MODEL:
        return None

    lines = [f"- {s['scenario']} ({s['status']})" for s in scenarios]
    context = "Scenarios:\n" + "\n".join(lines)

    try:
        resp = requests.post(
            f"{config.BASE_URL.rstrip('/')}/api/v0/chat/completions",
            headers=utils.get_headers(),
            json={
                "model": config.HELPER_MODEL,
                "messages": [
                    {"role": "system", "content": config.SCENARIOS_SUMMARY_PROMPT},
                    {"role": "user", "content": context}
                ],
                "stream": False,
                "max_tokens": 600
            },
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return text or None
    except Exception:
        return None


def build_scenarios_md(scenarios):
    complete = [s for s in scenarios if s["status"] == "complete"]
    partial = [s for s in scenarios if s["status"] == "partial"]
    none = [s for s in scenarios if s["status"] == "none"]

    lines = [
        "# Scenarios",
        "",
        "## Summary",
        "",
        f"{len(complete)} complete, {len(partial)} partial, {len(none)} not started.",
        "",
        "## Scenarios",
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
    if not config.SCENARIOS_DIR.exists():
        print(f"No {config.SCENARIOS_DIR}/ folder found.")
        utils.save_json(config.SCENARIOS_JSON, [])
        return

    models = utils.keyed_records(utils.load_json(config.MODELS_PATH, required=False))
    model_keys = utils.active_model_keys(models)
    saved_modes = load_saved_modes()

    scenarios = []
    for rel_path, item in find_scenario_dirs(config.SCENARIOS_DIR):
        has_q = has_questions(item)
        ready = True
        if config.REQUIRE_TEST_JSON and not (item / config.TEST_JSON).exists():
            ready = False
        if config.REQUIRE_AT_LEAST_ONE_QUESTION and not has_q:
            ready = False

        status, last_run = utils.scenario_completion(config.RESULTS_DIR / rel_path, model_keys)

        display_name = rel_path
        description = ""
        test_json_path = item / config.TEST_JSON
        if test_json_path.exists():
            t = utils.load_json(test_json_path, required=False) or {}
            display_name = get_display_name(t, rel_path)
            description = t.get("description", "")

        scenarios.append({
            "scenario": rel_path,
            "name": display_name,
            "description": description,
            "ready": ready,
            "status": status,
            "mode": saved_modes.get(rel_path, config.DEFAULT_MODE),
            "last_run": last_run
        })

    utils.save_json(config.SCENARIOS_JSON, scenarios)
    config.SCENARIOS_MD.write_text(build_scenarios_md(scenarios), encoding="utf-8")
    info_path = utils.write_info_md(config.SCENARIOS_DIR / "info.md", try_helper_summary(scenarios))

    print(f"Wrote {len(scenarios)} scenarios to {config.SCENARIOS_JSON}")
    print(f"Wrote {config.SCENARIOS_MD}")
    if info_path:
        print(f"Wrote {info_path}")
    else:
        print("Helper summary skipped. scenarios.md was not given helper text.")
    print(f"Default mode for new scenarios: {config.DEFAULT_MODE}")


if __name__ == "__main__":
    main()
