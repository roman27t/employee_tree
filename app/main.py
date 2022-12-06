import aioreloader
import aiohttp_sqlalchemy as ahsa
from aiohttp import web
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import i_config
from routers import get_routes

engine = create_async_engine(i_config.DB_URL, echo=True)
Session = orm.sessionmaker(engine, AsyncSession, expire_on_commit=False)


async def app_factory(re_loader: bool = False) -> web.Application:
    app = web.Application()
    ahsa.setup(
        app,
        [
            ahsa.bind(Session),
        ],
    )
    app.add_routes(get_routes())
    if re_loader:
        aioreloader.start()
    return app


if __name__ == '__main__':
    web.run_app(app_factory(re_loader=i_config.DEBUG), port=i_config.PORT)
