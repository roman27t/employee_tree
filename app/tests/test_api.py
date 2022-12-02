import random
import pytest
import json
from app.main import app_factory

pytest_plugins = ("pytest_asyncio",)
""" todo 
1. pytest полноценно не завелись, все работает через test_main. 
    Поэтому только минимальные полож.тест без pytest.mark.parametrize
2. бд пока только 1
"""


@pytest.mark.asyncio
async def test_main(aiohttp_client):
    client = await aiohttp_client(await app_factory())
    await _gen_position(aiohttp_client=aiohttp_client, client=client)
    await _get_staff(aiohttp_client=aiohttp_client, client=client)
    await _post_position(aiohttp_client=aiohttp_client, client=client)
    await _patch_position(aiohttp_client=aiohttp_client, client=client)


@pytest.mark.asyncio
async def _gen_position(aiohttp_client, client):
    response = await client.get("/system/init_data/")
    assert response.status == 200


@pytest.mark.asyncio
async def _get_staff(aiohttp_client, client):
    client = await aiohttp_client(await app_factory())
    response = await client.get("/staff/")
    assert response.status == 200
    data = await response.json()
    assert data["staff"]
    assert data["position"]


@pytest.mark.asyncio
async def _post_position(aiohttp_client, client):
    input_data = {
        "last_name": "Ivanov",
        "first_name": "Roman",
        "parent_id": random.randint(2, 3),
        "wage_rate": 99777.01,
        "position_id": 2,
    }
    response = await client.post("/staff/", data=json.dumps(input_data))
    assert response.status == 200
    data = await response.json()
    assert data


@pytest.mark.asyncio
async def _patch_position(aiohttp_client, client):
    input_data = {"last_name": "Sidorov", "first_name": "Alexey"}
    response = await client.patch("/staff/3/", data=json.dumps(input_data))
    assert response.status == 200
    data = await response.json()
    assert data
