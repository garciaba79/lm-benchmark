#!/usr/bin/env python3
"""
Evaluate LM Studio test results with a cloud model.

Reads result files from results/<scenario>/, sends them in batches to the
configured backend, and writes results.json plus a readable results.md.
The conversation is stored in evaluation-<model>.json (source of truth) and
evaluation-<model>.md. That JSON also stores usage: the judge requests and
token counts for this scenario. A model is scored when its record is in
results.json. test.md gets an evaluation status section.

The backend and model come from config.py. The API key is the one named for
that backend in .env.

Usage:
  python evaluate.py                                        # all scenarios (update mode)
  python evaluate.py --scenario summary/expedition
  python evaluate.py --force                                # re-evaluate everything
  python evaluate.py --dry-run
  python evaluate.py --batch-size 3

evaluate.py
version 0.3.0
"""

import argparse
import json
import sys
from pathlib import Path

import config
import utils

# Plugin loading
from plugins.base import EvaluationBackend
from plugins.grok_cli import GrokCLIBackend
from plugins.openai import OpenAICompatibleBackend
from plugins.anthropic import AnthropicBackend

# name -> key env var, default base URL, plugin kind
BACKENDS = {
    "grok_api": {
        "label": "Grok API",
        "key_env": "GROK_API_KEY",
        "base_url": "https://api.x.ai/v1",
        "kind": "openai",
    },
    "openai": {
        "label": "OpenAI",
        "key_env": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "kind": "openai",
    },
    "gemini": {
        "label": "Gemini",
        "key_env": "GEMINI_API_KEY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "kind": "openai",
    },
    "anthropic": {
        "label": "Anthropic",
        "key_env": "ANTHROPIC_API_KEY",
        "base_url": None,
        "kind": "anthropic",
    },
    "grok_cli": {
        "label": "Grok CLI",
        "key_env": None,
        "base_url": None,
        "kind": "grok_cli",
    },
}

# Set to True to print extra debug info from the script and plugins
DEBUG = False


def load_dotenv():
    """Load .env if present (simple key=value, no external dependency)."""
    env_path = Path(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in __import__("os").environ:
            __import__("os").environ[key] = val


class DryRunBackend(EvaluationBackend):
    def __init__(self, model):
        self.model = model

    def generate(self, messages: list[dict], **kwargs) -> str:
        raise RuntimeError("Dry run does not call the backend.")


def resolve_backend(dry_run: bool) -> EvaluationBackend:
    """Load the plugin selected by EVAL_BACKEND. The model is EVAL_MODEL."""
    load_dotenv()
    name = (config.EVAL_BACKEND or "").strip()
    spec = BACKENDS.get(name)
    if spec is None:
        known = ", ".join(BACKENDS)
        raise SystemExit(f"Unknown EVAL_BACKEND: {name!r}. Options: {known}")

    model = (config.EVAL_MODEL or "").strip()
    if not model:
        raise SystemExit("EVAL_MODEL is empty. Set the cloud model name in config.py.")

    override = (getattr(config, "EVAL_BASE_URL", "") or "").strip()
    base_url = override or spec["base_url"]
    key = ""
    if spec["key_env"]:
        key = __import__("os").environ.get(spec["key_env"], "").strip()
        if not key:
            message = f"{spec['label']} requires {spec['key_env']} in .env."
            if dry_run:
                print(f"Warning: {message}")
            else:
                raise SystemExit(message)

    print(f"Backend: {name} ({spec['label']})")
    print(f"Model: {model}")
    if base_url:
        print(f"Base URL: {base_url}")
    if spec["key_env"]:
        print(f"API key: {spec['key_env']} ({'set' if key else 'missing'})")

    if dry_run:
        return DryRunBackend(model)

    timeout = config.EVAL_TIMEOUT
    if spec["kind"] == "grok_cli":
        from plugins import grok_cli
        grok_cli.DEBUG = DEBUG
        return GrokCLIBackend(model=model, timeout=timeout)
    if spec["kind"] == "openai":
        return OpenAICompatibleBackend(base_url=base_url, api_key=key, model=model, timeout=timeout)
    if spec["kind"] == "anthropic":
        return AnthropicBackend(
            api_key=key,
            model=model,
            timeout=timeout,
            max_tokens=config.EVAL_MAX_TOKENS,
        )
    raise SystemExit(f"No plugin for EVAL_BACKEND: {name}")


SCORE_FIELDS = (
    "correctness",
    "quality",
    "task_understanding",
    "instruction_following",
    "usefulness",
    "faithfulness",
)
TEXT_FIELDS = ("pros", "cons", "notes")
RESULT_FIELDS = ("key", "avg_tps") + SCORE_FIELDS + TEXT_FIELDS

_SCORE_SCHEMA = {
    "anyOf": [
        {"type": "integer", "minimum": 0, "maximum": 100},
        {"type": "null"},
    ]
}
_MODEL_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "key": {"type": "string"},
        "avg_tps": {
            "anyOf": [
                {"type": "integer", "minimum": 0},
                {"type": "null"},
            ]
        },
        "correctness": _SCORE_SCHEMA,
        "quality": _SCORE_SCHEMA,
        "task_understanding": _SCORE_SCHEMA,
        "instruction_following": _SCORE_SCHEMA,
        "usefulness": _SCORE_SCHEMA,
        "faithfulness": _SCORE_SCHEMA,
        "pros": {"type": "string"},
        "cons": {"type": "string"},
        "notes": {"type": "string"},
    },
    "required": list(RESULT_FIELDS),
}
EVAL_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "evaluation_results",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "summary": {"type": "string"},
                "takeaways": {"type": "array", "items": {"type": "string"}},
                "practical": {"type": "array", "items": {"type": "string"}},
                "notes": {"type": "array", "items": {"type": "string"}},
                "models": {"type": "array", "items": _MODEL_SCHEMA},
            },
            "required": ["summary", "takeaways", "practical", "notes", "models"],
        },
    },
}


