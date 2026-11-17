"""
Simple plugin interface for cloud evaluation backends.
"""

from abc import ABC, abstractmethod


class EvaluationBackend(ABC):
    @abstractmethod
    def generate(self, messages: list[dict], **kwargs) -> str:
        """
        Send a conversation and return the assistant's text reply.

        messages: list of {"role": "user"|"assistant"|"system", "content": str}
        """
        raise NotImplementedError
