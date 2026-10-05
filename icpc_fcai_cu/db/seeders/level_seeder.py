from icpc_fcai_cu.db.models import Level


def seed():
    levels = [
        {
            "title": "Level 0",
            "slug": "level-0",
            "description": "Introduction to problem solving and programming fundamentals.",
            "level_number": 0,
        },
        {
            "title": "Level 1",
            "slug": "level-1",
            "description": "Building strong problem solving fundamentals.",
            "level_number": 1,
        },
        {
            "title": "Level 2",
            "slug": "level-2",
            "description": "Advanced algorithms and competitive programming topics.",
            "level_number": 2,
        },
    ]

    result = {}

    for data in levels:
        level, _ = Level.objects.update_or_create(
            slug=data["slug"],
            defaults={
                "title": data["title"],
                "description": data["description"],
                "level_number": data["level_number"],
            },
        )

        result[data["slug"]] = level

    return result