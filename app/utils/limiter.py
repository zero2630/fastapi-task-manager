from typing import Callable

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings

limiter = Limiter(key_func=get_remote_address, storage_uri=settings.redis_url)


def setup_limiter(app: FastAPI) -> None:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def noop_decorator(func):
    return func


def custom_limiter(limit_config: Callable):
    if settings.rate_limit_enabled:
        return limiter.limit(limit_config)
    return noop_decorator
