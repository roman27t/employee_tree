from aiohttp import web

from view import StaffView, init_data_view


def get_routes() -> list:
    return [
        web.get('/staff/', StaffView),
        web.get('/staff/{id}/', StaffView),
        web.post('/staff/', StaffView),
        web.patch('/staff/{id}/', StaffView),
        # todo service test urls --> init.sql
        web.get('/system/init_data/', init_data_view),
    ]
