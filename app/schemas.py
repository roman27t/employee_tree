import datetime as dt
from typing import Optional

from pydantic import BaseModel, PositiveInt, constr, condecimal


class PydBaseModel(BaseModel):
    def has_values(self) -> bool:
        return len([i for i in self.dict().values() if i is not None]) > 0

    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True
        validate_all = True


class IdSchema(PydBaseModel):
    id: PositiveInt


class PostSchema(PydBaseModel):
    parent_id: PositiveInt
    position_id: PositiveInt
    last_name: constr(max_length=50)
    first_name: constr(max_length=50)
    middle_name: constr(max_length=50) = ''
    wage_rate: condecimal(max_digits=10, decimal_places=2)
    birthdate: dt.date

    def dict_by_db(self) -> dict:
        exclude_keys = ('parent_id',)
        data = self.dict()
        for i in exclude_keys:
            del data[i]
        return data


class PatchSchema(PydBaseModel):
    position_id: Optional[PositiveInt]
    last_name: Optional[constr(max_length=50)]
    first_name: Optional[constr(max_length=50)]
    middle_name: Optional[constr(max_length=50)]
    wage_rate: Optional[condecimal(max_digits=10, decimal_places=2)]
    birthdate: Optional[dt.date]
