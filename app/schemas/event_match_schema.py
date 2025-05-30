from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from datetime import datetime

class EventMatchBase(BaseModel):
    description: Optional[str] = None
    date_registration: Optional[datetime] = None
    minute: Optional[float] = None
    type_event: Optional[str] = None
    athlete_id: Optional[str] = None  

class EventMatchCreate(EventMatchBase):
    pass

class EventMatchUpdate(EventMatchBase):
    description: Optional[str] = None
    date_registration: Optional[datetime] = None
    minute: Optional[float] = None
    type_event: Optional[str] = None
    athlete_id: Optional[str] = None

class EventMatchResponse(EventMatchBase):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }
