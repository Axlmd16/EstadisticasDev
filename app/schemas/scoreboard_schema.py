# app/schemas/scoreboard_schema.py - VERSIÓN CORREGIDA
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

class ScoreboardBase(BaseModel):
    status_game: Optional[str] = None  
    score_local: Optional[int] = None
    score_visitor: Optional[int] = None
    time_restant: Optional[int] = None
    match_id: Optional[str] = None  

class ScoreboardCreate(ScoreboardBase):
    pass

class ScoreboardUpdate(ScoreboardBase):
    pass

class ScoreboardResponse(ScoreboardBase):
    id: str = Field(alias="_id")  

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("status_game", mode="before")
    @classmethod
    def validate_status_game(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("match_id", mode="before")
    @classmethod
    def validate_match_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }