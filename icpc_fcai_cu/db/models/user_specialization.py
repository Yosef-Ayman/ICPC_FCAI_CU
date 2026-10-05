from django.conf import settings
from django.db import models


class UserSpecialization(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="specializations",
    )

    specialization = models.ForeignKey(
        "Specialization",
        on_delete=models.PROTECT,
        related_name="users",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "User Specialization"
        verbose_name_plural = "User Specializations"
        db_table = "user_specializations"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "specialization"],
                name="unique_user_specialization",
            ),
        ]

        indexes = [
            models.Index(
                fields=["user"],
                name="idx_user_spec_user",
            ),
            models.Index(
                fields=["specialization"],
                name="idx_user_spec_spec",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.specialization.name}"