from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fastapi_template import crud
from fastapi_template.common.secure import create_access_token
from fastapi_template.core.settings import Settings, get_settings
from fastapi_template.db.db import get_db_session
from fastapi_template.schemas.auth import RegisterUser

app = FastAPI()

router = APIRouter()


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_db_session),
):
    user = crud.user.authenticate(
        session, email=request.username, password=request.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = create_access_token(
        settings=settings,
        data=dict(sub=user.email),
        expires_delta=settings.jwt.access_token_expire_minutes,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    pass


@router.post("/signup")
def signup(
    session: Session = Depends(get_db_session),
    body: RegisterUser = Body(...),
):
    from fastapi_template.schemas.user import UserCreate

    user = crud.user.get_by_email(session, email=body.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(session, obj_in=UserCreate(**body.dict()))
    return user
