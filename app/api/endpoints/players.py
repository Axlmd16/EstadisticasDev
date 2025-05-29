from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.athlete_schema import AthleteCreate, AthleteUpdate, AthleteResponse
from beanie import PydanticObjectId
from app.services.player_service import player_service

router = APIRouter(prefix="/api/v1/athletes", tags=["Athletes"])

@router.post("/", response_model=AthleteResponse, status_code=status.HTTP_201_CREATED)
async def create_athlete(athlete: AthleteCreate):
    return await player_service.create_athlete(athlete)

@router.get("/", response_model=List[AthleteResponse])
async def list_athletes():
    return await player_service.list_athletes()

@router.get("/{athlete_id}", response_model=AthleteResponse)
async def get_athlete(athlete_id: PydanticObjectId):
    return await player_service.get_athlete(athlete_id)

@router.put("/{athlete_id}", response_model=AthleteResponse)
async def update_athlete(athlete_id: PydanticObjectId, athlete: AthleteUpdate):
    return await player_service.update_athlete(athlete_id, athlete)

@router.delete("/{athlete_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_athlete(athlete_id: PydanticObjectId):
    await player_service.delete_athlete(athlete_id)
    return None
