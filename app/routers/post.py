from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db import get_db
from app.schemas.post import PostResponse
from app.services.post import PostService
from app.user import current_active_user
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user) 
):
    service = PostService(db)
    return await service.create_post(title, content, file, user_id=user.id)

@router.get("/", response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    service = PostService(db)
    return await service.get_all_posts()


@router.get("/my-posts", response_model=List[PostResponse])
async def get_my_posts(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    service = PostService(db)
    return await service.get_user_posts(str(user.id))

@router.get("/{post_id}", response_model=PostResponse)
async def get_single_post(post_id: str, db: AsyncSession = Depends(get_db)):
    service = PostService(db)
    return await service.get_post_by_id(post_id)