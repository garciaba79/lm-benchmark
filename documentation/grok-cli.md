# Using Grok CLI with SuperGrok Subscription

This document explains how to install and use the official Grok CLI so that model calls draw from your SuperGrok weekly usage pool. No separate API key or per-token fees are required.

## What you need

- An active SuperGrok (or X Premium+) subscription.
- The official Grok CLI installed on your machine.

## Install the CLI

Any of the methods below make `grok` available in Git Bash, PowerShell, CMD, and Windows Terminal.  
You only need to install once. After that you can keep using your normal Git Bash terminal.

### Recommended on Windows (PowerShell installer)

Open PowerShell and run:

```powershell
irm https://x.ai/cli/install.ps1 | iex
```

This installs the native Windows binary to `%USERPROFILE%\.grok\bin` and adds it to your User PATH.  
Close and reopen your terminal of choice including Git Bash, CMD, or Windows Terminal. Then verify:

```bash
grok --version
```

### Alternative: npm (works everywhere)

If you already have Node.js:

```bash
npm i -g @xai-official/grok
```

The global npm bin directory is already on your PATH, so `grok` works immediately in Git Bash.

### Git Bash on macOS or Linux

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
```

This is the official method for macOS and Linux.  
On Windows Git Bash it sometimes fails with curl write errors when downloading the large binary.  
If it fails, use the PowerShell installer or npm instead.

### Notes

- The PowerShell installer is the most reliable option on Windows.
- After a successful install with PowerShell or npm, you can stay in Git Bash for daily use.
- You do not need to switch terminals permanently.

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

- `-p` or `--prompt` — the prompt text. Short prompts only. Windows rejects the process when the command line is longer than about 32,767 characters.
- `--prompt-file` — the same one-shot prompt, read from a file. `evaluate.py` uses this so a batch of result files is not placed on the command line.
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
