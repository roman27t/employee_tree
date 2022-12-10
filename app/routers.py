from aiohttp import web

from view import StaffView, init_data_view, StaffTemplateView


def get_routes() -> list:
    return [
        web.get('/', StaffTemplateView, name='index'),
        # API
        web.get('/staff/', StaffView, name='staff_tree'),
        web.get('/staff/{id}/', StaffView, name='staff'),
        web.post('/staff/', StaffView),
        web.patch('/staff/{id}/', StaffView),
        # service urls
        web.get('/system/init_data/', init_data_view),
    ]
