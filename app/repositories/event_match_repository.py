from .base_repository import BaseRepository
from app.models.event_match import EventMatch

class EventMatchRepository(BaseRepository):
    def __init__(self):
        super().__init__(EventMatch)
