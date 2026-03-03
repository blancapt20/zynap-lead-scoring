import json
import time
from typing import Protocol, runtime_checkable

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

    return json.dumps({"industry": "Other", "size": 0, "intent": "Unknown"})
