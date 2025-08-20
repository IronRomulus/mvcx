from pydantic import BaseModel


class Dto(BaseModel, frozen=True):
    pass
