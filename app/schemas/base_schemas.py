from pydantic import BaseModel, PositiveInt, ValidationError

from tools.exceptions import InValidException


class PydBaseModel(BaseModel):
    @classmethod
    def parse_custom(cls, data: str, code: str) -> 'PydBaseModel':
        try:
            return cls.parse_raw(data)
        except ValidationError as e:
            raise InValidException(status_code=400, code=code, message=str(e))

    def has_values(self) -> bool:
        return len([i for i in self.dict().values() if i is not None]) > 0

    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True
        validate_all = True


class IdSchema(PydBaseModel):
    id: PositiveInt
