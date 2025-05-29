# Repositorio de partidos

from .base_repository import BaseRepository
from app.models.match import Match

class MatchRepository(BaseRepository):
    def __init__(self):
        super().__init__(Match)
