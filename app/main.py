import aioreloader
from aiohttp import web
from sqlalchemy import orm
import aiohttp_sqlalchemy as ahsa
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from routers import get_routes

DB_ADDRESS = "postgresql+asyncpg://postgres:postgres@pg_db/postgres"  # todo duplicate
engine = create_async_engine(DB_ADDRESS, echo=True)
Session = orm.sessionmaker(engine, AsyncSession, expire_on_commit=False)


async def app_factory(re_loader: bool = True) -> web.Application:
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


if __name__ == "__main__":
    web.run_app(app_factory(), port=8000)
