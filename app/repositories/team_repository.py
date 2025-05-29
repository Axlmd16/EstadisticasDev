# Repositorio de equipos

from .base_repository import BaseRepository
from app.models.team import Team

class TeamRepository(BaseRepository):
    def __init__(self):
        super().__init__(Team)
