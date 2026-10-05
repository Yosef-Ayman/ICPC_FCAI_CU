from django.contrib.auth import get_user_model


User = get_user_model()


def seed():
    users = [
        {
            "username": "admin",
            "email": "admin@icpc-fcai-cu.com",
            "password": "password123",
            "first_name": "ICPC",
            "last_name": "Admin",
            "mobile_number": "01000000000",
            "is_staff": True,
            "is_superuser": True,
        },
        {
            "username": "mentor1",
            "email": "mentor1@icpc-fcai-cu.com",
            "password": "password123",
            "first_name": "Ahmed",
            "last_name": "Mentor",
        },
        {
            "username": "coach1",
            "email": "coach1@icpc-fcai-cu.com",
            "password": "password123",
            "first_name": "Mohamed",
            "last_name": "Coach",
        },
        {
            "username": "support1",
            "email": "support1@icpc-fcai-cu.com",
            "password": "password123",
            "first_name": "Omar",
            "last_name": "Support",
        },
        {
            "username": "media1",
            "email": "media1@icpc-fcai-cu.com",
            "password": "password123",
            "first_name": "Youssef",
            "last_name": "Media",
        },
        {
            "username": "student1",
            "email": "student1@icpc-fcai-cu.com",
            "password": "password123",
            "first_name": "Youssef",
            "last_name": "Student",
        },
        {
            "username": "student2",
            "email": "student2@icpc-fcai-cu.com",
            "password": "password123",
            "first_name": "Ahmed",
            "last_name": "Student",
        },
        {
            "username": "student3",
            "email": "student3@icpc-fcai-cu.com",
            "password": "password123",
            "first_name": "Mahmoud",
            "last_name": "Student",
        },
    ]

    result = {}

    for item in users:
        data = {
            key: value
            for key, value in item.items()
            if key not in {"password", "is_superuser"}
        }

        user, created = User.objects.get_or_create(
            username=item["username"],
            defaults=data,
        )

        if created:
            user.set_password(item["password"])

        user.is_staff = item.get("is_staff", user.is_staff)
        user.is_superuser = item.get("is_superuser", user.is_superuser)

        user.save()

        result[user.username] = user

    return result