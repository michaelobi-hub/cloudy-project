import uuid
from typing import Any
from fastapi_users import schemas
from pydantic import Field, BaseModel, EmailStr, ConfigDict
from app.models.user import UserRole, VerificationStatus

def remove_internal_fields(schema: dict[str, Any]) -> None:
    # Remove internal flags from the OpenAPI request body schema in Swagger UI
    properties = schema.get("properties", {})
    properties.pop("is_active", None)
    properties.pop("is_superuser", None)
    properties.pop("is_verified", None)

class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str | None = None
    last_name: str | None = None
    role: str = UserRole.REGULAR
    verification_status: str = VerificationStatus.PENDING

    is_active: bool = Field(default=False, exclude=True)
    is_superuser: bool = Field(default=False, exclude=True)
    is_verified: bool = Field(default=False, exclude=True)
    
    class Config:
        from_attributes = True

class UserCreate(schemas.BaseUserCreate):
    first_name: str | None = None
    last_name: str | None = None
    password: str
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra=remove_internal_fields
    )

    

class UserUpdate(schemas.BaseUserUpdate):
    first_name: str | None = None
    last_name: str | None = None
    