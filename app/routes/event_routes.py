from fastapi import APIRouter, HTTPException,Query
from typing import List, Optional
from app.models.event import Event, EventCreate, EventUpdate, EventResponse
from datetime import datetime
from beanie import PydanticObjectId
from app.models.registration import Registration,RegistrationCreate

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

# 5. EVENT REGISTRATION
@router.post("/{event_id}/register")
async def register_for_event(event_id: PydanticObjectId, reg_data: RegistrationCreate):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    # Check manual toggle
    if not getattr(event, "registration_open", True):
        raise HTTPException(status_code=400, detail="Registrations are closed for this event.")

    # ✅ ENFORCE CAPACITY LIMIT ON BACKEND
    limit = getattr(event, "registration_limit", 0)
    if limit > 0:
        current_count = await Registration.find({"event_id": event_id}).count()
        if current_count >= limit:
            raise HTTPException(status_code=400, detail="Registration full! The capacity limit has been reached.")

    # Prevent duplicate registrations
    existing_reg = await Registration.find_one({
        "event_id": event_id, 
        "email": reg_data.email
    })
    if existing_reg:
        raise HTTPException(status_code=400, detail="Email already registered for this event.")

    # Save the new registration
    new_registration = Registration(
        event_id=event_id,
        is_team_event=reg_data.is_team_event,
        team_name=reg_data.team_name,
        name=reg_data.name,
        email=reg_data.email,
        phone=reg_data.phone,
        usn=reg_data.usn,
        department=reg_data.department
    )
    await new_registration.insert()
    return {"message": "Successfully registered!"}

@router.get("/{event_id}/registrations")
async def get_registrations_for_event(event_id: PydanticObjectId):
    # Find all registrations linked to this event
    registrations = await Registration.find(Registration.event_id == event_id).to_list()
    return registrations

# 1.5 GET A SINGLE EVENT BY ID
@router.get("/{event_id}", response_model=EventResponse)
async def get_single_event(event_id: PydanticObjectId):
    event = await Event.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # ✅ ENFORCE CAPACITY LIMIT ON UI: 
    # If there's a limit, count current registrations.
    limit = getattr(event, "registration_limit", 0)
    if limit > 0 and getattr(event, "registration_open", True):
        # Count how many people are already registered
        current_count = await Registration.find({"event_id": event_id}).count()
        if current_count >= limit:
            # Tell the frontend the event is closed so it hides the form!
            event.registration_open = False 
            
    return event