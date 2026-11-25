# LM Benchmark

Briefing for a cloud model that needs to understand this project without opening the repository. The human manual is `documentation/get-started.md`. Cloud ranking setup is `documentation/evaluation.md`. This file is the single project description to paste into a chat.

## What it is

LM Benchmark is a file-based Python 3.14 project. It tests local LLMs in LM Studio on the same scenarios, saves the chats and the speed numbers, and can send those results to a cloud model for a ranked evaluation.

There is no database. A scenario is a folder of markdown questions. A result is a matching folder of markdown and JSON. Scripts upsert records by key. They write JSON lists, not dicts. A normal run does not delete other models' results. `clean.py` is the only script that removes live results, and it archives those records first.

`config.py` exits on import when the interpreter is older than Python 3.14. Dependencies are `requests` and `psutil`. LM Studio's local server is expected at `http://localhost:1234`.

## Scripts

| Script | What it does | What it does not do |
|--------|----------------|---------------------|
| `models.py` | Reads `GET /api/v1/models` and replaces `scenarios/models.json` with the installed LLMs, sorted by parameter size, then name, then file size. | Does not run tests. Does not keep hand edits. Does not delete result files. |
| `scenarios.py` | Scans `scenarios/` and rewrites `scenarios/scenarios.json` and `scenarios/scenarios.md`. Keeps the `mode` already stored for each scenario. A new scenario gets `update`. | Does not run tests. Does not change result files. |
| `run.py` | Loads one active model at a time, asks that scenario's questions in order, and writes that model's result files. | Does not rewrite `scenarios/models.json`. Does not delete other models' transcripts or records. A failed test leaves the previous good files in place. |
| `evaluate.py` | Sends result files for one scenario to the cloud backend named in `config.py` and writes a ranking. | Does not run local models. A dry run writes nothing. |
| `clean.py` | Archives historic models that are no longer on the active list, then removes those keys from the live results. | Does not call `models.py`. Refuses to run when the active list is missing or empty. |
| `config.py` | Shared settings. | |
| `utils.py` | JSON load and save, keyed upsert, stats tables, path and prompt lookup. | |

`models.py`, `scenarios.py`, and `run.py` take no arguments. Change `DRY_RUN`, `FORCE_MODE`, and `BASE_URL` in `config.py`. `evaluate.py` accepts `--scenario`, `--force`, `--dry-run`, and `--batch-size`. `clean.py` accepts the words `archive`, `clean`, `results`, and `stats`. With no words it uses the defaults in `config.py`, which archive and then clean.

## Folders

```
config.py
models.py
scenarios.py
run.py
evaluate.py
clean.py
utils.py
plugins/
meta/hardware.json

scenarios/
  models.json                 active list. Only models.py replaces this file.
  scenarios.json              one record per scenario: scenario, name, ready, status, mode
  scenarios.md                generated status report
  info.md                     helper-model prose about the scenario list, when the helper runs
  system.md                   lowest-precedence system prompt
  inference.json              lowest-precedence inference settings
  <group>/<scenario>/
    test.json                 name, description, optional system_prompt false, optional system string
    question1.md              question2.md, ... with no gaps
    system.md                 highest-precedence system prompt
    inference.json            highest-precedence inference settings

results/
  stats.json                  root stats, rebuilt from scenario stats
  stats.md
  <group>/<scenario>/
    <model-key>.md            human transcript
    <model-key>.json          reconstruction transcript
    models.json               historic models for this scenario
    stats.json
    stats.md
    test.md
    results.json              cloud scores, one record per model
    results.md                readable table written from results.json
    evaluation-<cloud-model>.json
    evaluation-<cloud-model>.md
    evaluation.json
    info.md                   helper prose for this scenario

archive/
  YYYY MM DD/                 one folder per calendar day
    stats.json                root records that were archived that day, merged by key
    stats.md
    results/<group>/<scenario>/
      <model-key>.md
      <model-key>.json
      models.json
      stats.json
      stats.md
      test.md
      info.md                 copy of the live file, when it existed
      results.json            copy of the live file, when it existed
      results.md              copy of the live file, when it existed
      evaluation-*            copies, when they existed
```

