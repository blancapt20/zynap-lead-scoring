import json
from pathlib import Path

from lead_scoring.models import Lead

DEFAULT_DATA_PATH = Path(__file__).parents[2] / "data" / "leads.json"


def load_leads(path: Path) -> list[Lead]:
    """Loads and validates leads from a JSON file."""
    with open(path, encoding="utf-8") as file:
        raw = json.load(file)
    return [Lead(**item) for item in raw]
