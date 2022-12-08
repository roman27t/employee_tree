import sys
import asyncio

import pytest

from sqlalchemy.orm import sessionmaker
from models import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text

from app.main import app_factory
from app.tools.init_data_db import init_data

DB_URL='postgresql+asyncpg://postgres:postgres@pg_db/postgres_test'
engine = create_async_engine(DB_URL, echo=True)


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
@pytest.fixture
async def create_test_client(aiohttp_client):
    async with engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS ltree;'))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    await init_data(sa_session=async_session())
    return await aiohttp_client(await app_factory(db_url=DB_URL))
