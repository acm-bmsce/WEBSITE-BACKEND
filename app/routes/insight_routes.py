from fastapi import APIRouter, HTTPException
from typing import List
from app.models.insight import Insight, InsightCreate, InsightUpdate
from beanie import PydanticObjectId

router = APIRouter()

# 1. GET ALL
@router.get("/", response_model=List[Insight])
async def get_insights(limit: int = 20, skip: int = 0):
    # You might want to sort by insertion order or add a date field later
    # For now, natural order (or reverse natural) is fine
    return await Insight.find_all()\
        .skip(skip)\
        .limit(limit)\
        .to_list()

@router.patch("/{id}", response_model=Insight)
async def update_insight(id: PydanticObjectId, insight_data: InsightUpdate):
    insight = await Insight.get(id)
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    
    # Convert Pydantic model to dict, excluding unset values
    update_data = insight_data.dict(exclude_unset=True)
    
    # Update in DB
    await insight.update({"$set": update_data})
    
    return insight

# 2. ADD NEW
@router.post("/", response_model=Insight)
async def add_insight(data: InsightCreate):
    new_insight = Insight(
        personName=data.personName,
        description=data.description,
        image=data.image,
        insta_link=data.insta_link,
        bgColor=data.bgColor # Uses default if not provided
    )
    await new_insight.insert()
    return new_insight

# 3. UPDATE
@router.patch("/{id}", response_model=Insight)
async def update_insight(id: PydanticObjectId, data: InsightUpdate):
    insight = await Insight.get(id)
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    
    # Update only provided fields
    update_data = data.dict(exclude_unset=True)
    await insight.set(update_data)
    return insight

# 4. DELETE
@router.delete("/{id}")
async def delete_insight(id: PydanticObjectId):
    insight = await Insight.get(id)
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    
    await insight.delete()
    return {"message": "Deleted successfully"}