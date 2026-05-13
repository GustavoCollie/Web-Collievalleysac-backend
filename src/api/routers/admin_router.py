from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.rbac_middleware import require_role
from api.schemas.admin_schemas import CreateUserRequest, MetricsResponse, UpdateUserRequest
from api.schemas.auth_schemas import UserListResponse, UserResponse
from application.dtos.auth_dto import RegisterInput
from application.use_cases.auth.register_user import RegisterUserUseCase
from domain.entities.user import Role, User
from domain.ports.repositories.user_repository import UserRepository
from domain.ports.services.auth_service import AuthService
from infrastructure.config.dependencies import get_auth_service, get_user_repository
from infrastructure.persistence.database import get_session
from infrastructure.persistence.models.user_model import UserORM
from infrastructure.persistence.models.order_model import OrderORM
from infrastructure.persistence.models.brokerage_model import BrokerageRequestORM
from infrastructure.persistence.models.advisory_model import AdvisoryRequestORM

router = APIRouter(prefix="/admin", tags=["admin"])


# --- User Management ---


@router.get("/users", response_model=UserListResponse)
async def list_users(
    _user=Depends(require_role("admin")),
    user_repo: UserRepository = Depends(get_user_repository),
):
    users = await user_repo.find_all()
    return UserListResponse(
        users=[UserResponse.from_entity(u) for u in users],
        total=len(users),
    )


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,
    _user=Depends(require_role("admin")),
    user_repo: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
):
    use_case = RegisterUserUseCase(user_repo, auth_service)
    user = await use_case.execute(
        RegisterInput(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            phone=request.phone,
            role=request.role,
        )
    )
    return UserResponse.from_entity(user)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    _admin=Depends(require_role("admin")),
    user_repo: UserRepository = Depends(get_user_repository),
):
    from domain.exceptions.base import EntityNotFound

    user = await user_repo.find_by_id(user_id)
    if not user:
        raise EntityNotFound("Usuario", str(user_id))

    if request.full_name is not None:
        user.full_name = request.full_name
    if request.phone is not None:
        user.phone = request.phone
    if request.role is not None:
        user.role = request.role
    if request.is_active is not None:
        user.is_active = request.is_active

    updated = await user_repo.update(user)
    return UserResponse.from_entity(updated)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    admin=Depends(require_role("admin")),
    user_repo: UserRepository = Depends(get_user_repository),
):
    admin_id, _ = admin
    if admin_id == user_id:
        from domain.exceptions.base import DomainException
        raise DomainException("No puedes eliminar tu propia cuenta de admin")

    await user_repo.delete(user_id)


# --- Metrics ---


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    _user=Depends(require_role("admin")),
    session: AsyncSession = Depends(get_session),
):
    # Total and active users
    total_users_result = await session.execute(select(func.count(UserORM.id)))
    total_users = total_users_result.scalar() or 0

    active_users_result = await session.execute(
        select(func.count(UserORM.id)).where(UserORM.is_active == True)
    )
    active_users = active_users_result.scalar() or 0

    # Orders count
    orders_result = await session.execute(select(func.count(OrderORM.id)))
    total_orders = orders_result.scalar() or 0

    # Brokerage requests count
    brokerage_result = await session.execute(select(func.count(BrokerageRequestORM.id)))
    total_brokerage = brokerage_result.scalar() or 0

    # Advisory requests count
    advisory_result = await session.execute(select(func.count(AdvisoryRequestORM.id)))
    total_advisory = advisory_result.scalar() or 0

    # Users by role
    role_result = await session.execute(
        select(UserORM.role, func.count(UserORM.id)).group_by(UserORM.role)
    )
    users_by_role = {row[0]: row[1] for row in role_result.all()}

    return MetricsResponse(
        total_users=total_users,
        active_users=active_users,
        total_orders=total_orders,
        total_brokerage_requests=total_brokerage,
        total_advisory_requests=total_advisory,
        users_by_role=users_by_role,
    )
