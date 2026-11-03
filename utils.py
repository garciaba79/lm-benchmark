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
        return load_json(path, required=False) or {}
    return {}


def load_system_prompt(scenario_path, test_info):
    if test_info.get("system_prompt") is False:
        return None
    inline = test_info.get("system")
    if inline and str(inline).strip():
        return str(inline).strip()
    path = find_file_with_precedence(scenario_path, "system.md")
    if path:
        return path.read_text(encoding="utf-8").strip()
    return None


def today_archive_folder():
    date_str = datetime.now().strftime("%Y %m %d")
    return config.ARCHIVE_DIR / date_str
