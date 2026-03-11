"""TDD: Tests for RSSEntry model — written before implementation."""

from datetime import datetime, timezone

import pytest


@pytest.mark.django_db
class TestRSSEntry:
    def test_create_entry(self):
        from rss.models import RSSEntry, RSSFeed

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        entry = RSSEntry.objects.create(
            feed=feed,
            title="Test Entry",
            link="https://example.com/post/1",
            summary="A test entry summary.",
            published_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        assert entry.pk is not None
        assert entry.feed == feed
        assert entry.title == "Test Entry"

    def test_entry_str(self):
        from rss.models import RSSEntry, RSSFeed

        feed = RSSFeed(name="Test", url="https://example.com/feed")
        entry = RSSEntry(feed=feed, title="My Post")
        assert "My Post" in str(entry)

    def test_entry_ordering_newest_first(self):
        from rss.models import RSSEntry, RSSFeed

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed,
            title="Older",
            link="https://example.com/1",
            published_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        RSSEntry.objects.create(
            feed=feed,
            title="Newer",
            link="https://example.com/2",
            published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
        )
        entries = list(RSSEntry.objects.all())
        assert entries[0].title == "Newer"

    def test_entry_cascade_delete(self):
        from rss.models import RSSEntry, RSSFeed

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed,
            title="Post",
            link="https://example.com/1",
            published_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        assert RSSEntry.objects.count() == 1
        feed.delete()
        assert RSSEntry.objects.count() == 0
        assert RSSEntry.objects.count() == 0
