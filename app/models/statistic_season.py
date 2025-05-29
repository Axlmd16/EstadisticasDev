from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId

class StatisticSeason(Document):
    most_fouls: Optional[ObjectId] = None
    most_red_cards: Optional[ObjectId] = None
    most_yellow_cards: Optional[ObjectId] = None
    top_assistant: Optional[ObjectId] = None
    top_scorer: Optional[ObjectId] = None
    season_id: Optional[ObjectId] = None

    class Settings:
        name = "statistic_season"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
