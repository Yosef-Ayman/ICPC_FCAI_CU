from django import forms
from django.utils.text import slugify

from icpc_fcai_cu.app.forms import StyledFormMixin
from icpc_fcai_cu.db.models import Level, Session, Student, Wave

DT_FORMAT = "%Y-%m-%dT%H:%M"


def datetime_field(label, required=True):
    return forms.DateTimeField(
        label=label,
        required=required,
        input_formats=[DT_FORMAT, "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format=DT_FORMAT),
    )


def unique_slug(model, text, fallback, exclude_pk=None):
    base = slugify(text)[:200] or fallback
    slug, i = base, 2

    while model.objects.filter(slug=slug).exclude(pk=exclude_pk).exists():
        slug = f"{base}-{i}"
        i += 1

    return slug


class AutoSlugMixin:
    """slug اختياري: لو فاضي بيتولد من العنوان."""
    slug_fallback = "item"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False
        self.fields["slug"].label = "Slug (auto if empty)"

    def clean(self):
        data = super().clean()

        if not data.get("slug") and data.get("title"):
            data["slug"] = unique_slug(
                self._meta.model,
                data["title"],
                self.slug_fallback,
                exclude_pk=self.instance.pk,
            )

        starts, ends = data.get("starts_at"), data.get("ends_at")
        if starts and ends and ends <= starts:
            self.add_error("ends_at", "End time must be after the start time.")

        return data


class WaveForm(AutoSlugMixin, StyledFormMixin, forms.ModelForm):
    slug_fallback = "wave"
    starts_at = datetime_field("Starts at")
    ends_at = datetime_field("Ends at", required=False)

    class Meta:
        model = Wave
        fields = ("title", "slug", "season", "starts_at", "ends_at", "description")


class SessionForm(AutoSlugMixin, StyledFormMixin, forms.ModelForm):
    slug_fallback = "session"
    starts_at = datetime_field("Starts at")
    ends_at = datetime_field("Ends at", required=False)

    class Meta:
        model = Session
        fields = ("title", "slug", "wave", "level", "starts_at", "ends_at", "description")


class StudentManageForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            "level",
            "faculty_year",
            "phone",
            "discord_handle",
            "codeforces_handle",
            "vjudge_handle",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_active"].label = "Active student"


class EnrollForm(StyledFormMixin, forms.Form):
    wave = forms.ModelChoiceField(queryset=Wave.objects.all())
    level = forms.ModelChoiceField(queryset=Level.objects.order_by("level_number"))
