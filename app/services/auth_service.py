from sqlalchemy.orm import Session 
from app.repositories.user_repo import UserRepository  
from app.core.security import verify_password, get_password_hash, create_access_token

class AuthService:
    def __init__(self, users: UserRepository | None = None) -> None:
        self.users = users or UserRepository()

    def register(self, db: Session, *, email: str, name: str, password: str):
        if self.users.get_by_email(db, email=email):
            raise ValueError("Email already registered")
        hashed = get_password_hash(password)
        return self.users.create_with_password(db, email=email, name=name, hashed_password=hashed)

    def login(self, db: Session, *, email: str, password: str) -> tuple[str, object]:
        user = self.users.get_by_email(db, email=email)
        if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        token = create_access_token(sub=user.email)
        return token, user
