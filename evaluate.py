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

    if name == "grok_cli":
        return GrokCLIBackend(model=model)
    if name in ("openai", "grok_api", "gemini"):
        return OpenAICompatibleBackend(base_url=base_url, model=model)
    if name == "anthropic":
        return AnthropicBackend(model=model)
    raise SystemExit(f"Unknown EVAL_BACKEND: {name}")


def parse_grok_md(path: Path) -> list[dict]:
    """Rebuild message history from an existing grok.md file."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    messages = []
    # Split on ## User / ## Assistant headings
    parts = re.split(r"^## (User|Assistant)\s*$", text, flags=re.MULTILINE)
    # parts[0] is the header, then alternating role, content
    for i in range(1, len(parts), 2):
        role = parts[i].lower()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if content:
            messages.append({"role": role, "content": content})
    return messages


def write_grok_md(path: Path, messages: list[dict]):
    lines = ["# Evaluation conversation", ""]
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"## {role}")
        lines.append("")
        lines.append(msg["content"].rstrip())
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


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

    grok_md_path = results_path / "grok.md"
    messages = parse_grok_md(grok_md_path)

    all_keys = {key for key, _ in result_files}
    already_evaluated = get_evaluated_keys(messages) if messages else set()
    missing = [key for key, _ in result_files if key not in already_evaluated]

    if not missing and not force:
        print(f"  All {len(all_keys)} models already evaluated, skipping.")
        utils.update_test_md_evaluation(results_path, len(all_keys), len(all_keys), [])
        return

    if force:
        missing = [key for key, _ in result_files]
        messages = []  # start fresh

    print(f"  Evaluating {len(missing)} model(s) (batch size {batch_size})")

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
            reply = backend.generate(messages)
            messages.append({"role": "assistant", "content": reply})
            print("  Initial prompt acknowledged.")

    # Batches
    file_map = {key: path for key, path in result_files}
    for i in range(0, len(missing), batch_size):
        batch_keys = missing[i:i + batch_size]
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
            reply = backend.generate(messages)
            messages.append({"role": "assistant", "content": reply})
            print(f"  Batch {i // batch_size + 1} complete.")

    # Final ranking
    messages.append({"role": "user", "content": config.EVAL_FINAL_PROMPT})
    if dry_run:
        final = "[dry-run final ranking]"
        messages.append({"role": "assistant", "content": final})
    else:
        final = backend.generate(messages)
        messages.append({"role": "assistant", "content": final})
        print("  Final ranking received.")

    # Write outputs
    evaluated_count = len(all_keys) if force or not already_evaluated else len(already_evaluated) + len(missing)
    missing_after = [k for k in all_keys if k not in (already_evaluated | set(missing))]

    if not dry_run:
        results_md = results_path / "results.md"
        results_md.write_text(final + "\n", encoding="utf-8")
        write_grok_md(grok_md_path, messages)
        print(f"  Wrote {results_md.name} and {grok_md_path.name}")
    else:
        print("  [dry-run] Skipping results.md and grok.md")

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


if __name__ == "__main__":
    main()
