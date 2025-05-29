from .base_repository import BaseRepository
from app.models.catalog_item import CatalogItem

class CatalogItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(CatalogItem)
