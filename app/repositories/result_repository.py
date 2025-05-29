from .base_repository import BaseRepository
from app.models.result import Result

class ResultRepository(BaseRepository):
    def __init__(self):
        super().__init__(Result)
