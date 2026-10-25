# from turtle import tiltangle
#
# from fastapi import FastAPI ,  HTTPException
# from app.data import get_topics , count_done
# from pydantic import BaseModel
#
# app = FastAPI()
#
# @app.get("/")
# def home():
#     return {"message":"Everything I Have"}
#
# @app.get("/topics")
# def topics():
#     return get_topics()
#
# @app.get("/stats")
# def stats():
#     return {"done": count_done()}
#
# @app.get("/topics/{title}")
# def topic_title(title: str):
#     for topic in get_topics():
#         if topic["title"].lower() == title.lower():
#             return topic
#
#     raise HTTPException(status_code=404, detail="Topic not found")
#
# class Topic(BaseModel):
#     title: str
#     status: str = "learning"
#
# @app.post("/topics", status_code=201)
# def add_topic(topic: Topic):
#     for t in get_topics():
#         if t["title"] == topic.title:
#             raise HTTPException(status_code=400 , detail="Topic already exicts")
#     get_topics().append(topic.model_dump())
#     return topic
#
# @app.put("/topics/{title}")
# def update_topic(title: str , topic: Topic):
#     for t in get_topics():
#         if t["title"] == title:
#             t["status"] = topic.status
#             t["title"] = topic.title
#             return t
#     raise HTTPException(status_code=404, detail="Topic not found")
#
# @app.delete("/topics/{title}")
# def delete_topic(title: str):
#     for t in get_topics():
#         if t["title"] == title:
#             get_topics().remove(t)
#             return {"deleted": title}
#     raise HTTPException(status_code=404, detail="Topic not found")
#
# from fastapi import FastAPI
# from app.routers import topics , stats
#
#
# app=FastAPI()
# app.include_router(topics.router)
# app.include_router(stats.router)
# @app.get("/")
# def home():
#     return {"message": "Everything I Have"}
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db
from app.routers import topics, stats

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(topics.router)
app.include_router(stats.router)

@app.get("/")
def home():
    return {"message": "Everything I Have"}
