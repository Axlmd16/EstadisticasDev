# app/schemas/match_schema.py - VERSIÓN CORREGIDA
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

class MatchBase(BaseModel):
    season_id: Optional[str] = None
    local_team_id: str
    visitor_team_id: str
    date: Optional[datetime] = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(MatchBase):
    season_id: Optional[str] = None
    local_team_id: Optional[str] = None
    visitor_team_id: Optional[str] = None
    date: Optional[datetime] = None

class MatchResponse(MatchBase):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None
      
    @field_validator("season_id", "local_team_id", "visitor_team_id", mode="before")
    @classmethod
    def validate_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }