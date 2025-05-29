from .base_repository import BaseRepository
from app.models.statistic_individual import StatisticIndividual

class StatisticIndividualRepository(BaseRepository):
    def __init__(self):
        super().__init__(StatisticIndividual)
