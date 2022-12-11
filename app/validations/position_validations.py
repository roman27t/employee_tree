from typing import Optional

from models import PositionModel
from schemas.position_shemas import PostPositionSchema, PatchPositionSchema
from tools.exceptions import InValidException
from validations.abstract_validations import ValidateAbstract


class PostPositionValidate(ValidateAbstract):
    def init(self):
        self.__obj: Optional[PositionModel] = None

    @property
    def obj_model(self) -> PositionModel:
        return self.__obj

    @property
    def input_schema(self) -> PostPositionSchema:
        return self.__input_schema

    def _sync_validations(self) -> tuple:
        return (self.__set_input_data,)

    def __set_input_data(self):
        self.__input_schema = PostPositionSchema.parse_custom(data=self.body, code='bad_schema')


class PatchPositionValidate(ValidateAbstract):
    def init(self):
        self.__obj: Optional[PositionModel] = None

    @property
    def input_schema(self) -> PatchPositionSchema:
        return self.__input_schema

    @property
    def obj_model(self) -> PositionModel:
        return self.__obj

    def _sync_validations(self) -> tuple:
        return (self.__set_input_data,)

    def _async_validations(self) -> tuple:
        return self.__validate_obj,

    def __set_input_data(self):
        self.__input_schema: PatchPositionSchema = PatchPositionSchema.parse_custom(data=self.body, code='bad_schema')
        if not self.__input_schema.has_values():
            raise InValidException(status_code=400, code='nothing_update')

    async def __validate_obj(self):
        self.__obj = await self._get_db_obj(class_model=PositionModel, pk=self.id_schema.id, code='bad_object')
