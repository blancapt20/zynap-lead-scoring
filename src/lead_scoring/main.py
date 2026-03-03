import json
import logging

from lead_scoring.pipeline import run_pipeline

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Running with mock_llm_call() via MockLLMClient.")
    results = run_pipeline()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
