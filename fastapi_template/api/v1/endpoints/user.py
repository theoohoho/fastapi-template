from fastapi import APIRouter, Depends

from .depends import get_current_active_user

router = APIRouter()


@router.get("/user/me")
def get_user_me(current_user: any = Depends(get_current_active_user)):
    return current_user
