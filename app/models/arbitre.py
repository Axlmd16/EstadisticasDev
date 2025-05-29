# Modelo de árbitro

from beanie import Document
from pydantic import Field
from typing import Optional

class Arbitre(Document):
    name: str
    license_number: Optional[str] = None

    class Settings:
        name = "arbitres"

    model_config = {
        "arbitrary_types_allowed": True,
    }
