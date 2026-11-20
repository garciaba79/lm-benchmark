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


def transcript_json_for_model(results_path, model):
    """JSON transcript beside the markdown file. Same model key."""
    return result_file_for_model(results_path, model).with_suffix(".json")


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
        f"Models recorded: {len(summary_models)}  ",
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


def records_as_list(data, key_field="key"):
    """
    Normalize a collection of records.

    Accepts a list of objects, or a dict whose values are objects
    (the dict key fills in key_field when the object does not have one).
    """
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict) and data and all(isinstance(value, dict) for value in data.values()):
        items = []
        for key, value in data.items():
            record = dict(value)
            record.setdefault(key_field, key)
            items.append(record)
        return items
    return []


def keyed_records(data, key_field="key"):
    """Return records in original order, one per key. A later duplicate replaces the earlier one."""
    order = []
    by_key = {}
    for record in records_as_list(data, key_field):
        key = record.get(key_field)
        if not key:
            continue
        if key not in by_key:
            order.append(key)
        by_key[key] = record
    return [by_key[key] for key in order]


def upsert_record(records, record, key_field="key"):
    """Replace the record with the same key, or append it. Other records stay in place."""
    key = record.get(key_field) if isinstance(record, dict) else None
    if not key:
        return keyed_records(records, key_field)
    updated = []
    found = False
    for existing in keyed_records(records, key_field):
        if existing.get(key_field) == key:
            updated.append(record)
            found = True
        else:
            updated.append(existing)
    if not found:
        updated.append(record)
    return updated


def remove_records(records, keys, key_field="key"):
    """Drop records whose key is in keys. Every other record stays."""
    drop = set(keys)
    return [record for record in keyed_records(records, key_field) if record.get(key_field) not in drop]


def active_model_keys(models):
    return [record["key"] for record in keyed_records(models)]


def completed_model_keys(results_path, model_keys):
    """Model keys whose result file exists. Extra markdown files are ignored."""
    results_path = Path(results_path)
    done = []
    for key in model_keys:
        if result_file_for_model(results_path, {"key": key}).exists():
            done.append(key)
    return done


