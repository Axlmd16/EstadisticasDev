from .base_repository import BaseRepository
from app.models.position_table import PositionTable

class PositionTableRepository(BaseRepository):
    def __init__(self):
        super().__init__(PositionTable)
