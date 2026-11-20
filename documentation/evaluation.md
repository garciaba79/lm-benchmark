# Evaluating Results with a Cloud Model

`evaluate.py` sends the model result files from a scenario to a cloud model and writes a ranked `results.md`.

## Quick start

1. Set `EVAL_BACKEND` and `EVAL_MODEL` in `config.py`. The default backend is `grok_api` and the default model is `grok-4.3`.
2. Put that backend's key in `.env`. `grok_api` reads `GROK_API_KEY` only. It does not use `OPENAI_API_KEY` or `GEMINI_API_KEY`.
3. Run:

   ```bash
   python evaluate.py
   ```

The Grok CLI plugin is still available (`EVAL_BACKEND = "grok_cli"`). It is not the default. See `grok-cli.md` if you use it. The grok_cli tends to fail due to terminal limitations.

## Common options

```bash
python evaluate.py --scenario summary/expedition   # one scenario
python evaluate.py --force                         # re-evaluate everything
python evaluate.py --dry-run                       # show what would be sent
python evaluate.py --batch-size 3                  # override batch size
```

## What it writes

In each scenario results folder:

- `results.md` — the final ranked evaluation
- `evaluation-<model>.json` — the conversation, plus `evaluated_keys` and `final_complete`
- `evaluation-<model>.md` — the same conversation in markdown
- `evaluation.json` — index of the evaluation files in the folder
- `test.md` — updated with an “Evaluation status” section at the bottom

`--dry-run` prints the plan and does not write these files. It does not need a successful API call. It warns when the selected key is missing.

## Configuration

Settings live in `config.py` under the EVALUATION SETTINGS section.

- `EVAL_BACKEND` — `"grok_api"` (default), `"openai"`, `"gemini"`, `"anthropic"`, or `"grok_cli"`
- `EVAL_BATCH_SIZE` — how many result files to send at once (default 5)
- `EVAL_MODEL` — cloud model name. This is the model the script uses. A value in `.env` does not override it
- `EVAL_BASE_URL` — optional override. Leave it empty to use the default URL for the backend
- `EVAL_TIMEOUT` — seconds for one API or CLI call. Every backend uses this value
- `EVAL_DRY_RUN` — default dry-run flag

Private keys go in `.env` (copy from `.env.example`). Each backend reads its own variable:

| Backend | Key | Default base URL |
|---------|-----|------------------|
| `grok_api` | `GROK_API_KEY` | `https://api.x.ai/v1` |
| `openai` | `OPENAI_API_KEY` | `https://api.openai.com/v1` |
| `gemini` | `GEMINI_API_KEY` | `https://generativelanguage.googleapis.com/v1beta/openai` |
| `anthropic` | `ANTHROPIC_API_KEY` | Anthropic's own endpoint |
| `grok_cli` | none | local `grok` command |

The script never falls back from one backend to another. If the chosen backend fails, it prints a clear error so you can fix the key, the model name, or the CLI login.

## Partial updates

The script loads `evaluation-<model>.json` for the configured model. `evaluated_keys` is the list of local model keys already scored. Only missing keys are sent. When new keys appear after a final ranking, that ranking turn is removed and a new one is requested at the end.

Older evaluation files do not have `evaluated_keys`. The script fills that list from the `### <model-key>` lines it wrote into the conversation, then saves the list. Use `--force` to start over.

The script reads `evaluation-<model>.json`. It does not read markdown transcripts. When a scenario finishes, it writes `evaluation-<model>.md` from that JSON.

Three hand transcripts that used to be named `grok.md` are now `evaluation-grok-4.3.md`:

- `results/summary/expedition/evaluation-grok-4.3.md`
- `results/react components/count/evaluation-grok-4.3.md`
- `results/function/fetch weather/evaluation-grok-4.3.md`

Those three folders have no `evaluation-grok-4.3.json`. The next `evaluate.py` run that scores them with `grok-4.3` will replace that markdown with the new conversation.
