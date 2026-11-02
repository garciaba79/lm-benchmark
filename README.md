# LM Studio Model Test Harness

A small set of Python scripts that run the same local models through the same conversations in LM Studio so you can compare them fairly.  

You put each test in its own folder. The scripts load the models one by one, ask the questions in order, and save the full chat plus speed and memory numbers. Results come out as plain markdown files. You can add a new test by making a folder, run only the models that are missing results, or re-run everything. Later you can hand the files to a cloud model for scoring.

## Features

- Run many models against many scenarios with identical inputs
- Update mode (run tests for missing results) or refresh mode (run tests for all current models)
- Optional custom inference settings per scenario
- System prompt fallback, per scenario prompt or default prompt
- Statistics for the models including tokens per second, time, and if spilled into RAM
- Snapshot of the models used for each scenario
- Get a summary for the models for each scenario and uisng a helper model (optional)

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
2. Edit `config.json` and set the optional `model` field if you want helper summaries.
3. Run `python get_models.py` and edit `models.json` to keep only the models you want to test.
4. Create a scenario folder under `scenarios/` containing at least `test.json` and `question1.md`. (see the example)
5. Run `python get_scenarios.py`.
6. Set the desired mode for each scenario in `scenarios.json` (default is `update`).
7. Run `python run_tests.py`.

Results appear under `results/<scenario-name>/`.

## Project layout

```
config.json
hardware.json
inference.json
get_models.py
get_scenarios.py
run_tests.py
models.json
scenarios.json
scenarios.md
system.md
README.md

documentation/
  get-started.md
  instructions.md
  lm-benchmark.md
  summary-app.md
  summary-context.md
  workflow.md

scenarios/
  weather app/
    test.json
    question1.md
    question2.md
    system.md          ← optional
    inference.json     ← optional override

results/
  weather app/
    models.json        ← snapshot of models used
    <model-key>.md     ← full conversation
    test.md
    stats.md
    stats.json
    results.md         ← paste cloud evaluation here
```

## Modes

Modes are set per scenario in `scenarios.json` (or overridden with `FORCE_MODE` in the script).

| Mode      | Behavior |
|-----------|----------|
| `none`    | Skip the scenario |
| `update`  | Run only models that do not already have a result file |
| `refresh` | Rerun every model currently listed in `models.json` (overwrites those files; leaves results for removed models alone) |

See [USAGE.md](USAGE.md) for full details on configuration, inference settings, system prompts, and hardware detection.

## License

MIT
