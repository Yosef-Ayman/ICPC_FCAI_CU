from django.shortcuts import render

from icpc_fcai_cu.db.models import UserWave, SessionAttendance
from icpc_fcai_cu.app.middleware.roles import student_required


@student_required
def waves(request):
    user_waves = (
        UserWave.objects
        .select_related("wave", "level")
        .filter(user=request.user)
        .order_by("-joined_at")
    )
    return render(request, "pages/me/waves.html", {"user_waves": user_waves})


@student_required
def attendances(request):
    records = list(
        SessionAttendance.objects
        .select_related("session")
        .filter(user=request.user)
        .order_by("-session__starts_at")
    )

    total = len(records)
    attended = sum(1 for r in records if r.attend)

    return render(
        request,
        "pages/me/attendances.html",
        {
            "records": records,
            "total": total,
            "attended": attended,
            "rate": round(attended / total * 100, 1) if total else 0,
        },
    )