from app.repositories.catalog_item_repository import CatalogItemRepository
from app.schemas.catalog_item_schema import CatalogItemSchema
from beanie import PydanticObjectId
from fastapi import HTTPException

class CatalogItemService:
    def __init__(self):
        self.repo = CatalogItemRepository()

    async def create_catalog_item(self, item: CatalogItemSchema) -> CatalogItemSchema:
        doc = await self.repo.create(item.dict())
        return CatalogItemSchema(**doc.dict())

    async def list_catalog_items(self) -> list[CatalogItemSchema]:
        items = await self.repo.list()
        return [CatalogItemSchema(**i.dict()) for i in items]

    async def get_catalog_item(self, item_id: PydanticObjectId) -> CatalogItemSchema:
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="CatalogItem not found")
        return CatalogItemSchema(**item.dict())

    async def delete_catalog_item(self, item_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(item_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="CatalogItem not found")

catalog_item_service = CatalogItemService()
