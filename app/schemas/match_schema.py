# app/schemas/match_schema.py - VERSIÓN CORREGIDA
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from bson import ObjectId

class MatchBase(BaseModel):
    season_id: Optional[str] = None 
    team_ids: List[str] = Field(default_factory=list)
    date: Optional[str] = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(MatchBase):
    season_id: Optional[str] = None
    team_ids: Optional[List[str]] = None
    date: Optional[str] = None

class MatchResponse(MatchBase):
    id: str = Field(alias="_id")  

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("season_id", mode="before")
    @classmethod
    def validate_season_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("team_ids", mode="before")
    @classmethod
    def validate_team_ids(cls, v):
        if isinstance(v, list):
            return [str(item) if isinstance(item, ObjectId) else str(item) for item in v]
        return []

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }