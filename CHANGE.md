# CHANGELOG

## 2026-11-19

### Keyed records and non-destructive runs

Run and evaluate now update records by model key. A normal run keeps historic results for models that are no longer on the active list.

- `scenarios/models.json` stays the active list. Only `models.py` replaces it, and it says so when it does. `clean.py` no longer calls `models.py`.
- `results/<scenario>/models.json` is the historic record. A successful test upserts that model key. A failure leaves the previous record in place.
- Scenario status is complete only when every active model key has its result file. Extra markdown files are not counted.
- `scenarios.py` keeps the mode already stored for a scenario.
- Root `results/stats.json` is rebuilt from scenario stats after a run that finished at least one test. A run with nothing to do leaves it alone.
- Helper-model text goes to `info.md`. `stats.md` and `scenarios.md` are generated from the recorded data.
- Helper model is `lfm2.5-1.2b-instruct`.
- Dry runs do not write hardware, results, or evaluation status.
- `evaluate.py` selects one backend, one key, and `EVAL_MODEL`. `grok_api` is the default. `evaluated_keys` in `evaluation-<model>.json` is the resume list.
- `EVAL_TIMEOUT` applies to the Grok API, OpenAI, Gemini, Anthropic, and the Grok CLI.
- The project requires Python 3.14.
- `documentation/lm-benchmark.md`, `documentation/summary-app.md`, and `documentation/plugin.md` match the current scripts and folders. `documentation/summary-context.md` stays the earlier session note.
- The three hand transcripts named `grok.md` are now `evaluation-grok-4.3.md`.

## 2026-11-18

### Evaluation improvements

Made evaluation more reliable and easier to resume or extend.

- Conversation is now saved as `evaluation-<model>.json` after every successful turn (source of truth).
- On restart the script loads that file, detects which models are already scored, and continues with only the missing ones.
- If a final-ranking turn already exists and new models are found, that turn and everything after it are removed before continuing.
- Human-readable `evaluation-<model>.md` is always regenerated from the JSON at the end of a scenario.
- Added `evaluation.json` index that lists which cloud models have been used for the scenario.
- Added `EVAL_TIMEOUT` (default 600 seconds) for API calls.
- API usage stats (requests and tokens) are printed at the end of a run.
- Added `DEBUG` flag in `evaluate.py` and the Grok CLI plugin for extra logging.
- Updated documentation for Grok CLI install/auth/switching and the evaluation workflow.

## 2026-11-17

### Evaluation support

Added a way to rank model results with a cloud model.

- New `evaluate.py` walks `results/` and sends model result files in batches to a configured backend.
- Supports partial updates: if some models are already evaluated, only the missing ones are sent and the existing conversation is continued.
- Writes the final ranking to `results.md` and the full turn-by-turn conversation to `grok.md`.
- Updates the evaluation status section at the bottom of `test.md` (models evaluated / missing).
- Plugin system under `plugins/` with three backends:
  - `grok_cli` (default, uses SuperGrok subscription, no API fees)
  - `openai` (OpenAI-compatible: OpenAI, Grok API, Gemini)
  - `anthropic`
- Backend is selected by `EVAL_BACKEND` in `config.py`. No automatic fallback.
- Private keys go in `.env`. Public settings stay in `config.py`.
- Command-line options: `--scenario`, `--force`, `--dry-run`, `--batch-size`.
- Shared helpers in `utils.py` so `run.py` and `evaluate.py` can both update `test.md` without overwriting each other.

## 2026-11-02

### Project restructure and clean.py

Reorganized the project so the root stays clean and related files live together.

- Renamed scripts for shorter, single-word names:
  - `get_models.py` → `models.py`
  - `get_scenarios.py` → `scenarios.py`
  - `run_tests.py` → `run.py`
  - new `clean.py`
- Moved shared paths, connection settings, and defaults into `config.py`.
- Moved pure helpers into `utils.py`.
- Moved `models.json`, `scenarios.json`, and `scenarios.md` into the `scenarios/` folder.
- Moved root-level `stats.json` and `stats.md` into the `results/` folder.
- Moved `system.md` and `inference.json` into the `scenarios/` folder.
- Added three-level precedence for system prompts and inference settings:
  1. scenario folder (highest)
  2. group folder
  3. scenarios root (lowest)
- Added `clean.py` to archive and remove results for models that are no longer installed.
  - `archive` copies removed-model data into `archive/YYYY MM DD/` (never modifies live results).
  - `clean` / `clean_results` / `clean_stats` update the live results and stats only.
  - Command-line options override the defaults in `config.py`.
  - Always refreshes the model list first and scenario status at the end when cleaning.
- Updated README and get-started to match the new layout and commands.

---

### run.py 0.10.0 (formerly run_tests.py 0.9.0)

Changed the main loop from scenario-first to model-first.

- A model is loaded once and then run through every scenario that still needs it (respecting mode, ready status, and existing result files).
- The model is unloaded and reloaded only when the requested context length changes. Other inference settings are sent on the chat request and do not cause a reload.
- Scenarios for a model are sorted by context length descending so larger contexts are handled first.
- Added `unload_models()` helper. It is called immediately before every load (first load or context-change reload) so any stray models (for example from the Continue plugin) are cleared.
- Spill / peak RAM is now tracked per model across all scenarios it runs and written to `results/stats.json` / `results/stats.md`. The Used RAM column was removed from per-scenario stats.
- Helper model summaries are generated at the very end of the run, after all test models have been unloaded, so they do not interrupt a loaded test model.
- Per-scenario result files, stats merges, models snapshots, and test.md are still written as soon as a model finishes a scenario.

All existing mode, system-prompt, and inference behaviors are unchanged (now with the new precedence rules).

---

Added graceful Ctrl-C handling.

- KeyboardInterrupt is caught at the top level of the run.
- On interrupt the script prints a short message, calls `unload_models` to clear any loaded models, and exits cleanly (status 130) without a traceback.

---

After a successful run, automatically calls `scenarios.py` (if present) so `scenarios.json` and `scenarios.md` reflect the latest status without a manual step.