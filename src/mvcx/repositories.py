from sqlalchemy import select

from mvcx.db import DbSession
from mvcx.di import inject
from mvcx.dtos import Dto
from mvcx.models import Model

__all__ = ["Repository"]


class Repository[Record: Model, CreateRecordDto: Dto, UpdateRecordDto: Dto]:
    @inject
    async def __init__(self, db: DbSession, model: type[Record]) -> None:
        self.db = db
        self.model = model

    async def create(self, create_record_dto: CreateRecordDto) -> Record:
        record = self.model(**create_record_dto.model_dump())
        self.db.add(record)
        return record

    async def get_by_id(self, id: int) -> Record:
        return await self.db.get_one(self.model, id)

    async def get_all(self) -> tuple[Record, ...]:
        stmt = select(self.model)
        return tuple(await self.db.scalars(stmt))

    async def update(self, record: Record, update_record_dto: UpdateRecordDto) -> None:
        for key, value in update_record_dto.model_dump(exclude_none=True).items():
            setattr(record, key, value)

    async def delete(self, record: Record) -> None:
        await self.db.delete(record)
