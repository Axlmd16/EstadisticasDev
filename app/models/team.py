# app/models/team.py - VERSIÓN CORREGIDA
from beanie import Document
from pydantic import Field
from typing import Optional, List
from bson import ObjectId

class Team(Document):
    name: str
    description: Optional[str] = None
    founded: Optional[int] = None
    athletes: List[ObjectId] = Field(default_factory=list)  

    class Settings:
        name = "teams"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }