from django.urls import path
from .views import (
    login_view,
    logout,
    admin_dashboard,
    bulk_upload,
    view_users,
    view_xml,
    statistics,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout, name="logout"),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/bulk-upload/", bulk_upload, name="bulk_upload"),
    path("admin/users/", view_users, name="view_users"),
    path("admin/xml/", view_xml, name="view_xml"),
    path("admin/statistics/", statistics, name="statistics"),
]
