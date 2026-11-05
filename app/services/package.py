import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.package import PackageModel
from app.schemas.package import PackageCreate

class PackageService:
    def __init__(self, db: AsyncSession):
        
        self.db = db

    async def create_package_service(self, package_data: PackageCreate, user_id: uuid.UUID) -> PackageModel:
        
        new_package = PackageModel(
            **package_data.model_dump(),
            created_by_user_id=user_id
        )
        self.db.add(new_package)
        await self.db.commit()
        await self.db.refresh(new_package)
        return new_package

    async def get_all_packages_service(self) -> list[PackageModel]:
        
        result = await self.db.execute(select(PackageModel))
        return list(result.scalars().all())