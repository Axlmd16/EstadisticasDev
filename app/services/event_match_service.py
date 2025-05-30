import logging
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId
from datetime import datetime
from app.repositories.statistic_individual_repository import StatisticIndividualRepository
from app.models.catalog_item import CatalogItem

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
        self.stat_repo = StatisticIndividualRepository()

    async def create_event_match(self, event: EventMatchCreate) -> EventMatchResponse:
        try:
            event_data = event.model_dump(exclude_unset=True)

            athlete_oid = ObjectId(event_data["athlete_id"]) if "athlete_id" in event_data and event_data["athlete_id"] else None
            type_event_oid = ObjectId(event_data["type_event"]) if "type_event" in event_data and event_data["type_event"] else None

            event_data["athlete_id"] = athlete_oid
            event_data["type_event"] = type_event_oid

            doc = await self.repo.create(event_data)

            if athlete_oid and type_event_oid:
                catalog_item = await CatalogItem.get(type_event_oid)
                if catalog_item and catalog_item.description in ["goal", "own goal", "foul", "red card", "yellow card"]:
                    field_to_update = catalog_item.description.replace(" ", "_")

                    # Buscar con el repo, no con collection
                    existing_stat = await self.stat_repo.model.find_one({"athlete_id": athlete_oid})

                    if not existing_stat:
                        new_stat_data = {
                            "athlete_id": athlete_oid,
                            "description": catalog_item.description,
                            "date_generation": datetime.utcnow().isoformat(),
                            "value": 1,
                            field_to_update: 1
                        }
                        await self.stat_repo.create(new_stat_data)
                    else:
                        current_value = getattr(existing_stat, field_to_update, 0)
                        if current_value is None:
                            current_value = 0
                        updated_value = current_value + 1

                        update_data = {
                            field_to_update: updated_value,
                            "date_generation": datetime.utcnow().isoformat()
                        }
                        await self.stat_repo.update(existing_stat.id, update_data)

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
