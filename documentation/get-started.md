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
- `HELPER_MODEL` — optional helper model used for short summaries (skipped if missing or unreachable)

### Paths

| Variable | Default | Purpose |
|----------|---------|---------|
| `SCENARIOS_DIR` | `scenarios` | Root folder for all tests |
| `RESULTS_DIR` | `results` | Root folder for all results |
| `ARCHIVE_DIR` | `archive` | Root folder for dated archives |
| `MODELS_PATH` | `scenarios/models.json` | List of models to test |
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

`test.json` can still set `"system_prompt": false` or supply an inline `"system"` string, which takes priority over any file.

If `USE_CUSTOM_INFER` is `False`, LM Studio defaults are used and no inference file is read.

## Results folder

For every scenario the runner creates a matching folder under `results/`.

| File | Purpose |
|------|---------|
| `<model-key>.md` | Full conversation for that model |
| `models.json` | Snapshot of models used (merged by key across runs) |
| `test.md` | Short overview of the current run |
| `stats.md` | Readable statistics table |
| `stats.json` | Raw numbers for later reporting (merged by model key) |
| `results.md` | Empty file where you paste a cloud-model evaluation |

Root-level system stats are written to `results/stats.json` and `results/stats.md`.

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

`clean.py` refreshes the model list, then:

- **archive** — copies conversation files and keyed stats for models that are no longer in `scenarios/models.json` into `archive/YYYY MM DD/`. If you run it again the same day it updates the keyed entries instead of replacing whole files.
- **results** — deletes the conversation `.md` files for those models.
- **stats** — removes those models from every `models.json`, `stats.json`, `stats.md`, and `test.md` (scenario and root).

`results.md` (the evaluation paste) is left alone. Empty result folders are left in place. The archive folder is never modified by a clean run.
