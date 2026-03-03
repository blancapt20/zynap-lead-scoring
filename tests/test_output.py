import pytest

from lead_scoring.models import EnrichedData, Lead, ScoredLead
from lead_scoring.output.formatter import build_scored_lead, determine_crm_action


@pytest.fixture
def sample_lead() -> Lead:
    return Lead(id="lead_001", email="sarah.connor@sky-net.org", raw_note="Automate threat response.")


@pytest.fixture
def sample_enriched() -> EnrichedData:
    return EnrichedData(industry="Cybersecurity", size=250, intent="Automate threat response")


# --- determine_crm_action ---

def test_high_score_routes_to_sales():
    assert determine_crm_action(85) == "PRIORITY_sales_route"


def test_score_at_threshold_routes_to_marketing():
    assert determine_crm_action(70) == "marketing_route"


def test_low_score_routes_to_marketing():
    assert determine_crm_action(30) == "marketing_route"


# --- build_scored_lead ---

def test_build_scored_lead_returns_correct_type(sample_lead, sample_enriched):
    result = build_scored_lead(sample_lead, sample_enriched, 85)
    assert isinstance(result, ScoredLead)


def test_build_scored_lead_preserves_fields(sample_lead, sample_enriched):
    result = build_scored_lead(sample_lead, sample_enriched, 85)
    assert result.id == "lead_001"
    assert result.email == "sarah.connor@sky-net.org"
    assert result.score == 85
    assert result.crm_action == "PRIORITY_sales_route"


def test_build_scored_lead_low_score(sample_lead, sample_enriched):
    result = build_scored_lead(sample_lead, sample_enriched, 30)
    assert result.crm_action == "marketing_route"
