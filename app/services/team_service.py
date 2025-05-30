# app/services/team_service.py - VERSIÓN CORREGIDA
from app.repositories.team_repository import TeamRepository
from app.schemas.team_schema import TeamCreate, TeamUpdate, TeamResponse
from beanie import PydanticObjectId
from fastapi import HTTPException, status
import logging
from app.services.statistics_team_service import statistic_team_service
from app.schemas.statistics_team_schema import StatisticTeamCreate

logger = logging.getLogger(__name__)

class TeamService:
    def __init__(self):
        self.repo = TeamRepository()

    async def create_team(self, team: TeamCreate) -> TeamResponse:
        try:
            team_data = team.model_dump(exclude_unset=True)
            doc = await self.repo.create(team_data)
            # Crear estadística de equipo automáticamente
            await statistic_team_service.create_statistic_team(
                StatisticTeamCreate(id_team=str(doc.id))
            )
            return TeamResponse(
                id=str(doc.id),
                name=doc.name,
                description=doc.description,
                founded=doc.founded,
                athletes=[str(athlete_id) for athlete_id in doc.athletes]
            )
        except Exception as e:
            logger.error(f"Error creating team: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating team: {str(e)}"
            )

    async def list_teams(self) -> list[TeamResponse]:
        try:
            teams = await self.repo.list()
            return [
                TeamResponse(
                    id=str(team.id),
                    name=team.name,
                    description=team.description,
                    founded=team.founded,
                    athletes=[str(athlete_id) for athlete_id in team.athletes]
                ) for team in teams
            ]
        except Exception as e:
            logger.error(f"Error listing teams: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving teams"
            )

    async def get_team(self, team_id: PydanticObjectId) -> TeamResponse:
        team = await self.repo.get_by_id(team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Team not found"
            )
        
        return TeamResponse(
            id=str(team.id),
            name=team.name,
            description=team.description,
            founded=team.founded,
            athletes=[str(athlete_id) for athlete_id in team.athletes]
        )

    async def update_team(self, team_id: PydanticObjectId, team: TeamUpdate) -> TeamResponse:
        db_team = await self.repo.get_by_id(team_id)
        if not db_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Team not found"
            )

        update_data = team.model_dump(exclude_unset=True)
        updated = await self.repo.update(team_id, update_data)
        
        return TeamResponse(
            id=str(updated.id),
            name=updated.name,
            description=updated.description,
            founded=updated.founded,
            athletes=[str(athlete_id) for athlete_id in updated.athletes]
        )

    async def delete_team(self, team_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(team_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Team not found"
            )

team_service = TeamService()