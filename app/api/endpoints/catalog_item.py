from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.catalog_item import CatalogItem
from app.schemas.catalog_item_schema import CatalogItemBase
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v1/catalog_items", tags=["CatalogItems"])

@router.post("/", response_model=CatalogItemBase, status_code=status.HTTP_201_CREATED)
async def create_catalog_item(item: CatalogItemBase):
    item_doc = CatalogItem(**item.dict())
    await item_doc.insert()
    return CatalogItemBase(**item_doc.dict())

@router.get("/", response_model=List[CatalogItemBase])
async def list_catalog_items():
    items = await CatalogItem.find_all().to_list()
    return [CatalogItemBase(**i.dict()) for i in items]

@router.get("/{item_id}", response_model=CatalogItemBase)
async def get_catalog_item(item_id: PydanticObjectId):
    item = await CatalogItem.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="CatalogItem not found")
    return CatalogItemBase(**item.dict())

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_catalog_item(item_id: PydanticObjectId):
    item = await CatalogItem.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="CatalogItem not found")
    await item.delete()
    return None
