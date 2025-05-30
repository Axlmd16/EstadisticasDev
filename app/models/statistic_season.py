from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId
from app.models.base_statistic import BaseStatistic

class StatisticSeason(BaseStatistic):
    most_fouls: Optional[ObjectId] = None
    most_red_cards: Optional[ObjectId] = None
    most_yellow_cards: Optional[ObjectId] = None
    top_assistant: Optional[ObjectId] = None
    top_scorer: Optional[ObjectId] = None
    id_season: Optional[ObjectId] = None

    class Settings:
        name = "statistic_season"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
