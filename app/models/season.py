# Modelo de temporada

from beanie import Document
from pydantic import Field
from typing import Optional

class Season(Document):
    year: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    class Settings:
        name = "seasons"

    model_config = {
        "arbitrary_types_allowed": True,
    }
