from fastapi import APIRouter, HTTPException, Depends # <--- Added Depends
from typing import List
from app.models.project import Project, ProjectCreate
from app.routes.user_routes import get_master_admin # <--- Import the Guard
from beanie import PydanticObjectId

router = APIRouter()

@router.post("/submit", response_model=Project)
async def submit_project(project_data: ProjectCreate):
    new_project = Project(
        title=project_data.title,
        description=project_data.description,
        team_members=project_data.team_members,
        github_link=project_data.github_link,
        demo_link=project_data.demo_link,
        image_url=project_data.image_url,
        status="PENDING"
    )
    await new_project.insert()
    return new_project

@router.get("/showcase", response_model=List[Project])
async def get_public_projects(limit: int = 20, skip: int = 0):
    # Sort by submission date (newest first)
    return await Project.find(Project.status == "APPROVED")\
        .sort(-Project.submission_date)\
        .skip(skip)\
        .limit(limit)\
        .to_list()

@router.patch("/{project_id}", response_model=Project, dependencies=[Depends(get_master_admin)])
async def update_project(project_id: PydanticObjectId, project_data: ProjectCreate):
    project = await Project.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Convert Pydantic model to dict, excluding unset values
    update_data = project_data.dict(exclude_unset=True)
    
    # Update the project in DB
    await project.update({"$set": update_data})
    
    return project

@router.get("/all", response_model=List[Project], dependencies=[Depends(get_master_admin)])
async def get_all_projects(limit: int = 20, skip: int = 0):
    return await Project.find_all()\
        .sort(-Project.submission_date)\
        .skip(skip)\
        .limit(limit)\
        .to_list()


@router.patch("/{project_id}/approve", dependencies=[Depends(get_master_admin)]) # <--- LOCKED
async def approve_project(project_id: str):
    project = await Project.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.status = "APPROVED"
    await project.save()
    return {"message": "Project approved successfully", "project": project}


@router.delete("/{project_id}", dependencies=[Depends(get_master_admin)])
async def delete_project(project_id: PydanticObjectId):
    project = await Project.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await project.delete()
    return {"message": "Project deleted successfully"}