# LM Benchmark

File-based Python project for testing local models in LM Studio on the same scenarios. Each scenario is a folder of questions. The scripts load one model at a time, run the questions in order, and write the chat and the stats under `results/`. `evaluate.py` can then rank those results with a cloud model.

This page is the current map of scripts and folders. Day-to-day settings are in [get-started.md](get-started.md). Cloud ranking is in [evaluation.md](evaluation.md). The short introduction is the repository [README](../README.md).

Python 3.14 is required. `config.py` exits on import when the interpreter is older.

## Scripts

| Script | Role |
|--------|------|
| `models.py` | Reads LM Studio and replaces `scenarios/models.json`. This is the only script that replaces the active list. |
| `scenarios.py` | Scans `scenarios/` and rewrites `scenarios/scenarios.json` and `scenarios/scenarios.md`. Modes already stored are kept. New scenarios get `update`. |
| `run.py` | Runs scenarios according to mode. Reads the active list and does not rewrite it. |
| `evaluate.py` | Sends result files to the cloud backend in `config.py` and writes the ranking. |
| `clean.py` | Archives, then removes, historic models that are no longer on the active list. It does not call `models.py`. |
| `config.py` | Shared settings: URLs, paths, modes, hardware thresholds, evaluation backend. |
| `utils.py` | JSON load and save, keyed updates, stats tables, path helpers. |

`models.py`, `scenarios.py`, and `run.py` take no arguments. Their switches are in `config.py` (`DRY_RUN`, `FORCE_MODE`, `BASE_URL`, and the rest). `evaluate.py` accepts `--scenario`, `--force`, `--dry-run`, and `--batch-size`. `clean.py` accepts `archive`, `clean`, `results`, and `stats`.

## Folders

```
config.py
models.py
scenarios.py
run.py
evaluate.py
clean.py
utils.py
plugins/
meta/hardware.json

scenarios/
  models.json              active list
  scenarios.json           name, ready, status, mode
  scenarios.md
  info.md                  helper prose, when the helper runs
  system.md                lowest-precedence system prompt
  inference.json           lowest-precedence inference settings
  <group>/<scenario>/
    test.json
    question1.md
    system.md              highest precedence
    inference.json         highest precedence

results/
  stats.json               root stats
  stats.md
  <group>/<scenario>/
    <model-key>.md
    models.json            historic models for this scenario
    stats.json
    stats.md
    test.md
    results.md
    evaluation-<model>.json
    evaluation-<model>.md
    evaluation.json
    info.md

archive/
  YYYY MM DD/results/      models removed from the active list
```

JSON lists stay lists of objects. Scripts accept a list or a dict of objects, update by key, and write a list.

## Active list and historic record

`scenarios/models.json` is the active list: the models to test now. `models.py` replaces the whole file from LM Studio. Hand edits there last until the next `models.py` run. `run.py` and `clean.py` only read it.

`results/<scenario>/models.json` is the historic record of models tested on that scenario. A successful test updates that one key and leaves the other keys in place. Historic results can outlive the active list.

A scenario is complete when every active model key has `results/<scenario>/<model-key>.md`. Extra markdown, including `evaluation-*.md`, is not counted. A failed test leaves the previous transcript and stats in place.

## Modes

Set per scenario in `scenarios/scenarios.json`. `FORCE_MODE` in `config.py` overrides them. A missing mode uses `update`.

| Mode | Behavior |
|------|----------|
| `none` | Skip the scenario |
| `update` | Run active models that do not already have a result file |
| `refresh` | Rerun every model on the active list and overwrite those files. Other result files stay |

## What a run writes

Per scenario:

- `<model-key>.md` — turn-by-turn chat and per-response stats
- `models.json` — historic model records, updated by key
- `stats.json` and `stats.md` — avg t/s, total time, and per-question times. The table is built from the records
- `test.md` — overview. An existing evaluation status section is kept
- `results.md` — created only when missing. `evaluate.py` later replaces it with the ranking
- `info.md` — helper-model prose, and only when the helper returns text

`meta/hardware.json` is written at the start of a real run. `DRY_RUN` prints the plan and writes nothing.

Root `results/stats.json` and `results/stats.md` are rebuilt from the scenario stats after a run that finishes at least one test. `overall_seconds` is that run's wall-clock time. Each model's `total_seconds` is the sum of its scenario records. The root table adds Used RAM, Peak RAM, and Scenarios.

## System prompt, inference, and questions

`system.md` and `inference.json` are resolved from the scenario folder, then parent group folders, then `scenarios/`. The nearest inference file replaces the ones above it.

`test.json` can set `"system_prompt": false` or an inline `"system"` string. The inline string wins. Otherwise a `system` string in the winning `inference.json` is used, then `system.md`.

`USE_CUSTOM_INFER` sends `temperature`, `top_p`, `top_k`, `repeat_penalty`, and `reasoning_effort` when they are set. When it is false, LM Studio defaults are used.

Question files are `question1.md`, `question2.md`, and so on. The loader stops at the first missing number.

Before the first load, and after each model finishes, the runner unloads models currently loaded in LM Studio. Chat timeout is `CHAT_TIMEOUT` (900 seconds).

RAM spill uses `psutil`. If system RAM rises by at least `RAM_SPILL_THRESHOLD_PERCENT` of `INSTALLED_RAM_GB` (25% of 32 GB), the model is marked `"used_ram": true`. That means the model spilled out of VRAM into system RAM.

The helper model is `lfm2.5-1.2b-instruct`. Its text goes to `scenarios/info.md` or `results/<scenario>/info.md`. `stats.md` and `scenarios.md` stay generated from the recorded data. A helper failure writes no placeholder.

## Evaluation and clean

`evaluate.py` uses `EVAL_BACKEND` and `EVAL_MODEL` from `config.py`. The default backend is `grok_api` and the default model is `grok-4.3`. The key for that backend comes from `.env`. Setup, resume, and the files it writes are in [evaluation.md](evaluation.md). Plugin code is in `plugins/`. The contract is in [plugin.md](plugin.md).

`clean.py` compares each scenario's historic model keys with the active list. If the active list is missing or empty, it stops. `archive` copies removed keys into `archive/YYYY MM DD/` and merges them into the archive records. `clean` then removes those keys from the live results. Stats for removed models stay in the archive. `results.md` and `evaluation-*` files stay. A markdown file whose key is not in that scenario's `models.json` is left alone.

## Workflow

1. Start the LM Studio server.
2. Run `python models.py`. Edit `scenarios/models.json` if you want a smaller active list.
3. Add a scenario folder with `test.json` and `question1.md`.
4. Run `python scenarios.py`.
5. Set modes in `scenarios/scenarios.json`.
6. Run `python run.py`.
7. Run `python evaluate.py` when you want a cloud ranking.

Hand-edit rules are in [get-started.md](get-started.md) under "Files you can edit by hand."
