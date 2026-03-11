/**
 * RSS Feed widget plugin.
 * Fetches entries from /api/rss/entries/ and renders a scrollable list.
 *
 * Note: data is the full JSON from the API endpoint (array of entries).
 */
import { registerWidget } from "../../registry.js";

function rssRender(container, data) {
    // Handle both REST and GraphQL response formats
    const entries = data.entries || data;

    if (!Array.isArray(entries) || entries.length === 0) {
      container.innerHTML = '<div class="widget-loading">No entries found.</div>';
      return;
    }

    const items = entries.map(entry => {
      const publishedAt = entry.publishedAt || entry.published_at;
      const feedName = entry.feedName || entry.feed_name;

      const date = publishedAt
        ? new Date(publishedAt).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
        : "";
      const summary = entry.summary
        ? `<div class="rss-entry-summary">${_truncate(entry.summary, 120)}</div>`
        : "";

      return `
        <div class="rss-entry">
          <div class="rss-entry-title">
            <a href="${_escapeHtml(entry.link)}" target="_blank" rel="noopener">${_escapeHtml(entry.title)}</a>
          </div>
          <div class="rss-entry-meta">${_escapeHtml(feedName)} &mdash; ${date}</div>
          ${summary}
        </div>
      `;
    });

    container.innerHTML = items.join("");
}

registerWidget({ type: "rss_feed", render: rssRender });

function _escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function _truncate(str, maxLen) {
  if (!str) return "";
  // Strip basic HTML tags from summary
  const plain = str.replace(/<[^>]+>/g, "");
  return plain.length > maxLen ? plain.slice(0, maxLen) + "…" : plain;
}

export { rssRender, _escapeHtml, _truncate };
