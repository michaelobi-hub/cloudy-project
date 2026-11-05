import uuid
from sqlalchemy import String
import enum
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from app.models.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    REGULAR = "regular"

class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default=UserRole.REGULAR, nullable=False)
    verification_status: Mapped[str] = mapped_column(String, default=VerificationStatus.PENDING)