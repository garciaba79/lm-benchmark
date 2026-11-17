"""
Grok CLI plugin.
Uses the official Grok CLI with your SuperGrok subscription (no API key required).
"""

import json
import shutil
import subprocess
from pathlib import Path

from .base import EvaluationBackend


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
        # The CLI is one-shot, so we must re-send the entire history each call.
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "").strip()
            if content:
                prompt_parts.append(f"### {role}\n{content}")
        full_prompt = "\n\n".join(prompt_parts)

        cmd = [self.command, "-p", full_prompt, "--output-format", self.output_format]
        if self.model:
            cmd.extend(["-m", self.model])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Grok CLI timed out.")

        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip() or "unknown error"
            raise RuntimeError(f"Grok CLI failed: {err}")

        output = result.stdout.strip()
        if self.output_format == "json":
            try:
                data = json.loads(output)
                # Common shapes: {"content": "..."} or {"message": {"content": "..."}}
                if isinstance(data, dict):
                    if "content" in data:
                        return str(data["content"]).strip()
                    msg = data.get("message") or data.get("choices", [{}])[0].get("message", {})
                    if isinstance(msg, dict) and "content" in msg:
                        return str(msg["content"]).strip()
            except json.JSONDecodeError:
                pass
        return output
