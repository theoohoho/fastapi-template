from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
def login():
    pass


@router.post("/logout")
def logout():
    pass
