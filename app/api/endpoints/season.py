from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.season_schema import SeasonCreate, SeasonUpdate, SeasonResponse
from beanie import PydanticObjectId
from app.services.season_service import season_service

router = APIRouter(prefix="/api/v1/seasons", tags=["Seasons"])

@router.post("/", response_model=SeasonResponse, status_code=status.HTTP_201_CREATED)
async def create_season(season: SeasonCreate):
    return await season_service.create_season(season)

@router.get("/", response_model=List[SeasonResponse])
async def list_seasons():
    return await season_service.list_seasons()

@router.get("/{season_id}", response_model=SeasonResponse)
async def get_season(season_id: PydanticObjectId):
    return await season_service.get_season(season_id)

@router.put("/{season_id}", response_model=SeasonResponse)
async def update_season(season_id: PydanticObjectId, season: SeasonUpdate):
    return await season_service.update_season(season_id, season)

@router.delete("/{season_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_season(season_id: PydanticObjectId):
    await season_service.delete_season(season_id)
    return None
