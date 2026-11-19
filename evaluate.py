#!/usr/bin/env python3
"""
Evaluate LM Studio test results with a cloud model.

Reads result files from results/<scenario>/, sends them in batches to the
configured backend, and writes a ranked results.md plus a full conversation
to grok.md. Also updates the evaluation status section in test.md.

Usage:
  python evaluate.py                                        # all scenarios (update mode)
  python evaluate.py --scenario summary/expedition
  python evaluate.py --force                                # re-evaluate everything
  python evaluate.py --dry-run
  python evaluate.py --batch-size 3

evaluate.py
version 0.1.0
"""

import argparse
import json
import re
import sys
from pathlib import Path

import config
import utils

# Plugin loading
from plugins.base import EvaluationBackend
from plugins.grok_cli import GrokCLIBackend
from plugins.openai import OpenAICompatibleBackend
from plugins.anthropic import AnthropicBackend

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


def get_backend() -> EvaluationBackend:
    load_dotenv()
    name = config.EVAL_BACKEND
    model = config.EVAL_MODEL
    base_url = config.EVAL_BASE_URL

    if DEBUG:
        print(f"  [debug] Loading backend: {name}")

    if name == "grok_cli":
        # Pass the debug flag into the plugin
        from plugins import grok_cli
        grok_cli.DEBUG = DEBUG
        return GrokCLIBackend(model=model)
    if name in ("openai", "grok_api", "gemini"):
        return OpenAICompatibleBackend(base_url=base_url, model=model)
    if name == "anthropic":
        return AnthropicBackend(model=model)
    raise SystemExit(f"Unknown EVAL_BACKEND: {name}")


def parse_conversation_json(path: Path) -> list[dict]:
    """Load message history from evaluation-<model>.json."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("messages") or []
    except (json.JSONDecodeError, OSError):
        return []


def write_conversation_json(path: Path, messages: list[dict], model_name: str):
    """Write the current conversation as the source of truth."""
    data = {
        "model": model_name,
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


def get_evaluated_keys(messages: list[dict]) -> set[str]:
    """Very simple heuristic: look for model keys that appear in assistant replies."""
    keys = set()
    for msg in messages:
        if msg["role"] == "assistant":
            # Look for patterns like `model-key` or model-key.md
            found = re.findall(r"`([a-zA-Z0-9._-]+\.md)`|`([a-zA-Z0-9._-]+)`", msg["content"])
            for a, b in found:
                key = a or b
                if key.endswith(".md"):
                    key = key[:-3]
                keys.add(key)
    return keys


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

    models = utils.load_json(models_path, required=False)
    if not isinstance(models, list) or not models:
        print(f"  Empty models.json in {results_path}, skipping.")
        return

    result_files = collect_result_files(results_path, models)
    if not result_files:
        print(f"  No result files found in {results_path}, skipping.")
        return

    model_name = getattr(backend, "model", None) or config.EVAL_MODEL or "unknown"
    safe_model = model_name.replace("/", "-")
    conv_json_path = results_path / f"evaluation-{safe_model}.json"
    conv_md_path = results_path / f"evaluation-{safe_model}.md"

    messages = [] if force else parse_conversation_json(conv_json_path)
    if messages and not force:
        messages = strip_final_ranking(messages)

    all_keys = {key for key, _ in result_files}
    already_evaluated = get_evaluated_keys(messages) if messages else set()
    missing = [key for key, _ in result_files if key not in already_evaluated]

    if not missing and not force:
        print(f"  All {len(all_keys)} models already evaluated, skipping.")
        utils.update_test_md_evaluation(results_path, len(all_keys), len(all_keys), [])
        return

    if force:
        missing = [key for key, _ in result_files]
        messages = []

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
            write_conversation_json(conv_json_path, messages, model_name)
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
            write_conversation_json(conv_json_path, messages, model_name)
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
        write_conversation_json(conv_json_path, messages, model_name)
        print("  Final ranking received.")

    # Write outputs
    evaluated_count = len(all_keys) if force or not already_evaluated else len(already_evaluated) + len(missing)
    missing_after = [k for k in all_keys if k not in (already_evaluated | set(missing))]

    if not dry_run:
        results_md = results_path / "results.md"
        results_md.write_text(final + "\n", encoding="utf-8")
        write_conversation_md(conv_md_path, messages)
        utils.write_evaluation_index(results_path)
        print(f"  Wrote {results_md.name}, {conv_json_path.name}, and {conv_md_path.name}")
    else:
        print("  [dry-run] Skipping result files")

    # Always update the evaluation status in test.md (even in dry-run)
    utils.update_test_md_evaluation(
        results_path,
        evaluated_count,
        len(all_keys),
        missing_after
    )
    print("  Updated evaluation status in test.md")


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
    dry_run = args.dry_run or config.EVAL_DRY_RUN

    print("")
    print(f"Backend: {config.EVAL_BACKEND}")
    print(f"Batch size: {batch_size}")
    if dry_run:
        print("DRY RUN — no API calls will be made")

    try:
        backend = get_backend()
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
