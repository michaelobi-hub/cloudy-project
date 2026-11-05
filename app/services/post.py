from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import uuid
from sqlalchemy import select
from fastapi import UploadFile, HTTPException, status
from app.models.post import Post
from app.utils.cloudinary import upload_file_to_cloudinary

class PostService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db # Stores the async database session

    async def create_post(self, title: str, content: str, file: UploadFile, user_id=None):
        
        media_url = await upload_file_to_cloudinary(file)

        # 2. Convert user_id to string so SQLite/aiosqlite can bind it safely
        string_user_id = str(user_id) if user_id else None

        # 3. Create post instance
        new_post = Post(title=title, content=content, media_url=media_url, user_id=string_user_id)

        # 4. Save to database asynchronously
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)

        return new_post

    async def get_all_posts(self):
        stmt = select(Post).options(selectinload(Post.user))
        result = await self.db.execute(select(Post))
        return result.scalars().all()

    async def get_user_posts(self, user_id: str):
        result = await self.db.execute(select(Post).where(Post.user_id == str(user_id)))
        return result.scalars().all()
    
    async def get_post_by_id(self, post_id: str):
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        post = result.scalar_one_or_none()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found"
            )
        return post