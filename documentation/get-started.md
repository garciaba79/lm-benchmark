# Usage

Detailed configuration, modes, and behavior for the LM Studio multi-scenario test project.

## Configuration files

### config.json

Connection settings for the LM Studio server.

```json
{
  "base_url": "http://localhost:1234",
  "api_token": "",
  "model": "lfm2.5-1.2b-instruct"
}
```

- `base_url` — LM Studio server address
- `api_token` — optional bearer token
- `model` — optional helper model used for short summaries (skipped if missing or unreachable)

### models.json

Created by `get_models.py`. Contains the list of models that will be tested. Edit this file to limit which models are included. The order in this file is preserved.

### scenarios.json

Created by `get_scenarios.py`. Each entry describes one scenario folder and includes:

- `scenario` — folder name
- `ready` — whether the folder contains the required files
- `status` — `none`, `partial`, or `complete`
- `mode` — `none`, `update`, or `refresh`
- `last_run` — timestamp of the newest result file (if any)

### inference.json

Optional. Used only when `USE_CUSTOM_INFER = True` in `run_tests.py`.

Contains inference settings that are passed to LM Studio (keys match the API):

```json
{
  "context_length": 16384,
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "repeat_penalty": 1.1,
  "reasoning_effort": "none"
}
```

If a scenario folder contains its own `inference.json`, that file is used instead of the root one for that scenario. If neither file exists, LM Studio defaults are used.

### hardware.json

Written automatically at the start of each run. Records installed RAM/VRAM and the base RAM reading used for spill detection. You can edit the installed values at the top of `run_tests.py` if your machine differs.

### system.md

Root system prompt. Used when a scenario does not provide its own `system.md` and when `test.json` does not set the system prompt.

## Scenario folder

Each scenario is a folder under `scenarios/`. Minimum required files:

- `test.json` — name, description, optional `system_prompt` flag
- `question1.md` — first question (add `question2.md`, `question3.md`, … as needed)

Optional:

- `system.md` — overrides the root system prompt for this scenario
- `inference.json` — overrides the root inference settings for this scenario (only when custom inference is enabled)

## Results folder

For every scenario the runner creates a matching folder under `results/`.

| File | Purpose |
|------|---------|
| `<model-key>.md` | Full conversation for that model |
| `models.json` | Snapshot of models used (merged by key across runs) |
| `test.md` | Short overview of the current run |
| `stats.md` | Readable statistics table (includes “Used RAM” column) |
| `stats.json` | Raw numbers for later reporting (merged by model key) |
| `results.md` | Empty file where you paste a cloud-model evaluation |

## Script configuration (top of run_tests.py)

| Variable | Default | Purpose |
|----------|---------|---------|
| `DRY_RUN` | `False` | Print what would run without loading models |
| `FORCE_MODE` | `None` | Override every scenario’s mode (`update`, `refresh`, or `none`) |
| `USE_CUSTOM_INFER` | `False` | When `True`, send settings from `inference.json` |
| `CHAT_TIMEOUT` | `900` | Seconds to wait for a single response |
| `INSTALLED_RAM_GB` | `32` | Used to calculate the spill threshold |
| `INSTALLED_VRAM_GB` | `16` | Reference only |
| `RAM_SPILL_THRESHOLD_PERCENT` | `25` | If RAM rises by this percent of installed RAM during a model, set `used_ram: true` |

## System prompt behavior

1. If `test.json` contains `"system_prompt": false`, no system message is sent.
2. If the system prompt `system` is set in `test.json`, it will be used. 
3. Otherwise the runner looks for `scenarios/<name>/system.md`.
4. If that file does not exist, it falls back to the root `system.md`.
5. If neither exists, no system message is sent.

## Hardware and spill detection

At the start of a run the script records current RAM usage (via `psutil`). While each model is running it tracks peak RAM. If the increase exceeds `RAM_SPILL_THRESHOLD_PERCENT` of `INSTALLED_RAM_GB`, the model’s entry in `stats.json` is marked `"used_ram": true`.

This is a simple heuristic. It works best when you do not load other large processes during the test run. If `psutil` is not installed the check is skipped.

## Unloading models

Before any tests start, the script lists currently loaded models via the LM Studio API and unloads them so the first test model gets a clean VRAM state. Each model is also unloaded after its own test finishes.

## Adding a new scenario

1. Create a folder under `scenarios/` (spaces, dashes, or underscores are fine).
2. Add `test.json` and at least `question1.md`.
3. Optionally add `system.md` or `inference.json`.
4. Run `python get_scenarios.py`.
5. Set the mode in `scenarios.json` and run `python run_tests.py`.
