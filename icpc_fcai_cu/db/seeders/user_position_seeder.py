from icpc_fcai_cu.db.models import UserPosition


def seed(users, positions):
    assignments = {
        "mentor1": ["Training"],
        "coach1": ["Training", "Technical"],
        "support1": ["Community", "Operations"],
        "media1": ["Media"],
    }

    result = []

    for username, position_names in assignments.items():
        for position_name in position_names:
            user_position, _ = UserPosition.objects.get_or_create(
                user=users[username],
                position=positions[position_name],
            )

            result.append(user_position)

    return result