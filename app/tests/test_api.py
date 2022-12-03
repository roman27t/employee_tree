import random
import pytest
import json

''' todo 
1. без pytest.mark.parametrize
2. бд пока только 1
'''


@pytest.mark.asyncio
async def test_gen_position(create_test_client, event_loop):
    client = await create_test_client
    response = await client.get('/system/init_data/')
    assert response.status == 200


@pytest.mark.asyncio
async def test_get_staff(create_test_client, event_loop):
    client = await create_test_client
    response = await client.get('/staff/')
    assert response.status == 200
    data = await response.json()
    assert data['staff']
    assert data['position']


@pytest.mark.asyncio
async def test__post_position(create_test_client, event_loop):
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
    assert data


@pytest.mark.asyncio
async def test_patch_position(create_test_client, event_loop):
    input_data = {'last_name': 'Sidorov', 'first_name': 'Alexey'}
    client = await create_test_client
    response = await client.patch('/staff/3/', data=json.dumps(input_data))
    assert response.status == 200
    data = await response.json()
    assert data
