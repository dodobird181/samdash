"""TDD: Tests for RSS API endpoints — written before implementation."""
import pytest
from datetime import datetime, timezone


@pytest.mark.django_db
class TestRSSAPI:
    def test_rss_requires_auth(self, api_client):
        response = api_client.get("/api/rss/entries/")
        assert response.status_code == 403

    def test_rss_entries_authenticated(self, authenticated_client):
        from rss.models import RSSFeed, RSSEntry
        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed, title="Post 1", link="https://example.com/1",
            summary="Summary", published_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
        )
        response = authenticated_client.get("/api/rss/entries/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == "Post 1"

    def test_rss_entry_shape(self, authenticated_client):
        from rss.models import RSSFeed, RSSEntry
        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed, title="Post", link="https://example.com/1",
            summary="Summary", published_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
        )
        response = authenticated_client.get("/api/rss/entries/")
        entry = response.json()[0]
        for field in ["id", "title", "link", "summary", "published_at", "feed_name"]:
            assert field in entry, f"Missing field: {field}"

    def test_rss_entries_ordered_newest_first(self, authenticated_client):
        from rss.models import RSSFeed, RSSEntry
        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed, title="Old", link="https://example.com/1",
            published_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
        )
        RSSEntry.objects.create(
            feed=feed, title="New", link="https://example.com/2",
            published_at=datetime(2024, 6, 1, tzinfo=timezone.utc)
        )
        response = authenticated_client.get("/api/rss/entries/")
        entries = response.json()
        assert entries[0]["title"] == "New"

    def test_rss_entries_limit_param(self, authenticated_client):
        from rss.models import RSSFeed, RSSEntry
        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        for i in range(20):
            RSSEntry.objects.create(
                feed=feed, title=f"Post {i}", link=f"https://example.com/{i}",
                published_at=datetime(2024, 1, i + 1, tzinfo=timezone.utc)
            )
        response = authenticated_client.get("/api/rss/entries/?limit=5")
        assert len(response.json()) == 5
