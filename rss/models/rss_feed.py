"""RSSFeed model."""

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
