from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId

class StatisticTeam(Document):
    games_played: Optional[int] = None
    games_drawn: Optional[int] = None
    matches_lost: Optional[int] = None
    matches_won: Optional[int] = None
    points: Optional[int] = None
    team_id: Optional[ObjectId] = None

    class Settings:
        name = "statistic_team"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
