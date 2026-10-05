from datetime import datetime, timedelta

from django.utils import timezone

from icpc_fcai_cu.db.models import Session


def seed(waves, levels):
    wave = waves["icpc-cu-2026"]

    def dt(month, day, hour=18):
        return timezone.make_aware(
            datetime(2026, month, day, hour, 0)
        )

    sessions = [
        {
            "title": "Introduction to Problem Solving",
            "slug": "introduction-to-problem-solving",
            "description": "Introduction to competitive programming and problem solving.",
            "wave": wave,
            "level": levels["level-0"],
            "starts_at": dt(10, 6),
            "ends_at": dt(10, 6, 20),
        },
        {
            "title": "Data Types & Arithmetic Operations",
            "slug": "data-types-arithmetic-operations",
            "description": "Programming data types and arithmetic operations.",
            "wave": wave,
            "level": levels["level-0"],
            "starts_at": dt(10, 13),
            "ends_at": dt(10, 13, 20),
        },
        {
            "title": "Conditions",
            "slug": "conditions",
            "description": "Conditional statements and decision making.",
            "wave": wave,
            "level": levels["level-0"],
            "starts_at": dt(10, 20),
            "ends_at": dt(10, 20, 20),
        },
        {
            "title": "DFS & BFS",
            "slug": "dfs-bfs",
            "description": "Graph traversal using DFS and BFS.",
            "wave": wave,
            "level": levels["level-2"],
            "starts_at": dt(10, 7),
            "ends_at": dt(10, 7, 20),
        },
        {
            "title": "Dijkstra",
            "slug": "dijkstra",
            "description": "Shortest path algorithms.",
            "wave": wave,
            "level": levels["level-2"],
            "starts_at": dt(10, 14),
            "ends_at": dt(10, 14, 20),
        },
        {
            "title": "Number Theory",
            "slug": "number-theory",
            "description": "Core number theory techniques for competitive programming.",
            "wave": wave,
            "level": levels["level-2"],
            "starts_at": dt(10, 21),
            "ends_at": dt(10, 21, 20),
        },
    ]

    result = {}

    for data in sessions:
        session, _ = Session.objects.update_or_create(
            slug=data["slug"],
            defaults=data,
        )

        result[data["slug"]] = session

    return result