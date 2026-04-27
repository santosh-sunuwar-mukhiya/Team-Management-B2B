from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference


app = FastAPI(
    title="Team Management API",
    description="API documentation for the Team Management service",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "hello world."}


# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
