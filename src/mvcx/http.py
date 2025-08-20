from typing import Any, Mapping, override

from starlette import status
from starlette.background import BackgroundTask
from starlette.datastructures import URL
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.routing import Route

__all__ = ["status", "Request", "Html", "Json", "Redirect", "Route"]


class Html(HTMLResponse):
    @override
    def __init__(
        self,
        content: str,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)


class Json(JSONResponse):
    @override
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)


class Redirect(RedirectResponse):
    @override
    def __init__(
        self,
        url: str | URL,
        status_code: int = 303,
        headers: Mapping[str, str] | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(url, status_code, headers, background)
