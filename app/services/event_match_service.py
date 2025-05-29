from app.repositories.event_match_repository import EventMatchRepository
from app.schemas.event_match_schema import EventMatchCreate, EventMatchUpdate, EventMatchResponse
from beanie import PydanticObjectId
from fastapi import HTTPException

class EventMatchService:
    def __init__(self):
        self.repo = EventMatchRepository()

    async def create_event_match(self, event: EventMatchCreate) -> EventMatchResponse:
        doc = await self.repo.create(event.dict())
        return EventMatchResponse(**doc.dict())

    async def list_event_matches(self) -> list[EventMatchResponse]:
        events = await self.repo.list()
        return [EventMatchResponse(**e.dict()) for e in events]

    async def get_event_match(self, event_id: PydanticObjectId) -> EventMatchResponse:
        event = await self.repo.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="EventMatch not found")
        return EventMatchResponse(**event.dict())

    async def update_event_match(self, event_id: PydanticObjectId, event: EventMatchUpdate) -> EventMatchResponse:
        db_event = await self.repo.get_by_id(event_id)
        if not db_event:
            raise HTTPException(status_code=404, detail="EventMatch not found")
        updated = await self.repo.update(event_id, event.dict(exclude_unset=True))
        return EventMatchResponse(**updated.dict())

    async def delete_event_match(self, event_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(event_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="EventMatch not found")

event_match_service = EventMatchService()
