from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.src.models.activity_type import ActivityTypes
from app.src.schemas.activity_type import ActivityTypeCreate  # и схема валидации


class ActivityTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, activity_type_id: int) -> ActivityTypes | None:
        stmt = select(ActivityTypes).where(ActivityTypes.id == activity_type_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_name(self, name: str) -> ActivityTypes | None:
        stmt = select(ActivityTypes).where(ActivityTypes.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ActivityTypes]:
        result = await self.db.execute(select(ActivityTypes))
        return result.scalars().all()

    async def create(self, activity_data: ActivityTypeCreate) -> ActivityTypes:
        activity = ActivityTypes(**activity_data.dict())
        self.db.add(activity)
        await self.db.commit()
        await self.db.refresh(activity)
        return activity

    async def delete(self, activity_type_id: int) -> bool:
        object = await self.get_by_id(activity_type_id)
        if object:
            await self.db.delete(object)
            await self.db.commit()

            return True
        return False

    async def resolve_subtree_ids(self, activity_id: int):

        async def _get_child_ids(activity_id: int) -> list[int]:
            stmt = select(ActivityTypes).where(
                ActivityTypes.parent_id == activity_id
            )
            result = await self.db.execute(stmt)
            children = result.scalars().all()

            if not children:
                return []

            ids = [child.id for child in children]

            for child in children:
                ids.extend(await _get_child_ids(child.id))

            return ids

        return await _get_child_ids(activity_id)
