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
