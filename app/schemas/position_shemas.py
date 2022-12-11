from typing import Optional

from pydantic import constr

from schemas.base_schemas import PydBaseModel


class PostPositionSchema(PydBaseModel):
    name: constr(min_length=2, max_length=50)
    detail: constr(max_length=255, default='')


class PatchPositionSchema(PydBaseModel):
    name: Optional[constr(min_length=2, max_length=50)]
    detail: Optional[constr(max_length=255, default='')]
