from django.db import models
from django.core.validators import MinValueValidator


class Level(models.Model):
    title = models.CharField(max_length=255)

    slug = models.SlugField(max_length=255, unique=True) 

    description = models.TextField(null=True, blank=True)

    level_number = models.PositiveIntegerField(
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Level"
        verbose_name_plural = "Levels"
        db_table = "levels"
        ordering = ("level_number",)

    def __str__(self):
        return f"Level {self.level_number} - {self.slug}"