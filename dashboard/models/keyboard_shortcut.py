"""KeyboardShortcut model."""

from django.db import models


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