## Two model lists

`scenarios/models.json` is the active list: the models to test now. `python models.py` replaces the whole file from LM Studio and prints that hand edits were discarded. Edit it after that refresh if you want a smaller set. `run.py` and `clean.py` only read it.

`results/<scenario>/models.json` is the historic record of models tested on that scenario. A successful test upserts the one model that just ran and leaves every other key in the file. Historic results can outlive the active list. Deleting a transcript makes `update` mode run that model again. Deleting the historic JSON row but keeping the transcript causes the next real `run.py` to put the active model's record back.

Both files are JSON lists of objects. The model key field is `key`. `scenarios.json` uses `scenario` as its key (the folder path, such as `function/fetch weather`). Scripts also accept a dict whose values are objects, then write a list again.

## Modes

Set on each scenario in `scenarios/scenarios.json`. `FORCE_MODE` in `config.py` overrides every scenario. A missing mode uses `DEFAULT_MODE`, which is `update`.

| Mode | Behavior |
|------|----------|
| `none` | Skip the scenario. |
| `update` | Run an active model only when `results/<scenario>/<model-key>.md` is missing. |
| `refresh` | Rerun every model on the active list and overwrite those result files. Every other result file stays. |

`update` is the right default. It fills gaps and does not spend another full run on models you already tested. Use `refresh` when the questions or the prompt changed and you want new answers from the current active list. Use `none` to leave a scenario out of this run. `scenarios.py` keeps the mode you set.

A scenario is complete only when every active model key has its `<model-key>.md`. Extra files, including `evaluation-*.md` and hand-written notes, are not counted. Status in `scenarios.json` is `none`, `partial`, or `complete` against the active list.

## What one successful test writes

For that model key only:

- `<model-key>.md` — title, model key, test name, timestamp, context label such as `16K`, then each user question and assistant reply. A stats line under a reply looks like `42 t/s, 300 tokens, 7s, 12%`. The system prompt is not written into this markdown.
- `<model-key>.json` — reconstruction file. Shape:

```json
{
  "key": "google-gemma-4-e4b",
  "display_name": "Gemma 4 E4B",
  "scenario": "function/fetch weather",
  "test": "Function Fetch Weather",
  "created": "11/19/2026, 01:02:03 PM",
  "context_length": 16384,
  "system_prompt": "optional text or null",
  "messages": [
    {"role": "user", "content": "question text"},
    {"role": "assistant", "content": "reply text", "stats_line": "42 t/s, 300 tokens, 7s, 12%"}
  ]
}
```

`system_prompt` is a field on the object. It is not inserted as a system or user message. The messages are only the questions and the replies. The chat request sent to LM Studio still includes the system prompt as a system message. That is separate from the saved transcript.

The same run also upserts that model into the scenario `models.json` and `stats.json`, then rebuilds `stats.md` and `test.md`. `stats.md` columns are Model, Avg t/s, Total time, and one column per question. `test.md` keeps an existing evaluation-status section. `results.md` is created only when it is missing, with a short paste placeholder. `evaluate.py` later writes `results.json` and replaces `results.md` from that file.

`DRY_RUN` prints the plan and writes nothing, including `meta/hardware.json`.

Root `results/stats.json` is rebuilt only after a real run that finished at least one test. `overall_seconds` on that file is the wall-clock time of that run. Each model's `total_seconds` is the sum of its scenario records. A model already on the root list is kept when this run did not touch it. `used_ram` stays true once any run has marked it true.

## System prompt and inference

Lookup order, highest first: the scenario folder, then each parent group folder, then `scenarios/`. The nearest `inference.json` replaces the ones above it. Fields are not merged.

`test.json` can set `"system_prompt": false`, which skips the prompt, or an inline `"system"` string, which wins. Otherwise a `system` string in the winning `inference.json` is used, then `system.md`.

`USE_CUSTOM_INFER` defaults to true. The chat request then forwards `temperature`, `top_p`, `top_k`, `repeat_penalty`, and `reasoning_effort` when they are set. The load request forwards `context_length` when it is set. When `USE_CUSTOM_INFER` is false, LM Studio's own defaults are used.

