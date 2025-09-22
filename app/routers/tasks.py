from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.deps import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.services.task_service import TaskService
from app.schemas.user import UserRead

router = APIRouter(prefix="/tasks", tags=["tasks"])

svc = TaskService()

@router.post("/me", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_my_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    return svc.add(db, owner_id=current_user.id, title=payload.title)

@router.get("/me", response_model=List[TaskRead])
def list_my_tasks(
    done: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    return svc.list(db, owner_id=current_user.id, done=done)

@router.patch("/{task_id}", response_model=TaskRead)
def update_my_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    try:
        return svc.update_owned(
            db,
            task_id=task_id,
            owner_id=current_user.id,
            title=payload.title,
            done=payload.done,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):
    try:
        svc.remove_owned(db, task_id=task_id, owner_id=current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
