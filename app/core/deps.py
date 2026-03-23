from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.db import get_async_session
from app.services.auth import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_active_user(
    token: Annotated[str, Depends(oauth2_scheme)], session=Depends(get_async_session)
):
    current_user = await get_current_user(token, session)
    return current_user
