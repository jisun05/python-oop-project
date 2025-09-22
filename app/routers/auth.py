from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import UserRegister, UserRead
from app.schemas.auth import Token
from app.services.auth_service import AuthService
from app.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

svc = AuthService()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    try:
        return svc.register(db, email=payload.email, name=payload.name, password=payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        token, _ = svc.login(db, email=form.username, password=form.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@router.get("/me", response_model=UserRead)
def me(current_user = Depends(get_current_user)):
    return current_user
