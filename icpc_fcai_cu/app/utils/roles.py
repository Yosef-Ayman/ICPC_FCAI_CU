ROLES = ("student", "mentor", "coach", "support", "media")


def get_roles(user):
    roles = []
    for role in ROLES:
        profile = getattr(user, f"{role}_profile", None)
        if profile is not None and profile.is_active:
            roles.append(role)
    return roles