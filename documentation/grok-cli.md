# Using Grok CLI with SuperGrok Subscription

This document explains how to install and use the official Grok CLI so that model calls draw from your SuperGrok weekly usage pool. No separate API key or per-token fees are required.

## What you need

- An active SuperGrok (or X Premium+) subscription.
- The official Grok CLI installed on your machine.

## Install the CLI

### Git Bash on Windows, macOS, Linux

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://x.ai/cli/install.ps1 | iex
```

After installing, restart your terminal or open a new Git Bash or PowerShell window and verify:

```bash
grok --version
```

## Authenticate with your subscription

1. Run `grok` in any directory.
2. Your browser opens. Sign in with the account that has SuperGrok.
3. The CLI stores a session token in `~/.grok/auth.json`.
4. Future calls reuse this token automatically. Tokens refresh in the background.

You only need to do this once per account or again if the token expires and cannot be refreshed.

## Switching between two SuperGrok accounts

The CLI stores one session at a time in `~/.grok/auth.json`. To switch:

1. Log out of the current account:

   ```bash
   grok logout
   ```

2. Run `grok` again and sign in with the other account in the browser.

3. The new session overwrites `~/.grok/auth.json`.

To avoid logging every time, you can keep two copies of the auth file and swap them:

```bash
# Save the current session
cp ~/.grok/auth.json ~/.grok/auth-account1.json

# Later, switch to the other account
cp ~/.grok/auth-account2.json ~/.grok/auth.json
```

After swapping, the next `grok` command uses the account whose token is in `auth.json`.

## Check which account is active

There is no dedicated “whoami” command. The easiest checks are:

- Run a short prompt and look at the response, or
- Open Grok in the browser while logged in as the same user and compare the weekly usage numbers.

If the CLI asks for an API key, the session token is missing or expired. Run `grok` again and complete the browser login.

## How billing works

- When a session token exists in `~/.grok/auth.json`, the CLI uses your SuperGrok subscription.
- Usage comes out of the shared weekly pool (same pool as Grok chat, Imagine, and other products).
- No API key is needed. No extra charges appear on the xAI API console.
- If you set an `XAI_API_KEY` environment variable and no session token exists, the CLI falls back to the paid API. To stay on the subscription, leave the session token in place and do not set `XAI_API_KEY`.

## Using the CLI from scripts

Headless mode is designed for scripts and automation:

```bash
grok -p "Explain this function" --output-format json
```

Common flags:

- `-p` or `--prompt` — the prompt text.
- `--output-format json` or `streaming-json` — structured output that is easy to parse.
- `-m` — optional model override.
- `--cwd` — set the working directory.

The process starts, runs the prompt against your subscription session, prints the result, and exits. You do not need an interactive TUI session open.

## Checking usage

Open Grok in the browser or app, go to Settings → Usage. You will see the weekly pool percentage and a breakdown by product (Chat, Build, Imagine, etc.). Heavy script use burns the pool faster than casual chat.

## Troubleshooting

- If the CLI asks for an API key, the session token is missing. Run `grok` again and complete the browser login.
- To force the API path (not recommended for this project), run `grok logout` then set `XAI_API_KEY`.
- Update the CLI anytime with `grok update`.

That is all you need. After the one-time login, any call to `grok -p ...` uses your SuperGrok subscription.
