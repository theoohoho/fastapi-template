import jose
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from fastapi_template import crud
from fastapi_template.core.settings import Settings, get_settings
from fastapi_template.db.db import get_db_session
from fastapi_template.model import user as model_user
from fastapi_template.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_current_user(
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jose.jwt.decode(
            token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
        )
        token_data = TokenData(username=payload.get("sub"))
    except jose.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = crud.user.get_by_email(session, email=token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_token(
    token: str = Depends(oauth2_scheme),
):
    return token


async def get_current_active_user(
    current_user: model_user.User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
