from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.src.repositories.buildings import BuildingRepository
from app.src.repositories.activity_types import ActivityTypeRepository
from app.src.repositories.organizations import OrganizationRepository

from app.src.services.organizations import OrganizationService
from app.src.schemas.organization import OrganizationCreateRequest, OrganizationOut, PhoneNumber
from app.src.core.db.session import get_session


async def get_building_repo(
    db: AsyncSession = Depends(get_session),
) -> BuildingRepository:
    return BuildingRepository(db)


async def get_activity_type_repo(
    db: AsyncSession = Depends(get_session),
) -> ActivityTypeRepository:
    return ActivityTypeRepository(db)


async def get_organization_repo(
    db: AsyncSession = Depends(get_session),
) -> OrganizationRepository:
    return OrganizationRepository(db)


async def get_organizations_service(
    buildings: BuildingRepository = Depends(get_building_repo),
    activity_types: ActivityTypeRepository = Depends(get_activity_type_repo),
    organizations: OrganizationRepository = Depends(get_organization_repo),
) -> OrganizationService:
    return OrganizationService(buildings, activity_types, organizations)


router = APIRouter(prefix="/organizations", tags=["Организации"])


@router.post(
    "/",
    response_model=OrganizationOut,
    summary="Добавить организацию",
    description="Метод для добавления новой организации в базу",
)
async def create_organization(
    data: OrganizationCreateRequest,
    service: OrganizationService = Depends(get_organizations_service),
):
    return await service.create_organization(data)


@router.post(
    "/phone_numbers",
    response_model=PhoneNumber,
    summary="Добавить номер телефона",
    description="Метод для добавления нового номера телефона",
)
async def add_phone_number(
    data: PhoneNumber,
    repo: OrganizationRepository = Depends(get_organization_repo),
):
    return await repo.add_phone_number(data)


@router.get(
    "/{organization_id}",
    response_model=OrganizationOut,
    summary="Получить организацию по ID",
    description="Метод для получения организации по ID",
)
async def get_organization_by_id(
    organization_id: int, repo: OrganizationRepository = Depends(get_organization_repo)
):

    organization = await repo.get_by_id(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return organization


@router.get(
    "/",
    response_model=List[OrganizationOut],
    summary="Получить отфильтрованный список организаций",
    description="Метод для запроса отфильтрованного списка организаций",
)
async def filter_organizations(
    name: str | None = None,
    address: str | None = None,
    activity: str | None = None,
    include_nested_activity: bool = False,
    service: OrganizationService = Depends(get_organizations_service),
):
    return await service.filter_organizations(
        name=name,
        address=address,
        activity_name=activity,
        include_nested_activity=include_nested_activity,
    )


@router.get(
    "/geo_radius/",
    response_model=List[OrganizationOut],
    summary="Получить все организации в гео-радиусе",
    description="Метод для получения всех организаций в заданном радиусе заданной точки",
)
async def get_organizations_in_radius(
    latitude: float,
    longitude: float,
    radius_meters: float,
    service: OrganizationService = Depends(get_organizations_service),
):

    return await service.get_organizations_in_radius(
        latitude=latitude, longitude=longitude, radius_meters=radius_meters
    )