def response_format_for(backend_name: str):
    """JSON schema for backends that accept OpenAI response_format."""
    if backend_name in ("grok_api", "openai"):
        return EVAL_RESPONSE_FORMAT
    return None


def blank_results(scenario: str, judge_model: str) -> dict:
    return {
        "version": 1,
        "scenario": scenario,
        "judge_model": judge_model,
        "summary": "",
        "takeaways": [],
        "practical": [],
        "notes": [],
        "models": [],
    }


def public_results(document: dict) -> dict:
    """The object the cloud model reads and returns."""
    return {
        "summary": document.get("summary") or "",
        "takeaways": list(document.get("takeaways") or []),
        "practical": list(document.get("practical") or []),
        "notes": list(document.get("notes") or []),
        "models": [ordered_model(model) for model in document.get("models") or []],
    }


def ordered_model(model: dict) -> dict:
    return {field: model.get(field) for field in RESULT_FIELDS}


def as_score(value, key: str, field: str):
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{key} {field} must be an integer from 0 to 100 or null")
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    if isinstance(value, int) and 0 <= value <= 100:
        return value
    raise ValueError(f"{key} {field} must be an integer from 0 to 100 or null")


def as_string_list(value, field: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list):
        items = []
        for item in value:
            if not isinstance(item, str):
                raise ValueError(f"{field} must be an array of strings")
            text = item.strip()
            if text:
                items.append(text)
        return items
    raise ValueError(f"{field} must be an array of strings")


def script_tps(key: str, tps_map: dict, fallback):
    raw = tps_map.get(key)
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return int(round(raw))
    if isinstance(fallback, (int, float)) and not isinstance(fallback, bool) and fallback >= 0:
        return int(round(fallback))
    return None


def normalize_model(item, tps_map: dict) -> dict:
    if not isinstance(item, dict):
        raise ValueError("a model entry must be an object")
    key = item.get("key")
    if not isinstance(key, str) or not key.strip():
        raise ValueError("a model entry is missing key")
    key = key.strip()
    record = {"key": key, "avg_tps": script_tps(key, tps_map, item.get("avg_tps"))}
    for field in SCORE_FIELDS:
        if field not in item:
            raise ValueError(f"{key} is missing {field}")
        record[field] = as_score(item.get(field), key, field)
    for field in TEXT_FIELDS:
        value = item.get(field, "")
        if value is None:
            value = ""
        if not isinstance(value, str):
            raise ValueError(f"{key} {field} must be a string")
        record[field] = value.strip()
    return ordered_model(record)


def extract_json_object(text: str) -> dict:
    raw = (text or "").strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("the reply is not a JSON object")
        try:
            data = json.loads(raw[start:end + 1])
        except json.JSONDecodeError as exc:
            raise ValueError(f"the reply is not valid JSON ({exc})") from exc
    if not isinstance(data, dict):
        raise ValueError("the reply must be a JSON object")
    return data


