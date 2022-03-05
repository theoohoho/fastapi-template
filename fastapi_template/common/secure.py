from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from fastapi_template.core.settings import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(settings: Settings, data: dict, expires_delta: int = 30):
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    data.update({"exp": expire})
    return jwt.encode(data, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
