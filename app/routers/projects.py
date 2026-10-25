from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Project, ProjectIn

router = APIRouter(prefix="/projects", tags=["projects"])

def get_or_404(session: Session, project_id: int):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("")
def list_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project)).all()

@router.get("/{project_id}")
def get_project(project_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, project_id)

@router.post("", status_code=201)
def add_project(data: ProjectIn, session: Session = Depends(get_session)):
    exists = session.exec(select(Project).where(Project.title == data.title)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Project already exists")
    project = Project(**data.model_dump())
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.put("/{project_id}")
def update_project(project_id: int, data: ProjectIn, session: Session = Depends(get_session)):
    project = get_or_404(session, project_id)
    project.title = data.title
    project.description = data.description
    project.link = data.link
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = get_or_404(session, project_id)
    if project.topics:
        raise HTTPException(status_code=400, detail="Project still has topics")
    session.delete(project)
    session.commit()
    return {"deleted": project_id}

@router.get("/{project_id}/topics")
def project_topics(project_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, project_id).topics
