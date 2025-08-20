from pydantic import BaseModel

__all__ = ["Dto"]


class Dto(BaseModel, frozen=True):
    pass
