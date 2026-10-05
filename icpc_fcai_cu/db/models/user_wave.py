from django.conf import settings
from django.db import models


class UserWave(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="waves",
    )

    wave = models.ForeignKey(
        "Wave",
        on_delete=models.CASCADE,
        related_name="users",
    )

    level = models.ForeignKey(
        "Level",
        on_delete=models.PROTECT,
        related_name="user_waves",
    )

    is_active = models.BooleanField(
        default=True,
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "User Wave"
        verbose_name_plural = "User Waves"
        db_table = "user_waves"
        ordering = ("-joined_at",)

        constraints = [
            models.UniqueConstraint(
                fields=("user", "wave"),
                name="unique_user_wave",
            ),
        ]

        indexes = [
            models.Index(
                fields=("user", "wave"),
            ),
            models.Index(
                fields=("wave", "level"),
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.wave} - {self.level}"