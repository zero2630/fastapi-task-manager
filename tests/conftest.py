import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.db import get_async_session
from app.main import app
from models import Base


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_engine):
    connection = await test_engine.connect()
    trans = await connection.begin()
    test_session_maker = async_sessionmaker(bind=connection)
    session = test_session_maker()

    async def override_get_async_session():
        yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    yield

    await session.close()
    if trans.is_active:
        await trans.rollback()
    await connection.close()

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def client(db_session):

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost",
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def test_user(client):
    body = {
        "email": "kekw@example.com",
        "password": "12345678",
    }

    response = await client.post("/signup", json=body)
    assert response.status_code == 200

    yield response


@pytest.fixture(scope="function")
async def user_token(test_user, client):
    data = {
        "username": "kekw@example.com",
        "password": "12345678",
    }
    response = await client.post("/token", data=data)
    response_data = response.json()

    assert response.status_code == 200
    assert "access_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"

    yield response_data["access_token"]
