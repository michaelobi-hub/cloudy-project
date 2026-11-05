import uuid
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class AdminUserResponse(BaseModel):
    """Schema for admins to view user details safely."""
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True