from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid
import json

from app.db import get_db
from app.schemas.farmer import FarmerCreate, FarmerResponse, FarmCreate, FarmResponse, FarmerRead, Gender, FarmingCategory
from app.services.farmer import FarmerService
from app.schemas.farmer import FarmingCategory
from app.user import current_active_user
from app.models.user import User

router = APIRouter(prefix="/farmers", tags=["Farmers & Farms"])

@router.post("/", response_model=FarmerRead, status_code=status.HTTP_201_CREATED)
async def create_farmer(
    payload: FarmerCreate,
    db: AsyncSession =Depends(get_db),
    user: User = Depends(current_active_user)
):
    # Pydantic will automatically validate and convert the strings into your Enums here!
    
    service = FarmerService(db)
    return await service.create_farmer(payload)

@router.get("/", response_model=List[FarmerResponse])
async def get_farmers(db: AsyncSession = Depends(get_db)):
    service = FarmerService(db)
    return await service.get_all_farmers()

@router.get("/{farmer_id}", response_model=FarmerResponse)
async def get_farmer(farmer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    service = FarmerService(db)
    return await service.get_farmer_by_id(farmer_id)

@router.post("/{farmer_id}/farms", response_model=FarmResponse, status_code=status.HTTP_201_CREATED)
async def add_farm(
    farmer_id: uuid.UUID,
    data: FarmCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    service = FarmerService(db)
    return await service.add_farm_to_farmer(farmer_id, data)

@router.get("/", response_model=List[FarmResponse])
async def get_farm(db: AsyncSession = Depends(get_db)):
    service = FarmerService(db)
    return await service.get_all_farms()
