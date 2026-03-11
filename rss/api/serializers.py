"""Serializers for the RSS API."""
from rest_framework import serializers
from rss.models import RSSEntry


class RSSEntrySerializer(serializers.ModelSerializer):
    feed_name = serializers.CharField(source="feed.name", read_only=True)

    class Meta:
        model = RSSEntry
        fields = ["id", "feed_name", "title", "link", "summary", "published_at"]
