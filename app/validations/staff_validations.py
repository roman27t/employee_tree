from abc import ABC, abstractmethod
from typing import Optional

from models import StaffModel, PositionModel
from schemas.staff_shemas import PostStaffSchema, PatchStaffSchema
from tools.exceptions import InValidException
from validations.abstract_validations import ValidateAbstract


class _StaffAbstractValidate(ValidateAbstract, ABC):
    def init(self):
        self._obj: Optional[StaffModel] = None

    @property
    def obj_model(self) -> StaffModel:
        return self._obj

    @abstractmethod
    def _set_input_data(self):
        pass

    def _sync_validations(self) -> tuple:
        return (self._set_input_data,)


class PostStaffValidate(_StaffAbstractValidate):
    @property
    def input_schema(self) -> PostStaffSchema:
        return self._input_schema

    def _async_validations(self) -> tuple:
        return (self.__validate_obj,)

    async def __validate_obj(self):
        _id = self._input_schema.parent_id
        self._obj = await self._get_db_obj(class_model=StaffModel, pk=_id, code='bad_parent')

    def _set_input_data(self):
        self._input_schema = PostStaffSchema.parse_custom(data=self.body, code='bad_schema')


class PatchStaffValidate(_StaffAbstractValidate):
    @property
    def input_schema(self) -> PatchStaffSchema:
        return self._input_schema

    def _async_validations(self) -> tuple:
        return self.__validate_position, self.__validate_obj

    def _set_input_data(self):
        self._input_schema: PatchStaffSchema = PatchStaffSchema.parse_custom(data=self.body, code='bad_schema')
        if not self._input_schema.has_values():
            raise InValidException(status_code=400, code='nothing_update')

    async def __validate_position(self):
        if not self.input_schema.position_id:
            return
        await self._get_db_obj(class_model=PositionModel, pk=self._input_schema.position_id, code='bad_position')

    async def __validate_obj(self):
        self._obj = await self._get_db_obj(class_model=StaffModel, pk=self.id_schema.id, code='bad_person')
