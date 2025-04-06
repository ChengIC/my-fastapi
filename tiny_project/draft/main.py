from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
app = FastAPI()

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

todos: List[Todo] = []

# Create a todo
@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    if any(t.id == todo.id for t in todos):
        raise HTTPException(status_code=400, detail="Todo with this ID already exists.")
    todos.append(todo)
    return todo

# List all todos
@app.get("/todos", response_model=List[Todo])
async def list_todos():
    return todos

# Get a todo by ID
@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

# Update a todo
@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

# Delete a todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)