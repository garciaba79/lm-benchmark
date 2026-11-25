#!/usr/bin/env python3
"""
Archive and remove results for models that are not on the active list.

The active list is scenarios/models.json. This script does not run models.py
and does not change that file. Run models.py yourself when you want LM Studio
to replace the active list.

A model that is still in a scenario's results, but not on the active list, is
a historic model. Archive copies that model's <model>.md and <model>.json and
upserts its records into the archive JSON files. It also copies scenario-level
info.md, results.md, results.json, evaluation.json, evaluation-<model>.json,
and evaluation-<model>.md into the archive and leaves those live copies in place.
Removing live records always archives first. Models that remain on the active
list are left in place.

Usage:
  python clean.py                       # uses the defaults in config.py
  python clean.py archive               # archive only
  python clean.py clean                 # clean results and stats
  python clean.py results               # remove result files only
  python clean.py stats                 # update stats files only
  python clean.py archive clean         # archive then clean

If any command-line options are given, only those options are enabled.
If no options are given, the defaults from config.py are used.

clean.py
version 0.3.0
"""

import shutil
import subprocess
import sys
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


def get_active_models():
    """Active list only. An empty or unreadable list aborts so results are not wiped."""
    if not config.MODELS_PATH.exists():
        print(f"Missing {config.MODELS_PATH}. Refusing to archive or clean.")
        raise SystemExit(1)
    data = utils.load_json(config.MODELS_PATH, required=True)
    if not isinstance(data, (list, dict)):
        print(f"{config.MODELS_PATH} must be a list of model records. Refusing to archive or clean.")
        raise SystemExit(1)
    models = utils.keyed_records(data)
    if not models:
        print(f"{config.MODELS_PATH} has no model keys.")
        print("Refusing to archive or clean. An empty active list does not delete results.")
        print("Restore the file, or run models.py and edit it, then try again.")
        raise SystemExit(1)
    return models


def collect_removed_models(active_keys):
    """Historic scenario records whose model key is not on the active list."""
    removed = {}
    if not config.RESULTS_DIR.exists():
        return removed

    for results_path in config.RESULTS_DIR.rglob("*"):
        if not results_path.is_dir():
            continue
        models_path = results_path / "models.json"
        if not models_path.exists():
            continue
        models = utils.keyed_records(utils.load_json(models_path, required=False))
        rel = results_path.relative_to(config.RESULTS_DIR).as_posix()
        if rel == ".":
            continue
        missing = [model for model in models if model.get("key") not in active_keys]
        if missing:
            removed[rel] = missing
    return removed


def has_inactive_root_models(active_keys):
    root_stats = utils.load_json(config.ROOT_STATS_JSON, required=False)
    if not isinstance(root_stats, dict):
        return False
    return any(
        record.get("key") not in active_keys
        for record in utils.keyed_records(root_stats.get("models"))
    )


def copy_scenario_snapshots(src_results, dst_results, rel):
    """Copy scenario-level files. The live copies stay."""
    names = ["info.md", "results.md", "results.json", "evaluation.json"]
    names.extend(path.name for path in src_results.glob("evaluation-*") if path.is_file())
    for name in names:
        src = src_results / name
        if src.is_file():
            shutil.copy2(src, dst_results / name)
            print(f"  Archived {rel}/{name}")


def archive_root_stats(archive_root, active_keys):
    root_stats = utils.load_json(config.ROOT_STATS_JSON, required=False)
    if not isinstance(root_stats, dict):
        return
    inactive = [
        record for record in utils.keyed_records(root_stats.get("models"))
        if record.get("key") not in active_keys
    ]
    if not inactive:
        return
    archive_stats_path = archive_root / "stats.json"
    existing_archive = utils.load_json(archive_stats_path, required=False) if archive_stats_path.exists() else {}
    archived_root_models = utils.keyed_records(existing_archive.get("models") if isinstance(existing_archive, dict) else [])
    for record in inactive:
        archived_root_models = utils.upsert_record(archived_root_models, record)
    archived_root = {
        "run_time": root_stats.get("run_time"),
        "overall_seconds": root_stats.get("overall_seconds"),
        "models": archived_root_models,
    }
    utils.save_json(archive_stats_path, archived_root)
    (archive_root / "stats.md").write_text(
        utils.build_root_stats_md(archived_root_models, archived_root.get("overall_seconds")),
        encoding="utf-8",
    )


