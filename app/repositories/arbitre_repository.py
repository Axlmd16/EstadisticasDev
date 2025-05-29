from .base_repository import BaseRepository
from app.models.arbitre import Arbitre

class ArbitreRepository(BaseRepository):
    def __init__(self):
        super().__init__(Arbitre)
