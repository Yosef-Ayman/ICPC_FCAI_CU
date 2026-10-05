from icpc_fcai_cu.db.models import Specialization


def seed():
    specializations = [
        "Backend Development",
        "Frontend Development",
        "Problem Solving",
        "Competitive Programming",
        "Graphic Design",
        "Video Editing",
        "Content Creation",
        "Social Media",
        "Event Management",
        "Public Relations",
        "Technical Writing",
        "Community Management",
    ]

    result = {}

    for name in specializations:
        specialization, _ = Specialization.objects.get_or_create(
            name=name,
        )

        result[name] = specialization

    return result