"""GraphQL schema for RSS app."""

import graphene
from graphene_django import DjangoObjectType
from rss.models import RSSFeed, RSSEntry


class RSSFeedType(DjangoObjectType):
    """GraphQL type for RSSFeed model."""

    class Meta:
        model = RSSFeed
        fields = ("id", "name", "url", "refresh_interval_minutes")


class RSSEntryType(DjangoObjectType):
    """GraphQL type for RSSEntry model."""

    feed_name = graphene.String()

    class Meta:
        model = RSSEntry
        fields = ("id", "feed", "title", "link", "summary", "published_at")

    def resolve_feed_name(self, info):
        """Return the name of the feed this entry belongs to."""
        return self.feed.name


class Query(graphene.ObjectType):
    """RSS GraphQL queries."""

    rss_entries = graphene.List(RSSEntryType, limit=graphene.Int())
    rss_feeds = graphene.List(RSSFeedType)

    def resolve_rss_entries(self, info, limit=None):
        """Return latest RSS entries, with optional limit."""
        user = info.context.user
        if not user.is_authenticated:
            return []

        entries = RSSEntry.objects.select_related("feed").order_by("-published_at")
        if limit is not None:
            entries = entries[:limit]
        return entries

    def resolve_rss_feeds(self, info):
        """Return all RSS feeds."""
        user = info.context.user
        if not user.is_authenticated:
            return []
        return RSSFeed.objects.all()


schema = graphene.Schema(query=Query)
