# app/models/match.py - VERSIÓN ACTUALIZADA
from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Match(Document):
    season_id: Optional[ObjectId] = None
    local_team_id: ObjectId 
    visitor_team_id: ObjectId  
    date: Optional[datetime] = None

    class Settings:
        name = "matches"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }