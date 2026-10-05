import uuid

from django.conf import settings
from django.db import models


class Session(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField(max_length=255, unique=True)

    description = models.TextField(null=True, blank=True)

    wave = models.ForeignKey(
        "Wave",
        null=True,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    level = models.ForeignKey(
        "Level",
        null=True,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    starts_at = models.DateTimeField()

    ends_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
        db_table = "sessions"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} - {self.slug}"