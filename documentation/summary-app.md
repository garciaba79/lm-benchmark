# LM Benchmark

Short description of the project. The full briefing, meant to be pasted to a cloud model, is [lm-benchmark.md](lm-benchmark.md).

LM Benchmark tests local models by asking them a series of questions across topics and categories. It saves each model's answers and speed numbers, then can ask a cloud model to evaluate, rank, and score them. Python 3.14.

Each set of questions is a folder under `scenarios/` with `test.json` and `question1.md`, `question2.md`, and so on. Optional `system.md` and `inference.json` can sit in that folder, in a parent group, or in `scenarios/`. The saved answers land in the matching folder under `results/`.

## Scripts

- `models.py` replaces the active list in `scenarios/models.json` with the models currently in LM Studio.
- `scenarios.py` rebuilds `scenarios/scenarios.json` and `scenarios/scenarios.md`, and keeps each scenario's mode. New scenarios start as `update`.
- `run.py` loads one model at a time, asks the questions in order, and writes `<model>.md`, `<model>.json`, historic `models.json`, `stats.json`, `stats.md`, and `test.md`.
- `evaluate.py` ranks a scenario with the backend in `config.py`. The default is the Grok API (`grok_api`, model `grok-4.3`).
- `clean.py` is the only script that removes live results. It first copies the removed models' transcripts and records into `archive/YYYY MM DD/`, then deletes those keys from the live files.

`scenarios/models.json` is who you want to test now. `results/<scenario>/models.json` is who has already been tested on that scenario. A normal run updates one key and leaves the others. JSON files are lists of records, updated by key.

`update` fills in missing result files. `refresh` reruns every active model and overwrites those files. `none` skips the scenario. Keep the default at `update`.

A scenario is complete when every model on the active list has a `<model>.md` file. `evaluation-<model>.md` and other extra markdown do not count.