Question files must be numbered `question1.md`, `question2.md`, and so on. The loader stops at the first missing number. `question1.md` and `question3.md` with no `question2.md` runs only question 1.

## Context length and the percent on a stats line

LM Studio's load API reports the context that was actually applied. `run.py` posts to `/api/v1/models/load` with `echo_load_config: true` and reads `load_config.context_length`. The list API also shows `loaded_instances[].config.context_length` for a model that is already loaded. The OpenAI-compatible chat API returns token counts. It does not return the configured window.

The number stored as `context_length` is chosen in this order:

1. The context LM Studio echoed from the load.
2. `context_length` in the winning `inference.json`.
3. `DEFAULT_CONTEXT_LENGTH` in `config.py`, which is 16384.

Most models in this project are loaded at 16K. Some are loaded at 8K. The runner reloads a model only when the requested context changes. Scenarios for one model are sorted so the larger context runs first.

The percent in a stats line is `usage.total_tokens` from that reply divided by the context length above. A line that says `12%` means the conversation occupied about 12 percent of the window after that reply. It is not a quality score.

## RAM spill

Before a model runs, `psutil` records system RAM in use. During the run the script tracks the peak. `spilled_to_ram()` returns true when the increase is at least `RAM_SPILL_THRESHOLD_PERCENT` of `INSTALLED_RAM_GB` (25 percent of 32 GB). That true value is stored as `used_ram` on the root stats. The older function name `get_fits_memory` meant the opposite of what it returned and has been removed. `used_ram: true` means the model spilled out of VRAM into system RAM. The check is a heuristic. It is skipped when `psutil` is missing. `meta/hardware.json` stores the installed RAM, installed VRAM, threshold, and the base RAM reading for that run.

The runner unloads every loaded LM Studio instance before the first test model, and again when the context length changes and after the model finishes.

## Helper model

`HELPER_MODEL` is `lfm2.5-1.2b-instruct`. After a real run that wrote results, the helper writes a short paragraph to `results/<scenario>/info.md`. `scenarios.py` can write `scenarios/info.md`. The helper text is not written into `stats.md` or `scenarios.md`. If the helper fails, the script writes no placeholder.

## Parameter size in models.py

LM Studio's `params_string` is used when it parses as a number of billions, such as `7B` or `230M`. When that field is missing, the script reads the model key. A normal token such as `7b` or `230m` works. Names that glue the size on as `e4b` or `e2b` (Gemma 4 E4B, E2B) are read as 4 and 2 billion. An MoE name such as `24b-a2b` stays 24 billion, because the active-parameter suffix is not treated as the model size.

## Evaluation

`evaluate.py` reads `<model-key>.md` files. It does not score `evaluation-*.md` or other notes.

`EVAL_BACKEND` defaults to `grok_api`. `EVAL_MODEL` defaults to `grok-4.3`. The model name comes from `config.py`, not from `.env`. Each backend reads one key:

| Backend | Key | Endpoint |
|---------|-----|----------|
| `grok_api` | `GROK_API_KEY` | `https://api.x.ai/v1` |
| `openai` | `OPENAI_API_KEY` | `https://api.openai.com/v1` |
| `gemini` | `GEMINI_API_KEY` | `https://generativelanguage.googleapis.com/v1beta/openai` |
| `anthropic` | `ANTHROPIC_API_KEY` | `https://api.anthropic.com/v1/messages` |
| `grok_cli` | none | local `grok` command, SuperGrok login |

There is no fallback from one provider's key to another. `EVAL_BASE_URL` overrides the OpenAI-compatible URL. Empty means the default above. `EVAL_TIMEOUT` is 600 seconds for every backend. `EVAL_BATCH_SIZE` is 5.

Anthropic requires `max_tokens` on every request. `EVAL_MAX_TOKENS` is 8192, which matches Claude 3.5's output cap. A newer Claude model can be given a higher number in `config.py`. The OpenAI-compatible plugins do not send a max-token cap.

