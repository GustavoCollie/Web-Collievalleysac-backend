from uuid import UUID
from typing import Callable

from fastapi import Depends, HTTPException, status

from api.middleware.auth_middleware import get_current_user_role


def require_role(*allowed_roles: str) -> Callable:
    """Dependency factory that enforces role-based access control.

    Usage:
        @router.get("/admin-only")
        async def admin_endpoint(user=Depends(require_role("admin"))):
            user_id, role = user
    """

    async def role_checker(
        user_data: tuple[UUID, str] = Depends(get_current_user_role),
    ) -> tuple[UUID, str]:
        user_id, role = user_data
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso",
            )
        return user_id, role

    return role_checker
