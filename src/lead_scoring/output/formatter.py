from lead_scoring.config import CRM_ACTION_MARKETING, CRM_ACTION_SALES, SALES_ROUTE_THRESHOLD
from lead_scoring.models import EnrichedData, Lead, ScoredLead


def determine_crm_action(score: int) -> str:
    """Routes the lead based on its score relative to the sales threshold."""
    return CRM_ACTION_SALES if score > SALES_ROUTE_THRESHOLD else CRM_ACTION_MARKETING


def build_scored_lead(lead: Lead, enriched_data: EnrichedData, score: int) -> ScoredLead:
    """Assembles the final ScoredLead object ready for CRM ingestion."""
    return ScoredLead(
        id=lead.id,
        email=lead.email,
        enriched_data=enriched_data,
        score=score,
        crm_action=determine_crm_action(score),
    )
