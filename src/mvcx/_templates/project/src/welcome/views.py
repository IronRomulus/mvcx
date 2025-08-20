from mvcx.http import Html, Request
from mvcx.templating import render_template
from mvcx.views import View


class WelcomeView(View):
    path = "/"

    def get(self, request: Request) -> Html:
        return render_template(request, "welcome_page.html")
