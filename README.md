# LM Studio Multi-Scenario Test Project

Scripts that let you run the same set of models against many independent test scenarios.

## Quick start

1. Make sure the LM Studio server is running.
2. Edit `config.json` if needed.
3. Run `python get_models.py` and edit `models.json` to set only the models you want to use.
4. Create a scenario folder under `scenarios/` with at least `test.json` and `question1.md`.
5. Run `python get_scenarios.py` to build `scenarios.json`.
6. Edit modes in `scenarios.json` (default is `none`).
7. Run `python run_tests.py`.

## Modes (set in scenarios.json)

- `none` — skip the scenario
- `update` — run only models that do not already have a result file
- `refresh` — run every model currently in `models.json` (overwrites those files; leaves old removed model results alone)

## System prompt

- If `test.json` has `"system_prompt": false`, no system message is used.
- Otherwise the runner uses `scenarios/<name>/system.md` if it exists, else the root `system.md`.

## Notes

- Result files use a stable name based on the model key so update mode can find them.
- A copy of `models.json` is saved inside each results folder as a snapshot.
- Configurable values sit at the top of each script.
- Models are sorted from smallest to largest.

## Layout

```
config.json
get_models.py
get_scenarios.py
run_tests.py
models.json
scenarios.json
system.md                  ← optional root system prompt
README.md

scenarios/
  weather app/
    test.json
    question1.md
    question2.md
    system.md              ← optional (overrides root)
  code 1/
    ...

results/
  weather app/
    models.json            ← snapshot used for this run
    <model-key>.md
    test_summary.md
    results.md
  code 1/
    ...
```