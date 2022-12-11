import json
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models import StaffModel, PositionModel
from schemas.staff_shemas import PostStaffSchema, PatchStaffSchema
from schemas.base_schemas import PydBaseModel, IdSchema
from tools.exceptions import InValidException


class ValidateAbstract(ABC):
    def __init__(self, db_session: AsyncSession, pk: int = None, body: str = ''):
        self.body = body
        self.pk = pk
        self.db_session = db_session
        self.code = ''
        self.status_code: Optional[int] = None
        self.message = ''
        self.id_schema: Optional[IdSchema] = None
        self.__input_schema: Optional[PydBaseModel] = None
        self.init()

    def init(self):
        pass

    @property
    @abstractmethod
    def input_schema(self) -> PydBaseModel:
        pass

    @property
    def output_data(self) -> dict:
        return {'code': self.code, 'message': self.message}

    def _set_error(self, status_code: int, code: str, message: str = ''):
        self.status_code = status_code
        self.code = code
        self.message = message or self.code.replace('_', ' ')

    def _sync_validations(self) -> tuple:
        return ()

    def _async_validations(self) -> tuple:
        return ()

    async def _get_db_obj(self, class_model, pk: int, code: str):
        async with self.db_session.begin():
            obj = await self.db_session.get(class_model, pk)
        if obj is None:
            raise InValidException(status_code=400, code=code)
        return obj

    def __validate_id_schema(self):
        if self.pk is not None:
            self.id_schema = IdSchema.parse_custom(data=json.dumps({'id': self.pk}), code='bad_schema_id')

    async def is_valid(self) -> bool:
        try:
            self.__validate_id_schema()
            [i() for i in self._sync_validations()]
            [await i() for i in self._async_validations()]
        except InValidException as e:
            self._set_error(status_code=e.status_code, code=e.code, message=e.message)
            return False
        self.status_code = 200
        return True


class GetValidate(ValidateAbstract):
    @property
    def input_schema(self) -> Optional[IdSchema]:
        return self.id_schema


class PostValidate(ValidateAbstract):
    def init(self):
        self.__obj: Optional[StaffModel] = None

    @property
    def obj_model(self) -> StaffModel:
        return self.__obj

    @property
    def input_schema(self) -> PostStaffSchema:
        return self.__input_schema

    def _sync_validations(self) -> tuple:
        return (self.__set_input_data,)

    def _async_validations(self) -> tuple:
        return (self.__validate_obj,)

    async def __validate_obj(self):
        _id = self.__input_schema.parent_id
        self.__obj = await self._get_db_obj(class_model=StaffModel, pk=_id, code='bad_parent')

    def __set_input_data(self):
        self.__input_schema = PostStaffSchema.parse_custom(data=self.body, code='bad_schema')


class PatchValidate(ValidateAbstract):
    def init(self):
        self.__obj: Optional[StaffModel] = None

    @property
    def input_schema(self) -> PatchStaffSchema:
        return self.__input_schema

    @property
    def obj_model(self) -> StaffModel:
        return self.__obj

    def _sync_validations(self) -> tuple:
        return (self.__set_input_data,)

    def _async_validations(self) -> tuple:
        return self.__validate_position, self.__validate_obj

    def __set_input_data(self):
        self.__input_schema: PatchStaffSchema = PatchStaffSchema.parse_custom(data=self.body, code='bad_schema')
        if not self.__input_schema.has_values():
            raise InValidException(status_code=400, code='nothing_update')

    async def __validate_position(self):
        if not self.input_schema.position_id:
            return
        await self._get_db_obj(class_model=PositionModel, pk=self.__input_schema.position_id, code='bad_position')

    async def __validate_obj(self):
        self.__obj = await self._get_db_obj(class_model=StaffModel, pk=self.id_schema.id, code='bad_person')
