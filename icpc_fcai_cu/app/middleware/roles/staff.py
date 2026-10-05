from functools import wraps

from django.shortcuts import render

# from icpc_fcai_cu.app.utils.responses import error_response


def staff_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request,
                "errors/401.html",
                status=401,
            )

        user = request.user
        mentor = getattr(user, "mentor_profile", None)
        coach = getattr(user, "coach_profile", None)

        if not ((mentor and mentor.is_active) or (coach and coach.is_active)):
            return render(
                request,
                "errors/403.html",
                status=403,
            )

        return view(request, *args, **kwargs)

    return wrapper