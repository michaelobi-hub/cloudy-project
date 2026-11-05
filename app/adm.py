from fastapi import Depends, HTTPException, status
from app.models.user import User, UserRole
from app.user import current_active_user  # Your standard fastapi-users dependency

async def get_admin_user(current_user: User = Depends(current_active_user)) -> User:
    """Dependency to check if the current active user has the ADMIN role."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    return current_user