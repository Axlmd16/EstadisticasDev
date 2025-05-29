from app.repositories.scoreboard_repository import ScoreboardRepository
from app.schemas.scoreboard_schema import ScoreboardCreate, ScoreboardUpdate, ScoreboardResponse
from beanie import PydanticObjectId
from fastapi import HTTPException

class ScoreboardService:
    def __init__(self):
        self.repo = ScoreboardRepository()

    async def create_scoreboard(self, scoreboard: ScoreboardCreate) -> ScoreboardResponse:
        doc = await self.repo.create(scoreboard.dict())
        return ScoreboardResponse(**doc.dict())

    async def list_scoreboards(self) -> list[ScoreboardResponse]:
        scoreboards = await self.repo.list()
        return [ScoreboardResponse(**s.dict()) for s in scoreboards]

    async def get_scoreboard(self, scoreboard_id: PydanticObjectId) -> ScoreboardResponse:
        scoreboard = await self.repo.get_by_id(scoreboard_id)
        if not scoreboard:
            raise HTTPException(status_code=404, detail="Scoreboard not found")
        return ScoreboardResponse(**scoreboard.dict())

    async def update_scoreboard(self, scoreboard_id: PydanticObjectId, scoreboard: ScoreboardUpdate) -> ScoreboardResponse:
        db_scoreboard = await self.repo.get_by_id(scoreboard_id)
        if not db_scoreboard:
            raise HTTPException(status_code=404, detail="Scoreboard not found")
        updated = await self.repo.update(scoreboard_id, scoreboard.dict(exclude_unset=True))
        return ScoreboardResponse(**updated.dict())

    async def delete_scoreboard(self, scoreboard_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(scoreboard_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Scoreboard not found")

scoreboard_service = ScoreboardService()
