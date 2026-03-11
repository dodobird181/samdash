"""Root URL configuration for samdash."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("api/", include("dashboard.api.urls")),
    path("api/rss/", include("rss.api.urls")),
    path("", include("dashboard.urls")),
]
