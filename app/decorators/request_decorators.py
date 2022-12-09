import functools

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
