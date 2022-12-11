from aiohttp import web

from view import StaffView, PositionView, StaffTemplateView, init_data_view


def get_routes() -> list:
    return [
        web.get('/', StaffTemplateView, name='index'),
        web.get('/staff/', StaffView, name='staff_tree'),
        web.get('/staff/{id}/', StaffView, name='staff'),
        web.post('/staff/', StaffView, name='staff_post'),
        web.patch('/staff/{id}/', StaffView, name='staff_patch'),
        web.get('/position/', PositionView, name='positions'),
        web.get('/position/{id}/', PositionView, name='position'),
        web.post('/position/', PositionView, name='position_post'),
        web.patch('/position/{id}/', PositionView, name='position_patch'),
        # service urls
        web.get('/system/init_data/', init_data_view, name='init_db'),
    ]
