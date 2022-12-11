import json
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from tools.exceptions import InValidException
from schemas.base_schemas import IdSchema, PydBaseModel


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
