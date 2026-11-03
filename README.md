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

- Python 3.9+
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
7. Set the desired mode for each scenario in `scenarios/scenarios.json` (default is `update`).
8. Run `python run.py`.

Results appear under `results/<scenario-path>/`.

## Project layout

```
config.py
utils.py
models.py
scenarios.py
run.py
clean.py
hardware.json

scenarios/
  models.json
  scenarios.json
  scenarios.md
  system.md              ← lowest precedence
  inference.json         ← lowest precedence
  function/
    inference.json       ← group level
    test1/
      test.json
      question1.md
      system.md          ← highest precedence
      inference.json     ← highest precedence

results/
  stats.json             ← root-level system stats
  stats.md
  function/
    test1/
      <model-key>.md
      models.json
      stats.json
      stats.md
      test.md
      results.md

archive/
  2026 11 04/            ← dated archive of removed models
    results/
      ...
```

## Modes

Modes are set per scenario in `scenarios/scenarios.json` (or overridden with `FORCE_MODE` in `config.py`).

| Mode      | Behavior |
|-----------|----------|
| `none`    | Skip the scenario |
| `update`  | Run only models that do not already have a result file |
| `refresh` | Rerun every model currently listed in models.json (overwrites those files; leaves results for removed models alone) |

## Cleaning and archiving

After you remove models from LM Studio you can clean the results so they only contain the models that are still installed.

```bash
python clean.py                 # archive then clean (uses config.py defaults)
python clean.py archive         # copy removed-model data only
python clean.py clean           # remove result files and update stats
python clean.py results         # remove conversation files only
python clean.py stats           # update stats and model lists only
```

Archive always runs first when enabled and never modifies the live results. Clean never touches the archive folder. The archive is written to `archive/YYYY MM DD/` and contains only the models that were removed.

See [get-started.md](get-started.md) for full details on configuration, inference settings, system prompts, and hardware detection.
