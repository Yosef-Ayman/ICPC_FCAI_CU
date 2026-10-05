from django.db import models


class LevelTimeline(models.Model):
    session = models.OneToOneField(
        "Session",
        on_delete=models.CASCADE,
        related_name="timeline",
    )

    starts_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Level Timeline"
        verbose_name_plural = "Level Timelines"
        db_table = "level_timelines"
        ordering = ("starts_at",)

        indexes = [
            models.Index(fields=("starts_at",)),
        ]

    def __str__(self):
        return f"{self.session} - {self.starts_at}"