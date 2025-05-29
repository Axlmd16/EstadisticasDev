from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.statistic_team import StatisticTeam
from app.schemas.statistic_schemas import StatisticTeamCreate, StatisticTeamUpdate, StatisticTeamResponse
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v1/statistics/team", tags=["StatisticsTeam"])

@router.post("/", response_model=StatisticTeamResponse, status_code=status.HTTP_201_CREATED)
async def create_statistic_team(stat: StatisticTeamCreate):
    stat_doc = StatisticTeam(**stat.dict())
    await stat_doc.insert()
    return StatisticTeamResponse(**stat_doc.dict())

@router.get("/", response_model=List[StatisticTeamResponse])
async def list_statistics_team():
    stats = await StatisticTeam.find_all().to_list()
    return [StatisticTeamResponse(**s.dict()) for s in stats]

@router.get("/{stat_id}", response_model=StatisticTeamResponse)
async def get_statistic_team(stat_id: PydanticObjectId):
    stat = await StatisticTeam.get(stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="StatisticTeam not found")
    return StatisticTeamResponse(**stat.dict())

@router.put("/{stat_id}", response_model=StatisticTeamResponse)
async def update_statistic_team(stat_id: PydanticObjectId, stat: StatisticTeamUpdate):
    db_stat = await StatisticTeam.get(stat_id)
    if not db_stat:
        raise HTTPException(status_code=404, detail="StatisticTeam not found")
    await db_stat.set({k: v for k, v in stat.dict(exclude_unset=True).items()})
    return StatisticTeamResponse(**db_stat.dict())

@router.delete("/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_statistic_team(stat_id: PydanticObjectId):
    stat = await StatisticTeam.get(stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="StatisticTeam not found")
    await stat.delete()
    return None
