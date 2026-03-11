"""TDD: Tests for RSSFeed model — written before implementation."""

import pytest


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
