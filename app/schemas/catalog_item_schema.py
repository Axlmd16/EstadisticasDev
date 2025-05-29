from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from app.utils import PyObjectId

class CatalogItemBase(BaseModel):
    code: str
    description: str
    category: str

class CatalogItemCreate(CatalogItemBase):
    pass

class CatalogItemUpdate(CatalogItemBase):
    code: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class CatalogItemResponse(CatalogItemBase):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        return str(v) if v else None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }
