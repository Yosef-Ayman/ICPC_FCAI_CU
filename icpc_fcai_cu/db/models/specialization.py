from django.db import models


class Specialization(models.Model):
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
        verbose_name = "Specialization"
        verbose_name_plural = "Specializations"
        db_table = "specializations"
        ordering = ("name",)

    def __str__(self):
        return self.name