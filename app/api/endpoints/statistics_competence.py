from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.statistics_competence_schema import (
    StatisticCompetenceCreate,
    StatisticCompetenceUpdate,
    StatisticCompetenceResponse,
)
from beanie import PydanticObjectId
from app.services.statistics_competence_service import statistic_competence_service

router = APIRouter(prefix="/api/v1/statistics/competence", tags=["StatisticCompetence"])

@router.post("/", response_model=StatisticCompetenceResponse, status_code=status.HTTP_201_CREATED)
async def create_statistic_competence(stat: StatisticCompetenceCreate):
    return await statistic_competence_service.create_statistic_competence(stat)

@router.get("/", response_model=List[StatisticCompetenceResponse])
async def list_statistic_competences():
    return await statistic_competence_service.list_statistic_competences()

@router.get("/{stat_id}", response_model=StatisticCompetenceResponse)
async def get_statistic_competence(stat_id: PydanticObjectId):
    return await statistic_competence_service.get_statistic_competence(stat_id)

@router.put("/{stat_id}", response_model=StatisticCompetenceResponse)
async def update_statistic_competence(stat_id: PydanticObjectId, stat: StatisticCompetenceUpdate):
    return await statistic_competence_service.update_statistic_competence(stat_id, stat)

@router.delete("/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_statistic_competence(stat_id: PydanticObjectId):
    await statistic_competence_service.delete_statistic_competence(stat_id)
    return None
