# app/models/table_rating.py - VERSIÓN CORREGIDA
from beanie import Document
from pydantic import Field
from typing import Optional, List
from bson import ObjectId

class TableRating(Document):
    last_update: Optional[str] = None
    competition_id: Optional[ObjectId] = None
    positions: List[ObjectId] = Field(default_factory=list)

    class Settings:
        name = "table_ratings"

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }

    async def delete(self, *args, **kwargs):
        """Elimina las posiciones asociadas cuando se elimina la tabla"""
        from app.models.position_table import PositionTable
        
        for pos_id in self.positions:
            try:
                pos = await PositionTable.get(pos_id)
                if pos:
                    await pos.delete()
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error deleting position {pos_id}: {str(e)}")
        
        return await super().delete(*args, **kwargs)