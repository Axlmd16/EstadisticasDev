# Modelo de evento de partido

from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId

class EventMatch(Document):
    description: Optional[str] = None
    date_registration: Optional[str] = None
    minute: Optional[int] = None
    type_event: Optional[ObjectId] = None
    match_id: Optional[ObjectId] = None
    athlete_id: Optional[ObjectId] = None

    class Settings:
        name = "event_match"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
