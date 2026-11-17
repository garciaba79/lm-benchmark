# CHANGELOG

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