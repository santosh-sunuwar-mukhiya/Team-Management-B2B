from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore

_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore",
)


class Setting(BaseSettings):
    CLERK_SECRET_KEY: str
    CLERK_PUBLISHABLE_KEY: str
    CLERK_JWKS_URL: str
    CLERK_WEBHOOK_SECRET: str
    DATABASE_URL: str
    FRONTEND_URL: str

    FREE_TIER_LIMIT: int = 2
    PRO_TIER_MEMBERSHIP_LIMIT = 0  # unlimited.

    model_config = _base_config


settings = Setting()
