import os
from contextlib import AbstractAsyncContextManager
from typing import Any, Awaitable, Callable, Mapping, Self, Sequence, override
from uuid import uuid4

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Route
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from starlette_csrf.middleware import CSRFMiddleware

from mvcx._cli._config import BUNDLE_DIR
from mvcx.views import View


class Mvcx(Starlette):
    @override
    def __init__(
        self,
        debug: bool = False,
        routes: Sequence[BaseRoute] | None = None,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Mapping[
            Any,
            Callable[[Request, Exception], Response | Awaitable[Response]]
            | Callable[[WebSocket, Exception], Awaitable[None]],
        ]
        | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Callable[[Self], AbstractAsyncContextManager[None, bool | None]]
        | Callable[[Self], AbstractAsyncContextManager[Mapping[str, Any], bool | None]]
        | None = None,
    ) -> None:
        super().__init__(
            debug,
            routes,
            middleware,
            exception_handlers,
            on_startup,
            on_shutdown,
            lifespan,
        )

        session_secret = os.getenv("SESSION_SECRET")
        if not session_secret:
            if not debug:
                session_secret = str(uuid4())
            else:
                session_secret = "session_secret"

        csrf_secret = os.getenv("CSRF_SECRET")
        if not csrf_secret:
            if not debug:
                csrf_secret = str(uuid4())
            else:
                csrf_secret = "csrf_secret"

        self.add_middleware(
            SessionMiddleware,
            session_secret,
            https_only=not debug,
        )
        self.add_middleware(CSRFMiddleware, csrf_secret)
        self.add_middleware(GZipMiddleware)

        self.mount(f"/{BUNDLE_DIR}", StaticFiles(directory=BUNDLE_DIR), "static")

    def add_view(self, view: type[View]) -> None:
        for route in view.routes():
            if isinstance(route, Route):
                self.add_route(
                    route.path,
                    route.endpoint,
                    list(route.methods) if route.methods else None,
                    route.name,
                    route.include_in_schema,
                )
            else:
                self.add_websocket_route(route.path, route.endpoint, route.name)
