# app/services/scoreboard_service.py - VERSIÓN CORREGIDA
from app.repositories.scoreboard_repository import ScoreboardRepository
from app.schemas.scoreboard_schema import ScoreboardCreate, ScoreboardUpdate, ScoreboardResponse
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId
from datetime import datetime
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

    async def _create_result_for_match(self, scoreboard) -> None:
        """Crea un resultado cuando el scoreboard se marca como final"""
        try:
            from app.services.result_service import result_service
            from app.schemas.result_schema import ResultCreate
            
            # Determinar ganador y perdedor
            winner = None
            loser = None
            details = f"Resultado final: {scoreboard.score_local} - {scoreboard.score_visitor}"
            
            if scoreboard.score_local is not None and scoreboard.score_visitor is not None:
                if scoreboard.score_local > scoreboard.score_visitor:
                    winner = 'local'
                    loser = 'visitor'
                elif scoreboard.score_local < scoreboard.score_visitor:
                    winner = 'visitor'
                    loser = 'local'
                else:
                    winner = 'draw'
                    loser = 'draw'
                    details = f"Empate: {scoreboard.score_local} - {scoreboard.score_visitor}"
            
            result_data = ResultCreate(
                date_registration=datetime.utcnow().isoformat(),
                score_local=scoreboard.score_local,
                score_visitor=scoreboard.score_visitor,
                scoreboard_id=str(scoreboard.id),
                winner=winner,
                loser=loser,
                details=details
            )
            
            await result_service.create_result(result_data)
            logger.info(f"Result created for scoreboard {scoreboard.id}")
            
        except Exception as e:
            logger.error(f"Error creating result for scoreboard {scoreboard.id}: {str(e)}")
            # No propagar el error para no bloquear la actualización del scoreboard

    async def _update_position_tables(self, scoreboard) -> None:
        """Actualiza las tablas de posiciones basado en el resultado"""
        try:
            from app.models.match import Match
            from app.models.table_rating import TableRating
            from app.models.position_table import PositionTable
            
            if not scoreboard.match_id:
                logger.warning("Scoreboard doesn't have match_id, skipping position update")
                return
            
            # Obtener el match
            match = await Match.get(scoreboard.match_id)
            if not match:
                logger.warning(f"Match {scoreboard.match_id} not found")
                return
            
            # Buscar la tabla de posiciones activa (asumiendo que hay una por defecto)
            # Puedes modificar esta lógica según tus necesidades
            table_rating = await TableRating.find_one({})
            if not table_rating:
                logger.warning("No active TableRating found")
                return
            
            # Calcular puntos para cada equipo
            points_local = 0
            points_visitor = 0
            
            if scoreboard.score_local is not None and scoreboard.score_visitor is not None:
                if scoreboard.score_local > scoreboard.score_visitor:
                    points_local = 3  # Victoria local
                    points_visitor = 0  # Derrota visitante
                elif scoreboard.score_local < scoreboard.score_visitor:
                    points_local = 0  # Derrota local
                    points_visitor = 3  # Victoria visitante
                else:
                    points_local = 1  # Empate local
                    points_visitor = 1  # Empate visitante
            
            # Actualizar posición del equipo local
            await self._update_team_position(
                table_rating.id, 
                match.local_team_id, 
                points_local
            )
            
            # Actualizar posición del equipo visitante
            await self._update_team_position(
                table_rating.id, 
                match.visitor_team_id, 
                points_visitor,
            )
            
            logger.info(f"Tabla de posiciones actualizada para el partido {match.id}")
            
            # Recalcular posiciones: ordenar por puntos_total descendente y asignar posición
            posiciones_actualizadas = await PositionTable.find({"table_rating_id": table_rating.id}).to_list()
            posiciones_ordenadas = sorted(posiciones_actualizadas, key=lambda x: x.points_total or 0, reverse=True)
            for idx, pos in enumerate(posiciones_ordenadas, start=1):
                pos.position = idx
                await pos.save()

            # Actualizar StatisticTeam de cada equipo
            from app.services.statistics_team_service import statistic_team_service
            for pos in posiciones_ordenadas:
                await statistic_team_service.update_from_position_table(pos)

        except Exception as e:
            logger.error(f"Error updating position tables: {str(e)}")
            # No propagar el error

    async def _update_team_position(self, table_rating_id: ObjectId, team_id: ObjectId, points: int) -> None:
        """Actualiza o crea la posición de un equipo específico"""
        from app.models.position_table import PositionTable
        
        # Buscar posición existente
        position = await PositionTable.find_one({
            "table_rating_id": table_rating_id,
            "team_id": team_id
        })
        
        if position:
            # Actualizar puntos existentes
            position.points_total = (position.points_total or 0) + points
            await position.replace()  
        else:
            # Crear nueva posición
            new_position = PositionTable(
                position=None,  # Se calculará después
                points_total=points,
                table_rating_id=table_rating_id,
                team_id=team_id
            )
            await new_position.insert()
            
            # Agregar a la lista de posiciones del TableRating
            from app.models.table_rating import TableRating
            table_rating = await TableRating.get(table_rating_id)
            if table_rating:
                if new_position.id not in table_rating.positions:
                    table_rating.positions.append(new_position.id)
                    await table_rating.replace()

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
        is_final_now = update_data.get('is_final', None)
        was_final = getattr(db_scoreboard, 'is_final', False)
        
        # Actualizar el scoreboard
        updated = await self.repo.update(scoreboard_id, update_data)

        if is_final_now is True and not was_final:
            logger.info(f"Scoreboard {scoreboard_id} marked as final, triggering post-game actions")
            
            # Crear resultado
            await self._create_result_for_match(updated)
            
            # Actualizar tabla de posiciones
            await self._update_position_tables(updated)
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
    
    # ✅ MÉTODO DEDICADO para finalizar
    async def finalize_scoreboard(self, scoreboard_id: PydanticObjectId) -> ScoreboardResponse:
        """Método específico para finalizar un scoreboard"""
        return await self.update_scoreboard(
            scoreboard_id, 
            ScoreboardUpdate(is_final=True)
        )

    async def finalize_scoreboard(self, scoreboard_id: PydanticObjectId) -> ScoreboardResponse:
        """Método específico para finalizar un scoreboard"""
        return await self.update_scoreboard(
            scoreboard_id, 
            ScoreboardUpdate(is_final=True)
        )

scoreboard_service = ScoreboardService()