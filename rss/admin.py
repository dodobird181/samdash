"""Django Admin registration for RSS models."""
from django.contrib import admin
from rss.models import RSSFeed, RSSEntry


@admin.register(RSSFeed)
class RSSFeedAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "refresh_interval_minutes"]
    search_fields = ["name", "url"]


@admin.register(RSSEntry)
class RSSEntryAdmin(admin.ModelAdmin):
    list_display = ["title", "feed", "published_at", "link"]
    list_filter = ["feed"]
    search_fields = ["title", "summary", "link"]
    ordering = ["-published_at"]
    date_hierarchy = "published_at"
