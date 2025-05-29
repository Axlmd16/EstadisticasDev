from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from bson import ObjectId

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    founded: Optional[int] = None

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    name: Optional[str] = None  
    description: Optional[str] = None
    founded: Optional[int] = None

class TeamResponse(TeamBase):
    id: str = Field(alias="_id") 
    athletes: List[str] = Field(default_factory=list)

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v) if v else None

    @field_validator("athletes", mode="before")
    @classmethod
    def validate_athletes(cls, v):
        if isinstance(v, list):
            return [str(item) if isinstance(item, ObjectId) else str(item) for item in v]
        return []

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }