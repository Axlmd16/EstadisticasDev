from typing import Type, TypeVar, List, Optional, Dict, Any
from beanie import Document, PydanticObjectId

T = TypeVar('T', bound=Document)

class BaseRepository:
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_by_id(self, id: PydanticObjectId) -> Optional[T]:
        return await self.model.get(id)

    async def create(self, data: Dict[str, Any]) -> T:
        doc = self.model(**data)
        await doc.insert()
        return doc

    async def update(self, id: PydanticObjectId, data: Dict[str, Any]) -> Optional[T]:
        doc = await self.model.get(id)
        if not doc:
            return None
        await doc.set(data)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.model.get(id)
        if not doc:
            return False
        await doc.delete()
        return True

    async def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        return await self.model.find_all().skip(skip).limit(limit).to_list()
