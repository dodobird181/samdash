"""RSS models: RSSFeed and RSSEntry."""
from django.db import models


class RSSFeed(models.Model):
    """A configured RSS feed source."""

    name = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    refresh_interval_minutes = models.PositiveIntegerField(default=60)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RSSEntry(models.Model):
    """A single entry fetched from an RSS feed."""

    feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE, related_name="entries")
    title = models.CharField(max_length=500)
    link = models.URLField(unique=True)
    summary = models.TextField(blank=True, default="")
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
