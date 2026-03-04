import json
import logging

from lead_scoring.enrichment.llm_client import ACTIVE_LLM_SETTINGS
from lead_scoring.pipeline import run_pipeline

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(
        "Running enrichment with provider=%s model=%s",
        ACTIVE_LLM_SETTINGS["provider"],
        ACTIVE_LLM_SETTINGS["model"],
    )
    results = run_pipeline()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
