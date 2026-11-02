# CHANGELOG

## 2026-11-02 

### run_tests.py 0.9.1

Added graceful Ctrl-C handling.

- KeyboardInterrupt is caught at the top level of the run.
- On interrupt the script prints a short message, calls `unload_models` to clear any loaded models, and exits cleanly (status 130) without a traceback.

### run_tests.py 0.9.0

Changed the main loop from scenario-first to model-first.

- A model is loaded once and then run through every scenario that still needs it (respecting mode, ready status, and existing result files).
- The model is unloaded and reloaded only when the requested context length changes. Other inference settings are sent on the chat request and do not cause a reload.
- Scenarios for a model are sorted by context length descending so larger contexts are handled first.
- Added `unload_models()` helper. It is called immediately before every load (first load or context-change reload) so any stray models (for example from the Continue plugin) are cleared.
- Spill / peak RAM is now tracked per model across all scenarios it runs and written to a new root-level `stats.json` / `stats.md`. The Used RAM column was removed from per-scenario stats.
- Helper model summaries are generated at the very end of the run, after all test models have been unloaded, so they do not interrupt a loaded test model.
- Per-scenario result files, stats merges, models snapshots, and test.md are still written as soon as a model finishes a scenario.

All existing mode, system-prompt, and inference behaviors are unchanged.
