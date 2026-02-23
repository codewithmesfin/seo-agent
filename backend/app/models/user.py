from datetime import datetime, timezone
from typing import Optional, List
from beanie import Document, Indexed
from pydantic import EmailStr, Field

class User(Document):
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    role: str = "user" # user, admin, pro
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    api_key: Optional[str] = None

    class Settings:
        name = "users"
        indexes = [
            "email",
            "api_key",
        ]

    async def update_updated_at(self):
        self.updated_at = datetime.now(timezone.utc)
        await self.save()
