"""
Grok CLI plugin.
Uses the official Grok CLI with your SuperGrok subscription (no API key required).
"""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from .base import EvaluationBackend

# Set to True to print debug info (command, prompt length, stderr, etc.)
DEBUG = False


class GrokCLIBackend(EvaluationBackend):
    def __init__(self, command="grok", model=None, output_format="json", timeout=None):
        self.command = command
        self.model = model
        self.output_format = output_format
        self.timeout = timeout or 600

    def generate(self, messages: list[dict], **kwargs) -> str:
        if not shutil.which(self.command):
            raise RuntimeError(
                f"Grok CLI not found ('{self.command}'). "
                "Install it and complete the one-time browser login."
            )

        # Build a single prompt that contains the full conversation history.
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "").strip()
            if content:
                prompt_parts.append(f"### {role}\n{content}")
        full_prompt = "\n\n".join(prompt_parts)

        if DEBUG:
            print(f"  [debug] Prompt length: {len(full_prompt)} characters")

        # --prompt-file keeps the prompt off the command line. Windows rejects
        # grok -p once the command line passes about 32,767 characters.
        prompt_path = None
        try:
            fd, prompt_path = tempfile.mkstemp(prefix="lm-benchmark-grok-", suffix=".md")
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(full_prompt)
            cmd = [self.command, "--prompt-file", prompt_path, "--output-format", self.output_format]
            if self.model:
                cmd.extend(["-m", self.model])

            if DEBUG:
                print(f"  [debug] Command: {' '.join(cmd[:3])} ...")

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=self.timeout,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                if DEBUG:
                    print("  [debug] subprocess timed out")
                raise RuntimeError("Grok CLI timed out.")
        finally:
            if prompt_path:
                try:
                    os.remove(prompt_path)
                except OSError:
                    pass

        if DEBUG:
            print(f"  [debug] Return code: {result.returncode}")
            if result.stderr:
                print(f"  [debug] stderr: {result.stderr.strip()}")
            if result.stdout:
                print(f"  [debug] stdout length: {len(result.stdout)} characters")

        if result.returncode != 0:
            err = (result.stderr or "").strip() or (result.stdout or "").strip() or "unknown error"
            raise RuntimeError(f"Grok CLI failed: {err}")

        output = (result.stdout or "").strip()
        if not output:
            err = (result.stderr or "").strip()
            raise RuntimeError(f"Grok CLI returned no output. stderr: {err or '(empty)'}")

        if self.output_format == "json":
            try:
                data = json.loads(output)
                if isinstance(data, dict):
                    if "content" in data and data["content"]:
                        return str(data["content"]).strip()
                    msg = data.get("message") or {}
                    if isinstance(msg, dict) and msg.get("content"):
                        return str(msg["content"]).strip()
                    choices = data.get("choices") or []
                    if choices and isinstance(choices[0], dict):
                        msg = choices[0].get("message") or {}
                        if isinstance(msg, dict) and msg.get("content"):
                            return str(msg["content"]).strip()
            except json.JSONDecodeError:
                if DEBUG:
                    print("  [debug] JSON decode failed, returning raw output")
        return output
