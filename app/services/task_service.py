from sqlalchemy.orm import Session  
from app.repositories.task_repo import TaskRepository  


class TaskService:
    def __init__(self, repo: TaskRepository | None = None):
        self.repo = repo or TaskRepository()

    def add(self, db: Session, *, owner_id: int, title: str):
        if not title or not title.strip():
            raise ValueError("title is required")
        return self.repo.create(db, owner_id=owner_id, title=title.strip())

    def list(self, db: Session, *, owner_id: int, done: bool | None = None):
        return self.repo.list_by_owner(db, owner_id=owner_id, done=done)

    def update(self, db: Session, *, task_id: int, title: str | None, done: bool | None):
        task = self.repo.get(db, task_id)
        if not task:
            raise ValueError("Task not found")
        return self.repo.update(db, task, title=title, done=done)

    def update_owned(
        self,
        db: Session,
        *,
        task_id: int,
        owner_id: int,
        title: str | None,
        done: bool | None,
    ):
        task = self.repo.get(db, task_id)
        if not task:
            raise ValueError("Task not found")
        if task.owner_id != owner_id:
            raise PermissionError("Forbidden: not the owner of this task")
        return self.repo.update(db, task, title=title, done=done)

    def remove(self, db: Session, *, task_id: int):
        task = self.repo.get(db, task_id)
        if not task:
            raise ValueError("Task not found")
        self.repo.delete(db, task)

    def remove_owned(self, db: Session, *, task_id: int, owner_id: int):
        task = self.repo.get(db, task_id)
        if not task:
            raise ValueError("Task not found")
        if task.owner_id != owner_id:
            raise PermissionError("Forbidden: not the owner of this task")
        self.repo.delete(db, task)
