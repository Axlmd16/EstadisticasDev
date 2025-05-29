import logging
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId

from app.repositories.event_match_repository import EventMatchRepository
from app.schemas.event_match_schema import (
    EventMatchCreate,
    EventMatchUpdate,
    EventMatchResponse,
)

logger = logging.getLogger(__name__)

class EventMatchService:
    def __init__(self):
        self.repo = EventMatchRepository()

    async def create_event_match(self, event: EventMatchCreate) -> EventMatchResponse:
        try:
            event_data = event.model_dump(exclude_unset=True)

            if "type_event" in event_data and event_data["type_event"]:
                event_data["type_event"] = ObjectId(event_data["type_event"])

            if "athlete_id" in event_data and event_data["athlete_id"]:
                event_data["athlete_id"] = ObjectId(event_data["athlete_id"])

            doc = await self.repo.create(event_data)
            return EventMatchResponse(
                id=str(doc.id),
                description=doc.description,
                date_registration=doc.date_registration,
                minute=doc.minute,
                type_event=str(doc.type_event) if doc.type_event else None,
                athlete_id=str(doc.athlete_id) if doc.athlete_id else None,
            )
        except Exception as e:
            logger.error(f"Error creating event match: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating event match: {str(e)}"
            )

    async def list_event_matches(self) -> list[EventMatchResponse]:
        try:
            events = await self.repo.list()
            return [
                EventMatchResponse(
                    id=str(e.id),
                    description=e.description,
                    date_registration=e.date_registration,
                    minute=e.minute,
                    type_event=str(e.type_event) if e.type_event else None,
                    athlete_id=str(e.athlete_id) if e.athlete_id else None,
                ) for e in events
            ]
        except Exception as e:
            logger.error(f"Error listing event matches: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving event matches"
            )

    async def get_event_match(self, event_id: PydanticObjectId) -> EventMatchResponse:
        event = await self.repo.get_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="EventMatch not found")
        return EventMatchResponse(
            id=str(event.id),
            description=event.description,
            date_registration=event.date_registration,
            minute=event.minute,
            type_event=str(event.type_event) if event.type_event else None,
            athlete_id=str(event.athlete_id) if event.athlete_id else None,
        )

    async def update_event_match(self, event_id: PydanticObjectId, event: EventMatchUpdate) -> EventMatchResponse:
        db_event = await self.repo.get_by_id(event_id)
        if not db_event:
            raise HTTPException(status_code=404, detail="EventMatch not found")

        update_data = event.model_dump(exclude_unset=True)

        if "type_event" in update_data and update_data["type_event"]:
            update_data["type_event"] = ObjectId(update_data["type_event"])

        if "athlete_id" in update_data and update_data["athlete_id"]:
            update_data["athlete_id"] = ObjectId(update_data["athlete_id"])

        updated = await self.repo.update(event_id, update_data)
        return EventMatchResponse(
            id=str(updated.id),
            description=updated.description,
            date_registration=updated.date_registration,
            minute=updated.minute,
            type_event=str(updated.type_event) if updated.type_event else None,
            athlete_id=str(updated.athlete_id) if updated.athlete_id else None,
        )

    async def delete_event_match(self, event_id: PydanticObjectId) -> None:
        deleted = await self.repo.delete(event_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="EventMatch not found")

event_match_service = EventMatchService()
