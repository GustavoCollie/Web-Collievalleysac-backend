from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.landing_schemas import (
    CreateSectionRequest,
    LandingSectionResponse,
    LandingSectionsListResponse,
    UpdateSectionRequest,
)
from api.middleware.rbac_middleware import require_role
from application.dtos.landing_dto import CreateSectionInput, UpdateSectionInput
from application.use_cases.landing.get_landing_sections import GetLandingSectionsUseCase
from application.use_cases.landing.update_landing_section import (
    CreateLandingSectionUseCase,
    DeleteLandingSectionUseCase,
    UpdateLandingSectionUseCase,
)
from infrastructure.persistence.database import get_session
from infrastructure.persistence.repositories.pg_landing_repository import PgLandingRepository

router = APIRouter(tags=["landing"])


def _get_landing_repo(session: AsyncSession = Depends(get_session)):
    return PgLandingRepository(session)


# Public: get visible sections for landing page
@router.get("/landing/sections", response_model=LandingSectionsListResponse)
async def get_public_sections(
    repo=Depends(_get_landing_repo),
):
    use_case = GetLandingSectionsUseCase(repo)
    sections = await use_case.execute(include_hidden=False)
    return LandingSectionsListResponse(
        sections=[LandingSectionResponse.from_entity(s) for s in sections]
    )


# Admin: get all sections (including hidden)
@router.get("/admin/landing/sections", response_model=LandingSectionsListResponse)
async def get_all_sections(
    user=Depends(require_role("admin")),
    repo=Depends(_get_landing_repo),
):
    use_case = GetLandingSectionsUseCase(repo)
    sections = await use_case.execute(include_hidden=True)
    return LandingSectionsListResponse(
        sections=[LandingSectionResponse.from_entity(s) for s in sections]
    )


# Admin: create section
@router.post(
    "/admin/landing/sections",
    response_model=LandingSectionResponse,
    status_code=201,
)
async def create_section(
    request: CreateSectionRequest,
    user=Depends(require_role("admin")),
    repo=Depends(_get_landing_repo),
):
    user_id, _ = user
    use_case = CreateLandingSectionUseCase(repo)
    section = await use_case.execute(
        CreateSectionInput(
            section_key=request.section_key,
            title=request.title,
            subtitle=request.subtitle,
            content=request.content,
            display_order=request.display_order,
            is_visible=request.is_visible,
            updated_by=user_id,
        )
    )
    return LandingSectionResponse.from_entity(section)


# Admin: update section
@router.put(
    "/admin/landing/sections/{section_key}",
    response_model=LandingSectionResponse,
)
async def update_section(
    section_key: str,
    request: UpdateSectionRequest,
    user=Depends(require_role("admin")),
    repo=Depends(_get_landing_repo),
):
    user_id, _ = user
    use_case = UpdateLandingSectionUseCase(repo)
    section = await use_case.execute(
        UpdateSectionInput(
            section_key=section_key,
            title=request.title,
            subtitle=request.subtitle,
            content=request.content,
            display_order=request.display_order,
            is_visible=request.is_visible,
            updated_by=user_id,
        )
    )
    return LandingSectionResponse.from_entity(section)


# Admin: delete section
@router.delete("/admin/landing/sections/{section_key}", status_code=204)
async def delete_section(
    section_key: str,
    user=Depends(require_role("admin")),
    repo=Depends(_get_landing_repo),
):
    use_case = DeleteLandingSectionUseCase(repo)
    await use_case.execute(section_key)
