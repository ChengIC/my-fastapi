from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool = False