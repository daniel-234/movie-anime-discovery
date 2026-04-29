from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView

from .forms import ProfileEditForm, UserEditForm


@never_cache
@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@never_cache
@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            request.user.profile.update(
                user_form.cleaned_data, profile_form.cleaned_data
            )
            messages.success(request, "Your profile was successfully updated.")
            return redirect("dashboard")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        "account/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )
