from typing import Optional

from models import StaffModel, PositionModel
from schemas.staff_shemas import PostStaffSchema, PatchStaffSchema
from tools.exceptions import InValidException
from validations.abstract_validations import ValidateAbstract


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