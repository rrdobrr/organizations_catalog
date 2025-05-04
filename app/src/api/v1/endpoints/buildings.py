from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.src.repositories.buildings import BuildingRepository
from app.src.schemas.building import BuildingCreate, BuildingOut
from app.src.core.db.session import get_session


router = APIRouter(prefix="/buildings", tags=["Здания"])


@router.post(
    "/",
    response_model=BuildingOut,
    summary="Добавить здание",
    description="Метод для добавления здания в базу.",
)
async def create_building(
    data: BuildingCreate, db: AsyncSession = Depends(get_session)
):
    return await BuildingRepository(db).create(data)


@router.get(
    "/",
    response_model=List[BuildingOut],
    summary="Получить все здания",
    description="Метод для получения всех зданий в списке",
)
async def list_buildings(db: AsyncSession = Depends(get_session)):
    return await BuildingRepository(db).get_all()


@router.get(
    "/geo_radius/",
    response_model=List[BuildingOut],
    summary="Получить все здания в гео-радиусе",
    description="Метод для получения всех зданий в заданном радиусе заданной точки",
)
async def list_buildings(
    latitude: float,
    longitude: float,
    radius_meters: float,
    db: AsyncSession = Depends(get_session),
):
    return await BuildingRepository(db).get_buildings_in_radius(
        latitude=latitude, longitude=longitude, radius_meters=radius_meters
    )
