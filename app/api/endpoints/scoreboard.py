from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.scoreboard_schema import ScoreboardCreate, ScoreboardUpdate, ScoreboardResponse
from beanie import PydanticObjectId
from app.services.scoreboard_service import scoreboard_service

router = APIRouter(prefix="/api/v1/scoreboards", tags=["Scoreboards"])

@router.post("/", response_model=ScoreboardResponse, status_code=status.HTTP_201_CREATED)
async def create_scoreboard(scoreboard: ScoreboardCreate):
    return await scoreboard_service.create_scoreboard(scoreboard)

@router.get("/", response_model=List[ScoreboardResponse])
async def list_scoreboards():
    return await scoreboard_service.list_scoreboards()

@router.get("/{scoreboard_id}", response_model=ScoreboardResponse)
async def get_scoreboard(scoreboard_id: PydanticObjectId):
    return await scoreboard_service.get_scoreboard(scoreboard_id)

@router.put("/{scoreboard_id}", response_model=ScoreboardResponse)
async def update_scoreboard(scoreboard_id: PydanticObjectId, scoreboard: ScoreboardUpdate):
    return await scoreboard_service.update_scoreboard(scoreboard_id, scoreboard)

@router.delete("/{scoreboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scoreboard(scoreboard_id: PydanticObjectId):
    await scoreboard_service.delete_scoreboard(scoreboard_id)
    return None
