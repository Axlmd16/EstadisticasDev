import redis.asyncio as redis
from app.config import settings
import logging
import json

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.client = None
        self._connect()

    def _connect(self):
        logger.info("Conectando a Redis...")
        try:
            self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            logger.info("Conexión a Redis establecida exitosamente")
        except Exception as e:
            logger.error(f"Error conectando a Redis: {str(e)}")
            raise

    async def set(self, key: str, value: any, expire: int = None):
        """Almacenar un valor en Redis"""
        try:
            str_value = json.dumps(value) if not isinstance(value, (str, int, float)) else str(value)
            await self.client.set(key, str_value)
            if expire:
                await self.client.expire(key, expire)
        except Exception as e:
            logger.error(f"Error al escribir en Redis: {str(e)}")
            raise

    async def get(self, key: str):
        """Obtener un valor de Redis"""
        try:
            value = await self.client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            logger.error(f"Error al leer de Redis: {str(e)}")
            raise

    async def delete(self, key: str):
        """Eliminar un valor de Redis"""
        try:
            await self.client.delete(key)
        except Exception as e:
            logger.error(f"Error al eliminar de Redis: {str(e)}")
            raise

    async def close(self):
        """Cerrar la conexión a Redis"""
        logger.info("Cerrando conexión a Redis...")
        try:
            await self.client.close()
            logger.info("Conexión a Redis cerrada")
        except Exception as e:
            logger.error(f"Error al cerrar la conexión a Redis: {str(e)}")
            raise

redis_client = RedisClient()
