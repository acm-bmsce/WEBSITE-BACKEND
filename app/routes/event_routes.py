from fastapi import APIRouter, HTTPException,Query
from typing import List, Optional
from app.models.event import Event, EventCreate, EventUpdate, EventResponse
from datetime import datetime
from beanie import PydanticObjectId

router = APIRouter()

# 1. GET EVENTS (With Pagination & Filtering)
@router.get("/", response_model=List[EventResponse])
async def get_events(
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
    featured: Optional[bool] = None,
):
    query_filters = {}

    # Featured filter (optional)
    if featured is not None:
        query_filters["is_featured"] = featured

    events = (
        await Event
        .find(query_filters)
        .sort(-Event.date)   # ✅ ALWAYS newest first
        .skip(skip)
        .limit(limit)
        .to_list()
    )

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
        registration_link=event_data.registration_link,
        
        # ✅ FIX: This was missing! Now it saves the featured status.
        is_featured=event_data.is_featured 
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