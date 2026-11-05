import uuid
from datetime import datetime
from sqlalchemy import String, Float, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class PackageModel(Base):
    __tablename__ = "packages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    total_value: Mapped[float] = mapped_column(Float, nullable=False)
    package_type: Mapped[str] = mapped_column(String, nullable=False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False) 
    fund_amount: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Optional: Track who created the package (e.g., an admin/manager)
    created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
