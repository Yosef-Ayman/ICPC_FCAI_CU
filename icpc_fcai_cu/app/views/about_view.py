from django.shortcuts import render

from icpc_fcai_cu.app.utils.responses import *


def index(request):
    """
    data = {
        "stats": {
            "trainees": 1000,
            "teams": 200,
            "medals": 15,
        },
        "story": {
            "title": "We don't just solve. We build problem solvers.",
        },
    }
    """
    return render(request=request, template_name="pages/about.html", status=200)