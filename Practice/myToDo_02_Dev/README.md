
## Quick Start
1. Run the project: `uvicorn app.main:app --reload`
2. Get the API documentation: `http://127.0.0.1:8000/docs` and test the API endpoints.


## Test
1. Run the tests: `pytest tests/test_todo.py -v`


## TO DO BEFORE PRODUCTION
- [ ] Add logging for bugs and errors 
- [ ] Add authentication and authorization for different users
- [ ] Connect to a database such as PostgreSQL storage for the TODO list data
- [ ] Test the API endpoints, database, and authentication and authorization
- [ ] Dockerize the application
- [ ] Build a CI/CD pipeline