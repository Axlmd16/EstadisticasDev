# Servicio de partidos

from app.repositories.match_repository import MatchRepository
from app.schemas.match_schema import MatchCreate, MatchUpdate, MatchResponse
from beanie import PydanticObjectId
from fastapi import HTTPException

class MatchService:
    def __init__(self):
        self.repo = MatchRepository()

    async def create_match(self, match: MatchCreate) -> MatchResponse:
        doc = await self.repo.create(match.dict())
        return MatchResponse(**doc.dict())

    async def list_matches(self) -> list[MatchResponse]:
        matches = await self.repo.list()
        return [MatchResponse(**m.dict()) for m in matches]

    async def get_match(self, match_id: PydanticObjectId) -> MatchResponse:
        match = await self.repo.get_by_id(match_id)
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        return MatchResponse(**match.dict())

    async def update_match(self, match_id: PydanticObjectId, match: MatchUpdate) -> MatchResponse:
        db_match = await self.repo.get_by_id(match_id)
        if not db_match:
            raise HTTPException(status_code=404, detail="Match not found")
        updated = await self.repo.update(match_id, match.dict(exclude_unset=True))
        return MatchResponse(**updated.dict())

    async def delete_match(self, match_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(match_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Match not found")

match_service = MatchService()
