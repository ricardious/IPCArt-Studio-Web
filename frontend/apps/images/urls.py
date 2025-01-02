from django.urls import path
from .views import gallery, upload, image_editor, help_view

urlpatterns = [
    path("user/gallery/", gallery, name="gallery"),
    path("user/upload_image/", upload, name="upload_image"),
    path("user/image_editor/", image_editor, name="image_editor"),
    path("user/help/", help_view, name="help"),
]
