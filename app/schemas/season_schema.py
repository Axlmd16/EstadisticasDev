from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from .catalog_item_schema import PyObjectId

# Schemas de temporada

class SeasonBase(BaseModel):
    year: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class SeasonCreate(SeasonBase):
    pass

class SeasonUpdate(SeasonBase):
    pass

class SeasonResponse(SeasonBase):
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
