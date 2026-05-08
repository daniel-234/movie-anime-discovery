from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "country")
        widgets = {
            "country": forms.Select(
                attrs={
                    "class": "w-full rounded-md border border-gray-300 px-3 py-2 "
                    "focus:border-blue-500 focus:ring focus:ring-blue-200 "
                    "focus:outline-none",
                }
            ),
        }
