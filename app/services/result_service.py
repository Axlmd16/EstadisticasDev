from app.repositories.result_repository import ResultRepository
from app.schemas.result_schema import ResultCreate, ResultUpdate, ResultResponse
from beanie import PydanticObjectId
from fastapi import HTTPException

class ResultService:
    def __init__(self):
        self.repo = ResultRepository()

    async def create_result(self, result: ResultCreate) -> ResultResponse:
        doc = await self.repo.create(result.dict())
        return ResultResponse(**doc.dict())

    async def list_results(self) -> list[ResultResponse]:
        results = await self.repo.list()
        return [ResultResponse(**r.dict()) for r in results]

    async def get_result(self, result_id: PydanticObjectId) -> ResultResponse:
        result = await self.repo.get_by_id(result_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        return ResultResponse(**result.dict())

    async def update_result(self, result_id: PydanticObjectId, result: ResultUpdate) -> ResultResponse:
        db_result = await self.repo.get_by_id(result_id)
        if not db_result:
            raise HTTPException(status_code=404, detail="Result not found")
        updated = await self.repo.update(result_id, result.dict(exclude_unset=True))
        return ResultResponse(**updated.dict())

    async def delete_result(self, result_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(result_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Result not found")

result_service = ResultService()
