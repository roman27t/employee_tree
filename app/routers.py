from aiohttp import web
from view import MyClassBasedView, init_data


def get_routes() -> list:
    return [
        web.get("/staff/", MyClassBasedView),
        web.get("/staff/{id}/", MyClassBasedView),
        web.post("/staff/", MyClassBasedView),
        web.patch("/staff/{id}/", MyClassBasedView),
        # service test urls
        web.get("/system/init_data/", init_data),
    ]
