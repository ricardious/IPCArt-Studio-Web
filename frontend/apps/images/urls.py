from django.urls import path
from .views import gallery

urlpatterns = [
    path("user/gallery/", gallery, name="gallery"),
]
