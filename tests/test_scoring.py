import pytest

from lead_scoring.models import EnrichedData, Lead
from lead_scoring.scoring.engine import score_lead
from lead_scoring.scoring.rules import content_quality, industry_fit, size_fit


# --- industry_fit ---

def test_industry_fit_cybersecurity():
    data = EnrichedData(industry="Cybersecurity", size=0, intent="x")
    assert industry_fit(data) == 50


def test_industry_fit_ai():
    data = EnrichedData(industry="AI", size=0, intent="x")
    assert industry_fit(data) == 50


def test_industry_fit_fintech():
    data = EnrichedData(industry="Fintech", size=0, intent="x")
    assert industry_fit(data) == 25


def test_industry_fit_other():
    data = EnrichedData(industry="Retail", size=0, intent="x")
    assert industry_fit(data) == 0


# --- size_fit ---

def test_size_fit_large_company():
    data = EnrichedData(industry="Other", size=250, intent="x")
    assert size_fit(data) == 25


def test_size_fit_mid_company():
    data = EnrichedData(industry="Other", size=75, intent="x")
    assert size_fit(data) == 10


def test_size_fit_small_company():
    data = EnrichedData(industry="Other", size=5, intent="x")
    assert size_fit(data) == 0


# --- content_quality ---

def test_content_quality_meaningful_note():
    lead = Lead(id="x", email="x@x.com", raw_note="We are looking to automate threat response.")
    assert content_quality(lead) == 10


def test_content_quality_vague_note():
    lead = Lead(id="x", email="x@x.com", raw_note="Interested in pricing")
    assert content_quality(lead) == 0


def test_content_quality_empty_note():
    lead = Lead(id="x", email="x@x.com", raw_note="")
    assert content_quality(lead) == 0


# --- engine ---

def test_score_lead_high_fit():
    lead = Lead(id="lead_001", email="a@b.com", raw_note="Automating security ops for our 300 person team.")
    data = EnrichedData(industry="Cybersecurity", size=300, intent="Automate security ops")
    score = score_lead(lead, data)
    assert score == 85  # 50 + 25 + 10


def test_score_lead_low_fit():
    lead = Lead(id="lead_002", email="a@b.com", raw_note="Interested in pricing")
    data = EnrichedData(industry="Retail", size=5, intent="Basic firewall")
    score = score_lead(lead, data)
    assert score == 0  # 0 + 0 + 0


def test_score_lead_clamped_to_100():
    lead = Lead(id="lead_x", email="a@b.com", raw_note="Very detailed note about complex needs.")
    data = EnrichedData(industry="Cybersecurity", size=500, intent="x")
    score = score_lead(lead, data)
    assert score <= 100
