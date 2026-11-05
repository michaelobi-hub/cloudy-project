import uuid
from sqlalchemy import Column, String, Float, Enum as SqlEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.schemas.farmer import Gender, FarmStatus, FarmingCategory

class FarmerModel(Base):
    __tablename__ = "farmers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    nin: Mapped[str] = mapped_column(String(11), unique=True, index=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[Gender] = mapped_column(SqlEnum(Gender), nullable=False)
    farming_category: Mapped[FarmingCategory | None] = mapped_column(SqlEnum(FarmingCategory), nullable=True)
    photo: Mapped[str | None] = mapped_column(String, nullable=True)
    additional_info: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    date_added: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relationship to farms
    farms: Mapped[list["FarmModel"]] = relationship("FarmModel", back_populates="farmer", cascade="all, delete-orphan")


class FarmModel(Base):
    __tablename__ = "farms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    farmer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    size_in_hectares: Mapped[float] = mapped_column(Float, nullable=False)
    farming_category: Mapped[FarmingCategory | None] = mapped_column(SqlEnum(FarmingCategory), nullable=True)
    status: Mapped[FarmStatus] = mapped_column(SqlEnum(FarmStatus), default=FarmStatus.ACTIVE, nullable=False)

    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    date_added: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relationship back to farmer
    farmer: Mapped["FarmerModel"] = relationship("FarmerModel", back_populates="farms")