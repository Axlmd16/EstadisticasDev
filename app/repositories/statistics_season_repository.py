from .base_repository import BaseRepository
from app.models.statistic_season import StatisticSeason

class StatisticSeasonRepository(BaseRepository):
    def __init__(self):
        super().__init__(StatisticSeason)