def parse_evaluation(text: str) -> dict:
    data = extract_json_object(text)
    summary = data.get("summary")
    if not isinstance(summary, str):
        raise ValueError("summary must be a string")
    models = data.get("models")
    if not isinstance(models, list):
        raise ValueError("models must be an array")
    return {
        "summary": summary.strip(),
        "takeaways": as_string_list(data.get("takeaways"), "takeaways"),
        "practical": as_string_list(data.get("practical"), "practical"),
        "notes": as_string_list(data.get("notes"), "notes"),
        "models": models,
    }


def sort_models(models: list[dict]) -> list[dict]:
    def rank(model):
        correctness = model.get("correctness")
        quality = model.get("quality")
        correctness_rank = correctness if isinstance(correctness, int) else -1
        quality_rank = quality if isinstance(quality, int) else -1
        return (-correctness_rank, -quality_rank, model.get("key") or "")

    return sorted(models, key=rank)


def merge_results(document: dict, parsed: dict, batch_keys: list[str], allowed_keys: set[str], tps_map: dict) -> dict:
    """Update rows the reply returned. Keep a stored row the reply left out."""
    by_key = {}
    for model in document.get("models") or []:
        key = model.get("key")
        if key:
            by_key[key] = ordered_model(model)

    problems = []
    returned = {}
    for item in parsed["models"]:
        try:
            record = normalize_model(item, tps_map)
        except ValueError as exc:
            problems.append(str(exc))
            continue
        if record["key"] not in allowed_keys:
            continue
        returned[record["key"]] = record

    missing = [key for key in batch_keys if key not in returned]
    batch_problems = []
    for problem in problems:
        if any(problem.startswith(f"{key} ") for key in batch_keys):
            batch_problems.append(problem)
        elif not any(problem.startswith(f"{key} ") for key in allowed_keys):
            batch_problems.append(problem)
        else:
            print(f"  Kept the previous scores. {problem}")
    if missing or batch_problems:
        parts = []
        if missing:
            parts.append("missing models: " + ", ".join(missing))
        if batch_problems:
            parts.append("; ".join(batch_problems))
        raise ValueError(". ".join(parts))

    for key, record in returned.items():
        by_key[key] = record
    for key, record in list(by_key.items()):
        record["avg_tps"] = script_tps(key, tps_map, record.get("avg_tps"))
        by_key[key] = ordered_model(record)

    merged = dict(document)
    if parsed["summary"]:
        merged["summary"] = parsed["summary"]
    if parsed["takeaways"]:
        merged["takeaways"] = parsed["takeaways"]
    if parsed["practical"]:
        merged["practical"] = parsed["practical"]
    if parsed["notes"]:
        merged["notes"] = parsed["notes"]
    merged["models"] = sort_models(list(by_key.values()))
    return merged


def load_tps_map(results_path: Path) -> dict:
    stats = utils.load_json(results_path / "stats.json", required=False)
    if not isinstance(stats, dict):
        return {}
    found = {}
    for record in utils.keyed_records(stats.get("models")):
        key = record.get("key")
        if key:
            found[key] = record.get("avg_tps")
    return found


def load_results(path: Path, scenario: str, judge_model: str) -> dict:
    document = blank_results(scenario, judge_model)
    if not path.exists():
        return document
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return document
    if not isinstance(data, dict):
        return document
    if isinstance(data.get("summary"), str):
        document["summary"] = data["summary"].strip()
    try:
        document["takeaways"] = as_string_list(data.get("takeaways"), "takeaways")
        document["practical"] = as_string_list(data.get("practical"), "practical")
        document["notes"] = as_string_list(data.get("notes"), "notes")
    except ValueError:
        pass
    models = []
    for item in data.get("models") or []:
        if not isinstance(item, dict) or not item.get("key"):
            continue
        try:
            models.append(normalize_model(item, {}))
        except ValueError:
            continue
    document["models"] = sort_models(models)
    return document


def write_results(path: Path, document: dict):
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def md_cell(value) -> str:
    if value is None:
        return "—"
    text = str(value).replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip()
    return text if text else "—"


