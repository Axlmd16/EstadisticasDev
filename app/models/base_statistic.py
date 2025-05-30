from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId
from app.utils import PyObjectId
from datetime import datetime

class BaseStatistic(Document):
    description: Optional[str]
    date_generation: Optional[datetime]
    value: Optional[float]

    class Settings:
        name = "statistics"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
