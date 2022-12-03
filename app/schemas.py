import datetime as dt
from typing import Optional
from pydantic import BaseModel
from pydantic import (
    PositiveInt,
    condecimal,
    constr,
)


class PydBaseModel(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True
        validate_all = True


class IdSchema(PydBaseModel):
    id: PositiveInt


class PostSchema(PydBaseModel):
    parent_id: PositiveInt
    position_id: PositiveInt
    last_name: constr(max_length=250)
    first_name: constr(max_length=250)
    middle_name: constr(max_length=250) = ''
    wage_rate: condecimal(max_digits=10, decimal_places=2)
    birthdate: dt.date


class PatchSchema(PydBaseModel):
    position_id: Optional[PositiveInt]
    last_name: Optional[constr(max_length=250)]
    first_name: Optional[constr(max_length=250)]
    middle_name: Optional[constr(max_length=250)]
    wage_rate: Optional[condecimal(max_digits=10, decimal_places=2)]
    birthdate: Optional[dt.date]
