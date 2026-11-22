"""
OpenAI-compatible plugin.
Works with OpenAI, Grok API, Gemini (OpenAI endpoint), and most other OpenAI-style APIs.
"""

import requests
import config

from .base import EvaluationBackend


class OpenAICompatibleBackend(EvaluationBackend):
    def __init__(self, base_url, api_key, model, timeout=None):
        if not base_url:
            raise RuntimeError("No base URL was provided for the OpenAI-compatible backend.")
        if not api_key:
            raise RuntimeError("No API key was provided for the OpenAI-compatible backend.")
        if not model:
            raise RuntimeError("No model was provided for the OpenAI-compatible backend.")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout or getattr(config, "EVAL_TIMEOUT", 600)

        # Usage stats collected during the run
        self.stats = {
            "requests": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

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
        response_format = kwargs.get("response_format")
        if response_format:
            payload["response_format"] = response_format
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            detail = ""
            response = getattr(e, "response", None)
            if response is not None and response.text:
                detail = f"\n{response.text[:1000]}"
            raise RuntimeError(f"OpenAI-compatible API request failed: {e}{detail}")


        data = resp.json()

        # Track usage
        self.stats["requests"] += 1
        usage = data.get("usage") or {}
        self.stats["prompt_tokens"] += usage.get("prompt_tokens", 0)
        self.stats["completion_tokens"] += usage.get("completion_tokens", 0)
        self.stats["total_tokens"] += usage.get("total_tokens", 0)

        try:
            choice = data["choices"][0]
            message = choice.get("message") or {}
            refusal = message.get("refusal")
            if refusal:
                raise RuntimeError(f"The model refused the request: {refusal}")
            content = (message.get("content") or "").strip()
            if choice.get("finish_reason") == "length":
                raise RuntimeError("The model reply was cut off (finish_reason=length).")
            if not content:
                raise RuntimeError("The model returned an empty reply.")
            return content
        except RuntimeError:
            raise
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Unexpected API response shape: {e}")

    def get_stats(self) -> dict:
        return dict(self.stats)
