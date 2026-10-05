from functools import wraps

from icpc_fcai_cu.app.utils.responses import error_response


def auth_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request,
                "errors/401.html",
                status=401,
            )

        return view(request, *args, **kwargs)

    return wrapper