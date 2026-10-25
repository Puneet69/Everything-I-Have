from typing import Literal
from sqlmodel import SQLModel, Field

class Topic(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(unique=True)
    status: str = "learning"
    description: str | None = None

class TopicIn(SQLModel):
    title: str
    status: Literal["learning", "done"] = "learning"
    description: str | None = None
