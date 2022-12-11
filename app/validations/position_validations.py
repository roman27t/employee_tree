from abc import ABC, abstractmethod
from typing import Optional

from models import PositionModel
from tools.exceptions import InValidException
from schemas.position_shemas import PostPositionSchema, PatchPositionSchema
from validations.abstract_validations import ValidateAbstract


class _PositionBaseValidate(ValidateAbstract, ABC):
    def init(self):
        self._obj: Optional[PositionModel] = None

    @property
    def obj_model(self) -> PositionModel:
        return self._obj

    @abstractmethod
    def _set_input_data(self):
        pass

    def _sync_validations(self) -> tuple:
        return (self._set_input_data,)


class PostPositionValidate(_PositionBaseValidate):
    @property
    def input_schema(self) -> PostPositionSchema:
        return self.__input_schema

    def _set_input_data(self):
        self.__input_schema = PostPositionSchema.parse_custom(data=self.body, code='bad_schema')


class PatchPositionValidate(_PositionBaseValidate):
    @property
    def input_schema(self) -> PatchPositionSchema:
        return self.__input_schema

    def _async_validations(self) -> tuple:
        return (self.__validate_obj,)

    def _set_input_data(self):
        self.__input_schema: PatchPositionSchema = PatchPositionSchema.parse_custom(data=self.body, code='bad_schema')
        if not self.__input_schema.has_values():
            raise InValidException(status_code=400, code='nothing_update')

    async def __validate_obj(self):
        self._obj = await self._get_db_obj(class_model=PositionModel, pk=self.id_schema.id, code='bad_object')
