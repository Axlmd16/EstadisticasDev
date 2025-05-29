# Servicio de estadísticas

from app.repositories.statistics_repository import StatisticsRepository
from app.models.statistic_competence import StatisticCompetence
from app.models.statistic_individual import StatisticIndividual
from app.models.statistic_team import StatisticTeam
from app.models.statistic_season import StatisticSeason
from app.schemas.statistic_schemas import (
    StatisticCompetenceCreate, StatisticCompetenceUpdate, StatisticCompetenceResponse,
    StatisticIndividualCreate, StatisticIndividualUpdate, StatisticIndividualResponse,
    StatisticTeamCreate, StatisticTeamUpdate, StatisticTeamResponse,
    StatisticSeasonCreate, StatisticSeasonUpdate, StatisticSeasonResponse
)
from beanie import PydanticObjectId
from fastapi import HTTPException

class StatisticsService:
    def __init__(self):
        self.competence_repo = StatisticsRepository(StatisticCompetence)
        self.individual_repo = StatisticsRepository(StatisticIndividual)
        self.team_repo = StatisticsRepository(StatisticTeam)
        self.season_repo = StatisticsRepository(StatisticSeason)

    # Métodos para StatisticCompetence
    async def create_statistic_competence(self, stat: StatisticCompetenceCreate) -> StatisticCompetenceResponse:
        doc = await self.competence_repo.create(stat.dict())
        return StatisticCompetenceResponse(**doc.dict())
    async def list_statistics_competence(self) -> list[StatisticCompetenceResponse]:
        stats = await self.competence_repo.list()
        return [StatisticCompetenceResponse(**s.dict()) for s in stats]
    async def get_statistic_competence(self, stat_id: PydanticObjectId) -> StatisticCompetenceResponse:
        stat = await self.competence_repo.get_by_id(stat_id)
        if not stat:
            raise HTTPException(status_code=404, detail="StatisticCompetence not found")
        return StatisticCompetenceResponse(**stat.dict())
    async def update_statistic_competence(self, stat_id: PydanticObjectId, stat: StatisticCompetenceUpdate) -> StatisticCompetenceResponse:
        db_stat = await self.competence_repo.get_by_id(stat_id)
        if not db_stat:
            raise HTTPException(status_code=404, detail="StatisticCompetence not found")
        updated = await self.competence_repo.update(stat_id, stat.dict(exclude_unset=True))
        return StatisticCompetenceResponse(**updated.dict())
    async def delete_statistic_competence(self, stat_id: PydanticObjectId) -> None:
        deleted = await self.competence_repo.delete(stat_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="StatisticCompetence not found")

    # Métodos para StatisticIndividual
    async def create_statistic_individual(self, stat: StatisticIndividualCreate) -> StatisticIndividualResponse:
        doc = await self.individual_repo.create(stat.dict())
        return StatisticIndividualResponse(**doc.dict())
    async def list_statistics_individual(self) -> list[StatisticIndividualResponse]:
        stats = await self.individual_repo.list()
        return [StatisticIndividualResponse(**s.dict()) for s in stats]
    async def get_statistic_individual(self, stat_id: PydanticObjectId) -> StatisticIndividualResponse:
        stat = await self.individual_repo.get_by_id(stat_id)
        if not stat:
            raise HTTPException(status_code=404, detail="StatisticIndividual not found")
        return StatisticIndividualResponse(**stat.dict())
    async def update_statistic_individual(self, stat_id: PydanticObjectId, stat: StatisticIndividualUpdate) -> StatisticIndividualResponse:
        db_stat = await self.individual_repo.get_by_id(stat_id)
        if not db_stat:
            raise HTTPException(status_code=404, detail="StatisticIndividual not found")
        updated = await self.individual_repo.update(stat_id, stat.dict(exclude_unset=True))
        return StatisticIndividualResponse(**updated.dict())
    async def delete_statistic_individual(self, stat_id: PydanticObjectId) -> None:
        deleted = await self.individual_repo.delete(stat_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="StatisticIndividual not found")

    # Métodos para StatisticTeam
    async def create_statistic_team(self, stat: StatisticTeamCreate) -> StatisticTeamResponse:
        doc = await self.team_repo.create(stat.dict())
        return StatisticTeamResponse(**doc.dict())
    async def list_statistics_team(self) -> list[StatisticTeamResponse]:
        stats = await self.team_repo.list()
        return [StatisticTeamResponse(**s.dict()) for s in stats]
    async def get_statistic_team(self, stat_id: PydanticObjectId) -> StatisticTeamResponse:
        stat = await self.team_repo.get_by_id(stat_id)
        if not stat:
            raise HTTPException(status_code=404, detail="StatisticTeam not found")
        return StatisticTeamResponse(**stat.dict())
    async def update_statistic_team(self, stat_id: PydanticObjectId, stat: StatisticTeamUpdate) -> StatisticTeamResponse:
        db_stat = await self.team_repo.get_by_id(stat_id)
        if not db_stat:
            raise HTTPException(status_code=404, detail="StatisticTeam not found")
        updated = await self.team_repo.update(stat_id, stat.dict(exclude_unset=True))
        return StatisticTeamResponse(**updated.dict())
    async def delete_statistic_team(self, stat_id: PydanticObjectId) -> None:
        deleted = await self.team_repo.delete(stat_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="StatisticTeam not found")

    # Métodos para StatisticSeason
    async def create_statistic_season(self, stat: StatisticSeasonCreate) -> StatisticSeasonResponse:
        doc = await self.season_repo.create(stat.dict())
        return StatisticSeasonResponse(**doc.dict())
    async def list_statistics_season(self) -> list[StatisticSeasonResponse]:
        stats = await self.season_repo.list()
        return [StatisticSeasonResponse(**s.dict()) for s in stats]
    async def get_statistic_season(self, stat_id: PydanticObjectId) -> StatisticSeasonResponse:
        stat = await self.season_repo.get_by_id(stat_id)
        if not stat:
            raise HTTPException(status_code=404, detail="StatisticSeason not found")
        return StatisticSeasonResponse(**stat.dict())
    async def update_statistic_season(self, stat_id: PydanticObjectId, stat: StatisticSeasonUpdate) -> StatisticSeasonResponse:
        db_stat = await self.season_repo.get_by_id(stat_id)
        if not db_stat:
            raise HTTPException(status_code=404, detail="StatisticSeason not found")
        updated = await self.season_repo.update(stat_id, stat.dict(exclude_unset=True))
        return StatisticSeasonResponse(**updated.dict())
    async def delete_statistic_season(self, stat_id: PydanticObjectId) -> None:
        deleted = await self.season_repo.delete(stat_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="StatisticSeason not found")

statistics_service = StatisticsService()
