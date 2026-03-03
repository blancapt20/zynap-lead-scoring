from lead_scoring.config import (
    CONTENT_QUALITY_SCORE,
    HIGH_EMPLOYEE_THRESHOLD,
    INDUSTRY_SCORES,
    LOW_EMPLOYEE_THRESHOLD,
    SIZE_SCORE_HIGH,
    SIZE_SCORE_MID,
    VAGUE_NOTES,
)
from lead_scoring.models import EnrichedData, Lead


def industry_fit(data: EnrichedData) -> int:
    """Awards points based on how well the lead's industry matches Zynap's ICP."""
    return INDUSTRY_SCORES.get(data.industry, 0)


def size_fit(data: EnrichedData) -> int:
    """Awards points based on the estimated company size."""
    if data.size > HIGH_EMPLOYEE_THRESHOLD:
        return SIZE_SCORE_HIGH
    if data.size > LOW_EMPLOYEE_THRESHOLD:
        return SIZE_SCORE_MID
    return 0


def content_quality(lead: Lead) -> int:
    """Awards points if the raw note contains meaningful intent beyond vague phrases."""
    normalized = lead.raw_note.strip().lower()
    if not normalized or normalized in VAGUE_NOTES:
        return 0
    return CONTENT_QUALITY_SCORE
