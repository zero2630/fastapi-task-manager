
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings


engine = create_async_engine(settings.database_url)


async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        async with session.begin():
            yield session


async def create_db():
    from models import base

    async with engine.begin() as connection:
        await connection.run_sync(base.Base.metadata.create_all)


async def drop_db():
    from models import base

    async with engine.begin() as connection:
        await connection.run_sync(base.Base.metadata.drop_all)
