from beanie import Document
from pydantic import Field
from typing import Optional, List
from bson import ObjectId

# Modelo de tabla de posiciones
class TableRating(Document):
    last_update: Optional[str] = None
    competition_id: Optional[ObjectId] = None
    positions: List[ObjectId] = Field(default_factory=list)

    class Settings:
        name = "table_ratings"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
