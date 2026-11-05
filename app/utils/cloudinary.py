import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

async def upload_file_to_cloudinary(file: UploadFile) -> str:
    try:
        file_content = await file.read()
        # resource_type="auto" handles both images and videos
        upload_result = cloudinary.uploader.upload(file_content, resource_type="auto")
        return upload_result.get("secure_url")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cloudinary upload failed: {str(e)}"
        )