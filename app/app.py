from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.base import Base

import app.models.user   
import app.models.farmer
import app.models.post
from app.db import create_db_and_table

from app.routers.post import router as post_router
from app.routers.auth import router as auth_router
from app.routers.farmer import router as farmer_router
from app.routers.package import router as package_router
from app.routers.admin import router as admin_router
app = FastAPI(title="CLOUDY")

@app.on_event("startup")
async def initialize_database():
    await create_db_and_table()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(farmer_router, prefix="/api/v1")  
app.include_router(package_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def root():
    return {"message": "Cloudy API is running and connected to Neon!"}