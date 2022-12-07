from abc import ABC, abstractmethod
from typing import Optional

from pydantic import ValidationError

from models import StaffModel, PositionModel
from schemas import IdSchema, PostSchema, PatchSchema, PydBaseModel


class InValidException(Exception):
    def __init__(self, status_code: int, code: str, message: str = ''):
        self.code = code
        self.message = message
        self.status_code = status_code


class ValidateAbstract(ABC):
    def __init__(self, db_session, pk: int = None, body: str = ''):
        self.body = body
        self.pk = pk
        self.db_session = db_session
        self.code = ''
        self.status_code = None
        self.message = ''
        self.id_schema: Optional[IdSchema] = None
        self.__input_schema = None
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

    def __validate_id_schema(self):
        if self.pk is not None:
            try:
                self.id_schema = IdSchema(id=self.pk)
            except ValidationError as e:
                raise InValidException(status_code=400, code='bad_schema_id', message=str(e))

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
        self.__parent_obj: Optional[StaffModel] = None

    @property
    def parent_obj(self) -> StaffModel:
        return self.__parent_obj

    @property
    def input_schema(self) -> PostSchema:
        return self.__input_schema

    def _sync_validations(self) -> tuple:
        return (self.__set_input_data,)

    def _async_validations(self) -> tuple:
        return (self.__validate_parent_obj,)

    async def __validate_parent_obj(self):
        async with self.db_session.begin():
            self.__parent_obj = await self.db_session.get(StaffModel, self.__input_schema.parent_id)
        if self.__parent_obj is None:
            raise InValidException(status_code=400, code='bad_parent')

    def __set_input_data(self):
        try:
            self.__input_schema = PostSchema.parse_raw(self.body)
        except ValidationError as e:
            raise InValidException(status_code=400, code='bad_schema', message=str(e))


class PatchValidate(ValidateAbstract):
    def init(self):
        self.__person: Optional[StaffModel] = None

    @property
    def input_schema(self) -> PatchSchema:
        return self.__input_schema

    @property
    def person(self) -> StaffModel:
        return self.__person

    def _sync_validations(self) -> tuple:
        return (self.__set_input_data,)

    def _async_validations(self) -> tuple:
        return self.__validate_position, self.__get_person

    def __set_input_data(self):
        try:
            self.__input_schema: PatchSchema = PatchSchema.parse_raw(self.body)
        except ValidationError as e:
            raise InValidException(status_code=400, code='bad_schema', message=str(e))
        if not self.__input_schema.has_values():
            raise InValidException(status_code=400, code='nothing_update')

    async def __validate_position(self):
        if not self.input_schema.position_id:
            return
        async with self.db_session.begin():
            position = await self.db_session.get(PositionModel, self.__input_schema.position_id)
        if position is None:
            raise InValidException(status_code=400, code='bad_position')

    async def __get_person(self):
        async with self.db_session.begin():
            self.__person = await self.db_session.get(StaffModel, self.id_schema.id)
        if self.__person is None:
            raise InValidException(status_code=400, code='bad_person')
