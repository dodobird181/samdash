"""URL patterns for the RSS API."""
from django.urls import path
from rss.api import views

urlpatterns = [
    path("entries/", views.entry_list, name="api-rss-entries"),
]
