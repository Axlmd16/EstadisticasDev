from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.statistic_individual import StatisticIndividual
from app.schemas.statistic_schemas import StatisticIndividualCreate, StatisticIndividualUpdate, StatisticIndividualResponse
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v1/statistics/individual", tags=["StatisticsIndividual"])

@router.post("/", response_model=StatisticIndividualResponse, status_code=status.HTTP_201_CREATED)
async def create_statistic_individual(stat: StatisticIndividualCreate):
    stat_doc = StatisticIndividual(**stat.dict())
    await stat_doc.insert()
    return StatisticIndividualResponse(**stat_doc.dict())

@router.get("/", response_model=List[StatisticIndividualResponse])
async def list_statistics_individual():
    stats = await StatisticIndividual.find_all().to_list()
    return [StatisticIndividualResponse(**s.dict()) for s in stats]

@router.get("/{stat_id}", response_model=StatisticIndividualResponse)
async def get_statistic_individual(stat_id: PydanticObjectId):
    stat = await StatisticIndividual.get(stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="StatisticIndividual not found")
    return StatisticIndividualResponse(**stat.dict())

@router.put("/{stat_id}", response_model=StatisticIndividualResponse)
async def update_statistic_individual(stat_id: PydanticObjectId, stat: StatisticIndividualUpdate):
    db_stat = await StatisticIndividual.get(stat_id)
    if not db_stat:
        raise HTTPException(status_code=404, detail="StatisticIndividual not found")
    await db_stat.set({k: v for k, v in stat.dict(exclude_unset=True).items()})
    return StatisticIndividualResponse(**db_stat.dict())

@router.delete("/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_statistic_individual(stat_id: PydanticObjectId):
    stat = await StatisticIndividual.get(stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="StatisticIndividual not found")
    await stat.delete()
    return None
