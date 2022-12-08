import sys
import asyncio

import pytest
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from main import app_factory
from models import Base
from tools.init_data_db import init_data

_T_DB_NAME = 'postgres_test'
_T_DB_URL=f'postgresql+asyncpg://postgres:postgres@pg_db/{_T_DB_NAME}'
engine = create_async_engine(_T_DB_URL, echo=True)


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
        if _T_DB_NAME in engine.url:
            await conn.execute(text('CREATE EXTENSION IF NOT EXISTS ltree;'))
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    await init_data(sa_session=async_session())
    return await aiohttp_client(await app_factory(db_url=_T_DB_URL))
