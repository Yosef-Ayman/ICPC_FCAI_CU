from django.shortcuts import render

from icpc_fcai_cu.app.middleware.roles import *
from icpc_fcai_cu.app.utils.responses import *


@student_required
def student(request):
    profile = request.user.student_profile
    return render(request, "pages/profile/student.html", {"profile": profile})

@mentor_required
def mentor(request):
    return render(request, "pages/profile/staff.html", {"profile": request.user.mentor_profile, "role": "Mentor"})

@coach_required
def coach(request):
    return render(request, "pages/profile/staff.html", {"profile": request.user.coach_profile, "role": "Coach"})

@support_required
def support(request):
    return render(request, "pages/profile/staff.html", {"profile": request.user.support_profile, "role": "Support"})

@media_required
def media(request):
    return render(request, "pages/profile/staff.html", {"profile": request.user.media_profile, "role": "Media"})