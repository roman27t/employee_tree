import functools
from aiohttp import web


def validation(class_validate, has_body: bool):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            _self = args[0]
            db_session = _self.get_sa_session()
            validator = class_validate(
                pk=_self.request.match_info.get('id'),
                body=await _self.request.text() if has_body else None,
                db_session=db_session,
            )
            if not await validator.is_valid():
                return web.json_response(validator.output_data, status=validator.status_code)
            response = await func(*args, **kwargs, validator=validator, db_session=db_session)
            return response

        return wrapped

    return wrapper
