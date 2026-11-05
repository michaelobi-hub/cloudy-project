from pydantic import BaseModel
import uuid
from datetime import datetime
from enum import Enum

class PackageCreate(BaseModel):
    title: str
    description: str
    total_value: float
    package_type: str
    fund_amount: int
    tenure_months: int



class PackageResponse(BaseModel):
    id: uuid.UUID
    title: str
    description:str
    total_value: float
    package_type:str
    tenure_months: int
    fund_amount: int
    created_by_user_id: uuid.UUID | None = None

class Config:
    from_attributes = True



