# app/services/match_service.py - VERSIÓN CORREGIDA
from app.repositories.match_repository import MatchRepository
from app.schemas.match_schema import MatchCreate, MatchUpdate, MatchResponse
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class MatchService:
    def __init__(self):
        self.repo = MatchRepository()

    def _convert_string_ids_to_objectid(self, data: dict) -> dict:
        """Convierte string IDs a ObjectId para almacenar en MongoDB"""
        converted_data = data.copy()
        
        if converted_data.get('season_id'):
            converted_data['season_id'] = ObjectId(converted_data['season_id'])
        
        if converted_data.get('team_ids'):
            converted_data['team_ids'] = [
                ObjectId(id_str) for id_str in converted_data['team_ids']
            ]
        
        return converted_data

    async def create_match(self, match: MatchCreate) -> MatchResponse:
        try:
            match_data = match.model_dump(exclude_unset=True)
            match_data = self._convert_string_ids_to_objectid(match_data)
            
            doc = await self.repo.create(match_data)
            
            return MatchResponse(
                id=str(doc.id),
                season_id=str(doc.season_id) if doc.season_id else None,
                team_ids=[str(tid) for tid in doc.team_ids],
                date=doc.date
            )
        except Exception as e:
            logger.error(f"Error creating match: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating match: {str(e)}"
            )

    async def list_matches(self) -> list[MatchResponse]:
        try:
            matches = await self.repo.list()
            return [
                MatchResponse(
                    id=str(match.id),
                    season_id=str(match.season_id) if match.season_id else None,
                    team_ids=[str(tid) for tid in match.team_ids],
                    date=match.date
                ) for match in matches
            ]
        except Exception as e:
            logger.error(f"Error listing matches: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving matches"
            )

    async def get_match(self, match_id: PydanticObjectId) -> MatchResponse:
        match = await self.repo.get_by_id(match_id)
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Match not found"
            )
        
        return MatchResponse(
            id=str(match.id),
            season_id=str(match.season_id) if match.season_id else None,
            team_ids=[str(tid) for tid in match.team_ids],
            date=match.date
        )

    async def update_match(self, match_id: PydanticObjectId, match: MatchUpdate) -> MatchResponse:
        db_match = await self.repo.get_by_id(match_id)
        if not db_match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Match not found"
            )
        
        update_data = match.model_dump(exclude_unset=True)
        update_data = self._convert_string_ids_to_objectid(update_data)
        
        updated = await self.repo.update(match_id, update_data)
        
        return MatchResponse(
            id=str(updated.id),
            season_id=str(updated.season_id) if updated.season_id else None,
            team_ids=[str(tid) for tid in updated.team_ids],
            date=updated.date
        )

    async def delete_match(self, match_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(match_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Match not found"
            )

match_service = MatchService()