"""
Grok CLI plugin.
Uses the official Grok CLI with your SuperGrok subscription (no API key required).
"""

import json
import shutil
import subprocess
from pathlib import Path

from .base import EvaluationBackend

# Set to True to print debug info (command, prompt length, stderr, etc.)
DEBUG = False


class GrokCLIBackend(EvaluationBackend):
    def __init__(self, command="grok", model=None, output_format="json"):
        self.command = command
        self.model = model
        self.output_format = output_format

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

        # Use -p (command-line argument). This works reliably but has a Windows length limit.
        cmd = [self.command, "-p", full_prompt, "--output-format", self.output_format]
        if self.model:
            cmd.extend(["-m", self.model])

        if DEBUG:
            print(f"  [debug] Command length: {sum(len(a) for a in cmd)} characters")
            print(f"  [debug] Using -p argument")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=300,
                check=False,
            )
        except subprocess.TimeoutExpired:
            if DEBUG:
                print("  [debug] subprocess timed out")
            raise RuntimeError("Grok CLI timed out.")
        except OSError as e:
            if getattr(e, "winerror", None) == 206 or "too long" in str(e).lower():
                raise RuntimeError(
                    f"Prompt too long for Windows command line ({len(full_prompt)} characters). "
                    "Lower EVAL_BATCH_SIZE or switch to the Grok API."
                )
            raise

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
