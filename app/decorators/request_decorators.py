import json
import functools
from typing import Callable

import aiohttp_jinja2

from aiohttp import web

from validations import ValidateAbstract


def validation(class_validate):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            _self = args[0]
            db_session = _self.get_sa_session()
            validator: ValidateAbstract = class_validate(
                pk=_self.request.match_info.get('id'),
                body=None if _self.request.method == 'GET' else await _self.request.text(),
                db_session=db_session,
            )
            if not await validator.is_valid():
                return web.json_response(validator.output_data, status=validator.status_code)
            response = await func(*args, **kwargs, validator=validator, db_session=db_session)
            return response

        return wrapped

    return wrapper


def response_formatter(template: str, template_id: str = '', handler: Callable = None, handler_id: Callable = None):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            _self = args[0]
            response: web.Response = await func(*args, **kwargs)
            pk = _self.request.match_info.get('id')
            current_template = template_id if pk else template
            if current_template and _self.request.query.get('html') == '1':
                data = json.loads(response.text)
                data['status'] = response.status == 200
                current_handler = handler_id if pk else handler
                context = current_handler(data) if current_handler else data
                return await aiohttp_jinja2.render_template_async(current_template, _self.request, context)
            return response

        return wrapped

    return wrapper
