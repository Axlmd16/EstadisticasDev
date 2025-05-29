from .base_repository import BaseRepository
from app.models.scoreboard import Scoreboard

class ScoreboardRepository(BaseRepository):
    def __init__(self):
        super().__init__(Scoreboard)
