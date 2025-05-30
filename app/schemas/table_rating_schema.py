from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from bson import ObjectId

class TableRatingBase(BaseModel):
    last_update: Optional[str] = None
    competition_id: Optional[str] = None 
    positions: List[str] = Field(default_factory=list) 
class TableRatingCreate(TableRatingBase):
    pass

class TableRatingUpdate(TableRatingBase):
    last_update: Optional[str] = None
    competition_id: Optional[str] = None
    positions: Optional[List[str]] = None

class TableRatingResponse(TableRatingBase):
    id: str = Field(alias="_id")  

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("competition_id", mode="before")
    @classmethod
    def validate_competition_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("positions", mode="before")
    @classmethod
    def validate_positions(cls, v):
        if isinstance(v, list):
            return [str(item) if isinstance(item, ObjectId) else str(item) for item in v]
        return []

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }