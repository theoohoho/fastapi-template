from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from fastapi_template import crud
from fastapi_template.common import enums, exceptions
from fastapi_template.common.secure import create_access_token
from fastapi_template.core.settings import Settings, get_settings
from fastapi_template.db import get_db_session
from fastapi_template.schemas.auth import RegisterUser
from fastapi_template.services import auth as auth_service

from .depends import get_current_active_user, get_current_token

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


@router.post(
    "/logout",
    status_code=status.HTTP_202_ACCEPTED,
)
def logout(
    token: str = Depends(get_current_token),
    current_user: any = Depends(get_current_active_user),
):
    auth_service.destroy_token(token, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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


@router.post(
    "/forgot-password",
    status_code=status.HTTP_202_ACCEPTED,
)
async def forgot_password(
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_db_session),
    email: EmailStr = Body(..., embed=True),
):
    try:
        user = crud.user.get_by_email(session, email=email)
    except exceptions.UserNotExists:
        return None

    try:
        auth_service.forgot_password(settings, user)
        pass
    except exceptions.UserInactive:
        pass

    return None


@router.post(
    "/reset-password",
)
async def reset_password(
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_db_session),
    token: str = Body(...),
    password: str = Body(...),
):
    try:
        auth_service.reset_password(settings, session, password, token)
    except (
        exceptions.InvalidResetPasswordToken,
        exceptions.UserNotExists,
        exceptions.UserInactive,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=enums.ErrorCode.RESET_PASSWORD_BAD_TOKEN,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": enums.ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
