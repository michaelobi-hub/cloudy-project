from datetime import datetime
from pydantic import BaseModel
import uuid
from app.schemas.user import UserRead

class PostResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    media_url: str | None = None
    created_at: datetime
    user: UserRead

    class Config:
        from_attributes = True