from fastapi import APIRouter, status
from typing import List
from beanie import PydanticObjectId
from app.schemas.statistic_individual_schema import (
    StatisticIndividualCreate,
    StatisticIndividualUpdate,
    StatisticIndividualResponse,
)
from app.services.statistic_individual_service import statistic_individual_service

router = APIRouter(prefix="/api/v1/statistics/individual", tags=["Statistics Individual"])

@router.post("/", response_model=StatisticIndividualResponse, status_code=status.HTTP_201_CREATED)
async def create_statistic(data: StatisticIndividualCreate):
    return await statistic_individual_service.create_statistic(data)

@router.get("/", response_model=List[StatisticIndividualResponse])
async def list_statistics():
    return await statistic_individual_service.list_statistics()

@router.get("/{stat_id}", response_model=StatisticIndividualResponse)
async def get_statistic(stat_id: PydanticObjectId):
    return await statistic_individual_service.get_statistic(stat_id)

@router.put("/{stat_id}", response_model=StatisticIndividualResponse)
async def update_statistic(stat_id: PydanticObjectId, data: StatisticIndividualUpdate):
    return await statistic_individual_service.update_statistic(stat_id, data)

@router.delete("/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_statistic(stat_id: PydanticObjectId):
    await statistic_individual_service.delete_statistic(stat_id)
    return None
