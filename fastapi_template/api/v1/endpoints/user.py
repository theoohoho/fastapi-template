from fastapi import APIRouter

router = APIRouter()


@router.post("/user_me")
def get_user_me():
    pass
