# Usage

Detailed configuration, modes, and behavior for the LM Studio multi-scenario test project.

## Configuration

All shared settings live in `config.py`.

### Connection

```python
BASE_URL = "http://localhost:1234"
API_TOKEN = ""
HELPER_MODEL = "lfm2.5-1.2b-instruct"
```

- `BASE_URL` — LM Studio server address
- `API_TOKEN` — optional bearer token
- `HELPER_MODEL` — optional helper model used for short summaries. Its text is written to `info.md` only. `stats.md` and `scenarios.md` stay generated from the recorded numbers. The current setting is `lfm2.5-1.2b-instruct`.

### Paths

| Variable | Default | Purpose |
|----------|---------|---------|
| `SCENARIOS_DIR` | `scenarios` | Root folder for all tests |
| `RESULTS_DIR` | `results` | Root folder for all results |
| `ARCHIVE_DIR` | `archive` | Root folder for dated archives |
| `MODELS_PATH` | `scenarios/models.json` | Active list of models to test |
| `SCENARIOS_JSON` | `scenarios/scenarios.json` | Scenario list with status and mode |
| `ROOT_STATS_JSON` | `results/stats.json` | System-wide model stats |
| `INFERENCE_PATH` | `scenarios/inference.json` | Lowest-precedence inference settings |
| `SYSTEM_PROMPT_PATH` | `scenarios/system.md` | Lowest-precedence system prompt |

### Run settings

| Variable | Default | Purpose |
|----------|---------|---------|
| `DRY_RUN` | `False` | Print what would run without loading models |
| `FORCE_MODE` | `None` | Override every scenario’s mode |
| `USE_CUSTOM_INFER` | `True` | When `True`, send settings from inference.json |
| `CHAT_TIMEOUT` | `900` | Seconds to wait for a single response |
| `INSTALLED_RAM_GB` | `32` | Used to calculate the spill threshold |
| `INSTALLED_VRAM_GB` | `16` | Reference only |
| `RAM_SPILL_THRESHOLD_PERCENT` | `25` | If RAM rises by this percent of installed RAM during a model, set `used_ram: true` |

### Clean settings

These are the defaults used by `clean.py` when you run it with no arguments.

| Variable | Default | Purpose |
|-----------|--------|---------|
| `ARCHIVE` | `True` | Copy data for removed models into a dated archive |
| `CLEAN`   | `True` | Clean both results and stats |
| `RESULTS` | `True` | Remove conversation files for removed models |
| `STATS`   | `True` | Strip removed models from stats and model lists |

## Scenario folder

Each scenario is a folder under `scenarios/` (nested group folders are allowed). Minimum required files:

- `test.json` — name, description, optional `system_prompt` flag
- `question1.md` — first question (add `question2.md`, `question3.md`, … as needed)

Optional:

- `system.md` — system prompt for this scenario (highest precedence)
- `inference.json` — inference settings for this scenario (highest precedence)

## System prompt and inference precedence

The runner looks for `system.md` and `inference.json` in this order (highest first):

1. The scenario folder itself (`scenarios/function/test1/system.md`)
2. Each parent group folder (`scenarios/function/system.md`)
3. The scenarios root (`scenarios/system.md`)

`test.json` can still set `"system_prompt": false` or supply an inline `"system"` string. That inline string wins. Otherwise a `system` string inside the winning `inference.json` is used, and then `system.md`.

If `USE_CUSTOM_INFER` is `False`, LM Studio defaults are used and no inference file is read. The chat request forwards `temperature`, `top_p`, `top_k`, `repeat_penalty`, and `reasoning_effort` when they are set. The nearest inference file replaces the ones above it. The files are not merged field by field.

## Results folder

For every scenario the runner creates a matching folder under `results/`.

