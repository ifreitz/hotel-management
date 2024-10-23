from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

from app.models import Event


router = APIRouter()


class EventSchema(BaseModel):
    hotel_id: int
    timestamp: datetime
    rpg_status: int
    room_id: int
    night_of_stay: date

    class Config:
        orm_mode = True


@router.post("/events", response_model=EventSchema)
async def create_event(event: EventSchema):
    """
    Creates a new event in the database.

    This endpoint allows for the creation of a new event. The event details are expected in the request body in JSON format.

    Parameters:
    - event (EventSchema): The event details to be created. This includes hotel_id, timestamp, rpg_status, room_id, and night_of_stay.

    Returns:
    - EventSchema: The created event object.
    """
    event_obj = await Event.create(**event.dict())
    return event_obj


@router.get("/events", response_model=List[EventSchema])
async def get_events(
    hotel_id: Optional[int] = None,
    updated__gte: Optional[datetime] = None,
    updated__lte: Optional[datetime] = None,
    rpg_status: Optional[int] = None,
    room_id: Optional[int] = None,
    night_of_stay__gte: Optional[date] = None,
    night_of_stay__lte: Optional[date] = None,
):
    """
    Retrieves a list of events based on various filters.

    This endpoint allows for filtering events by hotel ID, update date range, RPG status, room ID, and night of stay date range.

    Parameters:
    - hotel_id (Optional[int]): The ID of the hotel to filter events by.
    - updated__gte (Optional[datetime]): The start date and time for filtering events by their update timestamp.
    - updated__lte (Optional[datetime]): The end date and time for filtering events by their update timestamp.
    - rpg_status (Optional[int]): The RPG status to filter events by.
    - room_id (Optional[int]): The ID of the room to filter events by.
    - night_of_stay__gte (Optional[date]): The start date for filtering events by their night of stay.
    - night_of_stay__lte (Optional[date]): The end date for filtering events by their night of stay.

    Returns:
    - List[EventSchema]: A list of events that match the specified filters.
    """
    events_query = Event.all().order_by("timestamp")
    if hotel_id:
        events_query = events_query.filter(hotel_id=hotel_id)
    if updated__gte:
        events_query = events_query.filter(timestamp__gte=updated__gte)
    if updated__lte:
        events_query = events_query.filter(timestamp__lte=updated__lte)
    if rpg_status:
        events_query = events_query.filter(rpg_status=rpg_status)
    if room_id:
        events_query = events_query.filter(room_id=room_id)
    if night_of_stay__gte:
        events_query = events_query.filter(night_of_stay__gte=night_of_stay__gte)
    if night_of_stay__lte:
        events_query = events_query.filter(night_of_stay__lte=night_of_stay__lte)
    
    return await events_query
