"""Dashboard models: DashboardWidget and KeyboardShortcut."""

from django.db import models


class DashboardWidget(models.Model):
    """A configurable dashboard widget managed via Django Admin."""

    WIDGET_TYPES = [
        ("gold_price", "Gold Price"),
        ("silver_price", "Silver Price"),
        ("oil_price", "Oil Price"),
        ("treasury_10y", "US 10Y Treasury"),
        ("dow_gold_ratio", "Dow/Gold Ratio"),
        ("rss_feed", "RSS Feed"),
    ]

    title = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    api_endpoint = models.CharField(max_length=200, blank=True, default="")
    grid_x = models.PositiveIntegerField(default=0)
    grid_y = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=1)
    height = models.PositiveIntegerField(default=1)
    enabled = models.BooleanField(default=True)
    refresh_interval_seconds = models.PositiveIntegerField(default=300)

    class Meta:
        ordering = ["grid_y", "grid_x"]

    def __str__(self):
        return f"{self.title} ({self.widget_type})"


class KeyboardShortcut(models.Model):
    """A keyboard shortcut configurable via Django Admin."""

    ACTION_TYPES = [
        ("focus_widget", "Focus Widget"),
        ("expand_widget", "Expand Widget"),
        ("refresh_widget", "Refresh Widget"),
        ("next_widget", "Next Widget"),
        ("previous_widget", "Previous Widget"),
    ]

    key = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    target_widget = models.CharField(max_length=50, blank=True, default="")
    enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ["key"]

    def __str__(self):
        return f"{self.key} → {self.description}"
