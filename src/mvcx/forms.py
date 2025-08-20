from typing import Any, override

from starlette.requests import Request
from starlette_wtf import StarletteForm

__all__ = ["Form"]


class Form(StarletteForm):
    @override
    async def __init__(self, request: Request, **kwargs: Any) -> None:
        await self.from_formdata(request, **kwargs)
