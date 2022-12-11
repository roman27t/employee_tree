import sqlalchemy as sa
import aiohttp_jinja2
import aiohttp_sqlalchemy as ahsa
from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import Ltree
from sqlalchemy.ext.asyncio import AsyncSession

from models import StaffModel, PositionModel
from tools.front_side import front_staff_tree, front_staff_by_id
from validations import GetValidate, PostValidate, PatchValidate
from tools.init_data_db import init_data
from decorators.request_decorators import validation, response_formatter


class StaffView(web.View, ahsa.SAMixin):
    @response_formatter(
        template='staff_tree.html', template_id='staff.html',handler=front_staff_tree, handler_id=front_staff_by_id,
    )
    @validation(class_validate=GetValidate)
    async def get(self, validator: GetValidate, db_session: AsyncSession) -> web.Response:
        """
        ---
        description: return all employees or one employee.
        tags:
        - StaffView
        produces:
        - application/json
        parameters:
        - in: path
          name: id
          required: false
          type: integer
        responses:
            "200":  success
            "400":  error
        """
        _id = validator.input_schema.id if validator.input_schema else None
        query = sa.select(StaffModel, PositionModel).join(PositionModel)
        query = query.where(StaffModel.pk == _id).limit(1) if _id else query.order_by('path')
        result = await db_session.execute(query)
        result = result.scalars()
        data = {'staff': {}, 'position': {}}
        for i in result:
            data['staff'][i.pk] = i.serialized
            data['position'][i.position.pk] = i.position.serialized
        return web.json_response(data)

    @validation(class_validate=PostValidate)
    async def post(self, validator: PostValidate, db_session: AsyncSession):
        """
        ---
        description: create one employee.
        tags:
        - StaffView
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          description: Created user object
          required: false
          schema:
              $ref: '#/definitions/StaffPost'
        responses:
            "200":  success
            "400":  Validation error
            "403":  Duplicate Error
        """
        new_person = StaffModel(path=validator.parent_obj.path, **validator.input_schema.dict_by_db())
        db_session.add(new_person)
        try:
            await db_session.flush()
            new_person.path += Ltree(str(new_person.pk))
            await db_session.commit()
        except IntegrityError:
            return web.json_response({'message': 'Duplicate Error'}, status=403)
        return web.json_response(new_person.serialized)

    @validation(class_validate=PatchValidate)
    async def patch(self, validator: PatchValidate, db_session: AsyncSession):
        """
        ---
        description: update one employee.
        tags:
        - StaffView
        produces:
        - application/json
        parameters:
        - in: path
          name: id
          required: true
          type: integer
        - in: body
          name: body
          description: Created user object
          required: false
          schema:
              $ref: '#/definitions/StaffPatch'
        responses:
            "200":  success
            "400":  error
        """
        for key, value in validator.input_schema.dict().items():
            setattr(validator.person, key, value) if value is not None else None
        db_session.add(validator.person)
        await db_session.commit()
        return web.json_response(validator.person.serialized)


async def init_data_view(request):
    """
    ---
    description: service view
    tags:
    - System service
    produces:
    - application/json
    """
    await init_data(sa_session=ahsa.get_session(request))
    return web.json_response({})


class StaffTemplateView(web.View, ahsa.SAMixin):
    async def get(self):
        return await aiohttp_jinja2.render_template_async('index.html', self.request, {'index': True})
