from typing import Optional

from schemas.base_schemas import IdSchema
from validations.abstract_validations import ValidateAbstract


class GetValidate(ValidateAbstract):
    @property
    def input_schema(self) -> Optional[IdSchema]:
        return self.id_schema
