# Modelo de temporada

from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class Season(Document):
    name: str
    description: str
    startDate: datetime
    endDate: datetime

    class Settings:
        name = "seasons"

    model_config = {
        "arbitrary_types_allowed": True,
    }
