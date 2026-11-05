import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.adm import get_admin_user 
from app.services.admin import AdminService
from app.schemas.user import UserRead
from app.schemas.post import PostResponse
from app.schemas.farmer import FarmerResponse, FarmResponse
from app.schemas.package import PackageResponse

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_admin_user)]  # Secures the entire router
)

# Dependency injection for the service
def get_admin_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    return AdminService(db)

# --- GET ENDPOINTS ---
@router.get("/users", response_model=list[UserRead])
async def get_users(service: AdminService = Depends(get_admin_service)):
    return await service.get_all_users()

@router.get("/posts", response_model=list[PostResponse])
async def get_posts(service: AdminService = Depends(get_admin_service)):
    return await service.get_all_posts()

@router.get("/farmers", response_model=list[FarmerResponse])
async def get_farmers(service: AdminService = Depends(get_admin_service)):
    return await service.get_all_farmers()

@router.get("/farms", response_model=list[FarmResponse])
async def get_farms(service: AdminService = Depends(get_admin_service)):
    return await service.get_all_farms()

@router.get("/packages", response_model=list[PackageResponse])
async def get_packages(service: AdminService = Depends(get_admin_service)):
    return await service.get_all_packages()

# --- DELETE ENDPOINTS ---
@router.delete("/{entity_type}/{item_id}")
async def delete_entity(
    entity_type: str, 
    item_id: uuid.UUID, 
    service: AdminService = Depends(get_admin_service)
):
    """Dynamically routes the delete request based on the entity type in the URL."""
    success = False
    
    if entity_type == "users":
        success = await service.delete_user(item_id)
    elif entity_type == "posts":
        success = await service.delete_post(item_id)
    elif entity_type == "farmers":
        success = await service.delete_farmer(item_id)
    elif entity_type == "farms":
        success = await service.delete_farm(item_id)
    elif entity_type == "packages":
        success = await service.delete_package(item_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid entity type specified.")

    if not success:
        raise HTTPException(status_code=404, detail=f"{entity_type[:-1].capitalize()} not found.")
    
    return {"message": f"{entity_type[:-1].capitalize()} successfully deleted."}