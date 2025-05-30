# app/schemas/position_table_schema.py - VERSIÓN CORREGIDA
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

# Schemas de posición en tabla CORREGIDOS
class PositionTableBase(BaseModel):
    position: Optional[int] = None
    points_total: Optional[int] = None
    table_rating_id: Optional[str] = None 
    team_id: Optional[str] = None

class PositionTableCreate(PositionTableBase):
    pass

class PositionTableUpdate(PositionTableBase):
    position: Optional[int] = None
    points_total: Optional[int] = None
    table_rating_id: Optional[str] = None
    team_id: Optional[str] = None

class PositionTableResponse(PositionTableBase):
    id: str = Field(alias="_id")  

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("table_rating_id", mode="before")
    @classmethod
    def validate_table_rating_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("team_id", mode="before")
    @classmethod
    def validate_team_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }