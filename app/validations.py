from abc import ABC, abstractmethod
from typing import Optional

from pydantic import ValidationError
from schemas import PostSchema, IdSchema, PatchSchema
from models import StaffModel, PositionModel


class ValidateAbstract(ABC):
    def __init__(self, body: str, db_session, pk: int = None):
        self.body = body
        self.pk = pk
        self.db_session = db_session
        self.code = ''
        self.status_code = None
        self.message = ''
        self.id_schema: Optional[IdSchema] = None
        self.__input_schema = None
        self.parent_obj = None
        self.init()

    def init(self):
        pass

    @property
    @abstractmethod
    def input_schema(self):
        pass

    @property
    def output_data(self) -> dict:
        return {'code': self.code, 'message': self.message}

    def _set_error(self, status_code: int, code: str, message: str = ''):
        self.status_code = status_code
        self.code = code
        self.message = message or self.code.replace('_', ' ')

    def sync_validations(self) -> tuple:
        return ()

    def async_validations(self) -> tuple:
        return ()

    async def is_valid(self) -> bool:
        if self.pk is not None:
            try:
                self.id_schema = IdSchema(id=self.pk)
            except ValidationError as e:
                self._set_error(status_code=400, code='bad_schema_id', message=str(e))
                return False
        for i in self.sync_validations():
            if not i():
                return False
        for i in self.async_validations():
            if not await i():
                return False
        self.status_code = 200
        return True


class ValidatePost(ValidateAbstract):
    @property
    def input_schema(self) -> PostSchema:
        return self.__input_schema

    def sync_validations(self) -> tuple:
        return self.__set_input_data,

    def async_validations(self) -> tuple:
        return self.__validate_parent_obj,

    async def __validate_parent_obj(self):
        async with self.db_session.begin():
            self.parent_obj = await self.db_session.get(StaffModel, self.__input_schema.parent_id)
        if self.parent_obj is None:
            self._set_error(code='bad_parent', status_code=400)
            return False
        return True

    def __set_input_data(self):
        try:
            self.__input_schema = PostSchema.parse_raw(self.body)
        except ValidationError as e:
            self._set_error(status_code=400, code='bad_schema', message=str(e))
            return False
        return True


class ValidatePatch(ValidateAbstract):
    def init(self):
        self.__person: Optional[StaffModel] = None

    @property
    def input_schema(self) -> PatchSchema:
        return self.__input_schema

    @property
    def person(self) -> StaffModel:
        return self.__person

    def sync_validations(self) -> tuple:
        return self.__set_input_data,

    def async_validations(self) -> tuple:
        return self.__validate_position, self.__get_person

    def __set_input_data(self):
        try:
            self.__input_schema: PatchSchema = PatchSchema.parse_raw(self.body)
        except ValidationError as e:
            self._set_error(status_code=400, code='bad_schema', message=str(e))
            return False
        if not self.__input_schema.has_values():
            self._set_error(status_code=400, code='nothing_update')
            return False
        return True

    async def __validate_position(self):
        if not self.input_schema.position_id:
            return True
        async with self.db_session.begin():
            position = await self.db_session.get(PositionModel, self.__input_schema.position_id)
        if position is None:
            self._set_error(code='bad_position', status_code=400)
            return False
        return True

    async def __get_person(self):
        async with self.db_session.begin():
            self.__person = await self.db_session.get(StaffModel, self.id_schema.id)
        if self.__person is None:
            self._set_error(code='bad_person', status_code=400)
            return False
        return True
