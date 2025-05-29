from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.team_schema import TeamCreate, TeamUpdate, TeamResponse
from beanie import PydanticObjectId
from app.services.team_service import team_service

router = APIRouter(prefix="/api/v1/teams", tags=["Teams"])

@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(team: TeamCreate):
    return await team_service.create_team(team)

@router.get("/", response_model=List[TeamResponse])
async def list_teams():
    return await team_service.list_teams()

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: PydanticObjectId):
    return await team_service.get_team(team_id)

@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: PydanticObjectId, team: TeamUpdate):
    return await team_service.update_team(team_id, team)

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: PydanticObjectId):
    await team_service.delete_team(team_id)
    return None
