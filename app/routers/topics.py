# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Literal
# from app.data import get_topics
#
# router = APIRouter(prefix="/topics", tags=["topics"])
#
# class Topic(BaseModel):
#     title: str
#     status: Literal["learning" , "done"] = "learning"
#
# @router.get("")
# def list_topics(status: str | None = None):
#     if status:
#         return [t for t in get_topics() if t["status"]== status]
#     return get_topics()
#
# @router.get("/{title}")
# def get_topic(title: str):
#     for t in get_topics():
#         if t["title"]==title:
#             return t
#     raise HTTPException(status_code= 404 , detail="Topic not found")
#
# @router.post("", status_code=201)
# def add_topic(topic: Topic):
#     for t in get_topics():
#         if t["title"]==topic.title:
#             raise HTTPException(status_code= 404 , detail="Topic already exists")
#     get_topics().append(topic.model_dump())
#     return topic
#
# @router.put("/{title}")
# def update_topic(title: str, topic: Topic):
#     for t in get_topics():
#         if t["title"]==title:
#             t["status"] = topic.status
#             return t
#     raise HTTPException(status_code= 404 , detail="Topic not found")
#
# @router.delete("/{title}")
# def delete_topic(title: str):
#     for t in get_topics():
#         if t["title"]==title:
#             get_topics().remove(t)
#             return {"deleted": title}
#     raise HTTPException(status_code= 404 , detail="Topic not found")
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Topic, TopicIn

router = APIRouter(prefix="/topics", tags=["topics"])

def find_topic(session: Session, title: str):
    return session.exec(select(Topic).where(Topic.title == title)).first()

@router.get("")
def list_topics(status: str | None = None, session: Session = Depends(get_session)):
    query = select(Topic)
    if status:
        query = query.where(Topic.status == status)
    return session.exec(query).all()

@router.get("/{title}")
def get_topic(title: str, session: Session = Depends(get_session)):
    topic = find_topic(session, title)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.post("", status_code=201)
def add_topic(data: TopicIn, session: Session = Depends(get_session)):
    if find_topic(session, data.title):
        raise HTTPException(status_code=400, detail="Topic already exists")
    topic = Topic(**data.model_dump())
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return topic

@router.put("/{title}")
def update_topic(title: str, data: TopicIn, session: Session = Depends(get_session)):
    topic = find_topic(session, title)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    topic.status = data.status
    topic.description = data.description
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return topic

@router.delete("/{title}")
def delete_topic(title: str, session: Session = Depends(get_session)):
    topic = find_topic(session, title)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    session.delete(topic)
    session.commit()
    return {"deleted": title}
