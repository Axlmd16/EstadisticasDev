from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

# Modelo de resultado
class Result(Document):
    date_registration: Optional[datetime] = None
    details: Optional[str] = None
    loser: Optional[str] = None
    score_local: Optional[int] = None
    score_visitor: Optional[int] = None
    winner: Optional[str] = None
    scoreboard_id: Optional[ObjectId] = None

    class Settings:
        name = "results"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