| File | Purpose |
|------|---------|
| `<model-key>.md` | Full conversation for that model key |
| `models.json` | Historic models tested on this scenario, one record per model key |
| `test.md` | Overview. The evaluation status section is kept when the runner rewrites the file |
| `stats.md` | Statistics table generated from `stats.json` |
| `stats.json` | Raw numbers, one record per model key |
| `results.md` | Cloud ranking written by `evaluate.py`. The runner creates it only when it is missing |
| `evaluation-<model>.json` | Evaluation conversation and the list of scored model keys |
| `evaluation-<model>.md` | Readable copy of that conversation |
| `info.md` | Helper-model prose for this scenario |

A scenario is complete when every key in `scenarios/models.json` has a `<model-key>.md` file here. Extra files, including `evaluation-*.md`, are not counted. Historic models that are no longer on the active list can remain in these files. `run.py` updates the key it just tested and does not remove the others. A failed test does not replace a previous good record.

Root stats in `results/stats.json` and `results/stats.md` are rebuilt from the scenario stats after a run that finishes at least one test. A run with nothing to do leaves them alone. `overall_seconds` is the wall-clock time of that run. Each model's `total_seconds` is the sum of its scenario records.

## Hardware and spill detection

At the start of a run the script records current RAM usage (via `psutil`). While each model is running it tracks peak RAM. If the increase exceeds `RAM_SPILL_THRESHOLD_PERCENT` of `INSTALLED_RAM_GB`, the model’s entry in the root stats is marked `"used_ram": true`.

This is a simple heuristic. It works best when you do not load other large processes during the test run. If `psutil` is not installed the check is skipped.

## Unloading models

Before any load the script lists currently loaded models via the LM Studio API and unloads them so the test model gets a clean VRAM state. Each model is also unloaded after its own scenarios finish.

## Adding a new scenario

1. Create a folder under `scenarios/` (spaces, dashes, or underscores are fine; nested groups are allowed).
2. Add `test.json` and at least `question1.md`.
3. Optionally add `system.md` or `inference.json` at any level.
4. Run `python scenarios.py`.
5. Set the mode in `scenarios/scenarios.json` and run `python run.py`.

## Cleaning and archiving

`clean.py` does not run `models.py`. It reads the active list you already have. If that file is missing or has no model keys, it stops and leaves the results alone.

- **archive** — copies conversation files and stat records for model keys that are in a scenario's historic `models.json` but not on the active list. A second run on the same day updates those keys in the archive instead of replacing the archive files.
- **results** — deletes the conversation `.md` files for those keys.
- **stats** — removes those keys from the live `models.json`, `stats.json`, `stats.md`, `test.md`, and the root stats. The tables are rebuilt from the records that remain. The evaluation status section in `test.md` is kept.

The removed models' stats stay in the archive. Live results then match the active list. `results.md` and `evaluation-*` files are left alone. Empty result folders are left in place. A clean run does not modify the archive.

## Files you can edit by hand

| File | What is safe | What the scripts do |
|------|----------------|---------------------|
| `scenarios/models.json` | Add or remove models you want tested | `models.py` replaces the whole file from LM Studio. `run.py` and `clean.py` only read it |
| `scenarios/scenarios.json` | Change `mode` | A scan refreshes name, status, and `last_run`, and keeps `mode` |
| `results/<scenario>/<model-key>.md` | Delete a transcript to make update mode run that model again | Refresh overwrites that key's file. Other keys are not deleted |
| `results/<scenario>/models.json` | Remove a historic model record | A successful test updates that key. A missing record is added back when the transcript exists and the model is on the active list |
| `results/<scenario>/stats.json` | Edit a model's numbers | The next successful test of that key replaces its record. Other keys stay |
| `results/stats.json` | Short-lived notes only | The next run that finishes a test rebuilds this file from the scenario stats |
| `test.md` evaluation section | Edit the status text | `run.py` keeps the section. `evaluate.py` replaces it |
| `results.md` | Edit until the next evaluation | `evaluate.py` replaces it with the new ranking |
| `info.md` | Optional notes | Replaced when the helper model returns a summary |

Question files must be numbered without gaps (`question1.md`, `question2.md`, …). The loader stops at the first missing number.
