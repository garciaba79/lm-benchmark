"""
Anthropic plugin.
"""

import os

import requests

from .base import EvaluationBackend


class AnthropicBackend(EvaluationBackend):
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model or os.getenv("EVAL_MODEL") or "claude-3-5-sonnet-20241022"

        if not self.api_key:
            raise RuntimeError("No Anthropic API key found. Set ANTHROPIC_API_KEY in your .env file.")

    def generate(self, messages: list[dict], **kwargs) -> str:
        # Convert OpenAI-style messages to Anthropic format (system is separate).
        system = ""
        anthropic_messages = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "system":
                system = content
            elif role in ("user", "assistant"):
                anthropic_messages.append({"role": role, "content": content})

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": anthropic_messages,
        }
        if system:
            payload["system"] = system

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Anthropic API request failed: {e}")

        data = resp.json()
        try:
            return data["content"][0]["text"].strip()
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Unexpected Anthropic response shape: {e}")
