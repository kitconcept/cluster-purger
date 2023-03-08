from .healthcheck import router as healthcheck
from .info import router as info
from .proxy import router as proxy
from fastapi import FastAPI
from fastapi import Request

import time


app = FastAPI(title="Cluster Purger")


app.include_router(
    healthcheck,
    tags=["healthcheck"],
)

app.include_router(
    info,
    tags=["info"],
)

app.include_router(
    proxy,
    tags=["proxy"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Attach header with total process time for the request."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
