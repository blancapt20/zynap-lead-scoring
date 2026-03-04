import json
import time
from typing import Protocol, runtime_checkable

from lead_scoring.config import (
    API_KEY,
    LLM_MODEL,
    LLM_PROVIDER,
    LLM_RESPONSE_FORMAT,
    LLM_TEMPERATURE,
    LLM_TOP_P,
)

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - depends on optional runtime dependency
    OpenAI = None

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

    _MOCK_PATTERNS: list[tuple[tuple[str, ...], dict[str, str | int]]] = [
        (
            ("cybersecurity", "threat response", "sky-net"),
            {
                "industry": "Cybersecurity",
                "size": 250,
                "intent": "Automate threat response operations",
            },
        ),
        (
            ("bakery", "baking", "firewall for our wifi"),
            {
                "industry": "Retail",
                "size": 5,
                "intent": "Basic firewall protection for small business",
            },
        ),
        (
            ("fintech", "regulated", "aws"),
            {
                "industry": "Fintech",
                "size": 75,
                "intent": "Scalable security platform for regulated startup",
            },
        ),
        (
            ("interested in pricing", "pricing inquiry", "ghost"),
            {
                "industry": "Other",
                "size": 0,
                "intent": "General pricing inquiry with no additional context",
            },
        ),
    ]

    def complete(self, system: str, user: str) -> str:
        return mock_llm_call(user)


class OpenAILLMClient:
    """Calls OpenAI with strict JSON schema output for enrichment."""

    _INDUSTRY_ENUM = ["Cybersecurity", "AI", "Fintech", "Retail", "Other"]
    _ENRICHMENT_SCHEMA = {
        "type": "object",
        "properties": {
            "industry": {
                "type": "string",
                "enum": _INDUSTRY_ENUM,
                "description": "Lead industry label",
            },
            "size": {
                "type": "integer",
                "minimum": 0,
                "description": "Estimated number of employees",
            },
            "intent": {
                "type": "string",
                "description": "Short sentence describing lead intent",
            },
        },
        "required": ["industry", "size", "intent"],
        "additionalProperties": False,
    }

    def __init__(self, api_key: str) -> None:
        if OpenAI is None:
            raise RuntimeError("openai package is not installed. Add 'openai' to dependencies.")
        self._client = OpenAI(api_key=api_key)

    def complete(self, system: str, user: str) -> str:
        response = self._client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=LLM_TEMPERATURE,
            top_p=LLM_TOP_P,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "lead_enrichment",
                    "strict": True,
                    "schema": self._ENRICHMENT_SCHEMA,
                },
            },
        )

        message = response.choices[0].message
        refusal = getattr(message, "refusal", None)
        if refusal:
            raise ValueError(f"OpenAI refusal: {refusal}")
        if not message.content:
            raise ValueError("OpenAI returned empty content.")
        return message.content


def mock_llm_call(raw_prompt: str) -> str:
    """
    Simulates API latency and returns deterministic JSON for known test leads.
    """
    time.sleep(0.1)

    normalized = raw_prompt.lower()
    for keywords, response in MockLLMClient._MOCK_PATTERNS:
        if any(keyword in normalized for keyword in keywords):
            return json.dumps(response)

    # Keep return as strict JSON to mirror a real JSON-mode response.
    return json.dumps({"industry": "Other", "size": 0, "intent": "Unknown"})


def build_llm_client() -> LLMClient:
    """
    Builds the active client:
    - OpenAI structured outputs when API_KEY exists.
    - Mock deterministic client otherwise.
    """
    if API_KEY.strip():
        if not LLM_MODEL:
            raise ValueError("LLM_MODEL must be set in .env when API_KEY is provided.")
        return OpenAILLMClient(api_key=API_KEY.strip())
    return MockLLMClient()


# Expose active LLM settings for visibility/debugging.
ACTIVE_LLM_SETTINGS: dict[str, str | float] = {
    "provider": "openai" if API_KEY.strip() else LLM_PROVIDER,
    "model": LLM_MODEL,
    "temperature": LLM_TEMPERATURE,
    "top_p": LLM_TOP_P,
    "response_format": LLM_RESPONSE_FORMAT,
}
