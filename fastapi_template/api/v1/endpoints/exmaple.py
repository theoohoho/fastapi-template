from fastapi import APIRouter

router = APIRouter()


@router.get("async_endpoint")
async def foo_async():
    pass


@router.get("normal_endpoint")
def foo():
    pass