The Grok CLI plugin writes the prompt to a temporary file and runs `grok --prompt-file`. Putting the same text in `grok -p` fails on Windows once the command line passes about 32,767 characters. The temp file is deleted after the call.

Instructions for the judge live in `documentation/instructions.md`. `EVAL_BATCH_PROMPT` in `config.py` is the short text sent with the current JSON and the new transcripts.

The judge returns one JSON object: `summary`, `takeaways`, `practical`, `notes`, and `models`. Each model record has `key`, `avg_tps`, `correctness`, `quality`, `task_understanding`, `instruction_following`, `usefulness`, `faithfulness`, `pros`, `cons`, and `notes`. `grok_api` and `openai` send that shape as `response_format`. The script checks it again. `key` and `avg_tps` are then taken from the scenario's own files.

Files written for a finished scenario:

- `results.json` — the score table
- `results.md` — that table, sorted by correctness, then quality
- `evaluation-<model>.json` — the judge conversation, plus `evaluated_keys`, `final_complete`, and `usage` (requests and token counts for this judge on this scenario)
- `evaluation-<model>.md` — that conversation as markdown, regenerated from the JSON
- `evaluation.json` — index of those files
- `test.md` — an evaluation-status section is added or replaced

A key counts as scored when its record is in `results.json`. Each request sends the instructions, the current JSON, and the new transcripts. The script merges by key and keeps a row the reply omits. `--force` clears the conversation and `results.json`. `--dry-run` prints the plan and writes nothing.

This evaluation JSON is the judge's conversation. It is not the local model's transcript. The local transcript is `<model-key>.json`.

## clean.py

Compare each scenario's historic `models.json` with the active list. A key that is historic but not active is a removed model.

`archive` copies, and does not delete:

- that model's `<model-key>.md` and `<model-key>.json`
- that model's object inside the scenario `models.json` and `stats.json`, upserted into the archive copies of those files
- that model's object from root `results/stats.json`, upserted into `archive/YYYY MM DD/stats.json`
- a rebuilt archive `stats.md`
- a short archive `test.md` that lists the archived models
- copies of the live `info.md`, `results.md`, `results.json`, `evaluation.json`, and `evaluation-*` files

A second archive on the same day upserts the same keys. It does not replace the archive list with only the latest batch. Live `info.md`, `results.md`, `results.json`, and evaluation files stay where they are, because they describe the whole scenario. The archive holds a copy from that day.

`results` and `stats`, including `python clean.py clean`, archive first and then remove the live copies of those model keys. `results` deletes the transcript `.md` and `.json`. `stats` removes the keys from the live scenario `models.json`, `stats.json`, `stats.md`, `test.md`, and the root stats, then rebuilds the tables. The evaluation-status section in the live `test.md` is kept.

An empty or missing active list aborts. Nothing is archived or deleted. A transcript whose key is not in that scenario's `models.json` is not archived and is not deleted. Empty result folders are left in place. After a removal, `scenarios.py` runs so scenario status matches the files that remain.

## Usual workflow

1. Start the LM Studio server.
2. `python models.py`, then edit `scenarios/models.json` if you want fewer models.
3. Add a scenario folder with `test.json` and `question1.md`.
4. `python scenarios.py`.
5. Set `mode` in `scenarios/scenarios.json` when a scenario should not stay on `update`.
6. `python run.py`.
7. `python evaluate.py` when you want a cloud ranking.
8. `python clean.py` only when you want live results to drop models that are no longer on the active list. Their records remain under `archive/YYYY MM DD/`.

## Other documents

- `README.md` — short human introduction
- `documentation/get-started.md` — settings, precedence, and the hand-edit table
- `documentation/evaluation.md` — how to run the judge
- `documentation/workflow.md` — the same process done by hand
- `documentation/instructions.md` — the scoring instructions sent to the judge
- `documentation/plugin.md` — how a backend is wired
- `documentation/summary-app.md` — a one-page summary that points here
- `CHANGE.md` — dated history of behavior changes

Do not treat `results/` or `scenarios/` markdown as the specification. Those files are test content and test output.
