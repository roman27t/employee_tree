import json

import pytest


@pytest.mark.parametrize(
    'url,status_code,has_data',
    [
        ('/position/', 200, True),
        ('/position/7/', 200, True),
        ('/position/999999999/', 400, False),
        ('/position/aaaaa/', 400, False),
    ],
)
@pytest.mark.asyncio
async def test_get_position(create_test_client, event_loop, url: str, status_code: int, has_data: bool):
    client = await create_test_client
    response = await client.get(url)
    assert response.status == status_code
    data = await response.json()
    if status_code == 200:
        assert data['7']['name'] == 'security_guard'


@pytest.mark.parametrize(
    'input_data,status_code,',
    [
        ({'name': 'Lawyer', 'detail': 'detail of admin'}, 200),
        ({'name': 'economist'}, 200),
        ({'name': 'r'}, 400),
        ({'name': 'admin'}, 403),
    ],
)
@pytest.mark.asyncio
async def test_post_position(create_test_client, event_loop, input_data: dict, status_code: int):
    client = await create_test_client
    response = await client.post('/position/', data=json.dumps(input_data))
    assert response.status == status_code
    data = await response.json()
    if status_code == 200:
        assert data['name'] == input_data['name'].lower()


@pytest.mark.parametrize(
    'pk,input_data,status_code,',
    [
        (3, {'name': 'accountant', 'detail': 'accountant detail'}, 200),
        (3, {'detail': 'detail'}, 200),
        (3, {}, 400),
        (99999999, {'name': 'accountant', 'detail': 'detail detail'}, 400),
    ],
)
@pytest.mark.asyncio
async def test_patch_position(create_test_client, event_loop, pk: int, input_data: dict, status_code: int):
    client = await create_test_client
    response = await client.patch(f'/position/{pk}/', data=json.dumps(input_data))
    assert response.status == status_code
    data = await response.json()
    if status_code == 200:
        assert data
