import logging
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId

from app.repositories.statistics_competence_repository import StatisticCompetenceRepository
from app.schemas.statistics_competence_schema import (
    StatisticCompetenceCreate,
    StatisticCompetenceUpdate,
    StatisticCompetenceResponse,
)

logger = logging.getLogger(__name__)

class StatisticCompetenceService:
    def __init__(self):
        self.repo = StatisticCompetenceRepository()

    async def create_statistic_competence(self, stat: StatisticCompetenceCreate) -> StatisticCompetenceResponse:
        try:
            stat_data = stat.model_dump(exclude_unset=True)
            if "id_competition" in stat_data and stat_data["id_competition"]:
                stat_data["id_competition"] = ObjectId(stat_data["id_competition"])
            doc = await self.repo.create(stat_data)
            return StatisticCompetenceResponse(
                id=str(doc.id),
                description=doc.description,
                date_generation=doc.date_generation,
                value=doc.value,
                average_score=doc.average_score,
                matches_completed=doc.matches_completed,
                record_score=doc.record_score,
                total_parties=doc.total_parties,
                id_competition=str(doc.id_competition) if doc.id_competition else None,
            )
        except Exception as e:
            logger.error(f"Error creating statistic competence: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating statistic competence: {str(e)}"
            )

    async def list_statistic_competences(self) -> list[StatisticCompetenceResponse]:
        try:
            stats = await self.repo.list()
            return [
                StatisticCompetenceResponse(
                    id=str(s.id),
                    description=s.description,
                    date_generation=s.date_generation,
                    value=s.value,
                    average_score=s.average_score,
                    matches_completed=s.matches_completed,
                    record_score=s.record_score,
                    total_parties=s.total_parties,
                    id_competition=str(s.id_competition) if s.id_competition else None,
                ) for s in stats
            ]
        except Exception as e:
            logger.error(f"Error listing statistic competences: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving statistic competences"
            )

    async def get_statistic_competence(self, stat_id: PydanticObjectId) -> StatisticCompetenceResponse:
        stat = await self.repo.get_by_id(stat_id)
        if not stat:
            raise HTTPException(status_code=404, detail="StatisticCompetence not found")
        return StatisticCompetenceResponse(
            id=str(stat.id),
            description=stat.description,
            date_generation=stat.date_generation,
            value=stat.value,
            average_score=stat.average_score,
            matches_completed=stat.matches_completed,
            record_score=stat.record_score,
            total_parties=stat.total_parties,
            id_competition=str(stat.id_competition) if stat.id_competition else None,
        )

    async def update_statistic_competence(self, stat_id: PydanticObjectId, stat: StatisticCompetenceUpdate) -> StatisticCompetenceResponse:
        db_stat = await self.repo.get_by_id(stat_id)
        if not db_stat:
            raise HTTPException(status_code=404, detail="StatisticCompetence not found")

        update_data = stat.model_dump(exclude_unset=True)
        if "id_competition" in update_data and update_data["id_competition"]:
            update_data["id_competition"] = ObjectId(update_data["id_competition"])

        updated = await self.repo.update(stat_id, update_data)
        return StatisticCompetenceResponse(
            id=str(updated.id),
            description=updated.description,
            date_generation=updated.date_generation,
            value=updated.value,
            average_score=updated.average_score,
            matches_completed=updated.matches_completed,
            record_score=updated.record_score,
            total_parties=updated.total_parties,
            id_competition=str(updated.id_competition) if updated.id_competition else None,
        )

    async def delete_statistic_competence(self, stat_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(stat_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="StatisticCompetence not found")

statistic_competence_service = StatisticCompetenceService()
