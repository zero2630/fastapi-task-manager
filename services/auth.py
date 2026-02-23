from datetime import timedelta, datetime, timezone

from fastapi import HTTPException
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from schemas.auth import UserSignUp, UserRead, TokenData
from models.auth import UserModel
from config import Settings

settings = Settings()

SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_alg
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_ttl
ISSUER = settings.issuer
AUDIENCE = settings.audience


password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


async def authenticate_user(email: str, password: str, session):
    user = (
        await session.execute(select(UserModel).filter_by(email=email))
    ).scalar_one_or_none()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "exp": expire,
            "iss": ISSUER,
            "aud": AUDIENCE,
            "iat": datetime.now(timezone.utc),
            "nbf": datetime.now(timezone.utc),
            "token_type": "access",
        }
    )
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str, session):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        if payload.get("token_type") != "access":
            raise credentials_exception

        token_data = TokenData(user_id=user_id)

    except InvalidTokenError:
        raise credentials_exception

    user = await session.get(UserModel, int(user_id))

    if user is None:
        raise credentials_exception

    return UserRead.model_validate(user)


async def db_add_user(add_user: UserSignUp, session):
    hashed_password = get_password_hash(add_user.password)
    db_user = UserModel(
        email=add_user.email,
        hashed_password=hashed_password,
    )

    try:
        session.add(db_user)
        await session.flush()
        return db_user
    except IntegrityError as e:
        if isinstance(getattr(e.orig, "__cause__", None), UniqueViolationError):
            raise HTTPException(
                status_code=409, detail="User with that email already exists"
            )
        print(type(e.orig))
        raise HTTPException(status_code=500)


async def signup_user(add_user, session):
    user = await db_add_user(add_user, session)
    user_read = UserRead.model_validate(user)
    return user_read
