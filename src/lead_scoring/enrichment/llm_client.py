import json
import time
from typing import Protocol, runtime_checkable

import openai

from lead_scoring.config import OPENAI_API_KEY, OPENAI_MODEL, LLM_TIMEOUT_SECONDS


@runtime_checkable
class LLMClient(Protocol):
    def complete(self, system: str, user: str) -> str:
        """Send a system + user prompt and return the raw string response."""
        ...


class OpenAIClient:
    def __init__(self) -> None:
        self._client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def complete(self, system: str, user: str) -> str:
        response = self._client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0,
            timeout=LLM_TIMEOUT_SECONDS,
        )
        return response.choices[0].message.content or ""


class MockLLMClient:
    """
    Simulates an LLM response for local development and testing.
    Prompt engineering logic lives in enrichment/prompts.py — this client
    only fakes the network call and returns pre-baked responses.
    """

    _MOCK_RESPONSES: dict[str, dict] = {
        "sky-net": {
            "industry": "Cybersecurity",
            "size": 250,
            "intent": "Automate threat response operations",
        },
        "baking": {
            "industry": "Retail",
            "size": 5,
            "intent": "Basic firewall protection for small business",
        },
        "fintech": {
            "industry": "Fintech",
            "size": 75,
            "intent": "Scalable security platform for regulated startup",
        },
        "ghost": {
            "industry": "Other",
            "size": 0,
            "intent": "General pricing inquiry with no additional context",
        },
    }

    def complete(self, system: str, user: str) -> str:
        time.sleep(0.1)  # simulate network latency

        for keyword, response in self._MOCK_RESPONSES.items():
            if keyword in user.lower():
                return json.dumps(response)

        return json.dumps({"industry": "Other", "size": 0, "intent": "Unknown"})
