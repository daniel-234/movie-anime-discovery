from django.urls import path

from . import views

app_name = "library"

urlpatterns = [
    path("save/<str:content_type>/<int:object_id>/", views.save_item, name="save"),
    path(
        "unsave/<str:content_type>/<int:object_id>/", views.unsave_item, name="unsave"
    ),
]
