from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.arbitre_schema import ArbitreCreate, ArbitreUpdate, ArbitreResponse
from beanie import PydanticObjectId
from app.services.arbitre_service import arbitre_service

router = APIRouter(prefix="/api/v1/arbitres", tags=["Arbitres"])

@router.post("/", response_model=ArbitreResponse, status_code=status.HTTP_201_CREATED)
async def create_arbitre(arbitre: ArbitreCreate):
    return await arbitre_service.create_arbitre(arbitre)

@router.get("/", response_model=List[ArbitreResponse])
async def list_arbitres():
    return await arbitre_service.list_arbitres()

@router.get("/{arbitre_id}", response_model=ArbitreResponse)
async def get_arbitre(arbitre_id: PydanticObjectId):
    return await arbitre_service.get_arbitre(arbitre_id)

@router.put("/{arbitre_id}", response_model=ArbitreResponse)
async def update_arbitre(arbitre_id: PydanticObjectId, arbitre: ArbitreUpdate):
    return await arbitre_service.update_arbitre(arbitre_id, arbitre)

@router.delete("/{arbitre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_arbitre(arbitre_id: PydanticObjectId):
    await arbitre_service.delete_arbitre(arbitre_id)
    return None
