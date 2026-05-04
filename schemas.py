from pydantic import BaseModel
from typing import List, Optional

class JobRecommendation(BaseModel):
    job_title: str
    company: str
    match_score: float

class AnalysisResponse(BaseModel):
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    recommended_jobs: List[JobRecommendation]
    ats_score: float
    ats_feedback: List[str]
    action_verbs: List[str]
    quality_feedback: List[str]

class JobDescriptionInput(BaseModel):
    text: str
