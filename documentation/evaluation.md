# Evaluating Results with a Cloud Model

`evaluate.py` sends the model result files from a scenario to a cloud model and writes a ranked `results.md`.

## Quick start

1. Make sure the Grok CLI is installed and logged in, see `grok-cli.md`, or set up an API key in `.env`.
2. Run:

   ```bash
   python evaluate.py
   ```

By default it uses the Grok CLI backend and processes every scenario under `results/` that still has unevaluated models.

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
- `grok.md` — the full turn-by-turn conversation
- `test.md` — updated with an “Evaluation status” section at the bottom

## Configuration

Settings live in `config.py` under the EVALUATION SETTINGS section.

- `EVAL_BACKEND` — `"grok_cli"` (default), `"openai"`, `"anthropic"`, `"gemini"`, or `"grok_api"`
- `EVAL_BATCH_SIZE` — how many result files to send at once (default 5)
- `EVAL_MODEL` — optional model override
- `EVAL_BASE_URL` — optional base URL for OpenAI-compatible backends
- `EVAL_DRY_RUN` — default dry-run flag

Private keys go in `.env` (copy from `.env.example`). The script never falls back from one backend to another. If the chosen backend fails, it prints a clear error so you can fix the CLI login or the API key.

## Partial updates

If some models have already been evaluated, the script loads the existing `grok.md`, continues the conversation, and only sends the missing result files. Use `--force` to start over.
