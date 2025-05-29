# Modelo de temporada

from beanie import Document
from pydantic import Field
from typing import Optional

class Season(Document):
    name: str
    description: str
    startDate: str  # Considera usar datetime si tu app ya lo soporta
    endDate: str    # Considera usar datetime si tu app ya lo soporta

    class Settings:
        name = "seasons"

    model_config = {
        "arbitrary_types_allowed": True,
    }
