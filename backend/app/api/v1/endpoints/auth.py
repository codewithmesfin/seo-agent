from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, Token
from app.services import auth
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.schemas.user import TokenPayload

router = APIRouter()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

async def get_current_user(
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await User.get(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate) -> Any:
    user = await User.find_one(User.email == user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    user = User(
        email=user_in.email,
        hashed_password=auth.get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    await user.insert()
    return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await User.find_one(User.email == form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": auth.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": auth.create_refresh_token(user.id),
        "token_type": "bearer",
    }

@router.post("/api-key", response_model=Any)
async def generate_api_key(
    current_user: User = Depends(get_current_user)
) -> Any:
    import secrets
    api_key = secrets.token_urlsafe(32)
    current_user.api_key = api_key
    await current_user.save()
    return {"api_key": api_key}
