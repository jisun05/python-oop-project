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

<img width="162" height="448" alt="structure_OOP" src="https://github.com/user-attachments/assets/4846bcff-b8b5-4b42-a001-b5de609c3b96" />

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

1. **Build the image**
```bash
docker build -t python-oop-project .
```
2. **Run the container**
```bash
docker run -d --name python-oop-project -p 8000:8000 python-oop-project
```
```bash
Application: http://localhost:8000
API docs (Swagger): http://localhost:8000/docs
```
3. **Using Docker Compose**
If you prefer Compose (recommended for multi-service setups):
```bash
docker compose up --build
```
4. **Clean up**
Stop and remove the container and image:
```bash
docker stop python-oop-project && docker rm python-oop-project
docker rmi python-oop-project
```



