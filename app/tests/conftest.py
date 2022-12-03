import pytest
import sys
import asyncio
from app.main import app_factory

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

@pytest.fixture(scope="session")
def _database_url():
    return "postgresql+asyncpg://postgres:masterkey@localhost/dbtest"


# @pytest.fixture(scope="session")
# def init_database():
#     from myprorject.db import metadata
#
#     return metadata.create_all

# @pytest.fixture
# async def create_test_app():
#     app = app_factory()
#     # await app.startup()
#     yield app
#     # await app.shutdown()
#
#
# @pytest.fixture
# def create_test_client(create_test_app):
#     print(' create_test_client ')
#     return create_test_app.test_client()


# @pytest.fixture
# async def create_test_client(aiohttp_client):
#     client = await aiohttp_client(await app_factory())
#     return client


# @pytest.fixture
# async def create_test_client(aiohttp_client):
#     app = aiohttp_client(await app_factory())
#     yield app
#     # async with AsyncClient(app=app, base_url='http://localhost:8000/') as async_client:
#     #     yield async_client


# @pytest.fixture
# async def create_test_client(loop, aiohttp_client):
#     # app = web.Application()
#     # app.router.add_get('/', previous)
#     # app.router.add_post('/', previous)
#     return loop.run_until_complete(await app_factory())
#
#
# # @pytest.fixture
# # async def create_test_client(aiohttp_client):
# #     return await aiohttp_client(await app_factory())
#
#
# @pytest.fixture
# def loop():
#     return asyncio.get_event_loop()


# @pytest.fixture
# def loop(event_loop):
#     return event_loop

#
####################################


# @pytest.mark.asyncio
# @pytest.fixture
# async def create_test_client(aiohttp_client):
#     async with aiohttp_client(await app_factory()) as c:
#         yield c
#    # return await aiohttp_client(await app_factory())

@pytest.mark.asyncio
@pytest.fixture
async def create_test_client(aiohttp_client):
   return await aiohttp_client(await app_factory())
