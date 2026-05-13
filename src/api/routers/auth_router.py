from fastapi import APIRouter, Depends, Request

from api.middleware.rate_limiter import limiter
from api.schemas.auth_schemas import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from api.middleware.auth_middleware import get_current_user_id
from application.dtos.auth_dto import LoginInput, RefreshInput, RegisterInput
from application.use_cases.auth.get_profile import GetProfileUseCase
from application.use_cases.auth.login_user import LoginUserUseCase
from application.use_cases.auth.refresh_token import RefreshTokenUseCase
from application.use_cases.auth.register_user import RegisterUserUseCase
from infrastructure.config.dependencies import (
    get_auth_service,
    get_user_repository,
)
from domain.ports.repositories.user_repository import UserRepository
from domain.ports.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    request: RegisterRequest,
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


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(
    raw_request: Request,
    request: LoginRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
):
    use_case = LoginUserUseCase(user_repo, auth_service)
    tokens = await use_case.execute(
        LoginInput(email=request.email, password=request.password)
    )
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: RefreshRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
):
    use_case = RefreshTokenUseCase(user_repo, auth_service)
    tokens = await use_case.execute(RefreshInput(refresh_token=request.refresh_token))
    return TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    user_id=Depends(get_current_user_id),
    user_repo: UserRepository = Depends(get_user_repository),
):
    use_case = GetProfileUseCase(user_repo)
    user = await use_case.execute(user_id)
    return UserResponse.from_entity(user)
