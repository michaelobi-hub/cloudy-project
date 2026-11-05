from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, VerificationStatus

class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(getattr(User, "email") == email).first()

    def update_user_verification(self, user_id: str, status_val: VerificationStatus):
        user = self.db.query(User).filter(getattr(User, "id") == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        # Use setattr to safely assign the custom attribute
        setattr(user, "verification_status", str(status_val.value))

        self.db.commit()
        self.db.refresh(user)
        return user