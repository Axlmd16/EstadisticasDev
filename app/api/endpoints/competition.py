from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.competition import Competition
from app.schemas.competition_schema import CompetitionCreate, CompetitionUpdate, CompetitionResponse
from beanie import PydanticObjectId
from app.services.table_rating_service import table_rating_service
from app.schemas.table_rating_schema import TableRatingCreate

router = APIRouter(prefix="/api/v1/competitions", tags=["Competitions"])

@router.post("/", response_model=CompetitionResponse, status_code=status.HTTP_201_CREATED)
async def create_competition(competition: CompetitionCreate):
    competition_doc = Competition(**competition.dict())
    await competition_doc.insert()
    await table_rating_service.create_table_rating(
        TableRatingCreate(
            competition_id=str(competition_doc.id),  
            last_update=None,
            positions=[]
        )
    )
    return CompetitionResponse(**competition_doc.dict())

@router.get("/", response_model=List[CompetitionResponse])
async def list_competitions():
    competitions = await Competition.find_all().to_list()
    return [CompetitionResponse(**c.dict()) for c in competitions]

@router.get("/{competition_id}", response_model=CompetitionResponse)
async def get_competition(competition_id: PydanticObjectId):
    competition = await Competition.get(competition_id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return CompetitionResponse(**competition.dict())

@router.put("/{competition_id}", response_model=CompetitionResponse)
async def update_competition(competition_id: PydanticObjectId, competition: CompetitionUpdate):
    db_competition = await Competition.get(competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    await db_competition.set({k: v for k, v in competition.dict(exclude_unset=True).items()})
    return CompetitionResponse(**db_competition.dict())

@router.delete("/{competition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_competition(competition_id: PydanticObjectId):
    competition = await Competition.get(competition_id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    await competition.delete()
    return None
