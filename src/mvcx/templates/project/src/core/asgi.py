import os
from uuid import uuid4

from core.registry import ROUTES, VIEWS, WEBSOCKET_ROUTES
from dotenv import load_dotenv

from mvcx import Mvcx
from mvcx.middleware import CSRFMiddleware, GZipMiddleware, SessionMiddleware


def _create_app() -> Mvcx:
    load_dotenv()
    debug = os.getenv("DEBUG") in ["true", "1"] or False

    app = Mvcx(debug=debug, middleware=[])

    for view_class in VIEWS:
        app.add_view(view_class)

    for route in ROUTES:
        app.add_route(**route.__dict__)

    for websocket_route in WEBSOCKET_ROUTES:
        app.add_websocket_route(**websocket_route.__dict__)

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

    app.add_middleware(SessionMiddleware, session_secret)
    app.add_middleware(CSRFMiddleware, csrf_secret)
    app.add_middleware(GZipMiddleware)

    return app


app = _create_app()
