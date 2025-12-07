from fastapi import APIRouter, HTTPException
from typing import List
from app.models.project import Project, ProjectCreate

router = APIRouter()

# 1. PUBLIC: Submit a new project
@router.post("/submit", response_model=Project)
async def submit_project(project_data: ProjectCreate):
    new_project = Project(
        title=project_data.title,
        description=project_data.description,
        team_members=project_data.team_members,
        github_link=project_data.github_link,
        demo_link=project_data.demo_link,
        image_url=project_data.image_url,
        status="PENDING" # Force status to Pending on submission
    )
    await new_project.insert()
    return new_project

# 2. PUBLIC: Get only APPROVED projects (For the Showcase Page)
@router.get("/showcase", response_model=List[Project])
async def get_public_projects():
    projects = await Project.find(Project.status == "APPROVED").to_list()
    return projects

# 3. ADMIN: Get ALL projects (To review them)
@router.get("/all", response_model=List[Project])
async def get_all_projects():
    projects = await Project.find_all().to_list()
    return projects

# 4. ADMIN: Approve a project
@router.patch("/{project_id}/approve")
async def approve_project(project_id: str):
    project = await Project.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.status = "APPROVED"
    await project.save()
    return {"message": "Project approved successfully", "project": project}