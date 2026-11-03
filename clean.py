#!/usr/bin/env python3
"""
Clean and archive results for models that are no longer installed.

Usage:
  python clean.py                       # uses the defaults in config.py
  python clean.py archive               # archive only
  python clean.py clean                 # clean results and stats
  python clean.py results               # remove result files only
  python clean.py stats                 # update stats files only
  python clean.py archive clean         # archive then clean

If any command-line options are given, only those options are enabled.
If no options are given, the defaults from config.py are used.

Options:
  archive       Copy data for models that are no longer installed into
                archive/YYYY MM DD/. Always runs first when enabled.
                Does not modify the live results.
  clean         Clean both results and stats (same as results + stats).
  results       Remove the conversation .md files for missing models.
  stats         Remove missing models from models.json, stats.json, stats.md,
                and test.md (scenario and root).

Archive never modifies existing live files. Clean never touches the archive folder.
The script always refreshes the model list first (via models.py) and refreshes
scenario status at the end (via scenarios.py) when any clean option is used.

clean.py
version 0.1.0
"""

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import config
import utils


def parse_args():
    args = set(sys.argv[1:])
    valid = {"archive", "clean", "results", "stats"}
    unknown = args - valid
    if unknown:
        print(f"Unknown options: {', '.join(sorted(unknown))}")
        print("Valid options: archive, clean, results, stats")
        raise SystemExit(1)

    if not args:
        return {
            "archive": config.ARCHIVE,
            "clean": config.CLEAN,
            "results": config.RESULTS,
            "stats": config.STATS,
        }

    opts = {k: False for k in valid}
    for a in args:
        opts[a] = True
    if opts["clean"]:
        opts["results"] = True
        opts["stats"] = True
    return opts


def get_current_model_keys():
    models = utils.load_json(config.MODELS_PATH, required=False)
    if not isinstance(models, list):
        return set()
    return {m.get("key") for m in models if m.get("key")}


def collect_removed_models(current_keys):
    """Return dict of scenario_rel -> list of model dicts that are no longer installed."""
    removed = {}
    if not config.RESULTS_DIR.exists():
        return removed

    for results_path in config.RESULTS_DIR.rglob("*"):
        if not results_path.is_dir():
            continue
        models_path = results_path / "models.json"
        if not models_path.exists():
            continue
        models = utils.load_json(models_path, required=False)
        if not isinstance(models, list):
            continue
        rel = results_path.relative_to(config.RESULTS_DIR).as_posix()
        missing = [m for m in models if m.get("key") and m.get("key") not in current_keys]
        if missing:
            removed[rel] = missing
    return removed


