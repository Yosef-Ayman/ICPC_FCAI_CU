from django.shortcuts import render

from icpc_fcai_cu.db.models import Mentor, Coach, Support, Media

SECTIONS = (
    ("Coaches", Coach),
    ("Mentors", Mentor),
    ("Support", Support),
    ("Media", Media),
)


def index(request):
    sections = []

    for title, model in SECTIONS:
        members = (
            model.objects
            .select_related("user")
            .prefetch_related(
                "user__positions__position",
                "user__specializations__specialization",
            )
            .filter(is_active=True, user__is_active=True)
            .order_by("user__first_name", "user__last_name")
        )
        if members:
            sections.append({"title": title, "members": members})

    return render(request, "pages/team/index.html", {"sections": sections})