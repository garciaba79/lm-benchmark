# LM Studio Multi-Scenario Test Project

Scripts that let you run the same set of models against many independent test scenarios.

## Quick start

1. Make sure the LM Studio server is running.
2. Edit `config.json` set the `model` field for helper summaries if you want a summary.
3. Run `python get_models.py` then update `models.json` to set only the models you want to use.
4. Create a scenario folder under `scenarios/` with `test.json` and `question1.md`.
5. Run `python get_scenarios.py`.
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
- Configurable values and helper prompts sit at the top of each script.
- Models are sorted from smallest to largest.

## Layout

```
config.json
get_models.py
get_scenarios.py
run_tests.py
models.json
scenarios.json
scenarios.md
system.md
README.md

scenarios/
  weather app/
    test.json
    question1.md
    ...
    system.md              ← optional

results/
  weather app/
    models.json            ← snapshot
    <model-key>.md
    test.md
    stats.md
    stats.json
    results.md             ← paste cloud evaluation here
```



## Files written per scenario

- `test.md` — short overview
- `stats.md` — test statistics
- `stats.json` — raw numbers for later reports
- `results.md` — empty file for the cloud evaluation
- `models.json` — snapshot of the models used
