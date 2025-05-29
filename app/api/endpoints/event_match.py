from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.event_match_schema import EventMatchCreate, EventMatchUpdate, EventMatchResponse
from beanie import PydanticObjectId
from app.services.event_match_service import event_match_service

router = APIRouter(prefix="/api/v1/event_matches", tags=["EventMatches"])

@router.post("/", response_model=EventMatchResponse, status_code=status.HTTP_201_CREATED)
async def create_event_match(event: EventMatchCreate):
    return await event_match_service.create_event_match(event)

@router.get("/", response_model=List[EventMatchResponse])
async def list_event_matches():
    return await event_match_service.list_event_matches()

@router.get("/{event_id}", response_model=EventMatchResponse)
async def get_event_match(event_id: PydanticObjectId):
    return await event_match_service.get_event_match(event_id)

@router.put("/{event_id}", response_model=EventMatchResponse)
async def update_event_match(event_id: PydanticObjectId, event: EventMatchUpdate):
    return await event_match_service.update_event_match(event_id, event)

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_match(event_id: PydanticObjectId):
    await event_match_service.delete_event_match(event_id)
    return None
