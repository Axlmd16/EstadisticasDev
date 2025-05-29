from bson import ObjectId
from typing import Optional
from app.models.base_statistic import BaseStatistic  # Herencia
from pydantic import Field

class StatisticIndividual(BaseStatistic):
    fouls: Optional[int] = None
    games_played: Optional[int] = None
    points_scored: Optional[int] = None
    athlete_id: Optional[ObjectId] = None

    class Settings:
        name = "statistic_individual"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
