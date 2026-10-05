from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render

MANAGER_ROLES = ("coach", "support")


def _has_active_role(user, roles):
    for role in roles:
        profile = getattr(user, f"{role}_profile", None)
        if profile is not None and profile.is_active:
            return True
    return False


def is_manager(user):
    return user.is_authenticated and user.is_superuser


def role_required(role):
    """role = student | mentor | coach | support | media"""
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            if not _has_active_role(request.user, (role,)):
                return render(request, "errors/403.html", status=403)

            return view(request, *args, **kwargs)
        return wrapper
    return decorator


def staff_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        if not _has_active_role(request.user, ("mentor", "coach")):
            return render(request, "errors/403.html", status=403)

        return view(request, *args, **kwargs)
    return wrapper


def manager_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        if not is_manager(request.user):
            return render(request, "errors/403.html", status=403)

        return view(request, *args, **kwargs)
    return wrapper