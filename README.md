# LM Studio Model Test Harness

A small set of Python scripts that run the same local models through the same conversations in LM Studio so you can compare them fairly.

You put each test in its own folder under `scenarios/`. The scripts load the models one by one, ask the questions in order, and save the full chat plus speed and memory numbers. Results come out as plain markdown files under `results/`. You can add a new test by making a folder, run only the models that are missing results, or re-run everything. Later you can hand the files to a cloud model for scoring.

## Features

- Run many models against many scenarios with identical inputs
- Update mode (run tests for missing results) or refresh mode (run tests for all current models)
- Optional custom inference settings per scenario, group, or scenarios root
- System prompt fallback with the same three-level precedence
- Statistics for the models including tokens per second, time, and if spilled into RAM
- Snapshot of the models used for each scenario
- Optional helper model summaries
- Clean and archive results for models you have removed from LM Studio

## Requirements

- Python 3.14
- LM Studio with the local server running
- `requests`
- `psutil` (used for RAM readings and detect if the model spilled into RAM)

```bash
pip install requests psutil
```

## Quick start

1. Start the LM Studio server.
2. Edit `config.py` if you need a different base URL, token, or helper model.
3. Run `python models.py` and edit `scenarios/models.json` to keep only the models you want to test.
4. Create a scenario folder under `scenarios/` containing at least `test.json` and `question1.md`.
5. Optionally add `system.md` or `inference.json` at the scenario, group, or scenarios root level.
6. Run `python scenarios.py`.
7. Set the desired mode for each scenario in `scenarios/scenarios.json` (default for a new scenario is `update`). Later scans keep the mode you set.
8. Run `python run.py`.
9. Rank the finished scenarios with `python evaluate.py`. The default backend is the Grok API.

Results appear under `results/<scenario-path>/`.

`scenarios/models.json` is the active list: the models to test now. `models.py` replaces that file with whatever LM Studio currently has installed. Hand edits there are kept until the next `models.py` run. `run.py` reads the active list and does not rewrite it.

`results/<scenario>/models.json` is the historic record for that scenario. A successful test updates the matching model key and leaves the other models in the file. Result folders can hold models that are no longer on the active list. `clean.py` is the command that archives those models and removes them from the live results.

## Project layout

```
config.py
utils.py
models.py
scenarios.py
run.py
clean.py
evaluate.py
plugins/
meta/hardware.json

documentation/
scenarios/
  models.json                     ← active list
  scenarios.json
  scenarios.md
  info.md                         ← helper-model prose, when the helper runs
  system.md                       ← lowest precedence
  inference.json                  ← lowest precedence
  function/
    inference.json                ← group level
    test1/
      test.json
      question1.md
      system.md                   ← highest precedence
      inference.json              ← highest precedence

results/
  stats.json                      ← root stats, rebuilt from scenario stats
  stats.md
  function/
    test1/
      <model-key>.md
      models.json                 ← historic models for this scenario
      stats.json
      stats.md
      test.md
      results.json                ← cloud scores from evaluate.py
      results.md                  ← readable table written from results.json
      evaluation-<model>.json
      info.md                     ← helper-model prose, when the helper runs

archive/
  2026 11 04/                     ← dated archive of models removed from the active list
    results/
      ...
```

## Modes

Modes are set per scenario in `scenarios/scenarios.json` (or overridden with `FORCE_MODE` in `config.py`).

| Mode      | Behavior |
|-----------|----------|
| `none`    | Skip the scenario |
| `update`  | Run only models that do not already have a result file |
| `refresh` | Rerun every model on the active list (overwrites those result files; leaves every other result alone) |

## Cleaning and archiving

After you remove models from LM Studio you can clean the results so they only contain the models that are still installed. 

`clean.py` compares each scenario's historic `models.json` with the active list. It does not run `models.py`. If the active list is missing or has no model keys, it stops and leaves the results alone.

```bash
python clean.py                 # archive then clean (uses config.py defaults)
python clean.py archive         # copy removed-model data only
python clean.py clean           # archive, then remove result files and update stats
python clean.py results         # archive, then remove conversation files
python clean.py stats           # archive, then update stats and model lists
```

Archive copies each removed model key into `archive/YYYY MM DD/` and merges it into the archive records. A command that removes live records archives first. `info.md`, `results.md`, `results.json`, and `evaluation-*` files are copied into the archive and also left in the live folder.

See [documentation/get-started.md](documentation/get-started.md) for configuration, inference settings, system prompts, hand edits, and hardware detection. Cloud ranking is described in [documentation/evaluation.md](documentation/evaluation.md). Coding agents that work in this repository follow [AGENTS.md](AGENTS.md).
