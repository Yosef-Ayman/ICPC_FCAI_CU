from django.http import Http404
from django.shortcuts import render, get_object_or_404

from icpc_fcai_cu.db.models import Level


def index(request):
    levels = Level.objects.order_by("level_number")
    return render(request, "pages/levels/index.html", {"levels": levels})


def show(request, slug):
    level = get_object_or_404(Level, slug=slug)
    sessions = level.sessions.select_related("wave").order_by("starts_at")

    return render(
        request,
        "pages/levels/show.html",
        {"level": level, "sessions": sessions},
    )