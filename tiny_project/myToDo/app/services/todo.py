from typing import List, Optional
from fastapi import HTTPException
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoInDB
from app.db.session import SessionLocal

class TodoService:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal
    
    def create_todo(self, todo: TodoCreate) -> TodoInDB:
        """Create a new todo item with validation"""
        if self._todo_exists(todo.id):
            raise HTTPException(
                status_code=400,
                detail="Todo with this ID already exists"
            )
        
        new_todo = Todo(**todo.model_dump())
        self._save_todo(new_todo)
        return TodoInDB.model_validate(new_todo)
    
    def get_todo(self, todo_id: int) -> Optional[TodoInDB]:
        """Get a single todo by ID"""
        todo = self._find_todo_by_id(todo_id)
        return TodoInDB.model_validate(todo) if todo else None
    
    def get_all_todos(self) -> List[TodoInDB]:
        """Get all todo items"""
        return [TodoInDB.model_validate(todo) for todo in self._get_todos()]
    
    def update_todo(self, todo_id: int, todo_data: TodoUpdate) -> Optional[TodoInDB]:
        """Update an existing todo"""
        existing_todo = self._find_todo_by_id(todo_id)
        if not existing_todo:
            return None
            
        update_data = todo_data.model_dump(exclude_unset=True)
        updated_todo = existing_todo.model_copy(update=update_data)
        self._save_todo(updated_todo, self._find_todo_index(todo_id))
        return TodoInDB.model_validate(updated_todo)
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item"""
        index = self._find_todo_index(todo_id)
        if index is None:
            return False
            
        self._delete_todo(index)
        return True
    
    # Private helper methods
    def _get_todos(self) -> List[Todo]:
        return self.db.todos
    
    def _todo_exists(self, todo_id: int) -> bool:
        return any(t.id == todo_id for t in self._get_todos())
    
    def _find_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        return next((t for t in self._get_todos() if t.id == todo_id), None)
    
    def _find_todo_index(self, todo_id: int) -> Optional[int]:
        todos = self._get_todos()
        return next(
            (i for i, t in enumerate(todos) if t.id == todo_id),
            None
        )
    
    def _save_todo(self, todo: Todo, index: Optional[int] = None):
        if index is not None and 0 <= index < len(self.db.todos):
            self.db.todos[index] = todo
        else:
            self.db.todos.append(todo)
    
    def _delete_todo(self, index: int):
        if 0 <= index < len(self.db.todos):
            self.db.todos.pop(index)