from sqlalchemy.ext.asyncio import AsyncSession

from models import Base


async def update_db_object(db_session: AsyncSession, obj_model: Base, data: dict):
    for key, value in data.items():
        setattr(obj_model, key, value) if value is not None else None
    db_session.add(obj_model)
    await db_session.commit()
