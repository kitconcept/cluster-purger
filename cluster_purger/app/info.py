from cluster_purger.config import settings
from cluster_purger.utils import resolve_service_name
from fastapi import APIRouter


router = APIRouter()


@router.get("/info")
async def info():
    """Respond to a healthcheck."""
    service_name = settings.get_fresh("SERVICE_NAME")
    hostnames = settings.get_fresh("PUBLIC_SITES", default=[])
    return {
        "service_name": service_name,
        "addresses": resolve_service_name(service_name),
        "hostnames": hostnames,
    }
