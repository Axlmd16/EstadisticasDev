from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId

# Modelo de resultado
class Result(Document):
    date_registration: Optional[str] = None
    details: Optional[str] = None
    loser: Optional[str] = None
    score_local: Optional[int] = None
    score_visitor: Optional[int] = None
    status_result: Optional[ObjectId] = None
    winner: Optional[str] = None
    match_id: Optional[ObjectId] = None

    class Settings:
        name = "results"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
