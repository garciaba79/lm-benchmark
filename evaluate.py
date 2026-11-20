#!/usr/bin/env python3
"""
Evaluate LM Studio test results with a cloud model.

Reads result files from results/<scenario>/, sends them in batches to the
configured backend, and writes a ranked results.md. The conversation is stored
in evaluation-<model>.json (source of truth) and evaluation-<model>.md.
evaluated_keys in the JSON records which local model keys have been scored.
test.md gets an evaluation status section.

The backend and model come from config.py. The API key is the one named for
that backend in .env.

Usage:
  python evaluate.py                                        # all scenarios (update mode)
  python evaluate.py --scenario summary/expedition
  python evaluate.py --force                                # re-evaluate everything
  python evaluate.py --dry-run
  python evaluate.py --batch-size 3

evaluate.py
version 0.2.0
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


def keys_from_user_messages(messages: list[dict], known_keys: set[str]) -> list[str]:
    """Model keys this script put in batch messages as '### <key>' lines."""
    found = []
    seen = set()
    for msg in messages:
        if msg.get("role") != "user":
            continue
        for line in (msg.get("content") or "").splitlines():
            if not line.startswith("### "):
                continue
            key = line[4:].strip()
            if key in known_keys and key not in seen:
                seen.add(key)
                found.append(key)
    return found


def infer_final_complete(messages: list[dict]) -> bool:
    prompt = config.EVAL_FINAL_PROMPT
    for index, msg in enumerate(messages):
        if msg.get("role") == "user" and prompt in (msg.get("content") or ""):
            return any(later.get("role") == "assistant" for later in messages[index + 1:])
    return False


def load_evaluation_state(path: Path, known_keys: list[str]):
    """
    Return messages, evaluated key list, final_complete, and whether the file
    already stored evaluated_keys. Older files are seeded from their ### key lines.
    """
    known = set(known_keys)
    if not path.exists():
        return [], [], False, True
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return [], [], False, True
    messages = data.get("messages") or []
    had_keys = "evaluated_keys" in data
    if had_keys:
        evaluated = [key for key in data.get("evaluated_keys") or [] if key in known]
    else:
        evaluated = keys_from_user_messages(messages, known)
    if "final_complete" in data:
        final_complete = bool(data.get("final_complete"))
    else:
        final_complete = infer_final_complete(messages)
    return messages, evaluated, final_complete, had_keys


def write_conversation_json(path: Path, messages: list[dict], model_name: str, evaluated_keys: list[str], final_complete: bool):
    """Write the current conversation as the source of truth."""
    data = {
        "model": model_name,
        "evaluated_keys": list(evaluated_keys),
        "final_complete": final_complete,
        "messages": messages,
    }
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


def strip_final_ranking(messages: list[dict]) -> list[dict]:
    """Remove the final-ranking user turn and everything after it."""
    for i, msg in enumerate(messages):
        if msg.get("role") == "user" and config.EVAL_FINAL_PROMPT in msg.get("content", ""):
            return messages[:i]
    return messages


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

    messages, evaluated, final_complete, had_keys = load_evaluation_state(conv_json_path, ordered_keys)
    if force:
        messages = []
        evaluated = []
        final_complete = False
    evaluated_set = set(evaluated)
    missing = [key for key in ordered_keys if key not in evaluated_set]
    if missing and messages and not force:
        messages = strip_final_ranking(messages)
        final_complete = False

    if not missing and final_complete and not force:
        print(f"  All {len(ordered_keys)} models already evaluated, skipping.")
        if not dry_run:
            if not had_keys:
                write_conversation_json(conv_json_path, messages, model_name, evaluated, True)
            utils.update_test_md_evaluation(results_path, len(ordered_keys), len(ordered_keys), [])
            print("  Updated evaluation status in test.md")
        return

    if not missing and not force:
        print("  Scores are already recorded. Requesting the final ranking only.")
    else:
        print(f"  Evaluating {len(missing)} model(s) in batches of {batch_size}")

    # Load instructions once
    instructions = ""
    if config.EVAL_INSTRUCTIONS_PATH.exists():
        instructions = config.EVAL_INSTRUCTIONS_PATH.read_text(encoding="utf-8")

    # First message
    if not messages:
        first = config.EVAL_INITIAL_PROMPT
        if instructions:
            first = f"{first}\n\n---\n\n{instructions}"
        messages.append({"role": "user", "content": first})
        if not dry_run:
            print("  Sending initial prompt...")
            reply = backend.generate(messages)
            messages.append({"role": "assistant", "content": reply})
            write_conversation_json(conv_json_path, messages, model_name, evaluated, False)
            print("  Initial prompt acknowledged.")
        else:
            print("  [dry-run] Would send initial prompt")

    # Batches
    file_map = {key: path for key, path in result_files}
    total_batches = (len(missing) + batch_size - 1) // batch_size
    for i in range(0, len(missing), batch_size):
        batch_num = i // batch_size + 1
        batch_keys = missing[i:i + batch_size]
        print(f"  Batch {batch_num}/{total_batches}: {', '.join(batch_keys)}")

        batch_content = [config.EVAL_BATCH_PROMPT, ""]
        for key in batch_keys:
            path = file_map[key]
            content = path.read_text(encoding="utf-8")
            batch_content.append(f"### {key}")
            batch_content.append("")
            batch_content.append(content)
            batch_content.append("")
        user_msg = "\n".join(batch_content).rstrip()
        messages.append({"role": "user", "content": user_msg})

        if dry_run:
            print(f"  [dry-run] Would send batch of {len(batch_keys)} models")
            messages.append({"role": "assistant", "content": "[dry-run reply]"})
        else:
            if DEBUG:
                print(f"  [debug] About to call backend for batch {batch_num}")
            print(f"  Sending batch {batch_num}...")
            reply = backend.generate(messages)
            messages.append({"role": "assistant", "content": reply})
            for key in batch_keys:
                if key not in evaluated_set:
                    evaluated.append(key)
                    evaluated_set.add(key)
            write_conversation_json(conv_json_path, messages, model_name, evaluated, False)
            print(f"  Batch {batch_num} complete.")
            if DEBUG:
                print(f"  [debug] Reply length: {len(reply)} characters")

    # Final ranking
    print("  Requesting final ranking...")
    messages.append({"role": "user", "content": config.EVAL_FINAL_PROMPT})
    if dry_run:
        final = "[dry-run final ranking]"
        messages.append({"role": "assistant", "content": final})
        print("  [dry-run] Would request final ranking")
    else:
        final = backend.generate(messages)
        messages.append({"role": "assistant", "content": final})
        final_complete = True
        write_conversation_json(conv_json_path, messages, model_name, evaluated, True)
        print("  Final ranking received.")

    missing_after = [key for key in ordered_keys if key not in evaluated_set]
    evaluated_count = len(ordered_keys) - len(missing_after)

    if not dry_run:
        results_md = results_path / "results.md"
        results_md.write_text(final + "\n", encoding="utf-8")
        write_conversation_md(conv_md_path, messages)
        utils.write_evaluation_index(results_path)
        utils.update_test_md_evaluation(results_path, evaluated_count, len(ordered_keys), missing_after)
        print(f"  Wrote {results_md.name}, {conv_json_path.name}, and {conv_md_path.name}")
        print("  Updated evaluation status in test.md")
    else:
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
