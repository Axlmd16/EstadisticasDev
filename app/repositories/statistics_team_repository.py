from .base_repository import BaseRepository
from app.models.statistic_team import StatisticTeam

class StatisticTeamRepository(BaseRepository):
    def __init__(self):
        super().__init__(StatisticTeam)
