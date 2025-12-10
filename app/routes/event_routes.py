from fastapi import APIRouter, HTTPException
from typing import List
from app.models.event import Event, EventCreate, EventUpdate, EventResponse
from datetime import datetime
from beanie import PydanticObjectId

router = APIRouter()

# 1. GET EVENTS (With Pagination)
@router.get("/", response_model=List[EventResponse])
async def get_events(limit: int = 20, skip: int = 0, featured: bool = None):
    query = Event.find_all()
    
    # If featured=True is passed, return ONLY featured events
    if featured is not None:
        query = query.find(Event.is_featured == featured)
        
    # Sort by date (newest first)
    events = await query.sort(-Event.date).skip(skip).limit(limit).to_list()
    return events
# 2. CREATE A NEW EVENT
@router.post("/", response_model=EventResponse)
async def create_event(event_data: EventCreate):
    # Logic to convert "21-01-2024" string to a real Date object
    try:
        parsed_date = datetime.strptime(event_data.date_str, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY")

    # Logic to handle attendees (ensure it's an int)
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
        attendees=attendees_int,
        registration_link=event_data.registration_link
    )
    
    await new_event.insert()
    return new_event

# 3. UPDATE AN EVENT
@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(event_id: PydanticObjectId, event_data: EventUpdate):
    # Find the event
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Filter out None values (only update what was sent)
    update_query = event_data.dict(exclude_unset=True)
    
    # Handle Date conversion if provided
    if "date_str" in update_query:
        d_str = update_query.pop("date_str")
        try:
            update_query["date"] = datetime.strptime(d_str, "%d-%m-%Y")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY")

    # Apply updates
    await event.update({"$set": update_query})
    
    # Refetch to return updated data
    updated_event = await Event.get(event_id)
    return updated_event

# 4. DELETE AN EVENT
@router.delete("/{event_id}")
async def delete_event(event_id: PydanticObjectId):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    await event.delete()
    return {"message": "Event deleted successfully"}