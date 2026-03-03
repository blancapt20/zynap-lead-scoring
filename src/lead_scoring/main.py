import json
import logging
import sys
from pathlib import Path

from lead_scoring.enrichment.agent import enrich_lead
from lead_scoring.enrichment.llm_client import MockLLMClient, OpenAIClient
from lead_scoring.config import OPENAI_API_KEY
from lead_scoring.models import Lead
from lead_scoring.output.formatter import build_scored_lead
from lead_scoring.scoring.engine import score_lead

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parents[3] / "data" / "leads.json"


def load_leads(path: Path) -> list[Lead]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return [Lead(**item) for item in raw]


def run_pipeline(use_mock: bool = False) -> list[dict]:
    client = MockLLMClient() if use_mock else OpenAIClient()
    leads = load_leads(DATA_PATH)
    results = []

    for lead in leads:
        logger.info("Processing lead %s (%s)", lead.id, lead.email)

        enriched = enrich_lead(lead, client)
        score = score_lead(lead, enriched)
        scored_lead = build_scored_lead(lead, enriched, score)

        results.append(scored_lead.model_dump())

    return results


def main() -> None:
    use_mock = not bool(OPENAI_API_KEY)
    if use_mock:
        logger.info("No OPENAI_API_KEY found — running with MockLLMClient.")

    results = run_pipeline(use_mock=use_mock)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
