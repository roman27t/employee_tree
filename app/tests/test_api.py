import json
import random
import datetime as dt
from typing import Optional

import pytest


@pytest.mark.asyncio
async def test_gen_position(create_test_client, event_loop):
    client = await create_test_client
    response = await client.get('/system/init_data/')
    assert response.status == 200


@pytest.mark.parametrize(
    'url,status_code,has_data',
    [
        ('/staff/', 200, True),
        ('/staff/1/', 200, True),
        ('/staff/999999999/', 200, False),
        ('/staff/aaaaa/', 400, False),
    ],
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


def __create_data_person(exclude_fields: Optional[tuple[str]] = None) -> dict:
    birthdate = dt.datetime.strptime('21.11.1940', '%d.%m.%Y').date() + dt.timedelta(days=random.randint(1, 21900))
    person = {
        'last_name': 'Ivanov',
        'first_name': 'Roman',
        'parent_id': random.randint(2, 3),
        'wage_rate': 99777.01,
        'position_id': random.randint(1, 7),
        'birthdate': birthdate.isoformat(),
    }
    for field in exclude_fields or []:
        del person[field]
    return person


@pytest.mark.parametrize(
    'person,status_code,',
    [
        (__create_data_person(), 200),
        (__create_data_person(exclude_fields=('birthdate',)), 400),
    ],
)
@pytest.mark.asyncio
async def test_post_staff(create_test_client, event_loop, person: dict, status_code: int):
    client = await create_test_client
    response = await client.post('/staff/', data=json.dumps(person))
    assert response.status == status_code
    data = await response.json()
    if status_code == 200:
        assert data['last_name'] == person['last_name']


@pytest.mark.asyncio
async def test_post_staff_duplicate(create_test_client, event_loop):
    client = await create_test_client
    input_data = __create_data_person()
    response_1 = await client.post('/staff/', data=json.dumps(input_data))
    response_2 = await client.post('/staff/', data=json.dumps(input_data))
    assert response_1.status == 200
    assert response_2.status == 403


@pytest.mark.parametrize(
    'pk,input_data,status_code,',
    [
        (3, {'last_name': 'Sidorov', 'first_name': 'Alexey'}, 200),
        (3, {'last_name': 'Tor', 'birthdate': dt.datetime.strptime('21.11.2000', '%d.%m.%Y').date().isoformat()}, 200),
        (3, {}, 400),
        (3, {'last_name': 'Rebrov', 'birthdate': 'bad_date'}, 400),
        (3, {'last_name': 'Rebrov', 'position_id': 99999999}, 400),
        (99999999, {'last_name': 'Sidorov', 'first_name': 'Alexey'}, 400),
    ],
)
@pytest.mark.asyncio
async def test_patch_staff(create_test_client, event_loop, pk: int, input_data: dict, status_code: int):
    client = await create_test_client
    response = await client.patch(f'/staff/{pk}/', data=json.dumps(input_data))
    assert response.status == status_code
    data = await response.json()
    if status_code == 200:
        assert data


@pytest.mark.parametrize(
    'method,url,status_code,',
    [
        ('post', '/staff/', 400),
        ('patch', '/staff/3/', 400),
    ],
)
@pytest.mark.asyncio
async def test_send_bad_request_error(create_test_client, event_loop, method: str, url: str, status_code: int):
    client = await create_test_client
    client_method = getattr(client, method)
    response = await client_method(url, data='bad_data')
    assert response.status == status_code
