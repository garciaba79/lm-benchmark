# AGENTS.md

Instructions for a coding agent in this repository. Run commands from the repo root. Paths in `config.py` are relative to the current directory.

The scripts are the source of truth. When a doc and a script disagree, follow the script and update the doc.

`documentation/lm-benchmark.md` is a briefing for a model outside the repo. This file is how to change the code.

## Project

Python 3.14 scripts run the same local LM Studio models through the same scenario folders, save the chats and speed numbers, and can send those results to one cloud model for scores. No package, database, test suite, or linter.

`config.py` exits on import if the interpreter is older than 3.14. Dependencies are `requests` and `psutil`.

## Docs

| Change | Read |
| --- | --- |
| Setup, modes, folders, clean, hand edits | `README.md`, `documentation/get-started.md` |
| Scoring, resume, judge files | `documentation/evaluation.md` |
| A backend in `plugins/` | `documentation/plugin.md` |
| The text the judge receives | `documentation/instructions.md` |
| Briefing for a model outside the repo | `documentation/lm-benchmark.md` |
| Short form of that briefing | `documentation/summary-app.md` |
| Running a test by hand in LM Studio | `documentation/workflow.md` |

`todo.md` is personal. `CHANGE.md` is the changelog. `documentation/example/` is a sample scenario, separate from `scenarios/`.

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` when a cloud evaluation needs a key. Public settings stay in `config.py`. Each backend reads only its own variable (`GROK_API_KEY` for `grok_api`). LM Studio is expected at `http://localhost:1234`.

## Commands

| Command | What it does |
| --- | --- |
| `python models.py` | Replaces `scenarios/models.json` with the LLMs currently in LM Studio (`type` `llm` only). Discards hand edits. No flags. |
| `python scenarios.py` | Rewrites `scenarios/scenarios.json` and `scenarios/scenarios.md`. Keeps each scenario's `mode`. May rewrite `scenarios/info.md` when `HELPER_MODEL` is set. No flags. |
| `python run.py` | Unloads every model currently loaded in LM Studio, runs the tests, and writes result files. No flags. Controlled by `DRY_RUN`, `FORCE_MODE`, and `BASE_URL` in `config.py`. Calls `scenarios.py` when finished. |
| `python evaluate.py` | Sends transcripts to the cloud backend and rewrites the score files. Flags: `--scenario`, `--force`, `--dry-run`, `--batch-size`. |
| `python clean.py` | Archives historic models absent from the active list, then can delete those live records. Words: `archive`, `clean`, `results`, `stats`. No words uses the defaults in `config.py` (archive then clean). |
| `python -m py_compile <file>` | Syntax check only. |

`--scenario` is one token, a path relative to `results/`. Quote names with spaces:

```bash
python evaluate.py --dry-run --scenario "code/fim 1"
```

`evaluate.py --dry-run` prints the plan and writes nothing. A `run.py` pass that skips loads and writes needs `DRY_RUN = True` in `config.py`. Put that flag back after the check.

Run `models.py`, `scenarios.py`, `run.py`, `evaluate.py`, or `clean.py` only when the user asked for that run. They replace the active model list, call LM Studio, spend API credits, or archive and delete result files.

## Layout

Edit these:

- `config.py`, `utils.py`, and the entry points `models.py`, `scenarios.py`, `run.py`, `clean.py`, `evaluate.py`
- `plugins/`
- `documentation/`, `README.md`, `CHANGE.md`, `.env.example`
- Scenario sources under `scenarios/`: `test.json`, `question*.md`, `system.md`, `inference.json`

The scripts rewrite these. Change the writer, or edit the one field the writer preserves:

- `scenarios/models.json` is the active list. Only `models.py` replaces it.
- `scenarios/scenarios.json` keeps the hand-set `mode`.
- `results/` holds transcripts, stats, and scores. Git tracks this tree on purpose.
- `archive/` and `meta/` are gitignored.

A scenario is any folder under `scenarios/` that contains `test.json`. The id is the relative path with forward slashes.

## Data rules

