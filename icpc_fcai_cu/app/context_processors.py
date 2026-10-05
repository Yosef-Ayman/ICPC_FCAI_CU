from icpc_fcai_cu.db.models import Level
from icpc_fcai_cu.app.middleware.page_roles import _has_active_role, is_manager
from icpc_fcai_cu.app.middleware.coach_access import is_coach

ROLES = ("student", "mentor", "coach", "support", "media")


def navigation(request):
    user = request.user
    authenticated = user.is_authenticated

    roles = [r for r in ROLES if authenticated and _has_active_role(user, (r,))]
    staff_roles = [r for r in roles if r != "student"]

    if staff_roles or (authenticated and user.is_superuser):
        panel_layout = "layouts/staff-layout.html"
    elif "student" in roles:
        panel_layout = "layouts/student-layout.html"
    else:
        panel_layout = "layouts/guest-layout.html"

    return {
        "nav_levels": Level.objects.order_by("level_number"),
        "user_roles": roles,
        "panel_layout": panel_layout,
        "is_staff_member": "mentor" in roles or "coach" in roles,
        "is_manager": is_manager(user),
        "is_coach": is_coach(user),
    }
