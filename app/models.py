from typing import Literal
from sqlmodel import SQLModel, Field, Relationship

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(unique=True)
    description: str | None = None
    link: str | None = None
    topics: list["Topic"] = Relationship(back_populates="project")

class ProjectIn(SQLModel):
    title: str
    description: str | None = None
    link: str | None = None

class Topic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(unique=True)
    status: str = "learning"
    description: str | None = None
    project_id: int | None = Field(default=None, foreign_key="project.id")
    project: Project | None = Relationship(back_populates="topics")

class TopicIn(SQLModel):
    title: str
    status: Literal["learning", "done"] = "learning"
    description: str | None = None
    project_id: int | None = None
