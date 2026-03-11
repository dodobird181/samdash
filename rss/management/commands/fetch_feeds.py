"""Management command: fetch all configured RSS feeds and store entries."""
import time
import logging
from datetime import datetime, timezone

import feedparser
from django.core.management.base import BaseCommand

from rss.models import RSSFeed, RSSEntry

logger = logging.getLogger(__name__)


def fetch_feed(feed: RSSFeed) -> int:
    """Fetch a single RSS feed and store new entries. Returns count of new entries."""
    logger.info("Fetching feed: %s (%s)", feed.name, feed.url)
    parsed = feedparser.parse(feed.url)

    new_count = 0
    for raw in parsed.entries:
        link = getattr(raw, "link", "") or ""
        if not link:
            continue

        if RSSEntry.objects.filter(link=link).exists():
            continue

        title = getattr(raw, "title", "(no title)")
        summary = getattr(raw, "summary", "") or ""

        published_at = None
        if hasattr(raw, "published_parsed") and raw.published_parsed:
            try:
                published_at = datetime(*raw.published_parsed[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                pass

        RSSEntry.objects.create(
            feed=feed,
            title=title,
            link=link,
            summary=summary,
            published_at=published_at,
        )
        new_count += 1

    logger.info("Added %d new entries from %s", new_count, feed.name)
    return new_count


class Command(BaseCommand):
    """Fetch all enabled RSS feeds and store new entries."""

    help = "Fetch all RSS feeds and store new entries in the database"

    def handle(self, *args, **options):
        feeds = RSSFeed.objects.all()
        if not feeds.exists():
            self.stdout.write("No feeds configured.")
            return

        total = 0
        for feed in feeds:
            try:
                count = fetch_feed(feed)
                total += count
                self.stdout.write(self.style.SUCCESS(f"  {feed.name}: +{count} entries"))
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f"  {feed.name}: ERROR — {exc}"))
                logger.exception("Error fetching feed %s", feed.name)

        self.stdout.write(self.style.SUCCESS(f"Done. Total new entries: {total}"))
