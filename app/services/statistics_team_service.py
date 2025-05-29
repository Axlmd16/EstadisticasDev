import logging
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId

from app.repositories.statistics_team_repository import StatisticTeamRepository
from app.schemas.statistics_team_schema import (
    StatisticTeamCreate,
    StatisticTeamUpdate,
    StatisticTeamResponse,
)

logger = logging.getLogger(__name__)

class StatisticTeamService:
    def __init__(self):
        self.repo = StatisticTeamRepository()

    async def create_statistic_team(self, stat: StatisticTeamCreate) -> StatisticTeamResponse:
        try:
            stat_data = stat.model_dump(exclude_unset=True)

            if stat_data.get("id_team"):
                stat_data["id_team"] = ObjectId(stat_data["id_team"])

            doc = await self.repo.create(stat_data)
            return StatisticTeamResponse(
                id=str(doc.id),
                description=doc.description,
                date_generation=doc.date_generation,
                value=doc.value,
                games_played=doc.games_played,
                games_drawn=doc.games_drawn,
                matches_lost=doc.matches_lost,
                matches_won=doc.matches_won,
                points=doc.points,
                id_team=str(doc.id_team) if doc.id_team else None,
            )
        except Exception as e:
            logger.error(f"Error creating statistic team: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating statistic team: {str(e)}"
            )

    async def list_statistic_teams(self) -> list[StatisticTeamResponse]:
        try:
            stats = await self.repo.list()
            return [
                StatisticTeamResponse(
                    id=str(s.id),
                    description=s.description,
                    date_generation=s.date_generation,
                    value=s.value,
                    games_played=s.games_played,
                    games_drawn=s.games_drawn,
                    matches_lost=s.matches_lost,
                    matches_won=s.matches_won,
                    points=s.points,
                    id_team=str(s.id_team) if s.id_team else None,
                ) for s in stats
            ]
        except Exception as e:
            logger.error(f"Error listing statistic teams: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving statistic teams"
            )

    async def get_statistic_team(self, stat_id: PydanticObjectId) -> StatisticTeamResponse:
        stat = await self.repo.get_by_id(stat_id)
        if not stat:
            raise HTTPException(status_code=404, detail="StatisticTeam not found")
        return StatisticTeamResponse(
            id=str(stat.id),
            description=stat.description,
            date_generation=stat.date_generation,
            value=stat.value,
            games_played=stat.games_played,
            games_drawn=stat.games_drawn,
            matches_lost=stat.matches_lost,
            matches_won=stat.matches_won,
            points=stat.points,
            id_team=str(stat.id_team) if stat.id_team else None,
        )

    async def update_statistic_team(self, stat_id: PydanticObjectId, stat: StatisticTeamUpdate) -> StatisticTeamResponse:
        db_stat = await self.repo.get_by_id(stat_id)
        if not db_stat:
            raise HTTPException(status_code=404, detail="StatisticTeam not found")

        update_data = stat.model_dump(exclude_unset=True)

        if update_data.get("id_team"):
            update_data["id_team"] = ObjectId(update_data["id_team"])

        updated = await self.repo.update(stat_id, update_data)
        return StatisticTeamResponse(
            id=str(updated.id),
            description=updated.description,
            date_generation=updated.date_generation,
            value=updated.value,
            games_played=updated.games_played,
            games_drawn=updated.games_drawn,
            matches_lost=updated.matches_lost,
            matches_won=updated.matches_won,
            points=updated.points,
            id_team=str(updated.id_team) if updated.id_team else None,
        )

    async def delete_statistic_team(self, stat_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(stat_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="StatisticTeam not found")

statistic_team_service = StatisticTeamService()
