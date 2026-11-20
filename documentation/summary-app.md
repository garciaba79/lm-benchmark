# LM Benchmark

Short description of the project. The full briefing, meant to be pasted to a cloud model, is [lm-benchmark.md](lm-benchmark.md).

Python 3.14 scripts run the same local LM Studio models through the same scenario folders, save the chats and speed numbers, and can ask a cloud model to rank them.

Each scenario is a folder under `scenarios/` with `test.json` and `question1.md`, `question2.md`, and so on. Optional `system.md` and `inference.json` can sit in the scenario, in a parent group, or in `scenarios/`. Results land in the matching folder under `results/`.

## Scripts

- `models.py` replaces the active list in `scenarios/models.json` with the models currently in LM Studio.
- `scenarios.py` rebuilds `scenarios/scenarios.json` and `scenarios/scenarios.md`, and keeps each scenario's mode. New scenarios start as `update`.
- `run.py` loads one model at a time, asks the questions in order, and writes `<model-key>.md`, `<model-key>.json`, historic `models.json`, `stats.json`, `stats.md`, and `test.md`.
- `evaluate.py` ranks a scenario with the backend in `config.py`. The default is the Grok API (`grok_api`, model `grok-4.3`).
- `clean.py` is the only script that removes live results. It first copies the removed models' transcripts and records into `archive/YYYY MM DD/`, then deletes those keys from the live files.

`scenarios/models.json` is who you want to test now. `results/<scenario>/models.json` is who has already been tested on that scenario. A normal run updates one key and leaves the others. JSON files are lists of records, updated by key.

`update` fills in missing result files. `refresh` reruns every active model and overwrites those files. `none` skips the scenario. Keep the default at `update`.

A scenario is complete when every active model key has a `<model-key>.md` file. Evaluation notes and other extra markdown do not count.
