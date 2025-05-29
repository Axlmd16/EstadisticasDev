from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.statistic_season import StatisticSeason
from app.schemas.statistic_schemas import StatisticSeasonCreate, StatisticSeasonUpdate, StatisticSeasonResponse
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v1/statistics/season", tags=["StatisticsSeason"])

@router.post("/", response_model=StatisticSeasonResponse, status_code=status.HTTP_201_CREATED)
async def create_statistic_season(stat: StatisticSeasonCreate):
    stat_doc = StatisticSeason(**stat.dict())
    await stat_doc.insert()
    return StatisticSeasonResponse(**stat_doc.dict())

@router.get("/", response_model=List[StatisticSeasonResponse])
async def list_statistics_season():
    stats = await StatisticSeason.find_all().to_list()
    return [StatisticSeasonResponse(**s.dict()) for s in stats]

@router.get("/{stat_id}", response_model=StatisticSeasonResponse)
async def get_statistic_season(stat_id: PydanticObjectId):
    stat = await StatisticSeason.get(stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="StatisticSeason not found")
    return StatisticSeasonResponse(**stat.dict())

@router.put("/{stat_id}", response_model=StatisticSeasonResponse)
async def update_statistic_season(stat_id: PydanticObjectId, stat: StatisticSeasonUpdate):
    db_stat = await StatisticSeason.get(stat_id)
    if not db_stat:
        raise HTTPException(status_code=404, detail="StatisticSeason not found")
    await db_stat.set({k: v for k, v in stat.dict(exclude_unset=True).items()})
    return StatisticSeasonResponse(**db_stat.dict())

@router.delete("/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_statistic_season(stat_id: PydanticObjectId):
    stat = await StatisticSeason.get(stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="StatisticSeason not found")
    await stat.delete()
    return None
