import json
import logging
import time

from pydantic import ValidationError

from lead_scoring.config import LLM_MAX_RETRIES
from lead_scoring.models import EnrichedData, Lead
from lead_scoring.enrichment.llm_client import LLMClient
from lead_scoring.enrichment.prompts import ENRICHMENT_SYSTEM_PROMPT, ENRICHMENT_USER_PROMPT

logger = logging.getLogger(__name__)

_FALLBACK_ENRICHMENT = EnrichedData(industry="Other", size=0, intent="Could not enrich lead")


def enrich_lead(lead: Lead, client: LLMClient) -> EnrichedData:
    """
    Calls the LLM to extract structured enrichment data from a raw lead note.
    Retries up to LLM_MAX_RETRIES times on failure, then returns a safe fallback.
    """
    user_prompt = ENRICHMENT_USER_PROMPT.format(raw_note=lead.raw_note)

    for attempt in range(1, LLM_MAX_RETRIES + 1):
        try:
            raw_response = client.complete(system=ENRICHMENT_SYSTEM_PROMPT, user=user_prompt)
            return _parse_response(raw_response)

        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning("Lead %s — attempt %d: invalid LLM response: %s", lead.id, attempt, e)

        except Exception as e:
            logger.warning("Lead %s — attempt %d: LLM call failed: %s", lead.id, attempt, e)

        if attempt < LLM_MAX_RETRIES:
            time.sleep(0.5 * attempt)  # simple back-off

    logger.error("Lead %s — all retries exhausted, using fallback enrichment.", lead.id)
    return _FALLBACK_ENRICHMENT


def _parse_response(raw: str) -> EnrichedData:
    """Parses and validates the raw LLM string into an EnrichedData model."""
    data = json.loads(raw.strip())
    return EnrichedData(**data)
