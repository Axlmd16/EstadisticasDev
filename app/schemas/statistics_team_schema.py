from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from datetime import datetime

class StatisticTeamBase(BaseModel):
    description: Optional[str] = None
    date_generation: Optional[datetime] = None
    value: Optional[float] = None
    games_played: Optional[int] = None
    matches_drawn: Optional[int] = None  #
    matches_lost: Optional[int] = None
    matches_won: Optional[int] = None
    points: Optional[int] = None
    id_team: Optional[str] = None  

class StatisticTeamCreate(StatisticTeamBase):
    pass

class StatisticTeamUpdate(StatisticTeamBase):
    description: Optional[str] = None
    date_generation: Optional[datetime] = None
    value: Optional[float] = None
    games_played: Optional[int] = None
    matches_drawn: Optional[int] = None
    matches_lost: Optional[int] = None
    matches_won: Optional[int] = None
    points: Optional[int] = None
    id_team: Optional[str] = None

class StatisticTeamResponse(StatisticTeamBase):
    id: str = Field(alias="_id") 

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("id_team", mode="before")
    @classmethod
    def validate_id_team(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }