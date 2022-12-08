import datetime as dt
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy_utils import Ltree

from models import StaffModel, PositionModel

__NAMES = (
    'dev',
    'admin',
    'devops',
    'ba',
    'product',
    'chief',
    'security_guard',
    'cleaner',
    'receptionist',
)


async def init_data(sa_session):
    async with sa_session.begin():
        result = await sa_session.execute(sa.select(PositionModel).limit(1))
        position = result.scalars().first()
        if position is None:
            data = [PositionModel(name=i, detail=f'{i * 5} detail text') for i in __NAMES]
            sa_session.add_all(data)

    async with sa_session.begin():
        result = await sa_session.execute(sa.select(PositionModel).limit(1))
        position = result.scalars().first()

        result = await sa_session.execute(sa.select(StaffModel).limit(1))
        staff = result.scalars().first()
        if staff is None:
            person_1 = StaffModel(
                last_name='First',
                first_name='Ivan',
                wage_rate=Decimal(200000),
                path=Ltree('1'),
                position_id=position.pk,
                birthdate=dt.datetime.strptime('21.11.2000', '%d.%m.%Y').date(),
            )
            person_2 = StaffModel(
                last_name='Second',
                first_name='Petr',
                middle_name='Petrovich',
                wage_rate=Decimal(180_000),
                path=Ltree('1.2'),
                position_id=position.pk + 1,
                birthdate=dt.datetime.strptime('01.01.1960', '%d.%m.%Y').date(),
            )
            person_3 = StaffModel(
                last_name='Third',
                first_name='Anna',
                middle_name='Serhovich',
                wage_rate=Decimal(170_000),
                path=Ltree('1.3'),
                position_id=position.pk + 2,
                birthdate=dt.datetime.strptime('12.06.1975', '%d.%m.%Y').date(),
            )
            person_4 = StaffModel(
                last_name='Fourth',
                first_name='Ganna',
                wage_rate=Decimal(110_000),
                path=Ltree('1.3.4'),
                birthdate=dt.datetime.strptime('30.10.1982', '%d.%m.%Y').date(),
                position_id=position.pk + 3,
            )
            sa_session.add_all([person_1, person_2, person_3, person_4])
    return True
