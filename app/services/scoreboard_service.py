# app/services/scoreboard_service.py - VERSIÓN CORREGIDA
from app.repositories.scoreboard_repository import ScoreboardRepository
from app.schemas.scoreboard_schema import ScoreboardCreate, ScoreboardUpdate, ScoreboardResponse
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class ScoreboardService:
    def __init__(self):
        self.repo = ScoreboardRepository()

    def _convert_string_ids_to_objectid(self, data: dict) -> dict:
        """Convierte string IDs a ObjectId para almacenar en MongoDB"""
        converted_data = data.copy()
        
        if converted_data.get('status_game'):
            converted_data['status_game'] = ObjectId(converted_data['status_game'])
        
        if converted_data.get('match_id'):
            converted_data['match_id'] = ObjectId(converted_data['match_id'])
        
        return converted_data

    async def create_scoreboard(self, scoreboard: ScoreboardCreate) -> ScoreboardResponse:
        try:
            scoreboard_data = scoreboard.model_dump(exclude_unset=True)
            scoreboard_data = self._convert_string_ids_to_objectid(scoreboard_data)
            
            doc = await self.repo.create(scoreboard_data)
            
            return ScoreboardResponse(
                id=str(doc.id),
                last_update=doc.last_update,
                status_game=str(doc.status_game) if doc.status_game else None,
                score_local=doc.score_local,
                score_visitor=doc.score_visitor,
                time_restant=doc.time_restant,
                is_final=doc.is_final,
                match_id=str(doc.match_id) if doc.match_id else None
            )
        except Exception as e:
            logger.error(f"Error creating scoreboard: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating scoreboard: {str(e)}"
            )

    async def list_scoreboards(self) -> list[ScoreboardResponse]:
        try:
            scoreboards = await self.repo.list()
            return [
                ScoreboardResponse(
                    id=str(scoreboard.id),
                    last_update=scoreboard.last_update,
                    status_game=str(scoreboard.status_game) if scoreboard.status_game else None,
                    score_local=scoreboard.score_local,
                    score_visitor=scoreboard.score_visitor,
                    time_restant=scoreboard.time_restant,
                    is_final=scoreboard.is_final,
                    match_id=str(scoreboard.match_id) if scoreboard.match_id else None
                ) for scoreboard in scoreboards
            ]
        except Exception as e:
            logger.error(f"Error listing scoreboards: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving scoreboards"
            )

    async def get_scoreboard(self, scoreboard_id: PydanticObjectId) -> ScoreboardResponse:
        scoreboard = await self.repo.get_by_id(scoreboard_id)
        if not scoreboard:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Scoreboard not found"
            )
        
        return ScoreboardResponse(
            id=str(scoreboard.id),
            last_update=scoreboard.last_update,
            status_game=str(scoreboard.status_game) if scoreboard.status_game else None,
            score_local=scoreboard.score_local,
            score_visitor=scoreboard.score_visitor,
            time_restant=scoreboard.time_restant,
            is_final=scoreboard.is_final,
            match_id=str(scoreboard.match_id) if scoreboard.match_id else None
        )

    async def update_scoreboard(self, scoreboard_id: PydanticObjectId, scoreboard: ScoreboardUpdate) -> ScoreboardResponse:
        db_scoreboard = await self.repo.get_by_id(scoreboard_id)
        if not db_scoreboard:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Scoreboard not found"
            )
        
        update_data = scoreboard.model_dump(exclude_unset=True)
        update_data = self._convert_string_ids_to_objectid(update_data)
        
        # Detectar si is_final pasa a True y crear Result
        is_final_now = update_data.get('is_final', None)
        was_final = getattr(db_scoreboard, 'is_final', False)
        updated = await self.repo.update(scoreboard_id, update_data)
        
        # Si is_final se marca como True y antes no lo estaba, crear Result
        if is_final_now is True and not was_final:
            from app.services.result_service import result_service
            from app.schemas.result_schema import ResultCreate
            from datetime import datetime
            result_data = {
                'date_registration': datetime.utcnow().isoformat(),
                'score_local': updated.score_local,
                'score_visitor': updated.score_visitor,
                'scoreboard_id': str(updated.id),
                'winner': None,
                'loser': None,
                'details': None
            }
            # Determinar ganador y perdedor si aplica
            if updated.score_local is not None and updated.score_visitor is not None:
                if updated.score_local > updated.score_visitor:
                    result_data['winner'] = 'local'
                    result_data['loser'] = 'visitor'
                elif updated.score_local < updated.score_visitor:
                    result_data['winner'] = 'visitor'
                    result_data['loser'] = 'local'
                else:
                    result_data['winner'] = 'draw'
                    result_data['loser'] = 'draw'
            await result_service.create_result(ResultCreate(**result_data))
        return ScoreboardResponse(
            id=str(updated.id),
            last_update=updated.last_update,
            status_game=str(updated.status_game) if updated.status_game else None,
            score_local=updated.score_local,
            score_visitor=updated.score_visitor,
            time_restant=updated.time_restant,
            is_final=updated.is_final,
            match_id=str(updated.match_id) if updated.match_id else None
        )

    async def delete_scoreboard(self, scoreboard_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(scoreboard_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Scoreboard not found"
            )

scoreboard_service = ScoreboardService()