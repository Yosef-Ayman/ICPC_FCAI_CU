from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render

from .page_roles import _has_active_role


def is_coach(user):
    return user.is_authenticated and (
        user.is_superuser or _has_active_role(user, ("coach",))
    )


def coach_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        if not is_coach(request.user):
            return render(request, "errors/403.html", status=403)

        return view(request, *args, **kwargs)
    return wrapper
