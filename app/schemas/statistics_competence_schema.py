from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from datetime import datetime

class StatisticCompetenceBase(BaseModel):
    description: Optional[str] = None
    date_generation: Optional[datetime] = None
    value: Optional[float] = None
    average_score: Optional[float] = None
    matches_completed: Optional[int] = None
    record_score: Optional[int] = None
    total_parties: Optional[int] = None
    id_competition: Optional[str] = None  # <-- agregado

class StatisticCompetenceCreate(StatisticCompetenceBase):
    pass

class StatisticCompetenceUpdate(StatisticCompetenceBase):
    pass

class StatisticCompetenceResponse(StatisticCompetenceBase):
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
