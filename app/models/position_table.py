from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId

# Modelo de posición en tabla
class PositionTable(Document):
    position: Optional[int] = None
    points_total: Optional[int] = None
    table_rating_id: Optional[ObjectId] = None
    team_id: Optional[ObjectId] = None

    class Settings:
        name = "position_tables"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
