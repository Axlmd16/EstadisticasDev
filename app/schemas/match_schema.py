from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from bson import ObjectId
from .catalog_item_schema import PyObjectId

# Schemas de partido

class MatchBase(BaseModel):
    competition_id: Optional[PyObjectId] = None
    season_id: Optional[PyObjectId] = None
    scoreboard_id: Optional[PyObjectId] = None
    result_id: Optional[PyObjectId] = None
    event_match_ids: Optional[List[PyObjectId]] = []
    arbitre_id: Optional[PyObjectId] = None
    team_ids: Optional[List[PyObjectId]] = []
    date: Optional[str] = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id: Optional[str] = Field(None, alias="_id")
    event_match_ids: Optional[list[str]] = []
    team_ids: Optional[list[str]] = []

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, PyObjectId):
            return str(v)
        return v

    @field_validator("event_match_ids", mode="before")
    @classmethod
    def validate_event_match_ids(cls, v):
        if isinstance(v, list):
            return [str(i) if isinstance(i, (ObjectId, PyObjectId)) else i for i in v]
        return v

    @field_validator("team_ids", mode="before")
    @classmethod
    def validate_team_ids(cls, v):
        if isinstance(v, list):
            return [str(i) if isinstance(i, (ObjectId, PyObjectId)) else i for i in v]
        return v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str, PyObjectId: str},
    }
