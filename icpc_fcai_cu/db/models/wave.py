from django.db import models


class Wave(models.Model):
    title = models.CharField(max_length=255)

    slug = models.SlugField(max_length=255, unique=True) 

    description = models.TextField(null=True, blank=True) 

    season = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    starts_at = models.DateTimeField()

    ends_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Wave"
        verbose_name_plural = "Waves"
        db_table = "waves"
        ordering = ("-season", "-created_at")

    def __str__(self):
        return f"{self.title} - Season {self.season}"