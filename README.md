# LM Studio Multi-Scenario Test Project

A set of Python scripts for running the same set of local models against multiple independent test scenarios in LM Studio. Each scenario lives in its own folder, uses its own questions, and produces consistent markdown results plus statistics.

The project is designed to be simple, file based, and friendly. You can add a new scenario by creating a folder, run only the models that are missing results, or refresh everything. Results are written as markdown so they are easy to read and easy to hand to a cloud model for evaluation.

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
USAGE.md

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
