from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ActivityTypeCreateRequest(BaseModel):
    name: str
    parent_name: Optional[str] = None

class ActivityTypeCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ActivityTypeOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True  # нужно для ORM
