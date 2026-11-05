import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class FarmStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class FarmingCategory(str, Enum):
    CROP_FARMING = "crop_farming"
    FISHERY = "fishery"
    MIXED_FARMING = "mixed_farming"
    POULTRY = "poultry"
    LIVESTOCK = "livestock",
    OTHERS = "others"


class FarmCreate(BaseModel):
    name: str
    location: str
    size_in_hectares: float
    farming_category: Optional[FarmingCategory] = None
    status: FarmStatus = FarmStatus.ACTIVE
    date_added: Optional[str] = None

class FarmerCreate(BaseModel):
    full_name: str
    nin: str
    phone_number: str
    gender: Gender
    farming_category: Optional[FarmingCategory] = None
    photo: Optional[str] = None
    additional_info: Optional[str] = None
    date_added: Optional[str] = None

class FarmRead(BaseModel):
    id: uuid.UUID
    farmer_id: uuid.UUID
    name: str
    location: str
    size_in_hectares: float
    farming_category: Optional[FarmingCategory] = None
    status: FarmStatus
    created_at: datetime
    updated_at: datetime
    date_added: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

FarmResponse = FarmRead


class FarmerRead(BaseModel):
    id: uuid.UUID
    full_name: str
    nin: str
    phone_number: str
    gender: Gender
    farming_category: Optional[FarmingCategory] = None
    photo: Optional[str] = None
    additional_info: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    date_added: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

FarmerResponse = FarmerRead
