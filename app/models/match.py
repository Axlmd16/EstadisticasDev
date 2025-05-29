# app/models/match.py - VERSIÓN CORREGIDA
from beanie import Document
from pydantic import Field
from typing import Optional, List
from bson import ObjectId

class Match(Document):
    season_id: Optional[ObjectId] = None
    team_ids: List[ObjectId] = Field(default_factory=list)
    date: Optional[str] = None

    class Settings:
        name = "matches"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }