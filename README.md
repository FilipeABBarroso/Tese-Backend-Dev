# General Information
## Build With

* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

# Getting Started
In order to get this project up and running you will need to follow the next steps.

### Prerequisites

* Python 3.11.4 or latest
* SQL

### Setup

Create a postgres database and add it on the .env file, example:
```
DB_URL=postgresql+psycopg2://postgres:root@localhost:5432/postgres
```
Install dependencies
```
pip install -r requirements.txt
```
Run as Dev
```
python -m uvicorn main:app --reload
```