def archive_removed(removed, current_keys):
    archive_root = utils.today_archive_folder()
    archive_results = archive_root / "results"
    archive_results.mkdir(parents=True, exist_ok=True)
    print(f"Archiving to {archive_root}")

    for rel, models in removed.items():
        src_results = config.RESULTS_DIR / rel
        dst_results = archive_results / rel
        dst_results.mkdir(parents=True, exist_ok=True)

        # Copy conversation files
        for m in models:
            src_file = utils.result_file_for_model(src_results, m)
            if src_file.exists():
                dst_file = dst_results / src_file.name
                shutil.copy2(src_file, dst_file)
                print(f"  Archived {rel}/{src_file.name}")

        # Merge models.json (keyed update)
        dst_models_path = dst_results / "models.json"
        existing = utils.load_json(dst_models_path, required=False) if dst_models_path.exists() else []
        if not isinstance(existing, list):
            existing = []
        model_map = {m.get("key"): m for m in existing if m.get("key")}
        for m in models:
            if m.get("key"):
                model_map[m["key"]] = m
        utils.save_json(dst_models_path, list(model_map.values()))

        # Merge stats.json
        src_stats = utils.load_json(src_results / "stats.json", required=False)
        if isinstance(src_stats, dict):
            keep = [s for s in src_stats.get("models", []) if s.get("key") in {m.get("key") for m in models}]
            dst_stats_path = dst_results / "stats.json"
            existing_stats = utils.load_json(dst_stats_path, required=False) if dst_stats_path.exists() else {}
            if not isinstance(existing_stats, dict):
                existing_stats = {}
            old_map = {s.get("key"): s for s in existing_stats.get("models", []) if s.get("key")}
            for s in keep:
                if s.get("key"):
                    old_map[s["key"]] = s
            merged = {
                "scenario": rel,
                "run_time": src_stats.get("run_time"),
                "models": list(old_map.values())
            }
            utils.save_json(dst_stats_path, merged)

            # Simple stats.md
            lines = ["# Stats", "", f"Archived models for {rel}", ""]
            for s in merged["models"]:
                name = s.get("display_name") or s.get("key")
                lines.append(f"- {name}")
            (dst_results / "stats.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

        # Simple test.md
        lines = [f"# Archived: {rel}", "", "Models removed from live results:", ""]
        for m in models:
            name = m.get("display_name") or m.get("key")
            lines.append(f"- {name}")
        (dst_results / "test.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Root stats filtered to removed models
    root_stats = utils.load_json(config.ROOT_STATS_JSON, required=False)
    if isinstance(root_stats, dict):
        removed_keys = set()
        for models in removed.values():
            for m in models:
                if m.get("key"):
                    removed_keys.add(m.get("key"))
        keep = [s for s in root_stats.get("models", []) if s.get("key") in removed_keys]
        if keep:
            archived_root = {
                "run_time": root_stats.get("run_time"),
                "models": keep
            }
            utils.save_json(archive_root / "stats.json", archived_root)
            lines = ["# System Stats (archived)", ""]
            for s in keep:
                name = s.get("display_name") or s.get("key")
                lines.append(f"- {name}")
            (archive_root / "stats.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Archive complete.")


def results(removed):
    print("Cleaning result files...")
    for rel, models in removed.items():
        results_path = config.RESULTS_DIR / rel
        for m in models:
            rfile = utils.result_file_for_model(results_path, m)
            if rfile.exists():
                rfile.unlink()
                print(f"  Removed {rel}/{rfile.name}")


def clean_stats(removed, current_keys):
    print("Cleaning stats and model lists...")
    # Per-scenario
    for rel in removed:
        results_path = config.RESULTS_DIR / rel
        # models.json
        models_path = results_path / "models.json"
        models = utils.load_json(models_path, required=False)
        if isinstance(models, list):
            keep = [m for m in models if m.get("key") in current_keys]
            utils.save_json(models_path, keep)

        # stats.json
        stats_path = results_path / "stats.json"
        stats = utils.load_json(stats_path, required=False)
        if isinstance(stats, dict):
            keep = [s for s in stats.get("models", []) if s.get("key") in current_keys]
            stats["models"] = keep
            utils.save_json(stats_path, stats)
            # Rebuild a simple stats.md
            lines = ["# Stats", ""]
            for s in keep:
                name = s.get("display_name") or s.get("key")
                avg = f"{s.get('avg_tps', 0):.0f}" if s.get("avg_tps") is not None else "-"
                lines.append(f"- {name} ({avg} t/s)")
            (results_path / "stats.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

        # test.md
        test_path = results_path / "test.md"
        if test_path.exists():
            lines = [f"# Test: {rel}", "", "Models still present:", ""]
            kept_models = utils.load_json(models_path, required=False) if models_path.exists() else []
            if not isinstance(kept_models, list):
                kept_models = []
            for m in kept_models:
                name = m.get("display_name") or m.get("key")
                lines.append(f"- {name}")
            test_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Root stats
    root_stats = utils.load_json(config.ROOT_STATS_JSON, required=False)
    if isinstance(root_stats, dict):
        keep = [s for s in root_stats.get("models", []) if s.get("key") in current_keys]
        root_stats["models"] = keep
        utils.save_json(config.ROOT_STATS_JSON, root_stats)
        lines = ["# System Stats", ""]
        for s in keep:
            name = s.get("display_name") or s.get("key")
            lines.append(f"- {name}")
        config.ROOT_STATS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("  Updated root stats")


def main():
    opts = parse_args()
    print("Options:", {k: v for k, v in opts.items() if v})

    # Always refresh the model list first
    models_script = Path("models.py")
    if models_script.exists():
        print("Refreshing model list...")
        subprocess.run([sys.executable, str(models_script)], check=False)
    else:
        print("Warning: models.py not found, using existing models.json")

    current_keys = get_current_model_keys()
    removed = collect_removed_models(current_keys)

    if not removed:
        print("No removed models found in results.")
        return

    print(f"Found removed models in {len(removed)} scenario(s).")

    if opts["archive"]:
        archive_removed(removed, current_keys)

    if opts["results"]:
        results(removed)

    if opts["stats"]:
        clean_stats(removed, current_keys)

    if opts["results"] or opts["stats"]:
        scenarios_script = Path("scenarios.py")
        if scenarios_script.exists():
            print("Refreshing scenario status...")
            subprocess.run([sys.executable, str(scenarios_script)], check=False)

    print("Done.")


if __name__ == "__main__":
    main()
