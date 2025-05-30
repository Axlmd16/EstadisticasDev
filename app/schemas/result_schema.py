from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from datetime import datetime

class ResultBase(BaseModel):
    date_registration: Optional[datetime] = None
    details: Optional[str] = None
    loser: Optional[str] = None
    score_local: Optional[int] = None
    score_visitor: Optional[int] = None
    winner: Optional[str] = None
    scoreboard_id: Optional[str] = None  # ✅ String en schema

class ResultCreate(ResultBase):
    pass

class ResultUpdate(ResultBase):
    # ✅ Todos opcionales para updates
    pass

class ResultResponse(ResultBase):
    id: str = Field(alias="_id")  # ✅ Requerido, sin Optional

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("scoreboard_id", mode="before")
    @classmethod
    def validate_scoreboard_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }