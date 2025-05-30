# app/services/statistics_team_service.py - VERSIÓN CORREGIDA
import logging
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId

from app.repositories.statistics_team_repository import StatisticTeamRepository
from app.schemas.statistics_team_schema import (
    StatisticTeamCreate,
    StatisticTeamUpdate,
    StatisticTeamResponse,
)

logger = logging.getLogger(__name__)

class StatisticTeamService:
    def __init__(self):
        self.repo = StatisticTeamRepository()

    def _convert_string_ids_to_objectid(self, data: dict) -> dict:
        """Convierte string IDs a ObjectId para almacenar en MongoDB"""
        converted_data = data.copy()
        
        # Convertir id_team
        if converted_data.get('id_team'):
            converted_data['id_team'] = ObjectId(converted_data['id_team'])
        
        return converted_data

    async def create_statistic_team(self, stat: StatisticTeamCreate) -> StatisticTeamResponse:
        try:
            # ✅ CORREGIDO: Usar model_dump() y convertir IDs
            stat_data = stat.model_dump(exclude_unset=True)
            stat_data = self._convert_string_ids_to_objectid(stat_data)

            doc = await self.repo.create(stat_data)
            
            # ✅ CORREGIDO: Usar el nombre correcto del atributo del modelo
            return StatisticTeamResponse(
                id=str(doc.id),
                description=doc.description,
                date_generation=doc.date_generation,
                value=doc.value,
                games_played=doc.games_played,
                matches_drawn=doc.matches_drawn,  # ✅ CORREGIDO: del modelo
                matches_lost=doc.matches_lost,
                matches_won=doc.matches_won,
                points=doc.points,
                id_team=str(doc.id_team) if doc.id_team else None,
            )
        except Exception as e:
            logger.error(f"Error creating statistic team: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating statistic team: {str(e)}"
            )

    async def list_statistic_teams(self) -> list[StatisticTeamResponse]:
        try:
            stats = await self.repo.list()
            return [
                StatisticTeamResponse(
                    id=str(s.id),
                    description=s.description,
                    date_generation=s.date_generation,
                    value=s.value,
                    games_played=s.games_played,
                    matches_drawn=s.matches_drawn,  #
                    matches_lost=s.matches_lost,
                    matches_won=s.matches_won,
                    points=s.points,
                    id_team=str(s.id_team) if s.id_team else None,
                ) for s in stats
            ]
        except Exception as e:
            logger.error(f"Error listing statistic teams: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving statistic teams"
            )

    async def get_statistic_team(self, stat_id: PydanticObjectId) -> StatisticTeamResponse:
        stat = await self.repo.get_by_id(stat_id)
        if not stat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="StatisticTeam not found"
            )
        
        return StatisticTeamResponse(
            id=str(stat.id),
            description=stat.description,
            date_generation=stat.date_generation,
            value=stat.value,
            games_played=stat.games_played,
            matches_drawn=stat.matches_drawn,  
            matches_lost=stat.matches_lost,
            matches_won=stat.matches_won,
            points=stat.points,
            id_team=str(stat.id_team) if stat.id_team else None,
        )

    async def update_statistic_team(self, stat_id: PydanticObjectId, stat: StatisticTeamUpdate) -> StatisticTeamResponse:
        db_stat = await self.repo.get_by_id(stat_id)
        if not db_stat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="StatisticTeam not found"
            )

        update_data = stat.model_dump(exclude_unset=True)
        update_data = self._convert_string_ids_to_objectid(update_data)

        updated = await self.repo.update(stat_id, update_data)
        
        return StatisticTeamResponse(
            id=str(updated.id),
            description=updated.description,
            date_generation=updated.date_generation,
            value=updated.value,
            games_played=updated.games_played,
            matches_drawn=updated.matches_drawn, 
            matches_lost=updated.matches_lost,
            matches_won=updated.matches_won,
            points=updated.points,
            id_team=str(updated.id_team) if updated.id_team else None,
        )

    async def delete_statistic_team(self, stat_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(stat_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="StatisticTeam not found"
            )

    async def update_from_position_table(self, position_table):
        """
        Actualiza los campos de StatisticTeam (games_played, matches_won, matches_drawn, matches_lost, points)
        a partir de los datos de una PositionTable. Si no existe StatisticTeam, lo crea automáticamente con los valores correctos.
        """
        if not position_table.team_id:
            logger.warning("PositionTable sin team_id, omitiendo actualización de StatisticTeam")
            return

        # Asegurarse de que el team_id es ObjectId
        team_id = position_table.team_id
        if not isinstance(team_id, ObjectId):
            try:
                team_id = ObjectId(team_id)
            except Exception as e:
                logger.error(f"No se pudo convertir team_id a ObjectId: {position_table.team_id} - {e}")
                return

        from app.models.position_table import PositionTable
        all_positions = await PositionTable.find({"team_id": team_id}).to_list()
        games_played = len(all_positions)
        # Calcular victorias, empates, derrotas (si tienes esa lógica, aquí solo ejemplo con 0)
        matches_won = 0
        matches_drawn = 0
        matches_lost = 0
        # Si tienes lógica para calcular estos valores, agrégala aquí

        stat_team = await self.repo.find_one({"id_team": team_id})
        if not stat_team:
            logger.warning(f"No se encontró StatisticTeam para el equipo {team_id}, creando uno nuevo...")
            from app.schemas.statistics_team_schema import StatisticTeamCreate
            doc = await self.create_statistic_team(StatisticTeamCreate(
                id_team=str(team_id),
                points=position_table.points_total or 0,
                games_played=games_played,
                matches_won=matches_won,
                matches_drawn=matches_drawn,
                matches_lost=matches_lost
            ))
            stat_team = await self.repo.get_by_id(ObjectId(doc.id))
            if not stat_team:
                logger.error(f"No se pudo crear StatisticTeam para el equipo {team_id}")
                return

        # Actualizar campos básicos
        update_data = {
            "points": position_table.points_total or 0,
            "games_played": games_played,
            "matches_won": matches_won,
            "matches_drawn": matches_drawn,
            "matches_lost": matches_lost
        }

        await self.repo.update(stat_team.id, update_data)
        logger.info(f"StatisticTeam actualizado para el equipo {team_id}")

statistic_team_service = StatisticTeamService()