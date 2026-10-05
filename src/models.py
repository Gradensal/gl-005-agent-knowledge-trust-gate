from enum import StrEnum

from pydantic import BaseModel, Field


class TrustDecision(StrEnum):
    USE = "USE"
    VERIFY = "VERIFY"
    REJECT = "REJECT"


class Consequence(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class KnowledgeItem(BaseModel):
    knowledge_id: str = Field(min_length=1)
    statement: str = Field(min_length=5)
    source: str = Field(min_length=1)

    provenance: float = Field(ge=0.0, le=1.0)
    recency: float = Field(ge=0.0, le=1.0)
    expertise: float = Field(ge=0.0, le=1.0)
    corroboration: float = Field(ge=0.0, le=1.0)

    human_validation: bool = False
    conflict_detected: bool = False


class TrustResult(BaseModel):
    decision: TrustDecision
    score: float
    threshold: float
    reason: str


class TrustScenario(BaseModel):
    scenario_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    knowledge: KnowledgeItem


class ExperimentRecord(BaseModel):
    timestamp_utc: str
    scenario_id: str
    knowledge_id: str
    consequence: Consequence
    decision: TrustDecision
    score: float
    threshold: float
    reason: str