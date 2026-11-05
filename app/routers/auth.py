from fastapi import APIRouter
from app.user import fastapi_users, auth_backend
from app.schemas.user import UserRead, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

# Login & Logout JWT endpoints
router.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/jwt"
)

# Registration / Signup endpoint
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate)
)

# Forgot & Reset Password endpoints
router.include_router(
    fastapi_users.get_reset_password_router()
)