from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from app.utils import PyObjectId

# Schemas de eventos de partido

class EventMatchBase(BaseModel):
    description: Optional[str] = None
    date_registration: Optional[str] = None
    minute: Optional[int] = None
    type_event: Optional[PyObjectId] = None
    match_id: Optional[PyObjectId] = None
    athlete_id: Optional[PyObjectId] = None

class EventMatchCreate(EventMatchBase):
    pass

class EventMatchUpdate(EventMatchBase):
    pass

class EventMatchResponse(EventMatchBase):
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
