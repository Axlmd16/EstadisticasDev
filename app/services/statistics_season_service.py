import logging
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId

from app.repositories.statistics_season_repository import StatisticSeasonRepository
from app.schemas.statistics_season_schema import (
    StatisticSeasonCreate,
    StatisticSeasonUpdate,
    StatisticSeasonResponse,
)

logger = logging.getLogger(__name__)

class StatisticSeasonService:
    def __init__(self):
        self.repo = StatisticSeasonRepository()

    async def create_statistic_season(self, stat: StatisticSeasonCreate) -> StatisticSeasonResponse:
        try:
            stat_data = stat.model_dump(exclude_unset=True)

            for field in [
                "most_fouls", "most_red_cards", "most_yellow_cards",
                "top_assistant", "top_scorer", "id_season"
            ]:
                if field in stat_data and stat_data[field]:
                    stat_data[field] = ObjectId(stat_data[field])

            doc = await self.repo.create(stat_data)
            return StatisticSeasonResponse(
                id=str(doc.id),
                description=doc.description,
                date_generation=doc.date_generation,
                value=doc.value,
                most_fouls=str(doc.most_fouls) if doc.most_fouls else None,
                most_red_cards=str(doc.most_red_cards) if doc.most_red_cards else None,
                most_yellow_cards=str(doc.most_yellow_cards) if doc.most_yellow_cards else None,
                top_assistant=str(doc.top_assistant) if doc.top_assistant else None,
                top_scorer=str(doc.top_scorer) if doc.top_scorer else None,
                id_season=str(doc.id_season) if doc.id_season else None,
            )
        except Exception as e:
            logger.error(f"Error creating statistic season: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating statistic season: {str(e)}"
            )

    async def list_statistic_seasons(self) -> list[StatisticSeasonResponse]:
        try:
            stats = await self.repo.list()
            return [
                StatisticSeasonResponse(
                    id=str(s.id),
                    description=s.description,
                    date_generation=s.date_generation,
                    value=s.value,
                    most_fouls=str(s.most_fouls) if s.most_fouls else None,
                    most_red_cards=str(s.most_red_cards) if s.most_red_cards else None,
                    most_yellow_cards=str(s.most_yellow_cards) if s.most_yellow_cards else None,
                    top_assistant=str(s.top_assistant) if s.top_assistant else None,
                    top_scorer=str(s.top_scorer) if s.top_scorer else None,
                    id_season=str(s.id_season) if s.id_season else None,
                ) for s in stats
            ]
        except Exception as e:
            logger.error(f"Error listing statistic seasons: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving statistic seasons"
            )

    async def get_statistic_season(self, stat_id: PydanticObjectId) -> StatisticSeasonResponse:
        stat = await self.repo.get_by_id(stat_id)
        if not stat:
            raise HTTPException(status_code=404, detail="StatisticSeason not found")
        return StatisticSeasonResponse(
            id=str(stat.id),
            description=stat.description,
            date_generation=stat.date_generation,
            value=stat.value,
            most_fouls=str(stat.most_fouls) if stat.most_fouls else None,
            most_red_cards=str(stat.most_red_cards) if stat.most_red_cards else None,
            most_yellow_cards=str(stat.most_yellow_cards) if stat.most_yellow_cards else None,
            top_assistant=str(stat.top_assistant) if stat.top_assistant else None,
            top_scorer=str(stat.top_scorer) if stat.top_scorer else None,
            id_season=str(stat.id_season) if stat.id_season else None,
        )

    async def update_statistic_season(self, stat_id: PydanticObjectId, stat: StatisticSeasonUpdate) -> StatisticSeasonResponse:
        db_stat = await self.repo.get_by_id(stat_id)
        if not db_stat:
            raise HTTPException(status_code=404, detail="StatisticSeason not found")

        update_data = stat.model_dump(exclude_unset=True)
        for field in [
            "most_fouls", "most_red_cards", "most_yellow_cards",
            "top_assistant", "top_scorer", "id_season"
        ]:
            if field in update_data and update_data[field]:
                update_data[field] = ObjectId(update_data[field])

        updated = await self.repo.update(stat_id, update_data)
        return StatisticSeasonResponse(
            id=str(updated.id),
            description=updated.description,
            date_generation=updated.date_generation,
            value=updated.value,
            most_fouls=str(updated.most_fouls) if updated.most_fouls else None,
            most_red_cards=str(updated.most_red_cards) if updated.most_red_cards else None,
            most_yellow_cards=str(updated.most_yellow_cards) if updated.most_yellow_cards else None,
            top_assistant=str(updated.top_assistant) if updated.top_assistant else None,
            top_scorer=str(updated.top_scorer) if updated.top_scorer else None,
            id_season=str(updated.id_season) if updated.id_season else None,
        )

    async def delete_statistic_season(self, stat_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(stat_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="StatisticSeason not found")

statistic_season_service = StatisticSeasonService()
