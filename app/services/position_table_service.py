# app/services/position_table_service.py - VERSIÓN CORREGIDA
from app.repositories.position_table_repository import PositionTableRepository
from app.schemas.position_table_schema import PositionTableCreate, PositionTableUpdate, PositionTableResponse
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class PositionTableService:
    def __init__(self):
        self.repo = PositionTableRepository()

    def _convert_string_ids_to_objectid(self, data: dict) -> dict:
        """Convierte string IDs a ObjectId para almacenar en MongoDB"""
        converted_data = data.copy()
        
        # Convertir table_rating_id
        if converted_data.get('table_rating_id'):
            converted_data['table_rating_id'] = ObjectId(converted_data['table_rating_id'])
        
        # Convertir team_id
        if converted_data.get('team_id'):
            converted_data['team_id'] = ObjectId(converted_data['team_id'])
        
        return converted_data

    async def create_position_table(self, position_table: PositionTableCreate) -> PositionTableResponse:
        try:
            pt_data = position_table.model_dump(exclude_unset=True)
            pt_data = self._convert_string_ids_to_objectid(pt_data)
            
            doc = await self.repo.create(pt_data)
            
            return PositionTableResponse(
                id=str(doc.id),
                position=doc.position,
                points_total=doc.points_total,
                table_rating_id=str(doc.table_rating_id) if doc.table_rating_id else None,
                team_id=str(doc.team_id) if doc.team_id else None
            )
        except Exception as e:
            logger.error(f"Error creating position table: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating position table: {str(e)}"
            )

    async def list_position_tables(self) -> list[PositionTableResponse]:
        try:
            pts = await self.repo.list()
            return [
                PositionTableResponse(
                    id=str(pt.id),
                    position=pt.position,
                    points_total=pt.points_total,
                    table_rating_id=str(pt.table_rating_id) if pt.table_rating_id else None,
                    team_id=str(pt.team_id) if pt.team_id else None
                ) for pt in pts
            ]
        except Exception as e:
            logger.error(f"Error listing position tables: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving position tables"
            )

    async def get_position_table(self, position_table_id: PydanticObjectId) -> PositionTableResponse:
        pt = await self.repo.get_by_id(position_table_id)
        if not pt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="PositionTable not found"
            )
        
        return PositionTableResponse(
            id=str(pt.id),
            position=pt.position,
            points_total=pt.points_total,
            table_rating_id=str(pt.table_rating_id) if pt.table_rating_id else None,
            team_id=str(pt.team_id) if pt.team_id else None
        )

    async def update_position_table(self, position_table_id: PydanticObjectId, position_table: PositionTableUpdate) -> PositionTableResponse:
        db_pt = await self.repo.get_by_id(position_table_id)
        if not db_pt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="PositionTable not found"
            )
        
        # ✅ CORREGIDO: Usar model_dump() con exclude_unset y convertir IDs
        update_data = position_table.model_dump(exclude_unset=True)
        update_data = self._convert_string_ids_to_objectid(update_data)
        
        updated = await self.repo.update(position_table_id, update_data)
        
        return PositionTableResponse(
            id=str(updated.id),
            position=updated.position,
            points_total=updated.points_total,
            table_rating_id=str(updated.table_rating_id) if updated.table_rating_id else None,
            team_id=str(updated.team_id) if updated.team_id else None
        )

    async def delete_position_table(self, position_table_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(position_table_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="PositionTable not found"
            )

position_table_service = PositionTableService()