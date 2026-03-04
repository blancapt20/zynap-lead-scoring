import logging
from pathlib import Path

from lead_scoring.enrichment.agent import enrich_lead
from lead_scoring.enrichment.llm_client import LLMClient, build_llm_client
from lead_scoring.io import load_leads, resolve_data_path
from lead_scoring.output.formatter import build_scored_lead
from lead_scoring.scoring.engine import score_lead

logger = logging.getLogger(__name__)


def run_pipeline(data_path: Path | None = None, client: LLMClient | None = None) -> list[dict]:
    """
    Executes the full lead scoring flow and returns CRM-ready dictionaries.
    """
    llm_client = client or build_llm_client()
    leads = load_leads(resolve_data_path(data_path))
    results: list[dict] = []

    for lead in leads:
        logger.info("Processing lead %s (%s)", lead.id, lead.email)
        enriched = enrich_lead(lead, llm_client)
        score = score_lead(lead, enriched)
        scored_lead = build_scored_lead(lead, enriched, score)
        results.append(scored_lead.model_dump())

    return results
