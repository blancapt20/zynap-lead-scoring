from pydantic import BaseModel, Field


class Lead(BaseModel):
    id: str
    email: str
    raw_note: str


class EnrichedData(BaseModel):
    industry: str = Field(description="One of: Cybersecurity, AI, Fintech, Retail, Other")
    size: int = Field(description="Estimated number of employees", ge=0)
    intent: str = Field(description="Brief summary of what the lead is looking for")


class ScoredLead(BaseModel):
    id: str
    email: str
    enriched_data: EnrichedData
    score: int = Field(ge=0, le=100)
    crm_action: str
