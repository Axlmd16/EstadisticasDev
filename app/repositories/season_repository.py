from .base_repository import BaseRepository
from app.models.season import Season

class SeasonRepository(BaseRepository):
    def __init__(self):
        super().__init__(Season)
