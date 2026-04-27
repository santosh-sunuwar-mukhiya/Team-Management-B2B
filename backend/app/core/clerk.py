from clerk_backend_api import Clerk  # type: ignore
from app.config import settings

clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)
