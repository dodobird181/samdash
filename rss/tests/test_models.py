"""TDD: Tests for RSS models — written before implementation."""
import pytest
from datetime import datetime, timezone


@pytest.mark.django_db
class TestRSSFeed:
    def test_create_feed(self):
        from rss.models import RSSFeed
        f = RSSFeed.objects.create(
            name="Joan Westenberg",
            url="https://www.joanwestenberg.com/feed",
            refresh_interval_minutes=60,
        )
        assert f.pk is not None
        assert f.name == "Joan Westenberg"

    def test_feed_str(self):
        from rss.models import RSSFeed
        f = RSSFeed(name="Joan Westenberg", url="https://example.com/feed")
        assert "Joan Westenberg" in str(f)

    def test_feed_default_interval(self):
        from rss.models import RSSFeed
        f = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        assert f.refresh_interval_minutes == 60

    def test_feed_url_required(self):
        from rss.models import RSSFeed
        from django.core.exceptions import ValidationError
        f = RSSFeed(name="No URL", url="")
        with pytest.raises(ValidationError):
            f.full_clean()


@pytest.mark.django_db
class TestRSSEntry:
    def test_create_entry(self):
        from rss.models import RSSFeed, RSSEntry
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
        from rss.models import RSSFeed, RSSEntry
        feed = RSSFeed(name="Test", url="https://example.com/feed")
        entry = RSSEntry(feed=feed, title="My Post")
        assert "My Post" in str(entry)

    def test_entry_ordering_newest_first(self):
        from rss.models import RSSFeed, RSSEntry
        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed, title="Older", link="https://example.com/1",
            published_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        RSSEntry.objects.create(
            feed=feed, title="Newer", link="https://example.com/2",
            published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
        )
        entries = list(RSSEntry.objects.all())
        assert entries[0].title == "Newer"

    def test_entry_cascade_delete(self):
        from rss.models import RSSFeed, RSSEntry
        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed, title="Post", link="https://example.com/1",
            published_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )
        assert RSSEntry.objects.count() == 1
        feed.delete()
        assert RSSEntry.objects.count() == 0
