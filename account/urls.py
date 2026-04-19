from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import SignUpView

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("edit/", views.edit_profile, name="edit_profile"),
    path("", views.dashboard, name="dashboard"),
]
