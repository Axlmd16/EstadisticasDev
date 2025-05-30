from .base_repository import BaseRepository
from app.models.statistics_competence import StatisticCompetence

class StatisticCompetenceRepository(BaseRepository):
    def __init__(self):
        super().__init__(StatisticCompetence)
