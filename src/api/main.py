from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from domain.exceptions.base import DomainException, DuplicateEntity, EntityNotFound
from domain.exceptions.auth import InsufficientPermissions, InvalidCredentials
from domain.exceptions.order import OrderNotModifiable
from infrastructure.config.settings import settings
from api.middleware.rate_limiter import limiter
from api.routers import (
    auth_router, landing_router, admin_router, product_router,
    order_router, brokerage_router, advisory_router, collie_app_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup: run seed to ensure admin user and initial data exist
    from infrastructure.persistence.seed import seed
    try:
        await seed()
    except Exception as e:
        print(f"[SEED] Warning: seed failed: {e}")
    yield
    # Shutdown


app = FastAPI(
    title="Collie Valley SAC API",
    description="API para plataforma de agroexportación Collie Valley",
    version="0.1.0",
    lifespan=lifespan,
)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security headers
from api.middleware.security_headers import SecurityHeadersMiddleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(landing_router.router, prefix="/api/v1")
app.include_router(admin_router.router, prefix="/api/v1")
app.include_router(product_router.router, prefix="/api/v1")
app.include_router(order_router.router, prefix="/api/v1")
app.include_router(brokerage_router.router, prefix="/api/v1")
app.include_router(advisory_router.router, prefix="/api/v1")
app.include_router(collie_app_router.router, prefix="/api/v1")


# Global exception handlers
@app.exception_handler(EntityNotFound)
async def entity_not_found_handler(request: Request, exc: EntityNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(DuplicateEntity)
async def duplicate_entity_handler(request: Request, exc: DuplicateEntity) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": exc.message})


@app.exception_handler(InvalidCredentials)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentials) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": exc.message})


@app.exception_handler(InsufficientPermissions)
async def insufficient_permissions_handler(request: Request, exc: InsufficientPermissions) -> JSONResponse:
    return JSONResponse(status_code=403, content={"detail": exc.message})


@app.exception_handler(OrderNotModifiable)
async def order_not_modifiable_handler(request: Request, exc: OrderNotModifiable) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.message})


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": exc.message})


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "collie-valley-api"}
