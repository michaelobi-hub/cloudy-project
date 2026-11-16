from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
import uuid

from app.models.farmer import FarmerModel, FarmModel
from app.schemas.farmer import FarmerCreate, FarmCreate
class FarmerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_farmer(self, data: FarmerCreate):
        new_farmer = FarmerModel(**data.model_dump())

        self.db.add(new_farmer)
        await self.db.commit()
        return await self.get_farmer_by_id(new_farmer.id)

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
    