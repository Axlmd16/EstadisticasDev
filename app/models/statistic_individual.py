from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId

# Modelo de estadística individual
class StatisticIndividual(Document):
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
