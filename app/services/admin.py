import uuid
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.post import Post
from app.models.farmer import FarmerModel, FarmModel
from app.models.package import PackageModel

class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _delete_item(self, model, item_id: uuid.UUID) -> bool:
        """Generic helper to find and delete a record by ID."""
        item = await self.db.get(model, item_id)
        if not item:
            return False
        await self.db.delete(item)
        await self.db.commit()
        return True

    # --- GET ALL METHODS ---
    async def get_all_users(self) -> list[User]:
        return list((await self.db.execute(select(User))).scalars().all())

    async def get_all_posts(self) -> list[Post]:
        stmt = select(Post).options(selectinload(Post.user))
        return list((await self.db.execute(stmt)).scalars().all())

    async def get_all_farmers(self) -> list[FarmerModel]:
        return list((await self.db.execute(select(FarmerModel))).scalars().all())

    async def get_all_farms(self) -> list[FarmModel]:
        return list((await self.db.execute(select(FarmModel))).scalars().all())

    async def get_all_packages(self) -> list[PackageModel]:
        return list((await self.db.execute(select(PackageModel))).scalars().all())

    # --- DELETE METHODS ---
    async def delete_user(self, item_id: uuid.UUID) -> bool:
        return await self._delete_item(User, item_id)

    async def delete_post(self, item_id: uuid.UUID) -> bool:
        return await self._delete_item(Post, item_id)

    async def delete_farmer(self, item_id: uuid.UUID) -> bool:
        return await self._delete_item(FarmerModel, item_id)

    async def delete_farm(self, item_id: uuid.UUID) -> bool:
        return await self._delete_item(FarmModel, item_id)

    async def delete_package(self, item_id: uuid.UUID) -> bool:
        return await self._delete_item(PackageModel, item_id)