def render_results_md(document: dict) -> str:
    lines = ["# Evaluation Results", ""]
    lines.append("## Summary")
    lines.append("")
    lines.append(document.get("summary") or "")
    lines.append("")
    for heading, field in (
        ("Key takeaways", "takeaways"),
        ("Practical notes", "practical"),
        ("Additional notes", "notes"),
    ):
        lines.append(f"## {heading}")
        lines.append("")
        items = document.get(field) or []
        if items:
            lines.extend(f"- {item}" for item in items)
        lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Model | t/s | Correctness | Quality | Task understanding | Instruction following | Usefulness | Faithfulness | Pros | Cons | Notes |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for model in sort_models(document.get("models") or []):
        cells = [
            md_cell(model.get("key")),
            md_cell(model.get("avg_tps")),
            md_cell(model.get("correctness")),
            md_cell(model.get("quality")),
            md_cell(model.get("task_understanding")),
            md_cell(model.get("instruction_following")),
            md_cell(model.get("usefulness")),
            md_cell(model.get("faithfulness")),
            md_cell(model.get("pros")),
            md_cell(model.get("cons")),
            md_cell(model.get("notes")),
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def build_batch_message(instructions: str, document: dict, batch_keys: list[str], file_map: dict) -> str:
    parts = []
    if instructions:
        parts.append(instructions.rstrip())
        parts.append("")
        parts.append("---")
        parts.append("")
    parts.append(config.EVAL_BATCH_PROMPT.strip())
    parts.append("")
    parts.append("Current results JSON:")
    parts.append("")
    parts.append(json.dumps(public_results(document), indent=2))
    parts.append("")
    parts.append("New transcripts:")
    parts.append("")
    for key in batch_keys:
        content = file_map[key].read_text(encoding="utf-8").rstrip()
        parts.append(f"### {key}")
        parts.append("")
        parts.append(content)
        parts.append("")
    return "\n".join(parts).rstrip()


def repair_message(problem: str, batch_keys: list[str]) -> str:
    keys = ", ".join(batch_keys)
    return (
        "The previous reply could not be saved. "
        f"{problem}. "
        f"This batch must include these keys: {keys}. "
        "Return the full JSON object only, with every model from the current results "
        "and every new model. Use the same fields as the instructions."
    )


USAGE_FIELDS = ("requests", "prompt_tokens", "completion_tokens", "total_tokens")


def blank_usage() -> dict:
    return {field: 0 for field in USAGE_FIELDS}


def usage_counts(value) -> dict | None:
    """Copy a usage object. Return None when it is missing or not counts."""
    if not isinstance(value, dict):
        return None
    counts = blank_usage()
    for field in USAGE_FIELDS:
        raw = value.get(field, 0)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            return None
        number = int(raw)
        if number < 0:
            return None
        counts[field] = number
    return counts


def load_usage(path: Path) -> dict | None:
    """Usage already stored for this judge, or None when the file has none."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict) or "usage" not in data:
        return None
    return usage_counts(data.get("usage"))


def add_usage(base: dict, extra: dict) -> dict:
    return {field: base[field] + extra[field] for field in USAGE_FIELDS}


def backend_usage(backend) -> dict | None:
    """Process totals, or None when the backend does not track them."""
    if not hasattr(backend, "get_stats"):
        return None
    stats = backend.get_stats()
    if not isinstance(stats, dict):
        return None
    return usage_counts({field: stats.get(field, 0) for field in USAGE_FIELDS})


def usage_since(start: dict, current: dict) -> dict:
    return {field: max(0, current[field] - start[field]) for field in USAGE_FIELDS}


class UsageLedger:
    """Judge usage for one scenario. Each save adds only the new requests."""

    def __init__(self, stored: dict | None, backend):
        self.usage = None if stored is None else dict(stored)
        mark = backend_usage(backend)
        self.tracks = mark is not None
        self.mark = mark if mark is not None else blank_usage()

    def consume(self, backend) -> dict | None:
        if not self.tracks:
            return self.usage
        current = backend_usage(backend) or blank_usage()
        delta = usage_since(self.mark, current)
        self.mark = current
        if any(delta.values()):
            self.usage = add_usage(self.usage or blank_usage(), delta)
        return self.usage


def load_messages(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    messages = data.get("messages") if isinstance(data, dict) else None
    return messages if isinstance(messages, list) else []


def write_conversation_json(path: Path, messages: list[dict], model_name: str, evaluated_keys: list[str], final_complete: bool, usage: dict | None = None):
    """Write the current conversation as the source of truth."""
    data = {
        "model": model_name,
        "evaluated_keys": list(evaluated_keys),
        "final_complete": final_complete,
    }
    counts = usage_counts(usage) if usage is not None else None
    if counts is not None:
        data["usage"] = counts
    data["messages"] = messages
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_conversation_md(path: Path, messages: list[dict]):
    """Human-readable version generated from the JSON."""
    lines = ["# Evaluation Conversation", ""]
    for msg in messages:
        role = msg.get("role", "user").capitalize()
        content = msg.get("content", "").strip()
        lines.append(f"## {role}")
        lines.append("")
        lines.append(content)
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def collect_result_files(results_path: Path, models: list[dict]) -> list[tuple[str, Path]]:
    """Return list of (key, path) for result files that exist."""
    found = []
    for m in models:
        key = m.get("key")
        if not key:
            continue
        f = utils.result_file_for_model(results_path, m)
        if f.exists():
            found.append((key, f))
    return found


def request_evaluation(backend, user_content, document, batch_keys, allowed_keys, tps_map):
    """Ask for the JSON table. One repair turn when the reply cannot be merged."""
    response_format = response_format_for((config.EVAL_BACKEND or "").strip())
    conversation = [{"role": "user", "content": user_content}]
    last_problem = "the reply could not be saved"
    for attempt in (1, 2):
        try:
            reply = backend.generate(conversation, response_format=response_format)
        except RuntimeError as exc:
            last_problem = str(exc)
            print(f"  Request failed: {last_problem}")
            if attempt == 2:
                raise
            continue
        conversation.append({"role": "assistant", "content": reply})
        try:
            parsed = parse_evaluation(reply)
            merged = merge_results(document, parsed, batch_keys, allowed_keys, tps_map)
            return merged, conversation
        except ValueError as exc:
            last_problem = str(exc)
            print(f"  Reply was not usable: {last_problem}")
            if attempt == 2:
                raise
            conversation.append({"role": "user", "content": repair_message(last_problem, batch_keys)})
    raise RuntimeError(last_problem)


def publish_results(results_path, document, messages, model_name, ordered_keys, conv_json_path, conv_md_path, usage=None):
    stored = [model.get("key") for model in document.get("models") or []]
    missing = [key for key in ordered_keys if key not in stored]
    evaluated = [key for key in ordered_keys if key in stored]
    write_results(results_path / "results.json", document)
    results_md = results_path / "results.md"
    results_md.write_text(render_results_md(document), encoding="utf-8")
    write_conversation_json(conv_json_path, messages, model_name, evaluated, not missing, usage)
    write_conversation_md(conv_md_path, messages)
    utils.write_evaluation_index(results_path)
    utils.update_test_md_evaluation(results_path, len(evaluated), len(ordered_keys), missing)
    print(f"  Wrote {results_md.name}, results.json, {conv_json_path.name}, and {conv_md_path.name}")
    print("  Updated evaluation status in test.md")


def evaluate_scenario(results_path: Path, backend: EvaluationBackend, batch_size: int, force: bool, dry_run: bool):
    models_path = results_path / "models.json"
    if not models_path.exists():
        print(f"  No models.json in {results_path}, skipping.")
        return

    models = utils.keyed_records(utils.load_json(models_path, required=False))
    if not models:
        print(f"  Empty models.json in {results_path}, skipping.")
        return

    result_files = collect_result_files(results_path, models)
    if not result_files:
        print(f"  No result files found in {results_path}, skipping.")
        return

    model_name = getattr(backend, "model", None) or config.EVAL_MODEL or "unknown"
    safe_model = model_name.replace("/", "-").replace(" ", "-")
    conv_json_path = results_path / f"evaluation-{safe_model}.json"
    conv_md_path = results_path / f"evaluation-{safe_model}.md"
    ordered_keys = [key for key, _ in result_files]
    allowed_keys = set(ordered_keys)
    rel = results_path.relative_to(config.RESULTS_DIR).as_posix()
    tps_map = load_tps_map(results_path)

    messages = [] if force else load_messages(conv_json_path)
    ledger = UsageLedger(None if force else load_usage(conv_json_path), backend)
    if force:
        document = blank_results(rel, model_name)
    else:
        document = load_results(results_path / "results.json", rel, model_name)
        document["scenario"] = rel
        document["judge_model"] = model_name
        document["models"] = [model for model in document["models"] if model.get("key") in allowed_keys]
        for model in document["models"]:
            model["avg_tps"] = script_tps(model["key"], tps_map, model.get("avg_tps"))
        document["models"] = sort_models(document["models"])

    stored = {model.get("key") for model in document["models"]}
    missing = [key for key in ordered_keys if key not in stored]

    if not missing and not force:
        print(f"  All {len(ordered_keys)} models already evaluated, skipping.")
        if not dry_run:
            publish_results(
                results_path, document, messages, model_name, ordered_keys,
                conv_json_path, conv_md_path, ledger.consume(backend),
            )
        return

    print(f"  Evaluating {len(missing)} model(s) in batches of {batch_size}")
    if force and not dry_run:
        write_results(results_path / "results.json", document)

    instructions = ""
    if config.EVAL_INSTRUCTIONS_PATH.exists():
        instructions = config.EVAL_INSTRUCTIONS_PATH.read_text(encoding="utf-8")

    file_map = {key: path for key, path in result_files}
    total_batches = (len(missing) + batch_size - 1) // batch_size if missing else 0
    for i in range(0, len(missing), batch_size):
        batch_num = i // batch_size + 1
        batch_keys = missing[i:i + batch_size]
        print(f"  Batch {batch_num}/{total_batches}: {', '.join(batch_keys)}")
        user_msg = build_batch_message(instructions, document, batch_keys, file_map)

        if dry_run:
            print(f"  [dry-run] Would send batch of {len(batch_keys)} models")
            continue

        if DEBUG:
            print(f"  [debug] About to call backend for batch {batch_num}")
        print(f"  Sending batch {batch_num}...")
        document, exchange = request_evaluation(
            backend, user_msg, document, batch_keys, allowed_keys, tps_map
        )
        messages.extend(exchange)
        publish_results(
            results_path, document, messages, model_name, ordered_keys,
            conv_json_path, conv_md_path, ledger.consume(backend),
        )
        print(f"  Batch {batch_num} complete.")

    if dry_run:
        print("  [dry-run] Skipping result files")


def find_scenarios(target: str | None) -> list[Path]:
    if target:
        p = config.RESULTS_DIR / target
        if p.is_dir():
            return [p]
        print(f"Scenario not found: {target}")
        return []
    found = []
    if config.RESULTS_DIR.exists():
        for p in config.RESULTS_DIR.rglob("*"):
            if p.is_dir() and (p / "models.json").exists():
                found.append(p)
    return sorted(found)


def main():
    parser = argparse.ArgumentParser(description="Evaluate LM Studio test results.")
    parser.add_argument("--scenario", help="Relative path under results/ (e.g. summary/expedition)")
    parser.add_argument("--force", action="store_true", help="Re-evaluate all models even if already done")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be sent without calling the backend")
    parser.add_argument("--batch-size", type=int, default=None, help="Override EVAL_BATCH_SIZE")
    args = parser.parse_args()

    batch_size = args.batch_size if args.batch_size is not None else config.EVAL_BATCH_SIZE
    if batch_size < 1:
        raise SystemExit("Batch size must be at least 1.")
    dry_run = args.dry_run or config.EVAL_DRY_RUN

    print("")
    print(f"Batch size: {batch_size}")
    if dry_run:
        print("DRY RUN — no API calls will be made and no result files will be written")

    try:
        backend = resolve_backend(dry_run)
    except Exception as e:
        print(f"Failed to load backend: {e}")
        sys.exit(1)

    scenarios = find_scenarios(args.scenario)
    if not scenarios:
        print("No scenarios found.")
        return

    print(f"Scenarios to process: {len(scenarios)}")
    for results_path in scenarios:
        rel = results_path.relative_to(config.RESULTS_DIR).as_posix()
        print(f"\n=== {rel} ===")
        try:
            evaluate_scenario(results_path, backend, batch_size, args.force, dry_run)
        except Exception as e:
            print(f"  Error: {e}")

    print("\nDone.")

    # Print API usage stats if the backend tracks them
    if hasattr(backend, "get_stats"):
        stats = backend.get_stats()
        if stats.get("requests", 0) > 0:
            print("\nAPI usage:")
            print(f"  Requests:          {stats['requests']}")
            print(f"  Prompt tokens:     {stats['prompt_tokens']:,}")
            print(f"  Completion tokens: {stats['completion_tokens']:,}")
            print(f"  Total tokens:      {stats['total_tokens']:,}")


if __name__ == "__main__":
    main()
