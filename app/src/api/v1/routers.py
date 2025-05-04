from fastapi import APIRouter

from .endpoints.organizations import router as organization_router
from .endpoints.activity_types import router as activity_type_router
from .endpoints.buildings import router as building_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(organization_router)
api_router.include_router(activity_type_router)
api_router.include_router(building_router)
