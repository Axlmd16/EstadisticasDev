from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId
from app.utils import PyObjectId

class BaseStatistic(Document):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    description: Optional[str]
    date_generation: Optional[str]
    type_statistic: Optional[PyObjectId]  # Referencia a CatalogItem
    value: Optional[float]

    class Settings:
        name = "statistics"

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
