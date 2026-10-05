from icpc_fcai_cu.db.models import (
    Coach,
    Media,
    Mentor,
    Student,
    Support,
)


def seed(users, levels):
    mentor, _ = Mentor.objects.update_or_create(
        user=users["mentor1"],
        defaults={
            "bio": "ICPC mentor.",
            "codeforces_handle": "mentor_cf",
            "vjudge_handle": "mentor_vjudge",
            "is_active": True,
        },
    )

    coach, _ = Coach.objects.update_or_create(
        user=users["coach1"],
        defaults={
            "bio": "ICPC coach.",
            "codeforces_handle": "coach_cf",
            "vjudge_handle": "coach_vjudge",
            "is_active": True,
        },
    )

    support, _ = Support.objects.update_or_create(
        user=users["support1"],
        defaults={
            "bio": "Community support member.",
            "is_active": True,
        },
    )

    media, _ = Media.objects.update_or_create(
        user=users["media1"],
        defaults={
            "bio": "ICPC media team member.",
            "portfolio_url": "https://example.com/portfolio",
            "instagram_url": "https://instagram.com/example",
            "behance_url": "https://behance.net/example",
            "is_active": True,
        },
    )

    students = {}

    student_data = [
        ("student1", "CU2026001", "Third Year", "student1_discord", "student1_cf", "student1_vjudge", "level-2"),
        ("student2", "CU2026002", "Third Year", "student2_discord", "student2_cf", "student2_vjudge", "level-1"),
        ("student3", "CU2026003", "Second Year", "student3_discord", "student3_cf", "student3_vjudge", "level-0"),
    ]

    for (
        username,
        university_id,
        faculty_year,
        discord_handle,
        codeforces_handle,
        vjudge_handle,
        level_slug,
    ) in student_data:
        student, _ = Student.objects.update_or_create(
            user=users[username],
            defaults={
                "university_id": university_id,
                "faculty_year": faculty_year,
                "phone": "01000000000",
                "discord_handle": discord_handle,
                "codeforces_handle": codeforces_handle,
                "vjudge_handle": vjudge_handle,
                "level": levels[level_slug],
                "is_active": True,
            },
        )

        students[username] = student

    return {
        "mentor": mentor,
        "coach": coach,
        "support": support,
        "media": media,
        "students": students,
    }