import random
import pytest
import json

# todo отдельную бд под тесты


@pytest.mark.asyncio
async def test_gen_position(create_test_client, event_loop):
    client = await create_test_client
    response = await client.get('/system/init_data/')
    assert response.status == 200


@pytest.mark.parametrize(
        'url,status_code,has_data', [
        ('/staff/', 200, True),
        ('/staff/1/', 200, True),
        ('/staff/999999999/', 200, False),
        ('/staff/aaaaa/', 400, False),
    ]
)
@pytest.mark.asyncio
async def test_get_staff(create_test_client, event_loop, url: str, status_code: int, has_data: bool):
    client = await create_test_client
    response = await client.get(url)
    assert response.status == status_code
    data = await response.json()
    if status_code == 200:
        assert bool(data['staff']) is has_data
        assert bool(data['position']) is has_data


@pytest.mark.asyncio
async def test_post_staff(create_test_client, event_loop):
    input_data = {
        'last_name': 'Ivanov',
        'first_name': 'Roman',
        'parent_id': random.randint(2, 3),
        'wage_rate': 99777.01,
        'position_id': 2,
    }
    client = await create_test_client
    response = await client.post('/staff/', data=json.dumps(input_data))
    assert response.status == 200
    data = await response.json()
    assert data['last_name'] == input_data['last_name']


@pytest.mark.asyncio
async def test_patch_staff(create_test_client, event_loop):
    input_data = {'last_name': 'Sidorov', 'first_name': 'Alexey'}
    client = await create_test_client
    response = await client.patch('/staff/3/', data=json.dumps(input_data))
    assert response.status == 200
    data = await response.json()
    assert data


@pytest.mark.parametrize(
        'method,url,status_code,', [
        ('post', '/staff/', 400),
        ('patch', '/staff/3/', 400),
    ]
)
@pytest.mark.asyncio
async def test_send_bad_request_error(create_test_client, event_loop, method: str, url: str, status_code: int):
    client = await create_test_client
    client_method = getattr(client, method)
    response = await client_method(url, data='bad_data')
    assert response.status == status_code
