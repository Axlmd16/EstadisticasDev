from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.result_schema import ResultCreate, ResultUpdate, ResultResponse
from beanie import PydanticObjectId
from app.services.result_service import result_service

router = APIRouter(prefix="/api/v1/results", tags=["Results"])

@router.post("/", response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
async def create_result(result: ResultCreate):
    return await result_service.create_result(result)

@router.get("/", response_model=List[ResultResponse])
async def list_results():
    return await result_service.list_results()

@router.get("/{result_id}", response_model=ResultResponse)
async def get_result(result_id: PydanticObjectId):
    return await result_service.get_result(result_id)

@router.put("/{result_id}", response_model=ResultResponse)
async def update_result(result_id: PydanticObjectId, result: ResultUpdate):
    return await result_service.update_result(result_id, result)

@router.delete("/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_result(result_id: PydanticObjectId):
    await result_service.delete_result(result_id)
    return None
