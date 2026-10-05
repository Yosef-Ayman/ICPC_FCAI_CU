from functools import wraps

from django.shortcuts import render

# from icpc_fcai_cu.app.utils.responses import error_response


def mentor_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request,
                "errors/401.html",
                status=401,
            )

        if not hasattr(request.user, "mentor_profile"):
            return render(
                request,
                "errors/403.html",
                status=403,
            )

        if not request.user.mentor_profile.is_active:
            return render(
                request,
                "errors/403.html",
                status=403,
            )

        return view(request, *args, **kwargs)

    return wrapper