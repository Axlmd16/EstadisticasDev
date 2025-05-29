# Modelo de competencia

from beanie import Document
from pydantic import Field
from typing import Optional

class Competition(Document):
    name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    class Settings:
        name = "competitions"

    model_config = {
        "arbitrary_types_allowed": True,
    }
