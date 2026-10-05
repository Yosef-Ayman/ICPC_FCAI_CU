from django.shortcuts import render, get_object_or_404

from icpc_fcai_cu.db.models import Wave


def index(request):
    waves = Wave.objects.all()  # الـ ordering موجود في الـ Meta
    return render(request, "pages/waves/index.html", {"waves": waves})


def show(request, slug):
    wave = get_object_or_404(Wave, slug=slug)
    sessions = wave.sessions.select_related("level").order_by("starts_at")

    return render(
        request,
        "pages/waves/show.html",
        {"wave": wave, "sessions": sessions},
    )