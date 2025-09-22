from typing import Iterable
from sqlalchemy.orm import Session
from app.models.task import Task

class TaskRepository:
    """
        Repository layer dedicated to CRUD/queries for Task entities
    """

    def create(self, db: Session, *, owner_id: int, title: str) -> Task:
        t = Task(owner_id=owner_id, title=title)
        db.add(t)
        db.commit()
        db.refresh(t)
        return t

    def list_by_owner(self, db: Session, *, owner_id: int, done: bool | None = None) -> Iterable[Task]:
        q = db.query(Task).filter(Task.owner_id == owner_id)
        if done is not None:
            q = q.filter(Task.done == done)
        return q.order_by(Task.id.desc()).all()

    def get(self, db: Session, task_id: int) -> Task | None:
        return db.get(Task, task_id)

    def update(self, db: Session, task: Task, *, title: str | None = None, done: bool | None = None) -> Task:
        if title is not None:
            task.title = title
        if done is not None:
            task.done = done
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def delete(self, db: Session, task: Task) -> None:
        db.delete(task)
        db.commit()
