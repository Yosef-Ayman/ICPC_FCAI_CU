from datetime import datetime

from django.utils import timezone

from icpc_fcai_cu.db.models import LevelTimeline


def seed(sessions):
    timelines = [
        ("introduction-to-problem-solving", datetime(2026, 10, 6, 18, 0)),
        ("data-types-arithmetic-operations", datetime(2026, 10, 13, 18, 0)),
        ("conditions", datetime(2026, 10, 20, 18, 0)),
        ("dfs-bfs", datetime(2026, 10, 7, 18, 0)),
        ("dijkstra", datetime(2026, 10, 14, 18, 0)),
        ("number-theory", datetime(2026, 10, 21, 18, 0)),
    ]

    result = []

    for slug, starts_at in timelines:
        timeline, _ = LevelTimeline.objects.update_or_create(
            session=sessions[slug],
            defaults={
                "starts_at": timezone.make_aware(starts_at),
            },
        )

        result.append(timeline)

    return result