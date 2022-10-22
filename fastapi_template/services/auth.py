import jose
from loguru import logger
from sqlalchemy.orm import Session

from fastapi_template import crud, model
from fastapi_template.common import exceptions, secure
from fastapi_template.core import Settings
from fastapi_template.schemas.user import UserUpdate


def destroy_token(token, user):
    pass


def forgot_password(settings: Settings, user: model.User) -> None:
    if not user.is_active:
        raise exceptions.UserInactive()

    token_data = {
        "sub": str(user.id),
        "password_fgpt": secure.get_password_hash(user.hashed_password),
        "aud": settings.jwt.reset_password_aud,
    }
    token = secure.create_access_token(settings, token_data)
    # trigger handler on success.
    on_after_forgot_password(user, token)


def on_after_forgot_password(user, token):
    """
    Should make your own logic.
    """
    logger.info(f"Forgot password for user {user.email}, token: {token}")


def on_after_reset_password(user):
    """
    Should make your own logic.
    """
    pass


def reset_password(
    settings: Settings,
    session: Session,
    password: str,
    token: str,
):
    try:
        data = secure.decode_jwt(
            token,
            settings.jwt.secret_key,
            settings.jwt.algorithm,
            settings.jwt.reset_password_aud,
        )
    except jose.JWTError:
        raise exceptions.InvalidResetPasswordToken()

    try:
        user_id = int(data["sub"])
        password_fingerprint = data["password_fgpt"]
    except KeyError:
        raise exceptions.InvalidResetPasswordToken()

    try:
        user = crud.user.get(session, id=user_id)
    except exceptions.InvalidID:
        raise exceptions.InvalidResetPasswordToken()

    valid_password_fingerprint, _ = secure.verify_and_update(
        user.hashed_password, password_fingerprint
    )
    if not valid_password_fingerprint:
        raise exceptions.InvalidResetPasswordToken()

    if not user.is_active:
        raise exceptions.UserInactive()

    updated_user = crud.user.update(
        session, db_obj=user, obj_in=UserUpdate(password=password)
    )

    on_after_reset_password(user)

    return updated_user
