"""
OpenAI-compatible plugin.
Works with OpenAI, Grok API, Gemini (OpenAI endpoint), and most other OpenAI-style APIs.
"""

import os
from pathlib import Path

import requests
import config

from .base import EvaluationBackend


class OpenAICompatibleBackend(EvaluationBackend):
    def __init__(self, base_url=None, api_key=None, model=None):
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("GROK_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("EVAL_MODEL") or "gpt-4o"

        # Usage stats collected during the run
        self.stats = {
            "requests": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

        if not self.api_key:
            raise RuntimeError(
                "No API key found. Set OPENAI_API_KEY, GROK_API_KEY, or GEMINI_API_KEY in your .env file."
            )

    def generate(self, messages: list[dict], **kwargs) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        try:
            timeout = getattr(config, "EVAL_TIMEOUT", 180)
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"OpenAI-compatible API request failed: {e}")


        data = resp.json()

        # Track usage
        self.stats["requests"] += 1
        usage = data.get("usage") or {}
        self.stats["prompt_tokens"] += usage.get("prompt_tokens", 0)
        self.stats["completion_tokens"] += usage.get("completion_tokens", 0)
        self.stats["total_tokens"] += usage.get("total_tokens", 0)

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Unexpected API response shape: {e}")

    def get_stats(self) -> dict:
        return dict(self.stats)
