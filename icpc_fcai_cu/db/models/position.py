from django.db import models


class Position(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        db_table = "positions"
        ordering = ("name",)

    def __str__(self):
        return self.name