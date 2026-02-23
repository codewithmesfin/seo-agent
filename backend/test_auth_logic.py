import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.services import auth
from app.core.config import settings

async def test_auth():
    # Setup mock settings if needed, but here we just test the logic
    print("Testing password hashing...")
    password = "testpassword123"
    hashed = auth.get_password_hash(password)
    assert auth.verify_password(password, hashed)
    assert not auth.verify_password("wrongpassword", hashed)
    print("Password hashing works!")

    print("Testing token creation...")
    user_id = "507f1f77bcf86cd799439011"
    token = auth.create_access_token(user_id)
    assert token is not None
    print("Token creation works!")

if __name__ == "__main__":
    asyncio.run(test_auth())
