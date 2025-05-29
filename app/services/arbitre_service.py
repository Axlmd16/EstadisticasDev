from app.repositories.arbitre_repository import ArbitreRepository
from app.schemas.arbitre_schema import ArbitreCreate, ArbitreUpdate, ArbitreResponse
from beanie import PydanticObjectId
from fastapi import HTTPException

class ArbitreService:
    def __init__(self):
        self.repo = ArbitreRepository()

    async def create_arbitre(self, arbitre: ArbitreCreate) -> ArbitreResponse:
        doc = await self.repo.create(arbitre.dict())
        return ArbitreResponse(**doc.dict())

    async def list_arbitres(self) -> list[ArbitreResponse]:
        arbitres = await self.repo.list()
        return [ArbitreResponse(**a.dict()) for a in arbitres]

    async def get_arbitre(self, arbitre_id: PydanticObjectId) -> ArbitreResponse:
        arbitre = await self.repo.get_by_id(arbitre_id)
        if not arbitre:
            raise HTTPException(status_code=404, detail="Arbitre not found")
        return ArbitreResponse(**arbitre.dict())

    async def update_arbitre(self, arbitre_id: PydanticObjectId, arbitre: ArbitreUpdate) -> ArbitreResponse:
        db_arbitre = await self.repo.get_by_id(arbitre_id)
        if not db_arbitre:
            raise HTTPException(status_code=404, detail="Arbitre not found")
        updated = await self.repo.update(arbitre_id, arbitre.dict(exclude_unset=True))
        return ArbitreResponse(**updated.dict())

    async def delete_arbitre(self, arbitre_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(arbitre_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Arbitre not found")

arbitre_service = ArbitreService()
