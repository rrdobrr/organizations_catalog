from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import and_
from typing import List

from app.src.models.organization import Organization, Phone
from app.src.models.activity_type import ActivityTypes
from app.src.models.building import Building
from app.src.schemas.organization import OrganizationCreate, PhoneNumber


class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self, org_id: int
    ) -> Organization | None:
        stmt = select(Organization).where(Organization.id == org_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: OrganizationCreate) -> Organization:
        stmt = select(ActivityTypes).where(ActivityTypes.id.in_(data.activity_type_ids))
        result = await self.db.execute(stmt)
        activity_types = result.scalars().all()

        organization = Organization(
            name=data.name, building_id=data.building_id, activity_types=activity_types
        )
        self.db.add(organization)
        await self.db.commit()
        await self.db.refresh(organization)
        return organization

    async def filter(
        self,
        name: str | None = None,
        address: str | None = None,
        activity_ids: List[int] | None = None,
    ) -> list[Organization]:
        stmt = select(Organization)

        if address:
            stmt = stmt.join(Organization.building)
        if activity_ids:
            stmt = stmt.join(Organization.activity_types)

        conditions = []
        if name:
            conditions.append(Organization.name.ilike(f"%{name}%"))
        if address:
            conditions.append(Building.address.ilike(f"%{address}%"))
        if activity_ids:
            conditions.append(ActivityTypes.id.in_(activity_ids))

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_building_id(self, building_id: int) -> List[Organization]:
        stmt = select(Organization).where(Organization.building_id == building_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def add_phone_number(self, data: PhoneNumber) -> Phone:
        phone_number = Phone(number=data.number, organization_id=data.organization_id)
        self.db.add(phone_number)
        await self.db.commit()

        return phone_number


