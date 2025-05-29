from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.table_rating import TableRating
from app.schemas.table_rating_schema import TableRatingCreate, TableRatingUpdate, TableRatingResponse
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v1/table_ratings", tags=["TableRatings"])

@router.post("/", response_model=TableRatingResponse, status_code=status.HTTP_201_CREATED)
async def create_table_rating(table_rating: TableRatingCreate):
    table_rating_doc = TableRating(**table_rating.dict())
    await table_rating_doc.insert()
    return TableRatingResponse(**table_rating_doc.dict())

@router.get("/", response_model=List[TableRatingResponse])
async def list_table_ratings():
    table_ratings = await TableRating.find_all().to_list()
    return [TableRatingResponse(**t.dict()) for t in table_ratings]

@router.get("/{table_rating_id}", response_model=TableRatingResponse)
async def get_table_rating(table_rating_id: PydanticObjectId):
    table_rating = await TableRating.get(table_rating_id)
    if not table_rating:
        raise HTTPException(status_code=404, detail="TableRating not found")
    return TableRatingResponse(**table_rating.dict())

@router.put("/{table_rating_id}", response_model=TableRatingResponse)
async def update_table_rating(table_rating_id: PydanticObjectId, table_rating: TableRatingUpdate):
    db_table_rating = await TableRating.get(table_rating_id)
    if not db_table_rating:
        raise HTTPException(status_code=404, detail="TableRating not found")
    await db_table_rating.set({k: v for k, v in table_rating.dict(exclude_unset=True).items()})
    return TableRatingResponse(**db_table_rating.dict())

@router.delete("/{table_rating_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table_rating(table_rating_id: PydanticObjectId):
    table_rating = await TableRating.get(table_rating_id)
    if not table_rating:
        raise HTTPException(status_code=404, detail="TableRating not found")
    await table_rating.delete()
    return None
