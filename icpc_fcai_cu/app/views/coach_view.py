import csv

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from icpc_fcai_cu.app.forms_coach import (
    EnrollForm,
    SessionForm,
    StudentManageForm,
    WaveForm,
)
from icpc_fcai_cu.app.middleware.coach_access import coach_required
from icpc_fcai_cu.db.models import (
    Level,
    Session,
    SessionAttendance,
    Student,
    UserWave,
    Wave,
)

SESSIONS_PAGE_SIZE = 20
STUDENTS_PAGE_SIZE = 25


# ---------------------------------------------------------------- helpers

def _render(request, template, section, context=None, status=200):
    return render(request, template, {"section": section, **(context or {})}, status=status)


def _qs(request):
    params = request.GET.copy()
    params.pop("page", None)
    return params.urlencode()


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _rate(attended, total):
    return round(attended / total * 100, 1) if total else None


def _form_page(request, *, form_class, instance, section, heading, cancel_url,
               success_message, success_url, initial=None, delete_url=None):
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect(success_url)

        status = 422
    else:
        form = form_class(instance=instance, initial=initial)
        status = 200

    return _render(
        request,
        "pages/coach/form.html",
        section,
        {
            "form": form,
            "heading": heading,
            "cancel_url": cancel_url,
            "delete_url": delete_url,
            "editing": instance is not None,
        },
        status=status,
    )


# ---------------------------------------------------------------- dashboard

@coach_required
def dashboard(request):
    now = timezone.now()

    active_students = Student.objects.filter(is_active=True, user__is_active=True)

    by_level = Level.objects.annotate(
        n=Count(
            "students",
            filter=Q(students__is_active=True, students__user__is_active=True),
        )
    ).order_by("level_number")

    upcoming = (
        Session.objects
        .select_related("level", "wave")
        .filter(starts_at__gte=now)
        .order_by("starts_at")[:5]
    )

    needs_attendance = (
        Session.objects
        .select_related("level", "wave")
        .filter(starts_at__lt=now)
        .annotate(recorded=Count("attendances"))
        .filter(recorded=0)
        .order_by("-starts_at")[:5]
    )

    overall = SessionAttendance.objects.aggregate(
        total=Count("id"),
        attended=Count("id", filter=Q(attend=True)),
    )

    return _render(
        request,
        "pages/coach/dashboard.html",
        "dashboard",
        {
            "students_count": active_students.count(),
            "by_level": by_level,
            "current_wave": Wave.objects.first(),
            "upcoming": upcoming,
            "needs_attendance": needs_attendance,
            "overall_rate": _rate(overall["attended"], overall["total"]),
        },
    )


# ---------------------------------------------------------------- waves

@coach_required
def waves_index(request):
    waves = Wave.objects.annotate(
        session_count=Count("sessions", distinct=True),
        student_count=Count("users", distinct=True),
    )
    return _render(request, "pages/coach/waves/index.html", "waves", {"waves": waves})


@coach_required
def waves_create(request):
    return _form_page(
        request,
        form_class=WaveForm,
        instance=None,
        section="waves",
        heading="New wave",
        cancel_url=reverse("app:coach-waves"),
        success_message="Wave created.",
        success_url=reverse("app:coach-waves"),
    )


@coach_required
def waves_edit(request, slug):
    wave = get_object_or_404(Wave, slug=slug)

    return _form_page(
        request,
        form_class=WaveForm,
        instance=wave,
        section="waves",
        heading=f"Edit {wave.title}",
        cancel_url=reverse("app:coach-waves"),
        success_message="Wave updated.",
        success_url=reverse("app:coach-waves"),
    )


# ---------------------------------------------------------------- sessions