def archive_removed(removed, active_keys):
    archive_root = utils.today_archive_folder()
    archive_results = archive_root / "results"
    archive_results.mkdir(parents=True, exist_ok=True)
    print(f"Archiving to {archive_root}")

    for rel, models in removed.items():
        src_results = config.RESULTS_DIR / rel
        dst_results = archive_results / rel
        dst_results.mkdir(parents=True, exist_ok=True)

        for model in models:
            src_file = utils.result_file_for_model(src_results, model)
            if src_file.exists():
                shutil.copy2(src_file, dst_results / src_file.name)
                print(f"  Archived {rel}/{src_file.name}")
            src_json = utils.transcript_json_for_model(src_results, model)
            if src_json.exists():
                shutil.copy2(src_json, dst_results / src_json.name)
                print(f"  Archived {rel}/{src_json.name}")

        dst_models_path = dst_results / "models.json"
        archived_models = utils.keyed_records(utils.load_json(dst_models_path, required=False) if dst_models_path.exists() else [])
        for model in models:
            archived_models = utils.upsert_record(archived_models, model)
        utils.save_json(dst_models_path, archived_models)

        src_stats = utils.load_json(src_results / "stats.json", required=False)
        if isinstance(src_stats, dict):
            moving = {model.get("key") for model in models}
            dst_stats_path = dst_results / "stats.json"
            existing_stats = utils.load_json(dst_stats_path, required=False) if dst_stats_path.exists() else {}
            archived_stats_models = utils.keyed_records(existing_stats.get("models") if isinstance(existing_stats, dict) else [])
            for record in utils.keyed_records(src_stats.get("models")):
                if record.get("key") in moving:
                    archived_stats_models = utils.upsert_record(archived_stats_models, record)
            merged = {
                "scenario": rel,
                "run_time": src_stats.get("run_time") or (existing_stats.get("run_time") if isinstance(existing_stats, dict) else None),
                "overall_seconds": sum((record.get("total_seconds") or 0) for record in archived_stats_models if "error" not in record),
                "models": archived_stats_models,
            }
            utils.save_json(dst_stats_path, merged)
            (dst_results / "stats.md").write_text(utils.build_stats_md(merged), encoding="utf-8")

        lines = [f"# Archived: {rel}", "", "Models in this archive:", ""]
        for model in archived_models:
            lines.append(f"- {model.get('display_name') or model.get('key')}")
        (dst_results / "test.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        copy_scenario_snapshots(src_results, dst_results, rel)

    archive_root_stats(archive_root, active_keys)
    print("Archive complete.")


def results(removed):
    print("Cleaning result files...")
    for rel, models in removed.items():
        results_path = config.RESULTS_DIR / rel
        for m in models:
            rfile = utils.result_file_for_model(results_path, m)
            json_file = utils.transcript_json_for_model(results_path, m)
            for path in (rfile, json_file):
                if path.exists():
                    path.unlink()
                    print(f"  Removed {rel}/{path.name}")


def rewrite_scenario_views(results_path, rel):
    """Rebuild stats.md and test.md from the records that are still present."""
    stats_path = results_path / "stats.json"
    stats = utils.load_json(stats_path, required=False) if stats_path.exists() else {}
    if isinstance(stats, dict) and stats:
        models = utils.keyed_records(stats.get("models"))
        stats["models"] = models
        stats["overall_seconds"] = sum((model.get("total_seconds") or 0) for model in models if "error" not in model)
        utils.save_json(stats_path, stats)
        (results_path / "stats.md").write_text(utils.build_stats_md(stats), encoding="utf-8")
        summary_models = models
        created = stats.get("run_time") or ""
    else:
        summary_models = utils.keyed_records(utils.load_json(results_path / "models.json", required=False))
        created = ""

    test_path = results_path / "test.md"
    eval_section = ""
    if test_path.exists():
        eval_section = utils.evaluation_section(test_path.read_text(encoding="utf-8"))
    test_info = utils.load_json(config.SCENARIOS_DIR / rel / config.TEST_JSON, required=False) or {}
    test_md = utils.build_test_md(test_info if isinstance(test_info, dict) else {}, rel, created, summary_models)
    test_path.write_text(utils.append_evaluation_section(test_md, eval_section), encoding="utf-8")


def clean_stats(removed, active_keys):
    print("Cleaning stats and model lists...")
    for rel, models in removed.items():
        results_path = config.RESULTS_DIR / rel
        drop = {model.get("key") for model in models if model.get("key")}
        models_path = results_path / "models.json"
        if models_path.exists():
            kept = utils.remove_records(utils.load_json(models_path, required=False), drop)
            utils.save_json(models_path, kept)

        stats_path = results_path / "stats.json"
        if stats_path.exists():
            stats = utils.load_json(stats_path, required=False)
            if isinstance(stats, dict):
                stats["models"] = utils.remove_records(stats.get("models"), drop)
                utils.save_json(stats_path, stats)
        rewrite_scenario_views(results_path, rel)

    root_stats = utils.load_json(config.ROOT_STATS_JSON, required=False)
    if isinstance(root_stats, dict):
        root_stats["models"] = [
            model for model in utils.keyed_records(root_stats.get("models"))
            if model.get("key") in active_keys
        ]
        utils.save_json(config.ROOT_STATS_JSON, root_stats)
        config.ROOT_STATS_MD.write_text(
            utils.build_root_stats_md(root_stats["models"], root_stats.get("overall_seconds")),
            encoding="utf-8",
        )
        print("  Updated root stats")


def main():
    opts = parse_args()
    print("Options:", {k: v for k, v in opts.items() if v})
    print(f"Active model list: {config.MODELS_PATH}")

    active_models = get_active_models()
    active_keys = set(utils.active_model_keys(active_models))
    removed = collect_removed_models(active_keys)

    if not removed and not has_inactive_root_models(active_keys):
        print("No removed models found in results.")
        return

    if removed:
        print(f"Found removed models in {len(removed)} scenario(s).")
    else:
        print("Scenario results match the active list. Root stats still have other models.")

    will_remove = opts["results"] or opts["stats"]
    if opts["archive"] or will_remove:
        if will_remove and not opts["archive"]:
            print("Archiving before live records are removed.")
        archive_removed(removed, active_keys)

    if opts["results"]:
        results(removed)

    if opts["stats"]:
        clean_stats(removed, active_keys)

    if opts["results"] or opts["stats"]:
        scenarios_script = Path("scenarios.py")
        if scenarios_script.exists():
            print("Refreshing scenario status...")
            subprocess.run([sys.executable, str(scenarios_script)], check=False)

    print("Done.")


if __name__ == "__main__":
    main()
