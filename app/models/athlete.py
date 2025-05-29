from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId

# Modelo de atleta
class Athlete(Document):
    name: str
    position: Optional[str] = None
    team_id: Optional[ObjectId] = None

    class Settings:
        name = "athletes"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
