
from app.src.models.organization import Organization
from app.src.repositories.buildings import BuildingRepository
from app.src.repositories.activity_types import ActivityTypeRepository
from app.src.repositories.organizations import OrganizationRepository

from app.src.schemas.building import BuildingCreate
from app.src.schemas.organization import (
    OrganizationCreate,
    OrganizationOut,
    OrganizationCreateRequest,
)


class OrganizationService:
    def __init__(
        self,
        buildings: BuildingRepository,
        activity_types: ActivityTypeRepository,
        organizations: OrganizationRepository,
    ):
        self.buildings = buildings
        self.activity_types = activity_types
        self.organizations = organizations

    async def filter_organizations(
        self,
        name: str | None = None,
        address: str | None = None,
        activity_name: str | None = None,
        include_nested_activity: bool = False,
    ) -> list[Organization]:

        if activity_name:
            activity_obj = await self.activity_types.get_by_name(activity_name)
            if not activity_obj:
                raise ValueError(f"Activity '{activity_name}' not found")
            if include_nested_activity:
                activity_ids = await self.activity_types.resolve_subtree_ids(activity_obj.id)
            else:
                activity_ids = [activity_obj.id]
        else:
            activity_ids = None

        organizations = await self.organizations.filter(
            name=name, address=address, activity_ids=activity_ids
        )

        return organizations

    async def create_organization(
        self, data: OrganizationCreateRequest
    ) -> OrganizationOut:
        building = await self.buildings.get_by_address(data.address)
        if building is None:
            await self.buildings.create(
                BuildingCreate(address=data.address, latitude=None, longitude=None)
            )
            building = await self.buildings.get_by_address(data.address)

        activity_types = []
        for activity_name in data.activity_types:
            activity = await self.activity_types.get_by_name(activity_name)
            if activity is not None:
                activity_types.append(activity.id)
            else:
                raise ValueError(f"Activity type '{activity_name}' not found")

        new_organization = OrganizationCreate(
            name=data.name, building_id=building.id, activity_type_ids=activity_types
        )

        return await self.organizations.create(new_organization)

    async def get_organizations_in_radius(
        self, latitude: float, longitude: float, radius_meters: float
    ) -> list[Organization]:
        organizations_list = []

        buildings_in_radius = await self.buildings.get_buildings_in_radius(
            latitude=latitude, longitude=longitude, radius_meters=radius_meters
        )
        for building in buildings_in_radius:
            organizations = await self.organizations.get_by_building_id(building.id)
            organizations_list.extend(organizations)
        return organizations_list
