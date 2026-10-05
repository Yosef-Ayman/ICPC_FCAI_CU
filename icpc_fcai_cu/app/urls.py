from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "app"

urlpatterns = [
    path('', home_view.index, name="home-index"),
    path('about', about_view.index, name="about-index"),

    path('levels', level_view.index, name="levels-index"),
    path('levels/<slug:slug>', level_view.show, name="levels-show"),

    path('sessions', session_view.index, name="sessions-index"),
    path('sessions/<slug:slug>', session_view.show, name="sessions-show"),
    path('sessions/<slug:slug>/attendance', attendance_view.index, name="attendance-index"),

    path('waves', wave_view.index, name="waves-index"),
    path('waves/<slug:slug>', wave_view.show, name="waves-show"),

    path('team', team_view.index, name="team-index"),

    path('student/profile', profile_view.student, name="student-profile"),
    path('mentor/profile', profile_view.mentor, name="mentor-profile"),
    path('coach/profile', profile_view.coach, name="coach-profile"),
    path('support/profile', profile_view.support, name="support-profile"),
    path('media/profile', profile_view.media, name="media-profile"),

    path('me/waves', me_view.waves, name="me-waves"),
    path('me/attendances', me_view.attendances, name="me-attendances"),

    path('students', student_view.index, name="students-index"),
    path('students/<str:username>', student_view.show, name="students-show"),

    path('manage/staff', staff_admin_view.index, name="manage-staff-index"),
    path('manage/staff/create', staff_admin_view.create, name="manage-staff-create"),
    path('manage/staff/<str:username>', staff_admin_view.edit, name="manage-staff-edit"),
    path('manage/staff/<str:username>/toggle', staff_admin_view.toggle, name="manage-staff-toggle"),
    # path('manage/lookups', staff_admin_view.lookups, name="manage-lookups"),

    path('coach', coach_view.dashboard, name="coach-dashboard"),

    path('coach/waves', coach_view.waves_index, name="coach-waves"),
    path('coach/waves/create', coach_view.waves_create, name="coach-waves-create"),
    path('coach/waves/<slug:slug>/edit', coach_view.waves_edit, name="coach-waves-edit"),

    path('coach/sessions', coach_view.sessions_index, name="coach-sessions"),
    path('coach/sessions/create', coach_view.sessions_create, name="coach-sessions-create"),
    path('coach/sessions/<slug:slug>/edit', coach_view.sessions_edit, name="coach-sessions-edit"),
    path('coach/sessions/<slug:slug>/delete', coach_view.sessions_delete, name="coach-sessions-delete"),

    path('coach/students', coach_view.students_index, name="coach-students"),
    path('coach/students/<str:username>', coach_view.students_show, name="coach-students-show"),
    path('coach/students/<str:username>/waves/<slug:wave_slug>/remove', coach_view.students_wave_remove, name="coach-students-wave-remove"),

    path('coach/reports/attendance', coach_view.attendance_report, name="coach-report-attendance"),
]
