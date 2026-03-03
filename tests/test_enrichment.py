import json
import pytest

from lead_scoring.enrichment.agent import enrich_lead
from lead_scoring.enrichment.llm_client import MockLLMClient
from lead_scoring.models import EnrichedData, Lead


@pytest.fixture
def mock_client() -> MockLLMClient:
    return MockLLMClient()


@pytest.fixture
def cybersecurity_lead() -> Lead:
    return Lead(
        id="lead_001",
        email="sarah.connor@sky-net.org",
        raw_note="We are a cybersecurity firm based in London with about 250 employees.",
    )


@pytest.fixture
def vague_lead() -> Lead:
    return Lead(id="lead_004", email="unknown@ghost.com", raw_note="Interested in pricing.")


def test_enrich_lead_returns_enriched_data(mock_client, cybersecurity_lead):
    result = enrich_lead(cybersecurity_lead, mock_client)
    assert isinstance(result, EnrichedData)


def test_enrich_lead_cybersecurity_industry(mock_client, cybersecurity_lead):
    result = enrich_lead(cybersecurity_lead, mock_client)
    assert result.industry == "Cybersecurity"


def test_enrich_lead_size_extracted(mock_client, cybersecurity_lead):
    result = enrich_lead(cybersecurity_lead, mock_client)
    assert result.size == 250


def test_enrich_lead_fallback_on_invalid_response():
    class BrokenClient:
        def complete(self, system: str, user: str) -> str:
            raise TimeoutError("LLM timed out")

    lead = Lead(id="lead_x", email="x@x.com", raw_note="Some note")
    result = enrich_lead(lead, BrokenClient())

    assert result.industry == "Other"
    assert result.size == 0


def test_enrich_lead_fallback_on_malformed_json():
    class BadJSONClient:
        def complete(self, system: str, user: str) -> str:
            return "this is not json at all"

    lead = Lead(id="lead_x", email="x@x.com", raw_note="Some note")
    result = enrich_lead(lead, BadJSONClient())

    assert isinstance(result, EnrichedData)
