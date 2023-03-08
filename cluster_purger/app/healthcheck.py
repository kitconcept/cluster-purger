from fastapi import APIRouter


router = APIRouter()


@router.get("/ok")
async def healthcheck():
    """Respond to a healthcheck."""
    return "Ok"
