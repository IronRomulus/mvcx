from datetime import datetime, timezone
from functools import partial

from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column
from sqlalchemy.orm import relationship as sqa_relationship

__all__ = ["Model", "AuditModel", "relationship", "Mapped", "mapped_column"]


class Model(AsyncAttrs, DeclarativeBase, MappedAsDataclass):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True, init=False
    )


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class AuditModel(Model):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), default_factory=_utc_now, init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        default_factory=_utc_now,
        onupdate=_utc_now,
        init=False,
    )


relationship = partial(sqa_relationship, init=False)
