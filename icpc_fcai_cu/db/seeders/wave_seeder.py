from datetime import datetime

from django.utils import timezone

from icpc_fcai_cu.db.models import Wave


def seed():
    def dt(month, day):
        return timezone.make_aware(
            datetime(2026, month, day, 18, 0)
        )

    waves = [
        {
            "title": "Wave 2026/2027",
            "slug": "wave-2026-2027",
            "description": "ICPC FCAI CU training wave for 2026/2027.",
            "season": 2026,
            "starts_at": dt(10, 6),
            "ends_at": dt(12, 31),
        },
    ]

    result = {}

    for data in waves:
        wave, _ = Wave.objects.update_or_create(
            slug=data["slug"],
            defaults=data,
        )

        result[data["slug"]] = wave

    return result