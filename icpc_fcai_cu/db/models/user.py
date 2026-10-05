import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    username = models.CharField(
        max_length=128,
        unique=True,
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    mobile_number = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    # Identity
    first_name = models.CharField(
        max_length=255,
        blank=True,
    )

    last_name = models.CharField(
        max_length=255,
        blank=True,
    )

    # Tracking
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # Status
    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    # Email verification
    email_verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.username} <{self.email}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Mentor(models.Model):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="mentor_profile",
    )

    bio = models.TextField(
        null=True,
        blank=True,
    )

    codeforces_handle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )

    vjudge_handle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "mentors"

    def __str__(self):
        return self.user.full_name or self.user.username


class Coach(models.Model):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="coach_profile",
    )

    bio = models.TextField(
        null=True,
        blank=True,
    )

    codeforces_handle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )

    vjudge_handle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "coaches"

    def __str__(self):
        return self.user.full_name or self.user.username


class Support(models.Model):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="support_profile",
    )

    bio = models.TextField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "supports"

    def __str__(self):
        return self.user.full_name or self.user.username


class Media(models.Model):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="media_profile",
    )

    bio = models.TextField(
        null=True,
        blank=True,
    )

    portfolio_url = models.URLField(
        null=True,
        blank=True,
    )

    instagram_url = models.URLField(
        null=True,
        blank=True,
    )

    behance_url = models.URLField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "media_members"

    def __str__(self):
        return self.user.full_name or self.user.username


class Student(models.Model):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    university_id = models.CharField(max_length=50, unique=True)

    faculty_year = models.CharField(max_length=20)

    phone = models.CharField(max_length=20, blank=True)

    discord_handle = models.CharField(max_length=100, unique=True)

    codeforces_handle = models.CharField(max_length=100, null=True, blank=True, unique=True)

    vjudge_handle = models.CharField(max_length=100, null=True, blank=True, unique=True)

    level = models.ForeignKey(
        "Level",
        on_delete=models.PROTECT,
        related_name="students",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "students"

    def __str__(self):
        return self.user.full_name or self.user.username