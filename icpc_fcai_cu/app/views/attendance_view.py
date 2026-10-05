from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from icpc_fcai_cu.db.models import Session, Student, SessionAttendance
from icpc_fcai_cu.app.middleware.roles import staff_required


@staff_required
def index(request, slug):
    session = get_object_or_404(Session.objects.select_related("level"), slug=slug)

    students = (
        Student.objects
        .select_related("user")
        .filter(is_active=True, user__is_active=True, level=session.level)
        .order_by("user__first_name", "user__last_name")
        if session.level_id
        else Student.objects.none()
    )

    if request.method == "POST":
        present = set(request.POST.getlist("attended"))

        with transaction.atomic():
            for student in students:
                SessionAttendance.objects.update_or_create(
                    user=student.user,
                    session=session,
                    defaults={
                        "title": session.title,
                        "attend": student.user.username in present,
                    },
                )

        messages.success(request, "Attendance saved")
        return redirect("app:attendance-index", slug=session.slug)

    attendance_map = dict(
        SessionAttendance.objects
        .filter(session=session)
        .values_list("user_id", "attend")
    )

    rows = [
        {"student": s, "attend": attendance_map.get(s.user_id)}  # None = لسه متسجلش
        for s in students
    ]

    return render(
        request,
        "pages/attendance/index.html",
        {"session": session, "rows": rows},
    )