@coach_required
def sessions_index(request):
    now = timezone.now()
    wave_slug = request.GET.get("wave", "")
    level_number = _to_int(request.GET.get("level"))
    when = request.GET.get("when", "")

    sessions = (
        Session.objects
        .select_related("wave", "level")
        .annotate(
            recorded=Count("attendances"),
            attended=Count("attendances", filter=Q(attendances__attend=True)),
        )
    )

    if wave_slug:
        sessions = sessions.filter(wave__slug=wave_slug)
    if level_number is not None:
        sessions = sessions.filter(level__level_number=level_number)

    if when == "upcoming":
        sessions = sessions.filter(starts_at__gte=now).order_by("starts_at")
    elif when == "past":
        sessions = sessions.filter(starts_at__lt=now).order_by("-starts_at")
    else:
        sessions = sessions.order_by("-starts_at")

    page = Paginator(sessions, SESSIONS_PAGE_SIZE).get_page(request.GET.get("page"))

    return _render(
        request,
        "pages/coach/sessions/index.html",
        "sessions",
        {
            "page": page,
            "qs": _qs(request),
            "waves": Wave.objects.all(),
            "levels": Level.objects.order_by("level_number"),
            "wave_slug": wave_slug,
            "level_number": level_number,
            "when": when,
            "now": now,
        },
    )


@coach_required
def sessions_create(request):
    return _form_page(
        request,
        form_class=SessionForm,
        instance=None,
        section="sessions",
        heading="New session",
        cancel_url=reverse("app:coach-sessions"),
        success_message="Session created.",
        success_url=reverse("app:coach-sessions"),
        initial={"wave": Wave.objects.first()},
    )


@coach_required
def sessions_edit(request, slug):
    session = get_object_or_404(Session, slug=slug)
    can_delete = not session.attendances.exists()

    return _form_page(
        request,
        form_class=SessionForm,
        instance=session,
        section="sessions",
        heading=f"Edit {session.title}",
        cancel_url=reverse("app:coach-sessions"),
        success_message="Session updated.",
        success_url=reverse("app:coach-sessions"),
        delete_url=reverse("app:coach-sessions-delete", args=[session.slug]) if can_delete else None,
    )


@require_POST
@coach_required
def sessions_delete(request, slug):
    session = get_object_or_404(Session, slug=slug)

    if session.attendances.exists():
        messages.error(request, "This session has attendance records, so it can't be deleted.")
        return redirect("app:coach-sessions-edit", slug=session.slug)

    title = session.title
    session.delete()
    messages.success(request, f"Session “{title}” deleted.")
    return redirect("app:coach-sessions")


# ---------------------------------------------------------------- students

@coach_required
def students_index(request):
    q = request.GET.get("q", "").strip()
    level_number = _to_int(request.GET.get("level"))
    status = request.GET.get("status", "active")

    students = Student.objects.select_related("user", "level")

    if status == "inactive":
        students = students.filter(Q(is_active=False) | Q(user__is_active=False))
    elif status != "all":
        status = "active"
        students = students.filter(is_active=True, user__is_active=True)

    if level_number is not None:
        students = students.filter(level__level_number=level_number)

    if q:
        students = students.filter(
            Q(user__username__icontains=q)
            | Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
            | Q(university_id__icontains=q)
            | Q(discord_handle__icontains=q)
            | Q(codeforces_handle__icontains=q)
        )

    students = students.order_by("level__level_number", "user__first_name", "user__last_name")
    page = Paginator(students, STUDENTS_PAGE_SIZE).get_page(request.GET.get("page"))

    return _render(
        request,
        "pages/coach/students/index.html",
        "students",
        {
            "page": page,
            "qs": _qs(request),
            "q": q,
            "level_number": level_number,
            "status": status,
            "levels": Level.objects.order_by("level_number"),
        },
    )


