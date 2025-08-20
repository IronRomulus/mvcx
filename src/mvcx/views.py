import inspect
from typing import ClassVar

from starlette.routing import Route, WebSocketRoute

__all__ = ["View"]


class View:
    path: ClassVar[str] = "/"

    @classmethod
    def routes(cls) -> list[Route | WebSocketRoute]:
        routes: list[Route | WebSocketRoute] = []
        instance = cls()

        for name, member in inspect.getmembers(instance, inspect.ismethod):
            route_name = f"{cls.__name__}.{name}"

            method = name.lower()

            if method in ["get", "post", "put", "patch", "delete"]:
                routes.append(
                    Route(cls.path, member, methods=[method], name=route_name)
                )
                continue

            if method in ["websocket", "ws"]:
                routes.append(WebSocketRoute(cls.path, member, name=route_name))
                continue

        return routes
