from welcome.views import WelcomeView

from mvcx.models import Model
from mvcx.routing import Route, WebSocketRoute
from mvcx.views import View

VIEWS: list[type[View]] = [WelcomeView]

MODELS: list[type[Model]] = []

ROUTES: list[Route] = []

WEBSOCKET_ROUTES: list[WebSocketRoute] = []
