import sqlalchemy as sa
import aiohttp_sqlalchemy as ahsa
from aiohttp import web
from decimal import Decimal

from sqlalchemy_utils import Ltree
from pydantic import ValidationError
from models import StaffModel, PositionModel
from schemas import IdSchema, PostSchema, PatchSchema


class MyClassBasedView(web.View, ahsa.SAMixin):
    async def get(self):
        _id = self.request.match_info.get("id")
        if _id:
            try:
                IdSchema(id=_id)
            except ValidationError as e:
                return web.json_response({"message": str(e)}, status=400)
        db_session = self.get_sa_session()
        async with db_session.begin():
            query = sa.select(StaffModel, PositionModel).join(PositionModel)
            query = (
                query.where(StaffModel.pk == int(_id)).limit(_id)
                if _id
                else query.order_by("path")
            )
        result = await db_session.execute(query)
        result = result.scalars()
        data = {"staff": [], "position": {}}
        for i in result:
            data["staff"].append(i.serialized)
            data["position"][i.position.pk] = i.position.serialized
        return web.json_response(data)

    async def post(self):
        input_data = await self.request.json()
        try:
            input_schema = PostSchema(**input_data)
        except ValidationError as e:
            return web.json_response({"message": str(e)}, status=400)
        parent_id = input_data.get("parent_id")
        db_session = self.get_sa_session()
        async with db_session.begin():
            parent_obj = await db_session.get(StaffModel, int(parent_id))
            if parent_obj is None:
                return web.json_response({"message": "bad parent"}, status=400)

            new_person = StaffModel(path=parent_obj.path)
            for key, value in input_schema.dict().items():
                setattr(new_person, key, value)
            db_session.add(new_person)
            await db_session.flush()
            new_person.path += Ltree(str(new_person.pk))
            await db_session.commit()
        return web.json_response(new_person.serialized)

    async def patch(self):
        input_data = await self.request.json()
        try:
            id_schema = IdSchema(id=self.request.match_info.get("id"))
            patch_schema = PatchSchema(**input_data)
        except ValidationError as e:
            return web.json_response({"message": str(e)}, status=400)
        db_session = self.get_sa_session()
        async with db_session.begin():
            if input_data.get("position_id"):
                position = await db_session.get(
                    PositionModel, int(input_data["position_id"])
                )
                if position is None:
                    return web.json_response({"message": "bad position"}, status=400)

            person = await db_session.get(StaffModel, id_schema.id)
            for key, value in patch_schema.dict().items():
                if value is not None:
                    setattr(person, key, value)
            db_session.add(person)
            await db_session.commit()
        return web.json_response(person.serialized)


async def init_data(request):
    sa_session = ahsa.get_session(request)
    names = (
        "dev",
        "admin",
        "devops",
        "ba",
        "product",
        "chief",
        "security_guard",
        "cleaner",
        "receptionist",
    )

    async with sa_session.begin():
        result = await sa_session.execute(sa.select(PositionModel).limit(1))
        position = result.scalars().first()
        if position is None:
            data = [PositionModel(name=i, detail=f"{i * 5} detail text") for i in names]
            sa_session.add_all(data)

        result = await sa_session.execute(sa.select(StaffModel).limit(1))
        staff = result.scalars().first()
        if staff is None:
            person_1 = StaffModel(
                last_name="First",
                first_name="Ivan",
                wage_rate=Decimal(200000),
                path=Ltree("1"),
                position_id=1,
            )
            person_2 = StaffModel(
                last_name="Second",
                first_name="Petr",
                middle_name="Petrovich",
                wage_rate=Decimal(180_000),
                path=Ltree("1.2"),
                position_id=2,
            )
            person_3 = StaffModel(
                last_name="Third",
                first_name="Anna",
                middle_name="Serhovich",
                wage_rate=Decimal(170_000),
                path=Ltree("1.3"),
                position_id=3,
            )
            person_4 = StaffModel(
                last_name="Fourth",
                first_name="Ganna",
                wage_rate=Decimal(110_000),
                path=Ltree("1.3.4"),
                position_id=3,
            )
            sa_session.add_all([person_1, person_2, person_3, person_4])
    return web.json_response({})
