from app.repositories.position_table_repository import PositionTableRepository
from app.schemas.position_table_schema import PositionTableCreate, PositionTableUpdate, PositionTableResponse
from beanie import PydanticObjectId
from fastapi import HTTPException

class PositionTableService:
    def __init__(self):
        self.repo = PositionTableRepository()

    async def create_position_table(self, position_table: PositionTableCreate) -> PositionTableResponse:
        doc = await self.repo.create(position_table.dict())
        return PositionTableResponse(**doc.dict())

    async def list_position_tables(self) -> list[PositionTableResponse]:
        pts = await self.repo.list()
        return [PositionTableResponse(**p.dict()) for p in pts]

    async def get_position_table(self, position_table_id: PydanticObjectId) -> PositionTableResponse:
        pt = await self.repo.get_by_id(position_table_id)
        if not pt:
            raise HTTPException(status_code=404, detail="PositionTable not found")
        return PositionTableResponse(**pt.dict())

    async def update_position_table(self, position_table_id: PydanticObjectId, position_table: PositionTableUpdate) -> PositionTableResponse:
        db_pt = await self.repo.get_by_id(position_table_id)
        if not db_pt:
            raise HTTPException(status_code=404, detail="PositionTable not found")
        updated = await self.repo.update(position_table_id, position_table.dict(exclude_unset=True))
        return PositionTableResponse(**updated.dict())

    async def delete_position_table(self, position_table_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(position_table_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="PositionTable not found")

position_table_service = PositionTableService()
