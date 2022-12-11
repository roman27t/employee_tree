import datetime as dt
import re
from decimal import Decimal
from typing import Optional

from pydantic import PositiveInt, constr, validator, condecimal

from schemas.base_schemas import PydBaseModel
from tools.exceptions import InValidException

MIN_RATE = 500


class _FioSchema(PydBaseModel):
    last_name: constr(max_length=50)
    first_name: constr(max_length=50)
    middle_name: constr(max_length=50) = ''

    @validator('last_name', 'first_name', 'middle_name')
    def upgrade_fio(cls, v: str) -> str:
        if not v:
            return v
        if bool(re.search(r'\d', v)):
            raise InValidException(status_code=400, code='invalid', message='digits are deny')
        return v.capitalize()


class PostStaffSchema(_FioSchema):
    parent_id: PositiveInt
    position_id: PositiveInt
    birthdate: dt.date
    wage_rate: condecimal(max_digits=10, decimal_places=2, ge=Decimal(MIN_RATE))

    def dict_by_db(self) -> dict:
        exclude_keys = ('parent_id',)
        data = self.dict()
        for i in exclude_keys:
            del data[i]
        return data


class PatchStaffSchema(_FioSchema):
    position_id: Optional[PositiveInt]
    last_name: Optional[constr(max_length=50)]
    first_name: Optional[constr(max_length=50)]
    middle_name: Optional[constr(max_length=50)]
    wage_rate: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal(MIN_RATE))]
    birthdate: Optional[dt.date]
