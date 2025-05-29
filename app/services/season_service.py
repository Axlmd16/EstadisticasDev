from app.repositories.season_repository import SeasonRepository
from app.schemas.season_schema import SeasonCreate, SeasonUpdate, SeasonResponse
from beanie import PydanticObjectId
from fastapi import HTTPException

class SeasonService:
    def __init__(self):
        self.repo = SeasonRepository()

    async def create_season(self, season: SeasonCreate) -> SeasonResponse:
        doc = await self.repo.create(season.dict())
        return SeasonResponse(**doc.dict())

    async def list_seasons(self) -> list[SeasonResponse]:
        seasons = await self.repo.list()
        return [SeasonResponse(**s.dict()) for s in seasons]

    async def get_season(self, season_id: PydanticObjectId) -> SeasonResponse:
        season = await self.repo.get_by_id(season_id)
        if not season:
            raise HTTPException(status_code=404, detail="Season not found")
        return SeasonResponse(**season.dict())

    async def update_season(self, season_id: PydanticObjectId, season: SeasonUpdate) -> SeasonResponse:
        db_season = await self.repo.get_by_id(season_id)
        if not db_season:
            raise HTTPException(status_code=404, detail="Season not found")
        updated = await self.repo.update(season_id, season.dict(exclude_unset=True))
        return SeasonResponse(**updated.dict())

    async def delete_season(self, season_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(season_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Season not found")

season_service = SeasonService()
