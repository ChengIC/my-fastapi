from fastapi import FastAPI
from app.api.v1.endpoints import todo as todo_endpoints
from app.core.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(
    todo_endpoints.router,
    prefix="/api/v1/todos",
    tags=["todos"]
)