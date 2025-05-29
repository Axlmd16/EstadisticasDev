from beanie import Document
from pydantic import Field
from typing import Optional

class CatalogItem(Document):
    code: str
    description: str
    category: str

    class Settings:
        name = "catalog_items"

    model_config = {
        "arbitrary_types_allowed": True,
    }
