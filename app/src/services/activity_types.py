from typing import List

from app.src.repositories.activity_types import ActivityTypeRepository
from app.src.constants.activity_type import MAX_ACTIVITY_DEPTH
from app.src.models.activity_type import ActivityTypes
from app.src.schemas.activity_type import ActivityTypeCreate, ActivityTypeCreateRequest

from app.src.core.logging import logger

class ActivityTypeService:
    def __init__(self, repo: ActivityTypeRepository):
        self.repo = repo


    async def get_all(self) -> List[ActivityTypes]:
        return await self.repo.get_all()

    async def create(self, data: ActivityTypeCreateRequest) -> ActivityTypes:

        parent = await self.repo.get_by_name(data.parent_name)
        if parent:
            parent_depth = await self._get_depth(parent.id)
            if parent_depth >= MAX_ACTIVITY_DEPTH:
                raise ValueError(
                    f"Нельзя создать подкатегорию глубже {MAX_ACTIVITY_DEPTH} уровней"
                )


            logger.info(f'СМОТРИ: {parent}')
            logger.info(f'СМОТРИ: {parent}')
            logger.info(f'СМОТРИ: {parent}')
            logger.info(f'СМОТРИ: {parent}')
            logger.info(f'СМОТРИ: {parent}')
            data = ActivityTypeCreate(name=data.name, parent_id=parent.id)

        else:
            parent_depth = 0
            data = ActivityTypeCreate(name=data.name, parent_id=None)


        return await self.repo.create(data)

    async def _get_depth(self, parent_id: int, depth: int = 1) -> int:
        parent = await self.repo.get_by_id(parent_id)

        if parent is None:
            return depth

        if parent.parent_id is None:
            return depth
        return await self._get_depth(parent.parent_id, depth + 1)
