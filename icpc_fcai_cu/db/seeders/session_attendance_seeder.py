from icpc_fcai_cu.db.models import SessionAttendance


def seed(users, sessions):
    student_usernames = [
        "student1",
        "student2",
        "student3",
    ]

    result = []

    attendance = {
        "student1": {
            "introduction-to-problem-solving": True,
            "data-types-arithmetic-operations": True,
            "conditions": True,
            "dfs-bfs": True,
            "dijkstra": False,
            "number-theory": False,
        },
        "student2": {
            "introduction-to-problem-solving": True,
            "data-types-arithmetic-operations": True,
            "conditions": False,
            "dfs-bfs": True,
            "dijkstra": False,
            "number-theory": False,
        },
        "student3": {
            "introduction-to-problem-solving": True,
            "data-types-arithmetic-operations": False,
            "conditions": False,
            "dfs-bfs": False,
            "dijkstra": False,
            "number-theory": False,
        },
    }

    for username in student_usernames:
        user = users[username]

        for session_slug, attend in attendance[username].items():
            session = sessions[session_slug]

            attendance_record, _ = SessionAttendance.objects.update_or_create(
                user=user,
                session=session,
                defaults={
                    "title": session.title,
                    "attend": attend,
                },
            )

            result.append(attendance_record)

    return result