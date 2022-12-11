import pytest

from tools.init_data_db import T_1_FIRST_NAME


@pytest.mark.parametrize(
    'url,status_code,text',
    [
        ('/', 200, 'tree'),
        ('/staff/?html=1', 200, T_1_FIRST_NAME),
        ('/staff/1/?html=1', 200, T_1_FIRST_NAME),
        ('/staff/bad_id/?html=1', 200, 'Error'),
    ],
)
@pytest.mark.asyncio
async def test_html_pages(create_test_client, event_loop, url: str, status_code: int, text: str):
    client = await create_test_client
    response = await client.get(url)
    assert response.status == status_code
    assert text in await response.text()
