# my-fastapi
fast-api template for practice

## Full-Stack FastAPI Project (large-scale)
![FastAPI Full-Stack Project Architecture](large_project_architecture.png)

The architecture of an example of a full-stack FastAPI project is shown in the diagram above, illustrating a scalable structure with separate components of:

- `main.py`: Entry point of the project, launches the FastAPI application.
- `core/`: Core functionality, including configuration and security.
- `api/`: API routes and views, with version management.
- `models/`: Database models.
- `schemas/`: Data models for request and response validation.
- `crud/`: Database operations (CRUD: Create, Read, Update, Delete).
- `db/`: Database configurations and session management.
- `tests/`: Test files.
- `utils/`: Utility functions and common modules. 
- `ml/`: Machine learning models and utilities. (optional)
- `alembic/`: Alembic migrations for database.

**Reference:** 
1. [Full-Stack FastAPI Project](https://fastapi.tiangolo.com/project-generation/)
2. [FastAPI 大型项目架构 (Chinese)](https://www.cnblogs.com/wuhuacong/p/18380808)

## Comment on the large-scale project
However, large-scale monolithic projects built entirely with FastAPI are relatively rare in practice. Typically, FastAPI is used as a microservice component within a broader ecosystem, often integrated with services built on frameworks like Flask, Django, or Spring Boot.

The architecture patterns across these frameworks share similarities. For example:
1. Django's built-in migrations are functionally analogous to Alembic (used with FastAPI/SQLAlchemy).
2. Django's Model system serves a similar purpose to FastAPI's Pydantic models (for data validation) and SQLAlchemy models (for database interaction).


## Real-world FastAPI Project (see the example in `Practice` folder)
In practice, we often use FastAPI as a microservice component within a broader ecosystem, often integrated with services built on frameworks like Flask, Django, or Spring Boot.

Initially, we start with a single `main.py` file to launch the FastAPI application, as shown in the `myToDo_01_Draft` folder.

During the development, we refactor the code into multiple modules for scalability and testability, as shown in the `myToDo_02_Dev` folder.

For final production, we connect the application to the database, deploy the application with Docker, add the authentication, enhance the schema validation, CI/CD as shown in the `myToDo_03_Prod` folder.


The API can be built with the following steps:
1. **Carify the API design**: e.g. the API endpoints, routes, request/response schema, etc.
2. **Organize the code**: e.g. create the folders and files. We can start with one 'main.py' then refactor the code into multiple files as the project grows.
3. **Error handling**: add error handling for the API.
4. **Testing**: add the test for the API.
5. **Refactoring**: refactor the code to improve the readability and scalability.
6. **Deployment**: docker, GitHub Actions, etc.

However, the steps are not always linear. We often iterate all the steps above multiple times before the release of every version of the API.


