from icpc_fcai_cu.db.models import UserWave


def seed(users, levels, waves):
    assignments = [
        ("student1", "icpc-cu-2026", "level-2"),
        ("student2", "icpc-cu-2026", "level-1"),
        ("student3", "icpc-cu-2026", "level-0"),
    ]

    result = []

    for username, wave_slug, level_slug in assignments:
        user_wave, _ = UserWave.objects.update_or_create(
            user=users[username],
            wave=waves[wave_slug],
            defaults={
                "level": levels[level_slug],
                "is_active": True,
            },
        )

        result.append(user_wave)

    return result