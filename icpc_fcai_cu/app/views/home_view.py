from django.shortcuts import render
from django.utils import timezone

from icpc_fcai_cu.db.models import Level, Wave, Session


def index(request):
    levels = Level.objects.order_by("level_number")

    next_session = (
        Session.objects
        .select_related("level", "wave")
        .filter(starts_at__gte=timezone.now())
        .order_by("starts_at")
        .first()
    )

    current_wave = Wave.objects.order_by("-season", "-created_at").first()

    return render(
        request,
        "pages/home.html",
        {
            "levels": levels,
            "next_session": next_session,
            "current_wave": current_wave,
        },
    )