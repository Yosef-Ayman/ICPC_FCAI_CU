from icpc_fcai_cu.db.models import UserSpecialization


def seed(users, specializations):
    assignments = {
        "mentor1": [
            "Competitive Programming",
            "Problem Solving",
        ],
        "coach1": [
            "Competitive Programming",
            "Problem Solving",
        ],
        "support1": [
            "Community Management",
            "Event Management",
        ],
        "media1": [
            "Graphic Design",
            "Video Editing",
            "Social Media",
        ],
    }

    result = []

    for username, specialization_names in assignments.items():
        for specialization_name in specialization_names:
            user_specialization, _ = UserSpecialization.objects.get_or_create(
                user=users[username],
                specialization=specializations[specialization_name],
            )

            result.append(user_specialization)

    return result