"""Django Admin registration for dashboard models."""
from django.contrib import admin
from dashboard.models import DashboardWidget, KeyboardShortcut


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ["title", "widget_type", "grid_x", "grid_y", "width", "height", "enabled", "refresh_interval_seconds"]
    list_filter = ["enabled", "widget_type"]
    search_fields = ["title", "widget_type", "api_endpoint"]
    list_editable = ["enabled", "grid_x", "grid_y", "width", "height"]
    ordering = ["grid_y", "grid_x"]


@admin.register(KeyboardShortcut)
class KeyboardShortcutAdmin(admin.ModelAdmin):
    list_display = ["key", "description", "action_type", "target_widget", "enabled"]
    list_filter = ["enabled", "action_type"]
    search_fields = ["key", "description", "target_widget"]
    list_editable = ["enabled"]
