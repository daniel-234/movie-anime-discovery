from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache

from .forms import ProfileEditForm, SignUpForm, SignUpProfileForm, UserEditForm


@never_cache
@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def signup(request):
    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        profile_form = SignUpProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.profile.update({}, profile_form.cleaned_data)
            messages.success(
                request,
                "Account created. You can now log in.",
            )
            return redirect("account:login")
    else:
        user_form = SignUpForm()
        profile_form = SignUpProfileForm()

    return render(
        request,
        "registration/signup.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


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
            return redirect("account:dashboard")
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
