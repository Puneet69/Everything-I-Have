from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Topic

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("")
def stats(session: Session = Depends(get_session)):
    done = session.exec(select(Topic).where(Topic.status == "done")).all()
    return {"done": len(done)}
