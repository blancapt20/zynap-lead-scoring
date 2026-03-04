import os

from dotenv import load_dotenv

load_dotenv()

# --- LLM behaviour ---
LLM_MAX_RETRIES: int = 3
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock")
LLM_MODEL: str = os.getenv("LLM_MODEL", "").strip()
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))
LLM_TOP_P: float = float(os.getenv("LLM_TOP_P", "1.0"))
# Keep this explicit for JSON-output enforcement in real API clients.
LLM_RESPONSE_FORMAT: str = os.getenv("LLM_RESPONSE_FORMAT", "json_object")
API_KEY: str = os.getenv("API_KEY", "")

# --- Scoring: industry fit ---
# Maps industry label → points awarded
INDUSTRY_SCORES: dict[str, int] = {
    "Cybersecurity": 50,
    "AI": 50,
    "Fintech": 25,
}

# --- Scoring: size fit ---
HIGH_EMPLOYEE_THRESHOLD: int = 100   # > this → +25 pts
LOW_EMPLOYEE_THRESHOLD: int = 10     # > this and <= HIGH → +10 pts

SIZE_SCORE_HIGH: int = 25
SIZE_SCORE_MID: int = 10

# --- Scoring: content quality ---
CONTENT_QUALITY_SCORE: int = 10
VAGUE_NOTES: list[str] = [
    "interested in pricing",
    "pricing",
    "info",
    "information",
    "hello",
    "",
]

# --- CRM routing ---
SALES_ROUTE_THRESHOLD: int = 70
CRM_ACTION_SALES: str = "PRIORITY_sales_route"
CRM_ACTION_MARKETING: str = "marketing_route"
