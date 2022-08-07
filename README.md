# Backend API

This is a project done with Python 3.10.4

## Run locally

Download the repo
```
git clone https://github.com/omezaldama/zb-test-api.git
cd zb-test-api
```
Create a virtual environment and activate it.

On Windows:
```
virtualenv venv
. venv/Scripts/activate
```

On Linux:
```
mkvirtualenv zb-api
workon zb-api
```

Install dependencies.
```
pip install -r requirements.txt
```

Run the server.
```
uvicorn main:app
```
If you want to watch for changes, use the reload flag.
```
uvicorn main:app --reload
```
This will run the app on port 8000.
```
http://localhost:8000
```
Swagger documentation will be located in.
```
http://localhost:8000/docs
```
When running the app, it will immediately create (if not created already) an admin user with email admin@example.com and password abc123. You can use this user to login, get a token and authenticate requests.


## Running tests

First install the test dependencies (within your virtual environment).
```
pip install -r test-requirements.txt
```

To run all tests, from the project root
```
pytest
```
To run a specific test:
```
pytest tests/api/v1/test_products.py::test_get_products
```


## Project structure

File main.py is the entrypoint of the app.

Endpoint routes are defined in the folder /api.

Controllers are located in the folder /controllers.

Pydantic models are defined in folder /pd_models. Database models are defined in folder /db_models.

The folder /dependencies contains the dependencies used by this FastAPI app.

The folder /utils contains several utility functions and classes.

File settings.py contains settings for the app.

File requirements.txt contains the pip dependencies needed to run this app.


## Built with

* [Python 3.10.4](https://www.python.org/) - Main programming language
* [FastAPI 0.79.0](https://fastapi.tiangolo.com/) - Backend framework
* [SQLAlchemy 1.4.39](https://www.sqlalchemy.org/) - Python ORM
