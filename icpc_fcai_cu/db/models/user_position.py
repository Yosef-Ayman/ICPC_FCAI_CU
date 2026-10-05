from django.conf import settings
from django.db import models


class UserPosition(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="positions",
    )

    position = models.ForeignKey(
        "Position",
        on_delete=models.PROTECT,
        related_name="users",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "User Position"
        verbose_name_plural = "User Positions"
        db_table = "user_positions"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "position"],
                name="unique_user_position",
            ),
        ]

        indexes = [
            models.Index(
                fields=["user"],
                name="idx_user_position_user",
            ),
            models.Index(
                fields=["position"],
                name="idx_user_position_position",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.position.name}"