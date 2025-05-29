from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from .catalog_item_schema import PyObjectId

# Schemas de posición en tabla

class PositionTableBase(BaseModel):
    position: Optional[int] = None
    points_total: Optional[int] = None
    table_rating_id: Optional[PyObjectId] = None
    team_id: Optional[PyObjectId] = None

class PositionTableCreate(PositionTableBase):
    pass

class PositionTableUpdate(PositionTableBase):
    pass

class PositionTableResponse(PositionTableBase):
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
