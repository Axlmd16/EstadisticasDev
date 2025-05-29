# Servicio de jugadores
import logging
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId

from app.repositories.player_repository import PlayerRepository
from app.schemas.athlete_schema import AthleteCreate, AthleteUpdate, AthleteResponse

logger = logging.getLogger(__name__)

class PlayerService:
    def __init__(self):
        self.repo = PlayerRepository()

    async def create_athlete(self, athlete: AthleteCreate) -> AthleteResponse:
        try:
            athlete_data = athlete.model_dump(exclude_unset=True)

            if "team_id" in athlete_data and athlete_data["team_id"]:
                athlete_data["team_id"] = ObjectId(athlete_data["team_id"])

            doc = await self.repo.create(athlete_data)
            return AthleteResponse(
                id=str(doc.id),
                name=doc.name,
                position=doc.position,
                team_id=str(doc.team_id) if doc.team_id else None
            )
        except Exception as e:
            logger.error(f"Error creating athlete: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating athlete: {str(e)}"
            )

    async def list_athletes(self) -> list[AthleteResponse]:
        try:
            athletes = await self.repo.list()
            return [
                AthleteResponse(
                    id=str(a.id),
                    name=a.name,
                    position=a.position,
                    team_id=str(a.team_id) if a.team_id else None
                ) for a in athletes
            ]
        except Exception as e:
            logger.error(f"Error listing athletes: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving athletes"
            )

    async def get_athlete(self, athlete_id: PydanticObjectId) -> AthleteResponse:
        athlete = await self.repo.get_by_id(athlete_id)
        if not athlete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Athlete not found"
            )

        return AthleteResponse(
            id=str(athlete.id),
            name=athlete.name,
            position=athlete.position,
            team_id=str(athlete.team_id) if athlete.team_id else None
        )

    async def update_athlete(self, athlete_id: PydanticObjectId, athlete: AthleteUpdate) -> AthleteResponse:
        db_athlete = await self.repo.get_by_id(athlete_id)
        if not db_athlete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Athlete not found"
            )

        update_data = athlete.model_dump(exclude_unset=True)
        updated = await self.repo.update(athlete_id, update_data)

        return AthleteResponse(
            id=str(updated.id),
            name=updated.name,
            position=updated.position,
            team_id=str(updated.team_id) if updated.team_id else None
        )

    async def delete_athlete(self, athlete_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(athlete_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Athlete not found"
            )

player_service = PlayerService()
