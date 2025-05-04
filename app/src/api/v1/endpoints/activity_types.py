from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.src.core.db.session import get_session
from app.src.schemas.activity_type import ActivityTypeCreateRequest, ActivityTypeOut
from app.src.services.activity_types import ActivityTypeService
from app.src.repositories.activity_types import ActivityTypeRepository


async def get_activity_type_service(
    db: AsyncSession = Depends(get_session),
) -> ActivityTypeService:
    repo = ActivityTypeRepository(db)
    return ActivityTypeService(repo)


router = APIRouter(prefix="/activity-types", tags=["Виды деятельности"])


@router.post(
    "/",
    response_model=ActivityTypeOut,
    summary="Добавить вид деятельности",
    description="Метод для добавления вида деятельности.",
)
async def create_activity(
    data: ActivityTypeCreateRequest,
    service: ActivityTypeService = Depends(get_activity_type_service),
):
    try:
        return await service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=List[ActivityTypeOut],
    summary="Получить все виды деятельности",
    description="Метод для получения списка всех видов деятельности",
)
async def get_all(service: ActivityTypeService = Depends(get_activity_type_service)):

    return await service.get_all()
