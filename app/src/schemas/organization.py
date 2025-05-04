from pydantic import BaseModel
from typing import List
from datetime import datetime


class PhoneNumber(BaseModel):
    number: str
    organization_id: int



class OrganizationCreateRequest(BaseModel):
    name: str
    address: str
    activity_types: List[str]


class OrganizationCreate(BaseModel):
    name: str
    building_id: int
    activity_type_ids: List[int]


class OrganizationOut(BaseModel):
    id: int
    name: str
    building_id: int
    phones: List [PhoneNumber] = None
    created_at: datetime

    class Config:
        orm_mode = True


