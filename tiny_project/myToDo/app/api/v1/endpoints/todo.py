from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.todo import TodoCreate, TodoUpdate, TodoInDB
from app.services.todo import TodoService
from app.db.session import SessionLocal

# Create a dependency
def get_todo_service():
    return TodoService(SessionLocal)

router = APIRouter()

@router.post("/", response_model=TodoInDB)
async def create_todo(todo: TodoCreate, service: TodoService = Depends(get_todo_service)):
    return service.create_todo(todo)

@router.get("/", response_model=List[TodoInDB])
async def list_todos(service: TodoService = Depends(get_todo_service)):
    return service.get_all_todos()

@router.get("/{todo_id}", response_model=TodoInDB)
async def get_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    todo = service.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoInDB)
async def update_todo(todo_id: int, todo: TodoUpdate, service: TodoService = Depends(get_todo_service)):
    updated_todo = service.update_todo(todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, service: TodoService = Depends(get_todo_service)):
    if not service.delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}