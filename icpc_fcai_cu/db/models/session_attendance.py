from django.conf import settings
from django.db import models


class SessionAttendance(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="session_attendances",
    )

    title = models.CharField(max_length=255)

    session = models.ForeignKey(
        "Session",
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    attend = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Session Attendance"
        verbose_name_plural = "Session Attendances"
        db_table = "session_attendances"
        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=("user", "session"),
                name="unique_user_session_attendance",
            ),
        ]

        indexes = [
            models.Index(
                fields=("user", "session"),
            ),
            models.Index(
                fields=("session", "attend"),
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.session} - {self.attend}"