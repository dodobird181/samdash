"""TDD: Tests for fetch_feeds management command — written before implementation."""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone


def make_mock_entry(title, link, summary, published):
    entry = MagicMock()
    entry.title = title
    entry.link = link
    entry.summary = summary
    entry.published_parsed = published.timetuple()
    return entry


def make_mock_feed(entries):
    feed = MagicMock()
    feed.entries = entries
    feed.bozo = False
    return feed


@pytest.mark.django_db
class TestFetchFeeds:
    def test_fetch_creates_entries(self):
        from rss.models import RSSFeed, RSSEntry
        from rss.management.commands.fetch_feeds import fetch_feed

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        mock_parsed = make_mock_feed([
            make_mock_entry("Post 1", "https://example.com/1", "Summary 1",
                            datetime(2024, 1, 1, tzinfo=timezone.utc)),
        ])

        with patch("rss.management.commands.fetch_feeds.feedparser.parse", return_value=mock_parsed):
            fetch_feed(feed)

        assert RSSEntry.objects.filter(feed=feed).count() == 1
        entry = RSSEntry.objects.get(feed=feed)
        assert entry.title == "Post 1"
        assert entry.link == "https://example.com/1"

    def test_fetch_does_not_duplicate_entries(self):
        from rss.models import RSSFeed, RSSEntry
        from rss.management.commands.fetch_feeds import fetch_feed

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        RSSEntry.objects.create(
            feed=feed, title="Post 1", link="https://example.com/1",
            published_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        )

        mock_parsed = make_mock_feed([
            make_mock_entry("Post 1", "https://example.com/1", "Summary",
                            datetime(2024, 1, 1, tzinfo=timezone.utc)),
        ])

        with patch("rss.management.commands.fetch_feeds.feedparser.parse", return_value=mock_parsed):
            fetch_feed(feed)

        assert RSSEntry.objects.filter(feed=feed).count() == 1

    def test_fetch_multiple_entries(self):
        from rss.models import RSSFeed, RSSEntry
        from rss.management.commands.fetch_feeds import fetch_feed

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        entries = [
            make_mock_entry(f"Post {i}", f"https://example.com/{i}", f"Summary {i}",
                            datetime(2024, 1, i + 1, tzinfo=timezone.utc))
            for i in range(5)
        ]
        mock_parsed = make_mock_feed(entries)

        with patch("rss.management.commands.fetch_feeds.feedparser.parse", return_value=mock_parsed):
            fetch_feed(feed)

        assert RSSEntry.objects.filter(feed=feed).count() == 5

    def test_fetch_handles_missing_summary(self):
        from rss.models import RSSFeed, RSSEntry
        from rss.management.commands.fetch_feeds import fetch_feed

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        entry = make_mock_entry("Post", "https://example.com/1", "", datetime(2024, 1, 1, tzinfo=timezone.utc))
        del entry.summary  # simulate missing attribute
        entry.get = MagicMock(return_value="")
        mock_parsed = make_mock_feed([entry])

        with patch("rss.management.commands.fetch_feeds.feedparser.parse", return_value=mock_parsed):
            # Should not raise
            fetch_feed(feed)

    def test_fetch_skips_entry_with_no_link(self):
        from rss.models import RSSFeed, RSSEntry
        from rss.management.commands.fetch_feeds import fetch_feed

        feed = RSSFeed.objects.create(name="Test", url="https://example.com/feed")
        entry = MagicMock()
        entry.link = ""
        mock_parsed = make_mock_feed([entry])

        with patch("rss.management.commands.fetch_feeds.feedparser.parse", return_value=mock_parsed):
            fetch_feed(feed)

        assert RSSEntry.objects.filter(feed=feed).count() == 0

    def test_handle_with_no_feeds(self, capsys):
        from django.core.management import call_command
        call_command("fetch_feeds")
        captured = capsys.readouterr()
        assert "No feeds configured" in captured.out

    def test_handle_fetches_all_feeds(self, capsys):
        from rss.models import RSSFeed, RSSEntry
        from rss.management.commands.fetch_feeds import Command

        RSSFeed.objects.create(name="Feed A", url="https://a.com/feed")
        RSSFeed.objects.create(name="Feed B", url="https://b.com/feed")

        mock_parsed = make_mock_feed([
            make_mock_entry("Post", "https://a.com/1", "Summary",
                            datetime(2024, 1, 1, tzinfo=timezone.utc)),
        ])

        with patch("rss.management.commands.fetch_feeds.feedparser.parse", return_value=mock_parsed):
            from django.core.management import call_command
            call_command("fetch_feeds")

        captured = capsys.readouterr()
        assert "Done" in captured.out

    def test_handle_logs_error_on_exception(self, capsys):
        from rss.models import RSSFeed
        RSSFeed.objects.create(name="Bad Feed", url="https://bad.com/feed")

        with patch("rss.management.commands.fetch_feeds.fetch_feed", side_effect=Exception("boom")):
            from django.core.management import call_command
            call_command("fetch_feeds")

        captured = capsys.readouterr()
        assert "ERROR" in captured.out or "boom" in captured.out
