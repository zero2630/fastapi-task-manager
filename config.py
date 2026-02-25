from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: str
    redis_url: str

    origins: list[str]
    allowed_hosts: list[str]

    rate_limit_enabled: bool

    jwt_secret: str
    issuer: str
    audience: str
    jwt_alg: str
    access_ttl: int


settings = Settings()