- Active list: `scenarios/models.json`. Historic list: `results/<scenario>/models.json`. `run.py` reads the active list and upserts only the key it just tested.
- Store model, scenario, score, and stats data as JSON lists of objects. Upsert with `utils.upsert_record` and write a list back. A failed test leaves the previous files in place.
- A scenario is complete when every active model key has `results/<scenario>/<model-key>.md`. Extra markdown (including `evaluation-*.md`) does not count. Choose work from `ready`, `mode`, and whether that markdown file exists. `status` in `scenarios.json` is only the report `scenarios.py` writes.
- Modes: `none` (skip), `update` (write a missing transcript only), `refresh` (overwrite the active list's files). New scenarios get `update`. `FORCE_MODE` overrides every scenario when set.
- Questions are `question1.md`, `question2.md`, … with no gaps. The loader stops at the first missing number.
- Resolve `system.md` and `inference.json` from the scenario folder, then each parent, then `scenarios/`. The nearest file replaces the ones above it. An inline `system` string in `test.json` wins. `test.json` can set `"system_prompt": false`.
- `<model-key>.json` stores `system_prompt` and `context_length` on the object. Messages are user and assistant turns only. The markdown transcript omits the system prompt.
- Context length is the loaded LM Studio `load_config.context_length`, then the winning `inference.json`, then `DEFAULT_CONTEXT_LENGTH` (16384).
- `evaluate.py` scores models that already have a transcript and a historic record. A model is scored when its record is in `results.json`. `--force` clears the conversation and replaces `results.json`.
- `clean.py` reads the active list and does not call `models.py`. A missing or empty active list stops it. Live deletion archives first. `info.md`, `results.md`, `results.json`, and `evaluation-*` stay in the live folder.
- Helper prose goes to `info.md`. `stats.md` and `scenarios.md` are rendered from the records.
- `used_ram: true` means system RAM rose by at least `RAM_SPILL_THRESHOLD_PERCENT` of `INSTALLED_RAM_GB` while that model ran.

## Editing

Change a question, `test.json`, `system.md`, or `inference.json` only when the user wants that test changed. The same wording is what makes the model comparison fair.

`documentation/instructions.md` is sent to the judge on every batch. Edit it when the scoring contract changes.

Hand edits to `scenarios.md`, `stats.md`, `results.md`, and `evaluation-*.md` are overwritten by the next run of the script that owns them. Delete one `<model-key>.md` and its `.json` when the user wants `update` mode to run that model again.

`run.py` keeps the evaluation status section in `test.md`. `evaluate.py` replaces that section.

## When behavior changes

Update the doc in the table above that describes the change. Update `documentation/lm-benchmark.md` when the briefing would be wrong. Add a dated entry at the top of `CHANGE.md`. Bump the `version` line in that script's docstring.

Keep these aligned with the scripts: `README.md`, `documentation/get-started.md`, `documentation/evaluation.md`, `documentation/plugin.md`, `documentation/lm-benchmark.md`, and `.env.example`.

## Code style

Match the file you are editing.

- Module docstring at the top. Entry points include a `Usage:` block and a `version` line.
- Shared paths and defaults in `config.py`. Shared load, save, upsert, and table helpers in `utils.py`.
- Print one clear error line and raise `SystemExit`.
- Read and write JSON with `utils.load_json` and `utils.save_json` (UTF-8, indent 2).
- A new OpenAI-compatible backend is a new `BACKENDS` entry in `evaluate.py` with `"kind": "openai"` and its own `key_env`. A different protocol needs a class in `plugins/` that implements `EvaluationBackend.generate(messages)`, a `BACKENDS` entry, and a branch in `resolve_backend`. See `documentation/plugin.md`.
- Stay on the standard library plus `requests` and `psutil`. `evaluate.py` parses `.env` itself.
- Comments explain a constraint. The section banners in `config.py` stay as they are.
- Windows is a development target. `plugins/grok_cli.py` writes the prompt to a temp file and calls `grok --prompt-file` because the Windows command line is about 32,767 characters. Anthropic requests send `EVAL_MAX_TOKENS`. The OpenAI-compatible backends do not.

## Leave these alone

- Do not commit `.env`, `meta/`, `archive/`, or `__pycache__/`.
- Do not put API keys or machine secrets in `config.py` or in docs.
- Do not gitignore `results/`.
- Do not delete or rewrite `results/` or `archive/` as a cleanup. `clean.py` is the removal path, and only when the user asks.
- Do not change `DRY_RUN`, `FORCE_MODE`, `EVAL_BACKEND`, or `EVAL_MODEL` and leave them that way.
- Do not load or unload LM Studio models, and do not call the xAI, OpenAI, Gemini, or Anthropic APIs, unless the user asked for that run.
- Do not treat `todo.md` as a backlog. Ask before starting an item from it.
- Do not reformat unrelated code.

## Commits

Commit when the user asks. Stage the source you changed and the docs that describe it. Leave generated result files out unless the user asked to keep that run.