def scenario_completion(results_path, model_keys):
    """
    Status of one scenario against the active model list.
    none: no active model has a result file
    partial: some active models have a result file
    complete: every active model has a result file
    """
    if not model_keys:
        return "none", None
    done_paths = []
    for key in model_keys:
        path = result_file_for_model(results_path, {"key": key})
        if path.exists():
            done_paths.append(path)
    if not done_paths:
        return "none", None
    status = "complete" if len(done_paths) == len(model_keys) else "partial"
    newest = max(done_paths, key=lambda path: path.stat().st_mtime)
    last_run = datetime.fromtimestamp(newest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    return status, last_run


def evaluation_section(content):
    """Return the evaluation status block, or an empty string when it is absent."""
    if not content:
        return ""
    marker = "## Evaluation status"
    index = content.find(marker)
    if index == -1:
        return ""
    return content[index:].strip() + "\n"


def append_evaluation_section(content, section):
    if not section:
        return content
    return content.rstrip() + "\n\n" + section.strip() + "\n"


def write_info_md(path, text):
    """Write helper-model prose to info.md. Returns the path, or None when there is no text."""
    text = (text or "").strip()
    if not text:
        return None
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Info\n\n" + text + "\n", encoding="utf-8")
    return path


def build_stats_md(stats):
    models = keyed_records(stats.get("models") if isinstance(stats, dict) else [])
    models = [model for model in models if "error" not in model]
    if not models:
        return "# Stats\n\nNo models were run.\n"
    question_count = 0
    for model in models:
        question_count = max(question_count, len(model.get("question_times") or []))
    rows = []
    for model in models:
        name = model.get("display_name") or model.get("key") or "-"
        avg = f"{model.get('avg_tps', 0):.0f}" if model.get("avg_tps") is not None else "-"
        total = format_duration(model.get("total_seconds")) if model.get("total_seconds") is not None else "-"
        question_times = model.get("question_times") or []
        question_cells = []
        for index in range(question_count):
            if index < len(question_times) and question_times[index] is not None:
                question_cells.append(format_duration(question_times[index]))
            else:
                question_cells.append("-")
        rows.append([name, avg, total] + question_cells)
    headers = ["Model", "Avg t/s", "Total time"] + [f"Q{index + 1}" for index in range(question_count)]
    return _markdown_table("# Stats", headers, rows, stats.get("overall_seconds") if isinstance(stats, dict) else None)


def build_root_stats_md(system_stats, overall_seconds):
    models = [model for model in keyed_records(system_stats) if "error" not in model]
    if not models:
        return "# System Stats\n\nNo models were run.\n"
    rows = []
    for model in models:
        name = model.get("display_name") or model.get("key") or "-"
        avg = f"{model.get('avg_tps', 0):.0f}" if model.get("avg_tps") is not None else "-"
        total = format_duration(model.get("total_seconds")) if model.get("total_seconds") is not None else "-"
        used = "yes" if model.get("used_ram") else "no"
        peak = f"{model.get('peak_ram_gb')} GB" if model.get("peak_ram_gb") is not None else "-"
        scenario_count = len(model.get("scenarios") or [])
        rows.append([name, avg, total, used, peak, str(scenario_count)])
    headers = ["Model", "Avg t/s", "Total time", "Used RAM", "Peak RAM", "Scenarios"]
    return _markdown_table("# System Stats", headers, rows, overall_seconds)


def _markdown_table(title, headers, rows, overall_seconds):
    col_widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            col_widths[index] = max(col_widths[index], len(str(cell)))

    def pad_row(cells):
        return "| " + " | ".join(str(cell).ljust(col_widths[index]) for index, cell in enumerate(cells)) + " |"

    lines = [title, ""]
    if overall_seconds is not None:
        lines.append(f"Overall time (all models): {format_duration(overall_seconds)}")
        lines.append("")
    lines.append(pad_row(headers))
    lines.append("| " + " | ".join("-" * col_widths[index] for index in range(len(headers))) + " |")
    for row in rows:
        lines.append(pad_row(row))
    return "\n".join(lines) + "\n"


def iter_scenario_stats(results_dir=None):
    """Yield (scenario_rel, stats_dict) for each scenario stats.json. Skips the root stats file."""
    results_dir = Path(results_dir or config.RESULTS_DIR)
    if not results_dir.exists():
        return
    for stats_path in sorted(results_dir.rglob("stats.json")):
        if stats_path.parent == results_dir:
            continue
        data = load_json(stats_path, required=False)
        if not isinstance(data, dict):
            continue
        scenario = data.get("scenario") or stats_path.parent.relative_to(results_dir).as_posix()
        yield scenario, data


def aggregate_root_models(previous_models, ram_updates=None, results_dir=None):
    """
    Build the root model list from per-scenario stats.

    Models that already have a root record stay, including models that are no longer
    on the active list. Totals for a model are recomputed from its scenario stats.
    ram_updates supplies used_ram and peak_ram_gb for models that ran in this process.
    """
    ram_updates = ram_updates or {}
    previous = keyed_records(previous_models)
    previous_by_key = {record["key"]: record for record in previous}
    grouped = {}
    grouped_order = []
    for scenario, data in iter_scenario_stats(results_dir):
        for record in keyed_records(data.get("models")):
            if "error" in record:
                continue
            key = record.get("key")
            if key not in grouped:
                grouped[key] = []
                grouped_order.append(key)
            row = dict(record)
            row["_scenario"] = scenario
            grouped[key].append(row)

    order = [record["key"] for record in previous]
    for key in grouped_order:
        if key not in order:
            order.append(key)

    models = []
    for key in order:
        rows = grouped.get(key)
        old = previous_by_key.get(key)
        if not rows:
            if old:
                models.append(old)
            continue
        total_seconds = sum((row.get("total_seconds") or 0) for row in rows)
        weighted = 0.0
        weight = 0.0
        for row in rows:
            average = row.get("avg_tps")
            if average is None:
                continue
            seconds = row.get("total_seconds") or 0
            if seconds > 0:
                weighted += average * seconds
                weight += seconds
            else:
                weighted += average
                weight += 1
        scenarios = []
        for row in rows:
            name = row.get("_scenario")
            if name and name not in scenarios:
                scenarios.append(name)
        meta = rows[-1]
        ram = ram_updates.get(key) or {}
        peaks = []
        for value in (
            (old or {}).get("peak_ram_gb"),
            ram.get("peak_ram_gb"),
            *[row.get("peak_ram_gb") for row in rows],
        ):
            if isinstance(value, (int, float)):
                peaks.append(value)
        used_ram = bool((old or {}).get("used_ram")) or bool(ram.get("used_ram")) or any(row.get("used_ram") for row in rows)
        models.append({
            "key": key,
            "display_name": meta.get("display_name") or (old or {}).get("display_name"),
            "params": meta.get("params") if meta.get("params") is not None else (old or {}).get("params"),
            "quant": meta.get("quant") or (old or {}).get("quant"),
            "size_gb": meta.get("size_gb") if meta.get("size_gb") is not None else (old or {}).get("size_gb"),
            "avg_tps": (weighted / weight) if weight else 0,
            "total_seconds": total_seconds,
            "used_ram": used_ram,
            "peak_ram_gb": round(max(peaks), 1) if peaks else (old or {}).get("peak_ram_gb"),
            "scenarios": scenarios,
        })
    return models
