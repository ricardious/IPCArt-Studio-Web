from django.urls import path, include
from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path("", include("apps.users.urls")),
    path("", include("apps.images.urls")),
    path("", TemplateView.as_view(template_name="users/home.html"), name="home"),
]
