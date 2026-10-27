#!/usr/bin/env python3
"""
Run the full test suite against every model listed in models.json.
Loads each model, asks every question in order, captures stats,
writes one markdown file per model, plus a test summary and empty results.md.

run_tests.py
version 0.0.0
"""

import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
import requests

CONFIG_PATH = "config.json"
TEST_PATH = "test.json"
MODELS_PATH = "models.json"
QUESTIONS_PATH = "questions.json"
RESULTS_DIR = "results"

def load_json(path, required=True):
    if not os.path.exists(path):
        if required:
            print(f"Missing required file: {path}")
            raise SystemExit(1)
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_headers(token):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def safe_filename(name):
    # Keep it readable but filesystem-safe
    keep = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_ ."
    cleaned = "".join(c if c in keep else "-" for c in name)
    return cleaned.strip().replace("  ", " ")[:80]

def format_context(context_length):
    if not context_length:
        return "unknown"
    if context_length >= 1000:
        return f"{context_length // 1024}K" if context_length % 1024 == 0 else f"{context_length}"
    return str(context_length)

def load_model(base_url, headers, model_key):
    url = f"{base_url}/api/v1/models/load"
    payload = {
        "model": model_key,
        "echo_load_config": True
    }
    print(f"  Loading {model_key} ...")
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    context = None
    if "load_config" in data and data["load_config"]:
        context = data["load_config"].get("context_length")
    return data.get("instance_id"), context, data

def unload_model(base_url, headers, instance_id):
    if not instance_id:
        return
    url = f"{base_url}/api/v1/models/unload"
    try:
        requests.post(url, headers=headers, json={"instance_id": instance_id}, timeout=30)
        print(f"  Unloaded {instance_id}")
    except Exception as e:
        print(f"  Warning: could not unload {instance_id}: {e}")

def chat(base_url, headers, model_key, messages):
    url = f"{base_url}/api/v0/chat/completions"
    payload = {
        "model": model_key,
        "messages": messages,
        "stream": False,
        "max_tokens": -1
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=300)
    resp.raise_for_status()
    return resp.json()

def build_markdown(model_info, created_str, context_str, turns, overall_stats=None):
    lines = []
    name = model_info.get("display_name") or model_info.get("key")
    lines.append(f"# {name}")
    lines.append(f"Model: {model_info.get('key')}")
    lines.append(f"Created: {created_str}")
    lines.append("Exported from: LM Studio (via test script)")
    if overall_stats:
        lines.append(f"Tokens {overall_stats}")
    lines.append(f"Context {context_str}")
    lines.append("")

    for turn in turns:
        lines.append("### User")
        lines.append("")
        lines.append(turn["user"])
        lines.append("")
        lines.append("### Assistant")
        lines.append("")
        lines.append(turn["assistant"])
        lines.append("")
        if turn.get("stats_line"):
            lines.append(turn["stats_line"])
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"

