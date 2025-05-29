from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from .catalog_item_schema import PyObjectId

# Schemas de marcador

class ScoreboardBase(BaseModel):
    last_update: Optional[str] = None
    status_game: Optional[PyObjectId] = None
    score_local: Optional[int] = None
    score_visitor: Optional[int] = None
    time_restant: Optional[int] = None
    match_id: Optional[PyObjectId] = None

class ScoreboardCreate(ScoreboardBase):
    pass

class ScoreboardUpdate(ScoreboardBase):
    pass

class ScoreboardResponse(ScoreboardBase):
    id: Optional[str] = Field(None, alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, PyObjectId):
            return str(v)
        return v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str, PyObjectId: str},
    }
