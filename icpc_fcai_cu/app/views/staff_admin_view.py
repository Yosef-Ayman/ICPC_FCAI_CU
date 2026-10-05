import secrets
from functools import reduce
from operator import or_

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from icpc_fcai_cu.app.forms import ROLE_CONFIG, ROLE_FORMS, ROLE_LABELS, StaffUserForm
from icpc_fcai_cu.app.middleware.page_roles import MANAGER_ROLES, manager_required
from icpc_fcai_cu.db.models import (
    Position,
    Specialization,
    User,
    UserPosition,
    UserSpecialization,
)

PAGE_SIZE = 15


# ---------------------------------------------------------------- helpers

def _staff_filter():
    return reduce(or_, (Q(**{f"{role}_profile__isnull": False}) for role in ROLE_CONFIG))


def _staff_or_404(username):
    return get_object_or_404(
        User.objects.filter(_staff_filter()),
        username=username,
    )


def _profile(user, role):
    return getattr(user, f"{role}_profile", None)


def _int_list(values):
    out = []
    for v in values:
        try:
            out.append(int(v))
        except (TypeError, ValueError):
            continue
    return out


def _valid_ids(model, raw_values):
    return set(model.objects.filter(pk__in=_int_list(raw_values)).values_list("pk", flat=True))


def _sync(through, fk, user, wanted):
    existing = set(through.objects.filter(user=user).values_list(f"{fk}_id", flat=True))

    through.objects.filter(user=user, **{f"{fk}_id__in": existing - wanted}).delete()
    through.objects.bulk_create(
        [through(user=user, **{f"{fk}_id": pk}) for pk in wanted - existing]
    )


def _safe_next(request, default):
    target = request.POST.get("next") or ""
    if target and url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
        return target
    return default


def _is_self(request, user):
    return user.pk == request.user.pk


# ---------------------------------------------------------------- list

