from typing import Optional

from pydantic import constr, validator

from schemas.base_schemas import PydBaseModel


class PostPositionSchema(PydBaseModel):
    name: constr(min_length=2, max_length=50)
    detail: constr(max_length=255) = ''

    @validator('name')
    def upgrade_name(cls, v: str) -> str:
        return v.lower() if v else v


class PatchPositionSchema(PostPositionSchema):
    name: Optional[constr(min_length=2, max_length=50)]
    detail: Optional[constr(max_length=255)]
