from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class AnalysisResponse(BaseModel):

    semantic_score: float

    ats_score: float

    matched_skills: list[str]

    missing_skills: list[str]

    ai_feedback: str