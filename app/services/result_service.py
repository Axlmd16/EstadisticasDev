from app.repositories.result_repository import ResultRepository
from app.schemas.result_schema import ResultCreate, ResultUpdate, ResultResponse
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class ResultService:
    def __init__(self):
        self.repo = ResultRepository()

    def _convert_string_ids_to_objectid(self, data: dict) -> dict:
        """Convierte string IDs a ObjectId para almacenar en MongoDB"""
        converted_data = data.copy()
        
        if converted_data.get('scoreboard_id'):
            converted_data['scoreboard_id'] = ObjectId(converted_data['scoreboard_id'])
        
        return converted_data

    async def create_result(self, result: ResultCreate) -> ResultResponse:
        try:
            result_data = result.model_dump(exclude_unset=True)
            result_data = self._convert_string_ids_to_objectid(result_data)
            
            doc = await self.repo.create(result_data)
            
            return ResultResponse(
                id=str(doc.id),
                date_registration=doc.date_registration,
                details=doc.details,
                loser=doc.loser,
                score_local=doc.score_local,
                score_visitor=doc.score_visitor,
                winner=doc.winner,
                scoreboard_id=str(doc.scoreboard_id) if doc.scoreboard_id else None
            )
        except Exception as e:
            logger.error(f"Error creating result: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating result: {str(e)}"
            )

    async def list_results(self) -> list[ResultResponse]:
        try:
            results = await self.repo.list()
            return [
                ResultResponse(
                    id=str(result.id),
                    date_registration=result.date_registration,
                    details=result.details,
                    loser=result.loser,
                    score_local=result.score_local,
                    score_visitor=result.score_visitor,
                    winner=result.winner,
                    scoreboard_id=str(result.scoreboard_id) if result.scoreboard_id else None
                ) for result in results
            ]
        except Exception as e:
            logger.error(f"Error listing results: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving results"
            )

    async def get_result(self, result_id: PydanticObjectId) -> ResultResponse:
        result = await self.repo.get_by_id(result_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Result not found"
            )
        
        return ResultResponse(
            id=str(result.id),
            date_registration=result.date_registration,
            details=result.details,
            loser=result.loser,
            score_local=result.score_local,
            score_visitor=result.score_visitor,
            winner=result.winner,
            scoreboard_id=str(result.scoreboard_id) if result.scoreboard_id else None
        )

    async def update_result(self, result_id: PydanticObjectId, result: ResultUpdate) -> ResultResponse:
        db_result = await self.repo.get_by_id(result_id)
        if not db_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Result not found"
            )
        
        update_data = result.model_dump(exclude_unset=True)
        update_data = self._convert_string_ids_to_objectid(update_data)
        
        updated = await self.repo.update(result_id, update_data)
        
        return ResultResponse(
            id=str(updated.id),
            date_registration=updated.date_registration,
            details=updated.details,
            loser=updated.loser,
            score_local=updated.score_local,
            score_visitor=updated.score_visitor,
            winner=updated.winner,
            scoreboard_id=str(updated.scoreboard_id) if updated.scoreboard_id else None
        )

    async def delete_result(self, result_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(result_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Result not found"
            )

result_service = ResultService()