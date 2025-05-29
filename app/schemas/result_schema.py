from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from .catalog_item_schema import PyObjectId

# Schemas de resultado

class ResultBase(BaseModel):
    date_registration: Optional[str] = None
    details: Optional[str] = None
    loser: Optional[str] = None
    score_local: Optional[int] = None
    score_visitor: Optional[int] = None
    status_result: Optional[PyObjectId] = None
    winner: Optional[str] = None
    match_id: Optional[PyObjectId] = None

class ResultCreate(ResultBase):
    pass

class ResultUpdate(ResultBase):
    pass

class ResultResponse(ResultBase):
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
