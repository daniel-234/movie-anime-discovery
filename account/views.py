from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache

from media.services import get_saved_anime, get_saved_manga, get_saved_movies

from .forms import ProfileEditForm, SignUpForm, SignUpProfileForm, UserEditForm


@receiver(user_logged_in)
def welcome_on_login(sender, user, request, **kwargs):
    messages.success(request, f"Welcome back, {user.first_name or user.username}.")


@never_cache
@login_required
def dashboard(request):
    return render(
        request,
        "account/dashboard.html",
        {
            "section": "dashboard",
            "saved_movies": get_saved_movies(request.user),
            "saved_anime": get_saved_anime(request.user),
            "saved_manga": get_saved_manga(request.user),
        },
    )


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
