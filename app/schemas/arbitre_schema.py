from pydantic import BaseModel, Field, field_validator
from typing import Optional

# Schemas de árbitro

class ArbitreBase(BaseModel):
    name: str
    license_number: Optional[str] = None

class ArbitreCreate(ArbitreBase):
    pass

class ArbitreUpdate(ArbitreBase):
    name: Optional[str] = None
    license_number: Optional[str] = None

class ArbitreResponse(ArbitreBase):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        return str(v) if v else None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }
