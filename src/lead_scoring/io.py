import json
import os
from pathlib import Path

from lead_scoring.models import Lead

DEFAULT_RELATIVE_DATA_PATH = Path("data") / "leads.json"


def load_leads(path: Path) -> list[Lead]:
    """Loads and validates leads from a JSON file."""
    with open(path, encoding="utf-8") as file:
        raw = json.load(file)
    return [Lead(**item) for item in raw]


def resolve_data_path(data_path: Path | None = None) -> Path:
    """
    Resolves the input file path from explicit path, env var, or defaults.
    """
    candidates: list[Path] = []

    if data_path is not None:
        candidates.append(Path(data_path))

    env_value = os.environ.get("LEAD_SCORING_DATA_PATH")
    if env_value:
        candidates.append(Path(env_value))

    package_repo_root = Path(__file__).resolve().parents[2]
    candidates.append(package_repo_root / DEFAULT_RELATIVE_DATA_PATH)
    candidates.append(Path.cwd() / DEFAULT_RELATIVE_DATA_PATH)

    for candidate in candidates:
        if candidate.exists():
            return candidate

    tried = ", ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(
        f"Could not find leads input file. Tried: {tried}. "
        "Pass data_path to run_pipeline(...) or set LEAD_SCORING_DATA_PATH."
    )
