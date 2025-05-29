from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.match_schema import MatchCreate, MatchUpdate, MatchResponse
from beanie import PydanticObjectId
from app.services.match_service import match_service

router = APIRouter(prefix="/api/v1/matches", tags=["Matches"])

@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def create_match(match: MatchCreate):
    return await match_service.create_match(match)

@router.get("/", response_model=List[MatchResponse])
async def list_matches():
    return await match_service.list_matches()

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: PydanticObjectId):
    return await match_service.get_match(match_id)

@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(match_id: PydanticObjectId, match: MatchUpdate):
    return await match_service.update_match(match_id, match)

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(match_id: PydanticObjectId):
    await match_service.delete_match(match_id)
    return None
