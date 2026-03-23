from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.services import auth
from app.schemas.auth import Token, UserRead, UserSignUp
from app.core.db import get_async_session
from app.utils.limiter import custom_limiter
from app.core.deps import get_active_user

router = APIRouter()


@router.post("/signup", response_model=UserRead)
async def sign_up(
    user_data: UserSignUp, session=Depends(get_async_session)
) -> UserRead:
    user = await auth.signup_user(user_data, session)
    return user


@router.post("/token", response_model=Token)
@custom_limiter("10/minute")
async def login_for_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session=Depends(get_async_session),
) -> Token:
    user = await auth.authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    access_token_expires = timedelta(minutes=15)
    access_token = await auth.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=UserRead)
async def get_my_user(
    current_user=Depends(get_active_user),
) -> UserRead:
    return current_user
