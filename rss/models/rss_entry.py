"""RSSEntry model."""

from django.db import models

from rss.models.rss_feed import RSSFeed


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
