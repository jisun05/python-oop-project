# python-oop-project
# Task Manager API (FastAPI + SQLAlchemy)

A simple REST API for managing users and tasks.

Built with an OOP layered architecture (Repository / Service / Router) and using Pydantic v2 style.

# ✨ Features

REST API powered by FastAPI (+ auto documentation at /docs)

SQLAlchemy ORM + SQLite

OOP separation: Repository / Service layers

Filtering: done=true/false

Pytest + TestClient + dedicated test database

Pydantic v2 ConfigDict(from_attributes=True) applied




# 🗂️Project Structure
app
├── core
│   ├── log_config.py
│   └── security.py
├── db.py
├── deps.py
├── main.py
├── models
│   ├── task.py
│   └── user.py
├── repositories
│   ├── task_repo.py
│   └── user_repo.py
├── routers
│   ├── auth.py
│   ├── tasks.py
│   └── users.py
├── schemas
│   ├── auth.py
│   ├── task.py
│   └── user.py
└── services
    ├── auth_service.py
    ├── task_service.py
    └── user_service.py

## 🏗️ Architecture

API (Routes & Handlers): HTTP layer (request/response, status code / exception handling)

Services: Business logic (duplication / existence validation, etc.)

Repositories: Encapsulated DB access (ORM queries)


## 🧱 Tech Stack

FastAPI, Uvicorn

SQLAlchemy , SQLite

Pydantic v2 (ConfigDict(from_attributes=True))

Pytest, httpx, pytest-cov

## 🐳 Docker

1. Build the image
docker build -t python-oop-project .

2. Run the container
docker run -d --name python-oop-project -p 8000:8000 python-oop-project


Application: http://localhost:8000

API docs (Swagger): http://localhost:8000/docs

3. Development mode (with hot reload)

Mount your local source code into the container and enable --reload so changes are picked up instantly:

docker run -d --name python-oop-project -p 8000:8000 `
  -v ${PWD}:/app `
  python-oop-project uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

4. Using Docker Compose

If you prefer Compose (recommended for multi-service setups):

docker compose up --build

5. Clean up

Stop and remove the container and image:

docker stop python-oop-project && docker rm python-oop-project
docker rmi python-oop-project




