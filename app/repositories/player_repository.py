# Repositorio de jugadores

from .base_repository import BaseRepository
from app.models.athlete import Athlete

class PlayerRepository(BaseRepository):
    def __init__(self):
        super().__init__(Athlete)
