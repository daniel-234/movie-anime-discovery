from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

# Semantic class name; the actual styling lives in
# theme/static_src/src/styles.css under @layer components.
INPUT_CLASSES = "form-input"


def _apply_input_classes(form):
    """Attach INPUT_CLASSES to every widget on the form.

    Called from each form's __init__ after super().__init__() has populated
    self.fields. Overwrites any existing 'class' attr so styling has a single
    source of truth.
    """
    for field in form.fields.values():
        field.widget.attrs["class"] = INPUT_CLASSES


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # password1 and password2 are added by UserCreationForm.__init__,
        # so by this point they are in self.fields and get styled too.
        _apply_input_classes(self)


class SignUpProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("country",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_input_classes(self)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_input_classes(self)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "country")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_input_classes(self)
