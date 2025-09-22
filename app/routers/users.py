from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
svc = UserService()

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
        create a user.
        - Request body: UserCreate(email, name)
        - Response body: UserRead(id, email, name)
    """
    try: 
        return svc.register(db, email=payload.email, name=payload.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
        Retrieve a single user.
        - Path parameter: user_id
    """
    user = svc.get(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("", response_model=list[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve a single user.
        - Path parameter: user_id
    """
    return svc.get_all_users(db)