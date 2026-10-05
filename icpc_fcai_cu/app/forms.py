from django import forms

from icpc_fcai_cu.db.models import User, Mentor, Coach, Support, Media

HANDLES = ("bio", "codeforces_handle", "vjudge_handle")

ROLE_CONFIG = {
    "coach": (Coach, HANDLES),
    "mentor": (Mentor, HANDLES),
    "support": (Support, ("bio",)),
    "media": (Media, ("bio", "portfolio_url", "instagram_url", "behance_url")),
}

ROLE_LABELS = {
    "coach": "Coach",
    "mentor": "Mentor",
    "support": "Support",
    "media": "Media",
}

INPUT_CLASS = (
    "mt-2 w-full rounded-xl border border-neutral-300 bg-white px-4 py-3 text-sm "
    "outline-none transition focus:border-[#2b6aad] focus:ring-4 focus:ring-[#2b6aad]/10"
)
CHECKBOX_CLASS = "h-5 w-5 rounded border-neutral-300 accent-[#2b6aad]"


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = CHECKBOX_CLASS
            else:
                widget.attrs["class"] = INPUT_CLASS

            if isinstance(widget, forms.Textarea):
                widget.attrs["rows"] = 3

        if "is_active" in self.fields:
            self.fields["is_active"].label = "Enabled"


class StaffUserForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "mobile_number")


def _make_role_form(role):
    model, fields = ROLE_CONFIG[role]
    meta = type("Meta", (), {"model": model, "fields": tuple(fields) + ("is_active",)})
    return type(f"{model.__name__}Form", (StyledFormMixin, forms.ModelForm), {"Meta": meta})


ROLE_FORMS = {role: _make_role_form(role) for role in ROLE_CONFIG}
