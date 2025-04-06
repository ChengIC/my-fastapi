from typing import List, Dict, Optional
from app.models.todo import Todo

class Database:
    def __init__(self):
        self.todos: List[Todo] = []
        self._id_counter = 1  # Simple auto-increment simulation
    
    def generate_id(self) -> int:
        """Generate a unique ID for new todos"""
        new_id = self._id_counter
        self._id_counter += 1
        return new_id

# Singleton database instance
SessionLocal = Database()