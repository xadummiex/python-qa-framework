from sqlalchemy.orm import Session

from src.db.tables.user import User


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter_by(username=username).first()

    @staticmethod
    def delete_user_by_username(db: Session, username: str) -> None:
        user = db.query(User).filter_by(username=username).first()
        if user:
            db.delete(user)
            db.commit()

    @staticmethod
    def create_user(db: Session, username: str, password: str, role: str) -> User | None:
        user = User(username=username, password=password, role=role)
        db.add(user)
        db.commit()





