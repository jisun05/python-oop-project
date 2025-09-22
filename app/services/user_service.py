from sqlalchemy.orm import Session  
from app.repositories.user_repo import UserRepository 

class UserService:

    def __init__(self, repo: UserRepository | None = None) -> None:
        self.repo = repo or UserRepository()

    def register(self, db: Session, *, email: str, name: str):
        exists = self.repo.get_by_email(db, email=email)
        if exists:
            raise ValueError("Email already registered")
        return self.repo.create(db, email=email, name=name)

    def get(self, db: Session, user_id: int):
        return self.repo.get_by_id(db, user_id)
    
    def get_all_users(self, db: Session):
        return self.repo.get_all_users(db)
