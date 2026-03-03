import json
import time
from typing import Protocol, runtime_checkable

from lead_scoring.config import (
    LLM_MODEL,
    LLM_PROVIDER,
    LLM_RESPONSE_FORMAT,
    LLM_TEMPERATURE,
    LLM_TOP_P,
)

@runtime_checkable
class LLMClient(Protocol):
    def complete(self, system: str, user: str) -> str:
        """Send a system + user prompt and return the raw string response."""
        ...


class MockLLMClient:
    """
    Simulates an LLM response for local development and testing.
    Prompt engineering logic lives in enrichment/prompts.py — this client
    only fakes the network call and returns pre-baked responses.
    The real-client knobs already exist in config.py (model/temperature/top_p/
    response_format) so this module can be swapped with a provider call later.
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
        return mock_llm_call(user)


def mock_llm_call(raw_prompt: str) -> str:
    """
    Simulates API latency and returns deterministic JSON for known test leads.
    """
    time.sleep(0.1)

    for keyword, response in MockLLMClient._MOCK_RESPONSES.items():
        if keyword in raw_prompt.lower():
            return json.dumps(response)

    # Keep return as strict JSON to mirror a real JSON-mode response.
    return json.dumps({"industry": "Other", "size": 0, "intent": "Unknown"})


# Expose active LLM settings for visibility/debugging.
ACTIVE_LLM_SETTINGS: dict[str, str | float] = {
    "provider": LLM_PROVIDER,
    "model": LLM_MODEL,
    "temperature": LLM_TEMPERATURE,
    "top_p": LLM_TOP_P,
    "response_format": LLM_RESPONSE_FORMAT,
}
