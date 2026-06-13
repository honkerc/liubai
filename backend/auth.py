from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from passlib.hash import bcrypt
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from tortoise.exceptions import DoesNotExist

from config import SECRET_KEY
from models import User
from schemas import UserLogin, Token

router = APIRouter(prefix="/api/auth", tags=["auth"])

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def create_token(user: User) -> str:
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="无效的令牌")
    except JWTError:
        raise HTTPException(status_code=401, detail="无效的令牌")

    try:
        user = await User.get(id=user_id)
    except DoesNotExist:
        raise HTTPException(status_code=401, detail="用户不存在")

    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security),
) -> Optional[User]:
    if credentials is None:
        return None

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    try:
        return await User.get(id=user_id)
    except DoesNotExist:
        return None


@router.post("/login", response_model=Token)
async def login(data: UserLogin):
    try:
        user = await User.get(username=data.username)
    except DoesNotExist:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    if not bcrypt.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = create_token(user)
    return Token(access_token=token)
