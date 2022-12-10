import aiohttp_jinja2
import aioreloader
import jinja2
import aiohttp_sqlalchemy as ahsa
from aiohttp import web
from sqlalchemy import orm
from aiohttp_swagger import setup_swagger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import i_config
from routers import get_routes
from tools.swagger_data import DATA_SWAGGER


async def app_factory(re_loader: bool = False) -> web.Application:
    engine = create_async_engine(i_config.DB_URL, echo=True)
    Session = orm.sessionmaker(engine, AsyncSession, expire_on_commit=False)
    app = web.Application()
    ahsa.setup(
        app,
        [
            ahsa.bind(Session),
        ],
    )
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'), enable_async=True)
    app.add_routes(get_routes())
    setup_swagger(app, definitions=DATA_SWAGGER)
    if re_loader:
        aioreloader.start()
    return app


if __name__ == '__main__':
    web.run_app(app_factory(re_loader=i_config.DEBUG), port=i_config.PORT)
