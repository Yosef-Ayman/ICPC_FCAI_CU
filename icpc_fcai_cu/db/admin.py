from django.contrib import admin

from .models import (
    User,
    Mentor,
    Coach,
    Support,
    Media,
    Student,
    Level,
    Wave,
    UserWave,
    Session,
    SessionAttendance,
    LevelTimeline,
    Position,
    Specialization,
    UserPosition,
    UserSpecialization,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "date_joined",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "level_number",
        "slug",
        "created_at",
    )

    list_filter = (
        "level_number",
    )

    search_fields = (
        "title",
        "slug",
        "description",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "level_number",
    )


@admin.register(Wave)
class WaveAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "season",
        "starts_at",
        "ends_at",
        "created_at",
    )

    list_filter = (
        "season",
    )

    search_fields = (
        "title",
        "slug",
        "description",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-season",
        "-created_at",
    )


@admin.register(UserWave)
class UserWaveAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "wave",
        "level",
        "is_active",
        "joined_at",
        "updated_at",
    )

    list_filter = (
        "wave",
        "level",
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "wave__title",
        "level__title",
    )

    readonly_fields = (
        "joined_at",
        "updated_at",
    )

    ordering = (
        "-joined_at",
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "wave",
        "level",
        "starts_at",
        "ends_at",
        "created_at",
    )

    list_filter = (
        "wave",
        "level",
    )

    search_fields = (
        "title",
        "slug",
        "description",
        "wave__title",
        "level__title",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-starts_at",
    )


@admin.register(SessionAttendance)
class SessionAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "session",
        "attend",
        "created_at",
    )

    list_filter = (
        "attend",
        "session",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "session__title",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(LevelTimeline)
class LevelTimelineAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "starts_at",
    )

    list_filter = (
        "session",
    )

    search_fields = (
        "session__title",
        "session__slug",
    )

    ordering = (
        "starts_at",
    )


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "codeforces_handle",
        "vjudge_handle",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "codeforces_handle",
        "vjudge_handle",
        "bio",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "codeforces_handle",
        "vjudge_handle",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "codeforces_handle",
        "vjudge_handle",
        "bio",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "bio",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "portfolio_url",
        "instagram_url",
        "behance_url",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "bio",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "university_id",
        "faculty_year",
        "level",
        "discord_handle",
        "codeforces_handle",
        "vjudge_handle",
        "is_active",
        "created_at",
    )

    list_filter = (
        "level",
        "faculty_year",
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "university_id",
        "discord_handle",
        "codeforces_handle",
        "vjudge_handle",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )


@admin.register(UserPosition)
class UserPositionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "position",
        "created_at",
    )

    list_filter = (
        "position",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "position__name",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(UserSpecialization)
class UserSpecializationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "specialization",
        "created_at",
    )

    list_filter = (
        "specialization",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "specialization__name",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )