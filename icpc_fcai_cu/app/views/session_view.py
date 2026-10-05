from django.shortcuts import render, get_object_or_404

from icpc_fcai_cu.db.models import Session


def index(request):
    sessions = Session.objects.select_related("level", "wave").order_by("starts_at")
    return render(request, "pages/sessions/index.html", {"sessions": sessions})


def show(request, slug):
    session = get_object_or_404(
        Session.objects.select_related("level", "wave"),
        slug=slug,
    )
    return render(request, "pages/sessions/show.html", {"session": session})