@manager_required
def index(request):
    q = request.GET.get("q", "").strip()
    role = request.GET.get("role", "")
    status = request.GET.get("status", "")

    users = User.objects.all()

    if role in ROLE_CONFIG:
        users = users.filter(**{f"{role}_profile__isnull": False})
    else:
        users = users.filter(_staff_filter())

    if q:
        users = users.filter(
            Q(username__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
        )

    if status == "active":
        users = users.filter(is_active=True)
    elif status == "inactive":
        users = users.filter(is_active=False)

    users = (
        users
        .select_related(*[f"{r}_profile" for r in ROLE_CONFIG])
        .order_by("first_name", "last_name", "username")
    )

    page = Paginator(users, PAGE_SIZE).get_page(request.GET.get("page"))

    for u in page:
        u.role_badges = [
            {"label": ROLE_LABELS[r], "active": _profile(u, r).is_active}
            for r in ROLE_CONFIG
            if _profile(u, r) is not None
        ]

    params = request.GET.copy()
    params.pop("page", None)

    return render(
        request,
        "pages/manage/staff/index.html",
        {
            "page": page,
            "q": q,
            "role": role,
            "status": status,
            "role_choices": ROLE_LABELS,
            "qs": params.urlencode(),
        },
    )


# ---------------------------------------------------------------- create / edit

def _handle(request, user):
    """Shared by create (user=None) and edit. Returns (response, context)."""
    creating = user is None
    posted = request.method == "POST"

    if posted:
        user_form = StaffUserForm(request.POST, instance=user)
    else:
        user_form = StaffUserForm(instance=user)

    role_forms = {}
    enabled = {}

    for role, form_class in ROLE_FORMS.items():
        profile = None if creating else _profile(user, role)
        checked = bool(request.POST.get(f"{role}-is_active")) if posted else False
        enabled[role] = profile is not None or checked

        if posted and enabled[role]:
            role_forms[role] = form_class(request.POST, instance=profile, prefix=role)
        elif profile is None:
            role_forms[role] = form_class(prefix=role, initial={"is_active": False})
        else:
            role_forms[role] = form_class(instance=profile, prefix=role)

    if posted:
        selected_positions = _int_list(request.POST.getlist("positions"))
        selected_specs = _int_list(request.POST.getlist("specializations"))
    elif creating:
        selected_positions, selected_specs = [], []
    else:
        selected_positions = list(user.positions.values_list("position_id", flat=True))
        selected_specs = list(user.specializations.values_list("specialization_id", flat=True))

    if posted:
        valid = user_form.is_valid()

        for role, form in role_forms.items():
            if enabled[role]:
                valid = form.is_valid() and valid

        turned_on = [r for r in ROLE_CONFIG if request.POST.get(f"{r}-is_active")]

        if not turned_on:
            messages.error(request, "Enable at least one role for this staff member.")
            valid = False
        elif (
            not creating
            and _is_self(request, user)
            and not request.user.is_superuser
            and not any(r in MANAGER_ROLES for r in turned_on)
        ):
            messages.error(request, "You can't remove your own management access.")
            valid = False

        if valid:
            password = None

            with transaction.atomic():
                saved = user_form.save(commit=False)

                if creating:
                    password = secrets.token_urlsafe(9)
                    saved.set_password(password)

                saved.save()

                for role, form in role_forms.items():
                    if enabled[role]:
                        profile = form.save(commit=False)
                        profile.user = saved
                        profile.save()

                _sync(UserPosition, "position", saved,
                      _valid_ids(Position, request.POST.getlist("positions")))
                _sync(UserSpecialization, "specialization", saved,
                      _valid_ids(Specialization, request.POST.getlist("specializations")))

            if creating:
                messages.success(
                    request,
                    f"Account created for {saved.username}. "
                    f"Temporary password (shown once): {password}",
                )
            else:
                messages.success(request, "Staff member updated.")

            return redirect("app:manage-staff-index"), None

        messages.error(request, "Please fix the errors below.")

    context = {
        "creating": creating,
        "staff_user": user,
        "user_form": user_form,
        "sections": [
            {"key": r, "label": ROLE_LABELS[r], "form": role_forms[r]}
            for r in ROLE_CONFIG
        ],
        "positions": Position.objects.all(),
        "specializations": Specialization.objects.all(),
        "selected_positions": selected_positions,
        "selected_specs": selected_specs,
        "is_self": (not creating) and _is_self(request, user),
    }
    return None, context


@manager_required
def create(request):
    response, context = _handle(request, None)
    if response:
        return response
    status = 422 if request.method == "POST" else 200
    return render(request, "pages/manage/staff/form.html", context, status=status)


@manager_required
def edit(request, username):
    user = _staff_or_404(username)
    response, context = _handle(request, user)
    if response:
        return response
    status = 422 if request.method == "POST" else 200
    return render(request, "pages/manage/staff/form.html", context, status=status)


# ---------------------------------------------------------------- account actions

@require_POST
@manager_required
def toggle(request, username):
    user = _staff_or_404(username)
    fallback = "app:manage-staff-index"

    if _is_self(request, user):
        messages.error(request, "You can't deactivate your own account.")
        return redirect(_safe_next(request, fallback))

    user.is_active = not user.is_active
    user.save(update_fields=["is_active"])

    messages.success(
        request,
        f"{user.username} is now {'active' if user.is_active else 'inactive'}.",
    )
    return redirect(_safe_next(request, fallback))


# ---------------------------------------------------------------- positions & specializations

LOOKUPS = {
    "position": Position,
    "specialization": Specialization,
}


@manager_required
def lookups(request):
    if request.method == "POST":
        model = LOOKUPS.get(request.POST.get("kind"))
        action = request.POST.get("action")

        if model is None:
            messages.error(request, "Unknown type.")
            return redirect("app:manage-lookups")

        label = model._meta.verbose_name.lower()

        if action == "add":
            name = (request.POST.get("name") or "").strip()

            if not name:
                messages.error(request, "Name is required.")
            elif len(name) > 100:
                messages.error(request, "Name is too long (100 characters max).")
            elif model.objects.filter(name__iexact=name).exists():
                messages.error(request, f"This {label} already exists.")
            else:
                model.objects.create(name=name)
                messages.success(request, f"{label.capitalize()} added.")

        elif action == "delete":
            obj = model.objects.filter(pk=request.POST.get("pk")).first()

            if obj is None:
                messages.error(request, f"This {label} was not found.")
            else:
                try:
                    obj.delete()
                    messages.success(request, f"{label.capitalize()} deleted.")
                except ProtectedError:
                    messages.error(
                        request,
                        f"This {label} is assigned to staff members. Unassign it first.",
                    )

        return redirect("app:manage-lookups")

    return render(
        request,
        "pages/manage/lookups.html",
        {
            "positions": Position.objects.annotate(n=Count("users")).order_by("name"),
            "specializations": Specialization.objects.annotate(n=Count("users")).order_by("name"),
        },
    )
