## LM Benchmark

### LM Studio Multi Scenario Local Model Testing Project

This is a file-based Python project for systematically testing multiple local LLMs in LM Studio against the same set of scenarios. The goal is to remove manual repetition: load models, run identical ordered conversations, capture detailed stats, and produce consistent markdown outputs that can later be evaluated by a cloud model.
### Core idea  
Each test scenario lives in its own folder under `scenarios/`. A scenario contains its own questions as markdown files (`question1.md`, `question2.md`, …), an optional `system.md`, an optional `inference.json`, and a `test.json` with name/description. Results are written to a matching folder under `results/`. The same models are run against every scenario so inputs stay identical.
### Main scripts
- `get_models.py` — queries LM Studio and writes `models.json` (user sorts models by capability; the runner does not re-sort).
- `get_scenarios.py` — scans `scenarios/` and writes `scenarios.json` plus a short `scenarios.md` report.
- `run_tests.py` — the main runner. Reads scenarios, loads models one at a time, asks the questions in order, captures per-response stats, and writes results.
### Key files
- `config.json` — LM Studio base URL, optional API token, optional helper model for short summaries.
- `models.json` — master list of models to test.
- `scenarios.json` — list of scenarios with `ready`, `status` (none/partial/complete), and `mode`.
- `inference.json` — optional inference settings (context_length, temperature, top_p, top_k, repeat_penalty). Used only when `USE_CUSTOM_INFER = True`. A scenario can override with its own copy.
- `hardware.json` — written at the start of each run; records installed RAM/VRAM and base RAM reading.
- `system.md` — root system prompt (fallback).
### Modes

The mode can be set in run_tets.py config or per scenario in the scenarios.json file.  
The default mode for each scenario is `update`.  
You can override this per scenario with `FORCE_MODE`.  

- `none` — skip
- `update` — run only models that do not already have a result file
- `refresh` — rerun every model currently in models.json (overwrites those files; leaves results for removed models)
### What is written per scenario in the results folder for the scenario
- `<model-key>.md` — full turn-by-turn conversation with stats lines
- `models.json` — snapshot of models used (merged by key across runs)
- `test.md` — short overview of the run
- `stats.md` — aligned table of avg t/s, total time, per-question times, and “Used RAM”
- `stats.json` — raw numbers (also merged by model key)
- `results.md` — empty file where the user pastes a cloud-model evaluation
### Notable behaviors
- Before tests start, the runner unloads all currently loaded models so the first test model gets clean VRAM.
- System prompt: if `test.json` sets `"system_prompt": false` it is skipped; otherwise scenario `system.md` is used, falling back to root `system.md`.
- Inference: when `USE_CUSTOM_INFER` is false, LM Studio defaults are used. When true, scenario `inference.json` overrides root `inference.json`.
- RAM spill detection: records base RAM at start (via psutil). During each model it tracks peak RAM. If RAM rises by ≥25% of installed RAM (user has 32 GB RAM / 16 GB VRAM), the model is marked `"used_ram": true` in stats. This is a simple heuristic.
- Result files use stable names based on the model key so update mode can detect missing results.
- Chat timeout is configurable (default 900 s) because large models (e.g. 32B) can be slow.
- Individual result markdown files for models later removed from models.json are left alone.
- `models.json` and `stats.json` inside results folders are merged by model key (update if present, keep old entries).
### Workflow
1. Start LM Studio server.
2. Run `get_models.py`, edit `models.json`.
3. Create scenario folders with questions and `test.json`.
4. Run `get_scenarios.py`.
5. Set modes in `scenarios.json`.
6. Run `run_tests.py`.
7. Optionally paste cloud evaluation into each `results.md`.

The project is intentionally simple and git-friendly. No database. Everything needed for a scenario lives in its folder; everything produced by a run lives in the matching results folder.