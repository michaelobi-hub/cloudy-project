from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status, UploadFile, APIRouter
from typing import Optional, Union, List
import uuid

from app.models.farmer import FarmerModel, FarmModel
from app.schemas.farmer import FarmerCreate, FarmCreate
from app.utils.cloudinary import upload_file_to_cloudinary


router = APIRouter(prefix="/farmers", tags=["Farmers & Farms"])

class FarmerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_farmer(self, data: FarmerCreate, file: Optional[UploadFile] = None):
        photo_url = None
        if file:
            photo_url = await upload_file_to_cloudinary(file)

        new_farmer = FarmerModel(
            photo_url=photo_url,
            **data.model_dump()
        )

        self.db.add(new_farmer)
        await self.db.commit()
        await self.db.refresh(new_farmer)
        return new_farmer

    async def get_all_farmers(self):
        result = await self.db.execute(
            select(FarmerModel).options(selectinload(FarmerModel.farms))
        )
        return result.scalars().all()

    async def get_farmer_by_id(self, farmer_id: uuid.UUID):
        result = await self.db.execute(
            select(FarmerModel).options(selectinload(FarmerModel.farms)).where(FarmerModel.id == farmer_id)
        )
        farmer = result.scalar_one_or_none()
        if not farmer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found")
        return farmer

    async def get_all_farms(self):
        result = await self.db.execute(
            select(FarmModel).options(selectinload(FarmModel.farms))
        )
        return result.scalars().all()

    
    async def add_farm_to_farmer(self, farmer_id: uuid.UUID, data: FarmCreate):
        # Verify farmer existsfirst
        await self.get_farmer_by_id(farmer_id)

        new_farm = FarmModel(
            farmer_id=farmer_id,
            **data.model_dump()
        )

        self.db.add(new_farm)
        await self.db.commit()
        await self.db.refresh(new_farm)
        return new_farm
    