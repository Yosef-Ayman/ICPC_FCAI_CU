from icpc_fcai_cu.db.models import Position


def seed():
    positions = [
        "Leadership",
        "Technical",
        "Media",
        "Community",
        "Training",
        "Operations",
    ]

    result = {}

    for name in positions:
        position, _ = Position.objects.get_or_create(
            name=name,
        )

        result[name] = position

    return result