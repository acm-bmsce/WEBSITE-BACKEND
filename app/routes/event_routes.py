from fastapi import APIRouter, HTTPException
from typing import List
from app.models.event import Event, EventCreate, EventUpdate 
from datetime import datetime
from beanie import PydanticObjectId

router = APIRouter()

# 1. GET ALL EVENTS
@router.get("/", response_model=List[Event])
async def get_events():
    # Fetch all events and sort by date (descending)
    events = await Event.find_all().sort(-Event.date).to_list()
    return events

# 2. CREATE A NEW EVENT
@router.post("/", response_model=Event)
async def create_event(event_data: EventCreate):
    # Logic to convert "21-01-2024" to a real Date object
    try:
        parsed_date = datetime.strptime(event_data.date_str, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY")

    # Logic to handle attendees (convert string to int)
    attendees_int = int(event_data.attendees) if str(event_data.attendees).isdigit() else 0

    # Create the DB object
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        date=parsed_date,
        image=event_data.image,
        fullDescription=event_data.fullDescription,
        outcomes=event_data.outcomes,
        gallery=event_data.gallery,
        location=event_data.location,
        attendees=attendees_int
    )
    
    await new_event.insert()
    return new_event


@router.patch("/{event_id}", response_model=Event)
async def update_event(event_id: PydanticObjectId, event_data: EventUpdate):
    # Find the event
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Prepare data for update (exclude fields that were not sent)
    update_data = event_data.dict(exclude_unset=True)

    # If date is being updated, handle the conversion
    if "date_str" in update_data:
        try:
            update_data["date"] = datetime.strptime(update_data["date_str"], "%d-%m-%Y")
            del update_data["date_str"] # Remove string date, we only save real date object
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")

    # Update the database document
    await event.set(update_data)
    return event

# 4. DELETE AN EVENT
@router.delete("/{event_id}")
async def delete_event(event_id: PydanticObjectId):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    await event.delete()
    return {"message": "Event deleted successfully"}