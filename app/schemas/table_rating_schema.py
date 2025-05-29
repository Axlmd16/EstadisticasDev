from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from bson import ObjectId
from .catalog_item_schema import PyObjectId

# Schemas de tabla de posiciones

class TableRatingBase(BaseModel):
    last_update: Optional[str] = None
    competition_id: Optional[PyObjectId] = None
    positions: Optional[List[PyObjectId]] = []

class TableRatingCreate(TableRatingBase):
    pass

class TableRatingUpdate(TableRatingBase):
    pass

class TableRatingResponse(TableRatingBase):
    id: Optional[str] = Field(None, alias="_id")
    positions: Optional[list[str]] = []

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, PyObjectId):
            return str(v)
        return v

    @field_validator("positions", mode="before")
    @classmethod
    def validate_positions(cls, v):
        if isinstance(v, list):
            return [str(i) if isinstance(i, (ObjectId, PyObjectId)) else i for i in v]
        return v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str, PyObjectId: str},
    }
