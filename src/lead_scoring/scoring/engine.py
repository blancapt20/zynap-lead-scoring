from lead_scoring.models import EnrichedData, Lead
from lead_scoring.scoring.rules import content_quality, industry_fit, size_fit

# Registry of scoring rules — add new rules here without touching other files
_RULES = [
    lambda lead, data: industry_fit(data),
    lambda lead, data: size_fit(data),
    lambda lead, data: content_quality(lead),
]


def score_lead(lead: Lead, data: EnrichedData) -> int:
    """
    Applies all scoring rules and returns a clamped total score (0–100).
    To add a new rule: implement a function in rules.py and register it in _RULES.
    """
    total = sum(rule(lead, data) for rule in _RULES)
    return max(0, min(100, total))
