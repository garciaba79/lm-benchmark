# Evaluation plugins

`evaluate.py` scores local results by calling one cloud backend. The backends live in `plugins/`. How to run an evaluation is in [evaluation.md](evaluation.md). This page is the code contract.

## Interface

`plugins/base.py` defines `EvaluationBackend`. The method is:

```python
def generate(self, messages: list[dict], **kwargs) -> str:
    ...
```

`messages` is a list of `{"role": "user"|"assistant"|"system", "content": str}`. The return value is the assistant's text.

## Backends

| `EVAL_BACKEND` | Class | Key in `.env` | Default endpoint |
|----------------|-------|---------------|------------------|
| `grok_api` | `OpenAICompatibleBackend` in `plugins/openai.py` | `GROK_API_KEY` | `https://api.x.ai/v1` |
| `openai` | `OpenAICompatibleBackend` | `OPENAI_API_KEY` | `https://api.openai.com/v1` |
| `gemini` | `OpenAICompatibleBackend` | `GEMINI_API_KEY` | `https://generativelanguage.googleapis.com/v1beta/openai` |
| `anthropic` | `AnthropicBackend` in `plugins/anthropic.py` | `ANTHROPIC_API_KEY` | `https://api.anthropic.com/v1/messages` |
| `grok_cli` | `GrokCLIBackend` in `plugins/grok_cli.py` | none | local `grok` command |

The default in `config.py` is `EVAL_BACKEND = "grok_api"` and `EVAL_MODEL = "grok-4.3"`. `EVAL_BASE_URL` overrides the endpoint for the OpenAI-compatible backends. Leave it empty to use the table above. `EVAL_TIMEOUT` (600 seconds) is passed into every backend.

`evaluate.py` reads one key for the selected backend. It does not try another provider's key. A dry run warns when the key is missing and does not construct the client. A real run exits.

Anthropic's API requires `max_tokens`. `AnthropicBackend` sends `EVAL_MAX_TOKENS` from `config.py` (default 8192). The OpenAI-compatible backends do not send a max-token cap.

## How a backend is chosen

`BACKENDS` in `evaluate.py` maps the config name to a label, a key variable, a default base URL, and a kind (`openai`, `anthropic`, or `grok_cli`). `resolve_backend()` loads `.env`, checks `EVAL_MODEL`, and returns the matching class. The model name always comes from `EVAL_MODEL`.

`GrokCLIBackend` flattens the message list into one prompt, writes it to a temp file, and runs `grok --prompt-file`. That avoids the Windows command-line limit of about 32,767 characters, which `grok -p` hits on a large batch. The plugin uses the existing SuperGrok login and does not take an API key. The temp file is deleted after the call.

## Adding a backend

Another OpenAI-compatible service needs a new entry in `BACKENDS` with `"kind": "openai"`, its own `key_env`, and its default `base_url`. `resolve_backend()` already constructs `OpenAICompatibleBackend` for that kind.

A different protocol needs three pieces:

1. A class in `plugins/` that subclasses `EvaluationBackend` and implements `generate(messages)`.
2. An entry in `BACKENDS` with a new `kind`.
3. A branch in `resolve_backend()` that constructs it with the key, `EVAL_MODEL`, and `EVAL_TIMEOUT`.

Pass the key in from `resolve_backend()`. Do not read a different provider's environment variable as a fallback.
