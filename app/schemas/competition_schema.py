from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

# Schemas de competencia

class CompetitionBase(BaseModel):
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CompetitionCreate(CompetitionBase):
    pass

class CompetitionUpdate(CompetitionBase):
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CompetitionResponse(CompetitionBase):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        return str(v) if v else None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }
