import os
import uuid
from typing import Optional
from dotenv import load_dotenv
from fastapi import Depends, Request, HTTPException, status
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, schemas
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from pydantic import BaseModel
from pwdlib import PasswordHash
from app.db import get_user_db
from app.models.user import User, UserRole, VerificationStatus
from app.schemas.user import UserCreate

load_dotenv()

SECRET = os.getenv("SECRET", "SUPER_SECRET_KEY")
password_hash = PasswordHash.recommended()


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"🔒 Password reset requested for {user.email}. Token: {token}")

    async def create(
        self,
        user_create: schemas.BaseUserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        if getattr(user_create, "role", None) == UserRole.ADMIN:
            # Use setattr to safely assign the custom attribute on the Pydantic model
            setattr(user_create, "verification_status",
                    VerificationStatus.APPROVED)

        return await super().create(user_create=user_create, safe=safe, request=request)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered ({user.email}).")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="/api/v1/auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager, auth_backends=[auth_backend]
)

current_active_user = fastapi_users.current_user(active=True)
