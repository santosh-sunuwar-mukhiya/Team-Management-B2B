from fastapi import FastAPI # type: ignore
from scalar_fastapi import get_scalar_api_reference # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from .config import settings
from .api.routers import task, webhooks


app = FastAPI(
    title="Team Management API",
    description="API documentation for the Team Management service",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)
# app.include_router(webhooks.router)


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
