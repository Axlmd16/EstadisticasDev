from bson import ObjectId
from typing import Optional
from app.models.base_statistic import BaseStatistic  # Herencia
from pydantic import Field

class StatisticIndividual(BaseStatistic):
    goal: Optional[int] = None
    own_goal: Optional[int] = None
    foul: Optional[int] = None
    red_card: Optional[int] = None
    yellow_card: Optional[int] = None
    athlete_id: Optional[ObjectId] = None

    class Settings:
        name = "statistic_individual"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
