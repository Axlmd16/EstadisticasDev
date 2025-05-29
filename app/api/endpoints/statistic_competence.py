from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.statistic_competence import StatisticCompetence
from app.schemas.statistic_schemas import StatisticCompetenceCreate, StatisticCompetenceUpdate, StatisticCompetenceResponse
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v1/statistics/competence", tags=["StatisticsCompetence"])

@router.post("/", response_model=StatisticCompetenceResponse, status_code=status.HTTP_201_CREATED)
async def create_statistic_competence(stat: StatisticCompetenceCreate):
    stat_doc = StatisticCompetence(**stat.dict())
    await stat_doc.insert()
    return StatisticCompetenceResponse(**stat_doc.dict())

@router.get("/", response_model=List[StatisticCompetenceResponse])
async def list_statistics_competence():
    stats = await StatisticCompetence.find_all().to_list()
    return [StatisticCompetenceResponse(**s.dict()) for s in stats]

@router.get("/{stat_id}", response_model=StatisticCompetenceResponse)
async def get_statistic_competence(stat_id: PydanticObjectId):
    stat = await StatisticCompetence.get(stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="StatisticCompetence not found")
    return StatisticCompetenceResponse(**stat.dict())

@router.put("/{stat_id}", response_model=StatisticCompetenceResponse)
async def update_statistic_competence(stat_id: PydanticObjectId, stat: StatisticCompetenceUpdate):
    db_stat = await StatisticCompetence.get(stat_id)
    if not db_stat:
        raise HTTPException(status_code=404, detail="StatisticCompetence not found")
    await db_stat.set({k: v for k, v in stat.dict(exclude_unset=True).items()})
    return StatisticCompetenceResponse(**db_stat.dict())

@router.delete("/{stat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_statistic_competence(stat_id: PydanticObjectId):
    stat = await StatisticCompetence.get(stat_id)
    if not stat:
        raise HTTPException(status_code=404, detail="StatisticCompetence not found")
    await stat.delete()
    return None
