# Instructions for Creating a Pluggable Cloud AI Backend

Use this document as the full prompt when asking another AI to implement a plugin system. The goal is a simple, config-driven way to swap cloud AI providers (starting with Grok CLI) inside a Python project. The design should be generic enough that other providers can be added later as new plugins.

## Context

The project has (or will have) a `config.py` that selects which backend to use. The main script checks the config and loads the matching plugin. The first plugin is the official Grok CLI, which uses the user's SuperGrok subscription (no API fees). Later plugins could target other cloud AIs (OpenAI, Anthropic, etc.) if desired.

## Requirements

Create three things:

1. A small plugin interface / base class.
2. A Grok CLI plugin that implements the interface by calling the `grok` command via subprocess.
3. Example wiring so a main script can load the plugin named in `config.py`.

Also show what to add to `config.py`.

### Plugin interface

Define a simple abstract base or protocol. At minimum it should support:

- A method that takes a prompt string and returns the model's text response.
- Optional parameters for model name, output format, or extra flags.
- Clear error handling when the backend fails.

Name the method something like `generate(prompt: str, **kwargs) -> str`.

### Grok CLI plugin

- File name suggestion: `plugins/grok_cli.py` (or similar).
- Implementation uses `subprocess` to run:

  ```bash
  grok -p "<prompt>" --output-format json
  ```

- Parse the JSON (or plain text) and return the useful content.
- Assume the user has already installed the CLI and completed the one-time SuperGrok browser login (session lives in `~/.grok/auth.json`). Do not require or set an API key.
- Handle non-zero exit codes and missing `grok` binary with clear errors.
- Keep the plugin self-contained. No external dependencies beyond the Python standard library.

### Config

Show the relevant section for `config.py`. Example shape:

```python
# config.py
AI_BACKEND = "grok_cli"   # or "openai", "anthropic", etc.

# Optional per-backend settings
GROK_CLI = {
    "command": "grok",
    "default_model": None,
    "output_format": "json",
}
```

### Main script usage

Show a short example of how the main script loads and uses the plugin:

```python
from config import AI_BACKEND
# load the right plugin based on AI_BACKEND
# then:
response = plugin.generate("Summarize this text: ...")
```

The loading can be a simple if/elif, a dictionary of plugins, or a small factory. Prefer the simplest approach that is easy to extend.

### Genericity

Design the interface so a future plugin for another cloud AI (for example one that uses the OpenAI SDK or Anthropic SDK) can implement the same `generate` method. The main script should not care which plugin is loaded, only that it receives a string response.

## Deliverables the AI should produce

- The plugin interface code.
- The full Grok CLI plugin implementation.
- The config.py snippet.
- A short main-script example that demonstrates loading the configured plugin and calling it.
- Brief comments explaining how to add a new plugin later.

## Constraints

- Use only the Python standard library for the Grok CLI plugin.
- Do not hard-code API keys.
- Prefer clear, readable code over clever abstractions.
- The Grok CLI path must work with the existing SuperGrok session (no API key required).

Implement exactly these pieces. Do not add unrelated features.
