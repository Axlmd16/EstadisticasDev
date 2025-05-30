from .base_repository import BaseRepository
from app.models.scoreboard import Scoreboard

class ScoreboardRepository(BaseRepository):
    def __init__(self):
        super().__init__(Scoreboard)
        
    async def find_one(self, match_id: str):
        """
        Busca un scoreboard por match_id.
        :param match_id: ID del partido.
        :return: Scoreboard encontrado o None si no existe.
        """
        from bson import ObjectId
        return await self.model.find_one({"match_id": ObjectId(match_id)})