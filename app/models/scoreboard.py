from beanie import Document
from pydantic import Field
from typing import Optional
from bson import ObjectId

# Modelo Scoreboard con id de MongoDB y relación a Match.
class Scoreboard(Document):
    last_update: Optional[str] = None
    status_game: Optional[ObjectId] = None
    score_local: Optional[int] = None
    score_visitor: Optional[int] = None
    time_restant: Optional[int] = None
    arbitre_id: Optional[ObjectId] = None
    match_id: Optional[ObjectId] = None

    class Settings:
        name = "scoreboards"
        use_revision = True
        validate_on_save = True

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
