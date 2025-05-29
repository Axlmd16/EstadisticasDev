from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId
from app.models.base_statistic import BaseStatistic

class StatisticTeam(BaseStatistic):
    games_played: Optional[int] = None
    games_drawn: Optional[int] = None
    matches_lost: Optional[int] = None
    matches_won: Optional[int] = None
    points: Optional[int] = None
    id_team: Optional[ObjectId] = None

    class Settings:
        name = "statistic_team"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