def main():
    config = load_json(CONFIG_PATH)
    test_info = load_json(TEST_PATH)
    models = load_json(MODELS_PATH)
    questions = load_json(QUESTIONS_PATH)

    if not isinstance(questions, list) or not questions:
        print("questions.json must be a non-empty array of strings")
        raise SystemExit(1)

    base_url = config.get("base_url", "http://localhost:1234").rstrip("/")
    token = config.get("api_token", "")
    headers = get_headers(token)

    results_path = Path(RESULTS_DIR)
    results_path.mkdir(exist_ok=True)

    # Empty results.md for the cloud evaluation
    results_md = results_path / "results.md"
    if not results_md.exists():
        results_md.write_text("# Evaluation Results\n\nPaste the cloud model evaluation here.\n", encoding="utf-8")

    test_name = test_info.get("name", "Untitled Test")
    test_desc = test_info.get("description", "")
    run_time = datetime.now()
    run_str = run_time.strftime("%Y-%m-%d %H.%M")
    created_str = run_time.strftime("%m/%d/%Y, %I:%M:%S %p")

    summary_models = []
    print(f"Starting test: {test_name}")
    print(f"Models: {len(models)} | Questions: {len(questions)}")
    print(f"Results will be written to {RESULTS_DIR}/\n")

    for model in models:
        model_key = model.get("key")
        if not model_key:
            continue

        print(f"Testing {model_key}")
        instance_id = None
        context_length = None
        turns = []
        total_tokens = 0
        total_time = 0.0

        try:
            instance_id, context_length, load_data = load_model(base_url, headers, model_key)
            context_str = format_context(context_length)

            messages = []
            for q in questions:
                messages.append({"role": "user", "content": q})
                start = time.time()
                response = chat(base_url, headers, model_key, messages)
                elapsed = time.time() - start

                choice = response.get("choices", [{}])[0]
                assistant_text = choice.get("message", {}).get("content", "").strip()
                messages.append({"role": "assistant", "content": assistant_text})

                usage = response.get("usage", {})
                stats = response.get("stats", {})
                model_info_resp = response.get("model_info", {})

                completion_tokens = usage.get("completion_tokens", 0)
                total_tokens += usage.get("total_tokens", 0)
                gen_time = stats.get("generation_time", elapsed)
                tps = stats.get("tokens_per_second")
                if tps is None and gen_time and completion_tokens:
                    tps = completion_tokens / gen_time

                total_time += gen_time

                context_used = usage.get("total_tokens", 0)
                pct = 0
                if context_length and context_used:
                    pct = round((context_used / context_length) * 100)

                stats_parts = []
                if tps is not None:
                    stats_parts.append(f"{tps:.0f} t/s")
                if completion_tokens:
                    stats_parts.append(f"{completion_tokens} tokens")
                stats_parts.append(f"{gen_time:.0f}s")
                if pct:
                    stats_parts.append(f"{pct}%")

                stats_line = ", ".join(stats_parts) if stats_parts else None

                turns.append({
                    "user": q,
                    "assistant": assistant_text,
                    "stats_line": stats_line
                })

            # Overall stats line for the header (simple average or last)
            overall = None
            if turns and any(t.get("stats_line") for t in turns):
                # Just note that per-turn stats are below
                overall = "see turns"

            md_content = build_markdown(
                model,
                created_str,
                context_str,
                turns,
                overall
            )

            fname = safe_filename(f"{model.get('display_name') or model_key} - {run_str}")
            out_file = results_path / f"{fname}.md"
            out_file.write_text(md_content, encoding="utf-8")
            print(f"  Wrote {out_file.name}")

            summary_models.append({
                "key": model_key,
                "display_name": model.get("display_name"),
                "params": model.get("params"),
                "quant": model.get("quant"),
                "size_gb": model.get("size_gb"),
                "context": context_str,
                "file": out_file.name
            })

        except Exception as e:
            print(f"  Error with {model_key}: {e}")
            summary_models.append({
                "key": model_key,
                "error": str(e)
            })
        finally:
            unload_model(base_url, headers, instance_id)

        print()

    # Write test summary
    summary_lines = [
        f"# Test Summary: {test_name}",
        "",
        f"**Description:** {test_desc}",
        "",
        f"**Run time:** {created_str}",
        f"**Models tested:** {len(summary_models)}",
        f"**Questions:** {len(questions)}",
        "",
        "## Models",
        ""
    ]
    for sm in summary_models:
        if "error" in sm:
            summary_lines.append(f"- {sm['key']} — ERROR: {sm['error']}")
        else:
            summary_lines.append(
                f"- {sm.get('display_name') or sm['key']} "
                f"({sm.get('params') or '?'} / {sm.get('quant') or '?'} / {sm.get('size_gb')} GB) "
                f"Context: {sm.get('context')} → `{sm.get('file')}`"
            )

    summary_path = results_path / "test_summary.md"
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"Wrote {summary_path}")
    print(f"Empty evaluation file: {results_md}")
    print("Done.")

if __name__ == "__main__":
    main()
