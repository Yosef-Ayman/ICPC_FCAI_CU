from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from icpc_fcai_cu.db.models import User, Student, Level

REQUIRED_FIELDS = {
    "username": "Username",
    "password": "Password",
    "first_name": "First name",
    "last_name": "Last name",
    "university_id": "University ID",
    "faculty_year": "Faculty year",
    "discord_handle": "Discord handle",
}


def _clean(post, key):
    return (post.get(key) or "").strip()


def student(request):
    if request.user.is_authenticated:
        return redirect("app:student-profile")

    if request.method != "POST":
        return render(request, "pages/auth/register.html", {"form": {}, "errors": {}})

    data = {key: _clean(request.POST, key) for key in (
        "username", "email", "first_name", "last_name", "university_id",
        "faculty_year", "phone", "discord_handle",
        "codeforces_handle", "vjudge_handle",
    )}
    password = request.POST.get("password", "")
    password_confirm = request.POST.get("password_confirm", "")

    errors = {}

    # 1) Required fields
    for field, label in REQUIRED_FIELDS.items():
        value = password if field == "password" else data.get(field)
        if not value:
            errors[field] = f"{label} is required"

    # 2) Uniqueness
    email = data["email"] or None
    codeforces = data["codeforces_handle"] or None
    vjudge = data["vjudge_handle"] or None

    if "username" not in errors and User.objects.filter(username__iexact=data["username"]).exists():
        errors["username"] = "This username is already taken"
    if email and User.objects.filter(email__iexact=email).exists():
        errors["email"] = "This email is already registered"
    if "university_id" not in errors and Student.objects.filter(university_id=data["university_id"]).exists():
        errors["university_id"] = "This university ID is already registered"
    if "discord_handle" not in errors and Student.objects.filter(discord_handle=data["discord_handle"]).exists():
        errors["discord_handle"] = "This Discord handle is already used"
    if codeforces and Student.objects.filter(codeforces_handle=codeforces).exists():
        errors["codeforces_handle"] = "This Codeforces handle is already used"
    if vjudge and Student.objects.filter(vjudge_handle=vjudge).exists():
        errors["vjudge_handle"] = "This Vjudge handle is already used"

    # 3) Password
    if "password" not in errors:
        if password != password_confirm:
            errors["password_confirm"] = "Passwords do not match"
        else:
            candidate = User(
                username=data["username"],
                email=email,
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            try:
                validate_password(password, user=candidate)
            except ValidationError as e:
                errors["password"] = list(e.messages)

    # 4) Level
    level = Level.objects.order_by("level_number").first()
    if level is None:
        messages.error(request, "Registration is closed right now. Please try again later.")
        return render(request, "pages/auth/register.html", {"form": data, "errors": errors})

    if errors:
        return render(
            request,
            "pages/auth/register.html",
            {"form": data, "errors": errors},
            status=422,
        )

    # 5) Create (atomic جوه بلوك صغير عشان نقدر نمسك IntegrityError)
    try:
        with transaction.atomic():
            user = User(
                username=data["username"],
                email=email,  # None مش "" عشان الـ unique
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            user.set_password(password)
            user.save()

            Student.objects.create(
                user=user,
                university_id=data["university_id"],
                faculty_year=data["faculty_year"],
                phone=data["phone"],
                discord_handle=data["discord_handle"],
                codeforces_handle=codeforces,
                vjudge_handle=vjudge,
                level=level,
            )
    except IntegrityError:
        # حد سجل بنفس البيانات في نفس اللحظة (race condition)
        messages.error(request, "Some of these details were just taken. Please check and try again.")
        return render(
            request,
            "pages/auth/register.html",
            {"form": data, "errors": {}},
            status=409,
        )

    login(request, user)
    messages.success(request, "Your account has been created. Welcome!")
    return redirect("app:student-profile")