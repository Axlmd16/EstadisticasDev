from fastapi import APIRouter, Depends, Path
from beanie import PydanticObjectId

from app.schemas.statistics_team_schema import (
    StatisticTeamCreate,
    StatisticTeamUpdate,
    StatisticTeamResponse,
)
from app.services.statistics_team_service import statistic_team_service

router = APIRouter(prefix="/statistics/team", tags=["Statistic Team"])

@router.post("/", response_model=StatisticTeamResponse)
async def create_statistic_team(stat: StatisticTeamCreate):
    return await statistic_team_service.create_statistic_team(stat)

@router.get("/", response_model=list[StatisticTeamResponse])
async def list_statistic_teams():
    return await statistic_team_service.list_statistic_teams()

@router.get("/{stat_id}", response_model=StatisticTeamResponse)
async def get_statistic_team(stat_id: PydanticObjectId = Path(...)):
    return await statistic_team_service.get_statistic_team(stat_id)

@router.put("/{stat_id}", response_model=StatisticTeamResponse)
async def update_statistic_team(
    stat_id: PydanticObjectId = Path(...),
    stat: StatisticTeamUpdate = Depends()
):
    return await statistic_team_service.update_statistic_team(stat_id, stat)

@router.delete("/{stat_id}")
async def delete_statistic_team(stat_id: PydanticObjectId = Path(...)):
    await statistic_team_service.delete_statistic_team(stat_id)
    return {"message": "StatisticTeam deleted successfully"}
