from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from app.src.models.building import Building
from app.src.schemas.building import BuildingCreate


class BuildingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, building_id: int) -> Building | None:
        stmt = select(Building).where(Building.id == building_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_address(self, address: str) -> Building | None:
        stmt = select(Building).where(Building.address == address)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all(self) -> list[Building]:
        result = await self.db.execute(select(Building))
        return result.scalars().all()

    async def create(self, building_data: BuildingCreate) -> Building:

        building = Building(
            address=building_data.address,
            latitude=building_data.latitude,
            longitude=building_data.longitude,
        )
        if building.latitude:
            building.set_location()
        self.db.add(building)
        await self.db.commit()
        await self.db.refresh(building)
        return building

    async def delete(self, building_id: int) -> bool:
        object = await self.get_by_id(building_id)
        if object:
            await self.db.delete(object)
            await self.db.commit()

            return True
        return False

    async def get_buildings_in_radius(self, latitude: float, longitude: float, radius_meters: float) -> list[Building]:


        point = from_shape(Point(longitude, latitude), srid=4326)


        stmt = select(Building).where(
            ST_DWithin(Building.location, point, radius_meters)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()
