"""Tests for RSS GraphQL API."""

import pytest
from datetime import datetime, timezone
from graphene.test import Client
from config.schema import schema


@pytest.mark.django_db
class TestRSSGraphQL:
    def test_rss_entries_query_requires_auth(self):
        """Test that RSS entries query requires authentication."""
        from django.contrib.auth.models import AnonymousUser

        query = """
            query {
                rssEntries {
                    id
                    title
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": AnonymousUser()})()
        result = client.execute(query, context_value=mock_request)
        # Should return empty list when not authenticated
        assert result["data"]["rssEntries"] == []

    def test_rss_entries_query_authenticated(self, admin_user):
        """Test RSS entries query returns data when authenticated."""
        from rss.models import RSSFeed, RSSEntry

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed,
            title="Post 1",
            link="https://example.com/1",
            summary="Summary",
            published_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )

        query = """
            query {
                rssEntries {
                    id
                    title
                    link
                    summary
                    publishedAt
                    feedName
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": admin_user})()
        result = client.execute(query, context_value=mock_request)

        assert "errors" not in result
        assert len(result["data"]["rssEntries"]) >= 1
        assert result["data"]["rssEntries"][0]["title"] == "Post 1"
        assert result["data"]["rssEntries"][0]["feedName"] == "Test"

    def test_rss_entries_ordered_newest_first(self, admin_user):
        """Test that RSS entries are ordered newest first."""
        from rss.models import RSSFeed, RSSEntry

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed,
            title="Old",
            link="https://example.com/1",
            published_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        RSSEntry.objects.create(
            feed=feed,
            title="New",
            link="https://example.com/2",
            published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
        )

        query = """
            query {
                rssEntries {
                    title
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": admin_user})()
        result = client.execute(query, context_value=mock_request)

        entries = result["data"]["rssEntries"]
        assert entries[0]["title"] == "New"

    def test_rss_entries_with_limit(self, admin_user):
        """Test RSS entries query with limit parameter."""
        from rss.models import RSSFeed, RSSEntry

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        for i in range(20):
            RSSEntry.objects.create(
                feed=feed,
                title=f"Post {i}",
                link=f"https://example.com/{i}",
                published_at=datetime(2024, 1, i + 1, tzinfo=timezone.utc),
            )

        query = """
            query {
                rssEntries(limit: 5) {
                    title
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": admin_user})()
        result = client.execute(query, context_value=mock_request)

        assert len(result["data"]["rssEntries"]) == 5

    def test_rss_feeds_query(self, admin_user):
        """Test RSS feeds query returns all feeds."""
        from rss.models import RSSFeed

        RSSFeed.objects.create(name="Feed 1", url="https://example.com/feed1")
        RSSFeed.objects.create(name="Feed 2", url="https://example.com/feed2")

        query = """
            query {
                rssFeeds {
                    id
                    name
                    url
                    refreshIntervalMinutes
                }
            }
        """
        client = Client(schema)
        mock_request = type("Request", (), {"user": admin_user})()
        result = client.execute(query, context_value=mock_request)

        assert "errors" not in result
        assert len(result["data"]["rssFeeds"]) == 2
        feed_names = [f["name"] for f in result["data"]["rssFeeds"]]
        assert "Feed 1" in feed_names
        assert "Feed 2" in feed_names
