import pytest
from fastapi import HTTPException
from app.services.todo import TodoService
from app.schemas.todo import TodoCreate, TodoUpdate, TodoInDB
from app.db.session import Database

@pytest.fixture
def todo_service():
    """Fixture providing a fresh TodoService instance for each test"""
    # Create a new in-memory database for each test
    db = Database()
    db.todos = []
    db._id_counter = 1
    return TodoService(db)

@pytest.fixture
def sample_todo_data():
    """Fixture providing sample todo data"""
    return {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False
    }

def test_create_todo(todo_service, sample_todo_data):
    """Test creating a new todo"""
    # Create with explicit ID
    todo_data = TodoCreate(id=1, **sample_todo_data)
    created_todo = todo_service.create_todo(todo_data)
    
    assert isinstance(created_todo, TodoInDB)
    assert created_todo.id == 1
    assert created_todo.title == "Test Todo"
    assert created_todo.description == "Test Description"
    assert created_todo.completed is False

def test_create_todo_duplicate_id(todo_service, sample_todo_data):
    """Test creating a todo with duplicate ID"""
    todo_data = TodoCreate(id=1, **sample_todo_data)
    todo_service.create_todo(todo_data)
    
    # Try to create another with same ID
    with pytest.raises(HTTPException) as exc_info:
        todo_service.create_todo(todo_data)
    
    assert exc_info.value.status_code == 400
    assert "already exists" in str(exc_info.value.detail)

def test_get_todo(todo_service, sample_todo_data):
    """Test retrieving a single todo"""
    # Create a todo first
    todo_data = TodoCreate(id=1, **sample_todo_data)
    created_todo = todo_service.create_todo(todo_data)
    
    # Retrieve it
    retrieved_todo = todo_service.get_todo(1)
    
    assert retrieved_todo is not None
    assert retrieved_todo.id == created_todo.id
    assert retrieved_todo.title == created_todo.title

def test_get_nonexistent_todo(todo_service):
    """Test retrieving a todo that doesn't exist"""
    assert todo_service.get_todo(999) is None

def test_get_all_todos(todo_service, sample_todo_data):
    """Test retrieving all todos"""
    # Create several todos
    todos_to_create = [
        TodoCreate(id=1, **sample_todo_data),
        TodoCreate(id=2, title="Another Todo", description='sample description', completed=True)
    ]
    
    for todo_data in todos_to_create:
        todo_service.create_todo(todo_data)
    
    all_todos = todo_service.get_all_todos()
    
    assert len(all_todos) == 2
    assert all(isinstance(todo, TodoInDB) for todo in all_todos)
    assert {todo.id for todo in all_todos} == {1, 2}

def test_update_todo(todo_service, sample_todo_data):
    """Test updating a todo"""
    # Create first
    todo_data = TodoCreate(id=1, **sample_todo_data)
    todo_service.create_todo(todo_data)
    
    # Update
    updated_todo = todo_service.update_todo(1, TodoUpdate(title='Updated Title', completed=True))
    
    assert updated_todo is not None
    assert updated_todo.title == "Updated Title"
    assert updated_todo.completed is True
    assert updated_todo.description == sample_todo_data["description"]  # unchanged

def test_update_nonexistent_todo(todo_service):
    """Test updating a todo that doesn't exist"""
    update_data = TodoUpdate(title="Should Fail")
    assert todo_service.update_todo(999, update_data) is None

def test_partial_update(todo_service, sample_todo_data):
    """Test partial updates (only changing some fields)"""
    # Create first
    todo_data = TodoCreate(id=1, **sample_todo_data)
    todo_service.create_todo(todo_data)
    
    # Partial update
    update_data = TodoUpdate(completed=True)  # only update completed status
    updated_todo = todo_service.update_todo(1, update_data)
    
    assert updated_todo is not None
    assert updated_todo.completed is True
    assert updated_todo.title == sample_todo_data["title"]  # unchanged
    assert updated_todo.description == sample_todo_data["description"]  # unchanged

def test_delete_todo(todo_service, sample_todo_data):
    """Test deleting a todo"""
    # Create first
    todo_data = TodoCreate(id=1, **sample_todo_data)
    todo_service.create_todo(todo_data)
    
    # Delete and verify
    assert todo_service.delete_todo(1) is True
    assert todo_service.get_todo(1) is None
    assert len(todo_service.get_all_todos()) == 0

def test_delete_nonexistent_todo(todo_service):
    """Test deleting a todo that doesn't exist"""
    assert todo_service.delete_todo(999) is False