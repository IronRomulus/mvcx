import inspect
from pathlib import Path
from typing import Any, Mapping, override

import jinja2
from lucide.jinja import lucide
from starlette.background import BackgroundTask
from starlette.templating import Jinja2Templates

from mvcx.requests import Request
from mvcx.responses import Html

__all__ = ["Templates", "render_template"]


class Templates(Jinja2Templates):
    @override
    def _setup_env_defaults(self, env: jinja2.Environment) -> None:
        super()._setup_env_defaults(env)

        @jinja2.pass_context
        def path_for(
            context: dict[str, Any],
            name: str,
            /,
            **path_params: Any,
        ) -> str:
            request: Request = context["request"]
            return request.url_for(name, **path_params).path

        env.globals.setdefault("path_for", path_for)
        env.globals.setdefault("lucide", lucide)


def render_template(
    request: Request,
    name: str,
    context: dict[str, Any] | None = None,
    *,
    status_code: int = 200,
    headers: Mapping[str, str] | None = None,
    media_type: str | None = None,
    background: BackgroundTask | None = None,
) -> Html:
    if context is None:
        context = {}

    context.setdefault("request", request)
    context.setdefault("cookies", request.cookies)
    context.setdefault("session", request.session)

    template_dirs = [
        Path("templates").resolve(),
        Path(inspect.stack()[1].filename).resolve().parent / "templates",
    ]
    loader = jinja2.FileSystemLoader(template_dirs)
    env = jinja2.Environment(loader=loader)
    templates = Templates(env=env)

    return templates.TemplateResponse(
        request, name, context, status_code, headers, media_type, background
    )  # type: ignore
