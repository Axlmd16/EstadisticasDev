from .base_repository import BaseRepository
from app.models.table_rating import TableRating

class TableRatingRepository(BaseRepository):
    def __init__(self):
        super().__init__(TableRating)
