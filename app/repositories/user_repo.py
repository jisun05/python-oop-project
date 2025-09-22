from sqlalchemy.orm import Session  # SQLAlchemy session type
from app.models.user import User


class UserRepository:
    """
    Repository layer encapsulating DB access.
        Services depend on this layer to keep business logic testable and swappable.
    """

    def create(self, db: Session, *, email: str, name: str) -> User:
        user = User(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.get(User, user_id)

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create_with_password(self, db: Session, *, email: str, name: str, hashed_password: str) -> User:
        user = User(email=email, name=name, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_all_users(self, db: Session) -> list[User]:
        return db.query(User).all()