"""
Shared pure helpers for the LM Studio model test harness.
"""

import json
import re
from datetime import datetime
from pathlib import Path

import config


def load_json(path, required=True):
    path = Path(path)
    if not path.exists():
        if required:
            print(f"Missing required file: {path}")
            raise SystemExit(1)
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        if required:
            print(f"Failed to load {path}: {e}")
            raise SystemExit(1)
        return {}


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_headers(token=None):
    headers = {"Content-Type": "application/json"}
    token = token if token is not None else config.API_TOKEN
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def safe_filename(name):
    keep = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_ ."
    cleaned = "".join(c if c in keep else "-" for c in str(name))
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


def result_file_for_model(results_path, model):
    key = model.get("key") or model.get("display_name") or "unknown"
    return Path(results_path) / f"{safe_filename(key)}.md"


def find_file_with_precedence(scenario_path, filename):
    """
    Look for filename starting at the scenario folder, then each parent
    group folder, then the scenarios root. Highest precedence first.
    """
    scenario_path = Path(scenario_path)
    candidates = []
    current = scenario_path
    # Walk up to (but not past) the scenarios root
    while current != config.SCENARIOS_DIR and current.parent != current:
        candidates.append(current / filename)
        current = current.parent
    candidates.append(config.SCENARIOS_DIR / filename)

    for path in candidates:
        if path.exists():
            return path
    return None


def load_inference(scenario_path):
    if not config.USE_CUSTOM_INFER:
        return {}
    path = find_file_with_precedence(scenario_path, "inference.json")
    if path:
        data = load_json(path, required=False) or {}
        # Keep a note of where it came from for debugging if needed
        data["_source"] = str(path)
        return data
    return {}


def load_system_prompt(scenario_path, test_info):
    if test_info.get("system_prompt") is False:
        return None
    inline = test_info.get("system")
    if inline and str(inline).strip():
        return str(inline).strip()

    # inference.json "system" field wins over system.md at the same level
    inference = load_inference(scenario_path)
    system_from_inference = inference.get("system")
    if system_from_inference and str(system_from_inference).strip():
        return str(system_from_inference).strip()

    path = find_file_with_precedence(scenario_path, "system.md")
    if path:
        return path.read_text(encoding="utf-8").strip()
    return None


def today_archive_folder():
    date_str = datetime.now().strftime("%Y %m %d")
    return config.ARCHIVE_DIR / date_str


def build_test_md(test_info, name, created_str, summary_models, eval_status=None):
    """
    Build the content for a scenario's test.md file.
    eval_status is an optional dict: {"evaluated": int, "total": int, "missing": list[str]}
    """
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

    if eval_status:
        lines.extend([
            "",
            "## Evaluation status",
            "",
            "#### Model results evaluated",
            "",
            f"{eval_status.get('evaluated', 0)} / {eval_status.get('total', 0)} models",
            "",
            "#### Models missing",
            "",
            ", ".join(eval_status.get("missing") or ["None"])
        ])

    return "\n".join(lines).rstrip() + "\n"


def update_test_md_evaluation(results_path, evaluated, total, missing_keys):
    """
    Update or append the evaluation status section in test.md.
    Preserves the existing test section written by run.py.
    """
    results_path = Path(results_path)
    test_md_path = results_path / "test.md"
    eval_block = [
        "",
        "## Evaluation status",
        "",
        "#### Model results evaluated",
        "",
        f"{evaluated} / {total} models",
        "",
        "#### Models missing",
        "",
        ", ".join(missing_keys) if missing_keys else "None",
        ""
    ]
    eval_text = "\n".join(eval_block)

    if test_md_path.exists():
        content = test_md_path.read_text(encoding="utf-8")
        if "## Evaluation status" in content:
            content = content.split("## Evaluation status")[0].rstrip() + "\n"
        content = content.rstrip() + "\n" + eval_text
    else:
        content = f"# Test\n\n(No test run recorded yet)\n{eval_text}"

    test_md_path.write_text(content, encoding="utf-8")
    return test_md_path


def write_evaluation_index(results_path):
    """
    Scan the results folder for evaluation-<model>.json files and write
    a simple evaluation.json index. Overwrites any existing file.
    """
    results_path = Path(results_path)
    entries = []
    for path in sorted(results_path.glob("evaluation-*.json")):
        model_name = path.stem.replace("evaluation-", "", 1)
        entries.append({
            "model": model_name,
            "file": path.name,
            "updated": path.stat().st_mtime
        })
    index = {"evaluations": entries}
    out = results_path / "evaluation.json"
    out.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return out