@coach_required
def students_show(request, username):
    student = get_object_or_404(
        Student.objects.select_related("user", "level"),
        user__username=username,
    )

    update_form = StudentManageForm(instance=student)
    enroll_form = EnrollForm(initial={"level": student.level})
    status = 200

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update":
            update_form = StudentManageForm(request.POST, instance=student)

            if update_form.is_valid():
                update_form.save()
                messages.success(request, "Student updated.")
                return redirect("app:coach-students-show", username=username)

            status = 422

        elif action == "enroll":
            enroll_form = EnrollForm(request.POST)

            if enroll_form.is_valid():
                UserWave.objects.update_or_create(
                    user=student.user,
                    wave=enroll_form.cleaned_data["wave"],
                    defaults={
                        "level": enroll_form.cleaned_data["level"],
                        "is_active": True,
                    },
                )
                messages.success(request, "Wave enrollment saved.")
                return redirect("app:coach-students-show", username=username)

            status = 422

    summary = SessionAttendance.objects.filter(user=student.user).aggregate(
        total=Count("id"),
        attended=Count("id", filter=Q(attend=True)),
    )

    return _render(
        request,
        "pages/coach/students/show.html",
        "students",
        {
            "student": student,
            "update_form": update_form,
            "enroll_form": enroll_form,
            "user_waves": UserWave.objects.select_related("wave", "level").filter(user=student.user),
            "recent": (
                SessionAttendance.objects
                .select_related("session")
                .filter(user=student.user)
                .order_by("-session__starts_at")[:10]
            ),
            "total": summary["total"],
            "attended": summary["attended"],
            "rate": _rate(summary["attended"], summary["total"]),
        },
        status=status,
    )


@require_POST
@coach_required
def students_wave_remove(request, username, wave_slug):
    deleted, _ = UserWave.objects.filter(
        user__username=username,
        wave__slug=wave_slug,
    ).delete()

    messages.success(request, "Enrollment removed." if deleted else "Enrollment not found.")
    return redirect("app:coach-students-show", username=username)


# ---------------------------------------------------------------- attendance report

@coach_required
def attendance_report(request):
    waves = Wave.objects.all()
    wave = Wave.objects.filter(slug=request.GET.get("wave")).first() or waves.first()
    level_number = _to_int(request.GET.get("level"))

    rows, sessions_count = [], 0

    if wave:
        sessions = wave.sessions.all()
        students = Student.objects.select_related("user", "level").filter(
            is_active=True, user__is_active=True
        )

        if level_number is not None:
            sessions = sessions.filter(level__level_number=level_number)
            students = students.filter(level__level_number=level_number)

        sessions_count = sessions.count()

        students = students.annotate(
            total=Count(
                "user__session_attendances",
                filter=Q(user__session_attendances__session__wave=wave),
            ),
            attended=Count(
                "user__session_attendances",
                filter=Q(
                    user__session_attendances__session__wave=wave,
                    user__session_attendances__attend=True,
                ),
            ),
        )

        for s in students:
            rows.append(
                {
                    "name": s.user.full_name or s.user.username,
                    "username": s.user.username,
                    "level": s.level.level_number,
                    "total": s.total,
                    "attended": s.attended,
                    "rate": _rate(s.attended, s.total),
                }
            )

        rows.sort(key=lambda r: (r["rate"] is None, r["rate"] or 0, r["name"]))

    if request.GET.get("format") == "csv" and wave:
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="attendance-{wave.slug}.csv"'
        response.write("\ufeff")  # عشان Excel يقرا العربي صح

        writer = csv.writer(response)
        writer.writerow(["Name", "Username", "Level", "Sessions", "Attended", "Rate %"])
        for r in rows:
            writer.writerow(
                [r["name"], r["username"], r["level"], r["total"], r["attended"],
                 "" if r["rate"] is None else r["rate"]]
            )
        return response

    return _render(
        request,
        "pages/coach/reports/attendance.html",
        "reports",
        {
            "waves": waves,
            "wave": wave,
            "levels": Level.objects.order_by("level_number"),
            "level_number": level_number,
            "rows": rows,
            "sessions_count": sessions_count,
            "qs": _qs(request),
        },
    )
