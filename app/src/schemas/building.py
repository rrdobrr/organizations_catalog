from pydantic import BaseModel
from typing import Optional


class BuildingCreate(BaseModel):
    address: Optional[str]
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class BuildingOut(BaseModel):
    address: Optional[str]
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        orm_mode = True