from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

class StatisticSeasonBase(BaseModel):
    description: Optional[str] = None
    date_generation: Optional[str] = None
    value: Optional[float] = None
    most_fouls: Optional[str] = None
    most_red_cards: Optional[str] = None
    most_yellow_cards: Optional[str] = None
    top_assistant: Optional[str] = None
    top_scorer: Optional[str] = None
    id_season: Optional[str] = None

class StatisticSeasonCreate(StatisticSeasonBase):
    pass

class StatisticSeasonUpdate(StatisticSeasonBase):
    pass

class StatisticSeasonResponse(StatisticSeasonBase):
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
