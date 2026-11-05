from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models.user import User
from app.user import current_active_user
from app.schemas.package import PackageCreate, PackageResponse
from app.services.package import PackageService  

router = APIRouter(
    prefix="/packages",
    tags=["Packages"]
)

@router.post("/", response_model=PackageResponse)
async def create_package(
    package_data: PackageCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user)
):
    
    service = PackageService(db)  
    return await service.create_package_service(package_data,user.id)

@router.get("/", response_model=list[PackageResponse])
async def get_packages(db: AsyncSession = Depends(get_db)):
    
    service = PackageService(db) 
    return await service.get_all_packages_service()