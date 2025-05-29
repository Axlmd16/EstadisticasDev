from fastapi import APIRouter, HTTPException, status
from typing import List
from beanie import PydanticObjectId
from app.schemas.statistics_season_schema import (
    StatisticSeasonCreate,
    StatisticSeasonUpdate,
    StatisticSeasonResponse,
)
from app.services.statistics_season_service import statistic_season_service

router = APIRouter(prefix="/api/v1/statistics/season", tags=["StatisticSeasons"])

@router.post("/", response_model=StatisticSeasonResponse, status_code=status.HTTP_201_CREATED)
async def create_statistic_season(stat: StatisticSeasonCreate):
    return await statistic_season_service.create_statistic_season(stat)

@router.get("/", response_model=List[StatisticSeasonResponse])
async def list_statistic_seasons():
    return await statistic_season_service.list_statistic_seasons()

@router.get("/{stat_id}", response_model=StatisticSeasonResponse)
async def get_statistic_season(stat_id: PydanticObjectId):
    return await statistic_season_service.get_statistic_season(stat_id)

@router.put("/{stat_id}", response_model=StatisticSeasonResponse)
async def update_statistic_season(stat_id: PydanticObjectId, stat: StatisticSeasonUpdate):
    return await statistic_season_service.update_statistic_season(stat_id, stat)

@router.delete("/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_statistic_season(stat_id: PydanticObjectId):
    await statistic_season_service.delete_statistic_season(stat_id)
    return None
