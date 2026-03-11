"""Serializers for dashboard API."""
from rest_framework import serializers
from dashboard.models import DashboardWidget, KeyboardShortcut


class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = [
            "id", "title", "widget_type", "api_endpoint",
            "grid_x", "grid_y", "width", "height",
            "enabled", "refresh_interval_seconds",
        ]


class KeyboardShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyboardShortcut
        fields = ["id", "key", "description", "action_type", "target_widget", "enabled"]
