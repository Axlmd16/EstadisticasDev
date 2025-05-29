# Repositorio de estadísticas

from .base_repository import BaseRepository
from app.models.statistic_competence import StatisticCompetence
from app.models.statistic_individual import StatisticIndividual
from app.models.statistic_team import StatisticTeam
from app.models.statistic_season import StatisticSeason

class StatisticsRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)

# Ejemplo de uso:
# repo = StatisticsRepository(StatisticCompetence)
# repo = StatisticsRepository(StatisticIndividual)
# repo = StatisticsRepository(StatisticTeam)
# repo = StatisticsRepository(StatisticSeason)
