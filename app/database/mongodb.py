from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging
from beanie import init_beanie
from app.models.arbitre import Arbitre
from app.models.athlete import Athlete
from app.models.catalog_item import CatalogItem
from app.models.competition import Competition
from app.models.event_match import EventMatch
from app.models.match import Match
from app.models.position_table import PositionTable
from app.models.result import Result
from app.models.scoreboard import Scoreboard
from app.models.season import Season
from app.models.table_rating import TableRating
from app.models.team import Team
from app.models.statistic_competence import StatisticCompetence
from app.models.statistic_individual import StatisticIndividual
from app.models.statistic_season import StatisticSeason
from app.models.statistic_team import StatisticTeam

logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    
    async def connect_to_database(self):
        logger.info("Conectando a MongoDB...")
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URL)
            await init_beanie(
                database=self.client.get_default_database(),
                document_models=[
                    Arbitre, Athlete, CatalogItem, Competition,
                    EventMatch, Match, PositionTable, Result,
                    Scoreboard, Season, TableRating, Team,
                    StatisticCompetence, StatisticIndividual,
                    StatisticSeason, StatisticTeam
                ]
            )
            logger.info("Conexión a MongoDB establecida exitosamente")
        except Exception as e:
            logger.error(f"Error conectando a MongoDB: {str(e)}")
            raise

    async def close_database_connection(self):
        logger.info("Cerrando conexión a MongoDB...")
        if self.client:
            self.client.close()
            logger.info("Conexión a MongoDB cerrada")

    def get_database(self):
        if not self.client:
            raise RuntimeError("No hay conexión a MongoDB establecida")
        return self.client.get_default_database()

mongodb = MongoDB()

async def connect_to_mongo():
    await mongodb.connect_to_database()

async def close_mongo_connection():
    await mongodb.close_database_connection()

def get_database():
    return mongodb.get_database()
