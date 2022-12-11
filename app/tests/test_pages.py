import pytest

from consts.page_format import RequestFormat
from tools.init_data_db import T_1_FIRST_NAME

req_format = RequestFormat()


@pytest.mark.parametrize(
    'url,status_code,text',
    [
        ('/', 200, 'tree'),
        (f'/staff/?{req_format.param_encode}', 200, T_1_FIRST_NAME),
        (f'/staff/1/?{req_format.param_encode}', 200, T_1_FIRST_NAME),
        (f'/staff/bad_id/?{req_format.param_encode}', 200, 'Error'),
    ],
)
@pytest.mark.asyncio
async def test_html_pages(create_test_client, event_loop, url: str, status_code: int, text: str):
    client = await create_test_client
    response = await client.get(url)
    assert response.status == status_code
    assert text in await response.text()
