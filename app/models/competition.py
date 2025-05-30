# Modelo de competencia

from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class Competition(Document):
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Settings:
        name = "competitions"

    model_config = {
        "arbitrary_types_allowed": True,
    }
