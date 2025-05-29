from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId

class StatisticCompetence(Document):
    average_score: Optional[float] = None
    matches_completed: Optional[int] = None
    record_score: Optional[int] = None
    total_parties: Optional[int] = None
    competition_id: Optional[ObjectId] = None

    class Settings:
        name = "statistic_competence"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
