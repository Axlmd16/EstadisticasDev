from app.repositories.table_rating_repository import TableRatingRepository
from app.schemas.table_rating_schema import TableRatingCreate, TableRatingUpdate, TableRatingResponse
from beanie import PydanticObjectId
from fastapi import HTTPException

class TableRatingService:
    def __init__(self):
        self.repo = TableRatingRepository()

    async def create_table_rating(self, table_rating: TableRatingCreate) -> TableRatingResponse:
        doc = await self.repo.create(table_rating.dict())
        return TableRatingResponse(**doc.dict())

    async def list_table_ratings(self) -> list[TableRatingResponse]:
        trs = await self.repo.list()
        return [TableRatingResponse(**t.dict()) for t in trs]

    async def get_table_rating(self, table_rating_id: PydanticObjectId) -> TableRatingResponse:
        tr = await self.repo.get_by_id(table_rating_id)
        if not tr:
            raise HTTPException(status_code=404, detail="TableRating not found")
        return TableRatingResponse(**tr.dict())

    async def update_table_rating(self, table_rating_id: PydanticObjectId, table_rating: TableRatingUpdate) -> TableRatingResponse:
        db_tr = await self.repo.get_by_id(table_rating_id)
        if not db_tr:
            raise HTTPException(status_code=404, detail="TableRating not found")
        updated = await self.repo.update(table_rating_id, table_rating.dict(exclude_unset=True))
        return TableRatingResponse(**updated.dict())

    async def delete_table_rating(self, table_rating_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(table_rating_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="TableRating not found")

table_rating_service = TableRatingService()
