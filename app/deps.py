from fastapi import Depends, HTTPException, status  
from fastapi.security import OAuth2PasswordBearer 
from sqlalchemy.orm import Session 
from app.db import get_db 
from app.repositories.user_repo import UserRepository 
from app.core.security import decode_token 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme),         
    db: Session = Depends(get_db),        
):
    try:
        payload = decode_token(token)          
        email: str | None = payload.get("sub")   
        if not email:
          
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = UserRepository().get_by_email(db, email=email) 
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or missing user",
        )
    return user  
