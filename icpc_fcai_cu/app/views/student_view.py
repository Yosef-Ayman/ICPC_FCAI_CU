from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import render

from icpc_fcai_cu.db.models import Student
from icpc_fcai_cu.app.middleware.roles import *


STUDENTS_DEFAULT_LIMIT = 12
STUDENTS_MAX_LIMIT = 24

RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW = 60


def _get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "unknown")


def _rate_limit(request, key_prefix):
    ip = _get_client_ip(request)

    key = f"rate-limit:{key_prefix}:{ip}"

    if cache.add(key, 1, timeout=RATE_LIMIT_WINDOW):
        return True

    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=RATE_LIMIT_WINDOW)
        return True

    return count <= RATE_LIMIT_REQUESTS


def _get_limit(request):
    raw_limit = request.GET.get("limit")

    try:
        limit = int(raw_limit)
    except (TypeError, ValueError):
        limit = STUDENTS_DEFAULT_LIMIT

    return max(1, min(limit, STUDENTS_MAX_LIMIT))


def index(request):
    if not _rate_limit(request, "students-index"):
        return render(
            request,
            "errors/429.html",
            status=429,
        )

    limit = _get_limit(request)

    students_queryset = (
        Student.objects
        .filter(is_active=True)
        .select_related(
            "user",
            "level",
        )
        .prefetch_related(
            "user__positions__position",
            "user__specializations__specialization",
            "user__waves__wave",
            "user__waves__level",
        )
        .order_by(
            "level__level_number",
            "user__first_name",
            "user__last_name",
        )
    )

    paginator = Paginator(
        students_queryset,
        limit,
    )

    page_number = request.GET.get("page", 1)

    try:
        page = paginator.get_page(page_number)
    except Exception:
        page = paginator.get_page(1)

    return render(
        request,
        "pages/students/index.html",
        {
            "students": page.object_list,
            "page": page,
            "paginator": paginator,
            "limit": limit,
            "max_limit": STUDENTS_MAX_LIMIT,
        },
    )

def show(request, username):
    if not _rate_limit(request, "students-show"):
        return render(
            request,
            "errors/429.html",
            status=429,
        )

    student = (
        Student.objects
        .filter(
            user__username=username,
            is_active=True,
            user__is_active=True,
        )
        .select_related(
            "user",
            "level",
        )
        .prefetch_related(
            "user__positions__position",
            "user__specializations__specialization",
            "user__waves__wave",
            "user__waves__level",
            "user__session_attendances__session",
        )
        .first()
    )

    if student is None:
        raise Http404("Student not found.")

    attendances = list(
        student.user.session_attendances.all()
    )

    attendance_total = len(attendances)
    attendance_attended = sum(
        1 for attendance in attendances
        if attendance.attend
    )

    attendance_rate = (
        round((attendance_attended / attendance_total) * 100)
        if attendance_total
        else 0
    )

    return render(
        request,
        "pages/students/show.html",
        {
            "student": student,
            "positions": student.user.positions.all(),
            "specializations": student.user.specializations.all(),
            "waves": student.user.waves.all(),
            "attendance_total": attendance_total,
            "attendance_attended": attendance_attended,
            "attendance_rate": attendance_rate,
        },
    )