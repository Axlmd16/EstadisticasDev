from pydantic import BaseModel, Field, field_validator, ValidationError, root_validator
from typing import Optional
from bson import ObjectId

class StatisticIndividualBase(BaseModel):
    description: Optional[str] = None
    date_generation: Optional[str] = None
    value: Optional[float] = None
    fouls: Optional[int] = None
    games_played: Optional[int] = None
    points_scored: Optional[int] = None
    athlete_id: Optional[str] = None

class StatisticIndividualCreate(StatisticIndividualBase):
    pass

class StatisticIndividualUpdate(StatisticIndividualBase):
    description: Optional[str] = None
    date_generation: Optional[str] = None
    value: Optional[float] = None
    fouls: Optional[int] = None
    games_played: Optional[int] = None
    points_scored: Optional[int] = None
    athlete_id: Optional[str] = None

class StatisticIndividualResponse(StatisticIndividualBase):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        return str(v) if v else None

    @field_validator("athlete_id", mode="before")
    @classmethod
    def validate_athlete_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    @root_validator(pre=True)
    def check_fields(cls, values):
        for k, v in values.items():
            try:
                # Intentar validar tipos manualmente si querés
                pass
            except Exception as e:
                print(f"Error en campo '{k}': valor '{v}', error: {e}")
                raise e
        return values

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }
