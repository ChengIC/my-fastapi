from typing import Optional
from pydantic import BaseModel, ConfigDict

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    id: int

class TodoUpdate(TodoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoInDB(TodoCreate):
    model_config = ConfigDict(from_attributes=True)