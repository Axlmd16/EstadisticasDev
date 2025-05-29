from typing import Optional
from bson import ObjectId
from app.models.base_statistic import BaseStatistic

class StatisticCompetence(BaseStatistic):
    average_score: Optional[float] = None
    matches_completed: Optional[int] = None
    record_score: Optional[int] = None
    total_parties: Optional[int] = None
    id_competition: Optional[ObjectId] = None  # <-- agregado

    class Settings:
        name = "statistic_competence"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
