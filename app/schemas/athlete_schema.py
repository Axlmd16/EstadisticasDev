from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

# Schemas de atleta

class AthleteBase(BaseModel):
    name: str
    position: Optional[str] = None
    team_id: Optional[str] = None

class AthleteCreate(AthleteBase):
    pass

class AthleteUpdate(AthleteBase):
    name: Optional[str] = None
    position: Optional[str] = None
    team_id: Optional[str] = None

class AthleteResponse(AthleteBase):
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
