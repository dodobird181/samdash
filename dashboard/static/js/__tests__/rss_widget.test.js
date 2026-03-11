/**
 * Tests for the RSS feed widget plugin.
 */
import { describe, it, expect, beforeEach, vi } from "vitest";
import { _escapeHtml, _truncate, rssRender } from "../widgets/rss_feed/widget.js";

describe("RSS feed widget helpers", () => {
  describe("_escapeHtml", () => {
    it("escapes ampersands", () => {
      expect(_escapeHtml("a & b")).toBe("a &amp; b");
    });

    it("escapes angle brackets", () => {
      expect(_escapeHtml("<script>")).toBe("&lt;script&gt;");
    });

    it("escapes double quotes", () => {
      expect(_escapeHtml('"hello"')).toBe("&quot;hello&quot;");
    });

    it("handles empty string", () => {
      expect(_escapeHtml("")).toBe("");
    });

    it("handles null/undefined", () => {
      expect(_escapeHtml(null)).toBe("");
      expect(_escapeHtml(undefined)).toBe("");
    });
  });

  describe("_truncate", () => {
    it("truncates text longer than maxLen", () => {
      const result = _truncate("a".repeat(200), 100);
      expect(result.length).toBeLessThanOrEqual(102); // 100 + "…"
      expect(result.endsWith("…")).toBe(true);
    });

    it("does not truncate text shorter than maxLen", () => {
      const result = _truncate("short text", 100);
      expect(result).toBe("short text");
    });

    it("strips HTML tags before truncating", () => {
      const result = _truncate("<p>Hello <strong>world</strong></p>", 200);
      expect(result).not.toContain("<p>");
      expect(result).toContain("Hello");
    });

    it("handles empty string", () => {
      expect(_truncate("", 100)).toBe("");
    });

    it("handles null", () => {
      expect(_truncate(null, 100)).toBe("");
    });
  });

  describe("rssRender", () => {
    let container;

    beforeEach(() => {
      container = document.createElement("div");
    });

    it("renders a list of entries", () => {
      const data = [
        {
          title: "Post One",
          link: "https://example.com/1",
          summary: "A summary.",
          feed_name: "Test Feed",
          published_at: "2024-01-01T00:00:00Z",
        },
      ];
      rssRender(container, data);
      expect(container.innerHTML).toContain("Post One");
      expect(container.innerHTML).toContain("https://example.com/1");
    });

    it("shows 'no entries' message when data is empty", () => {
      rssRender(container, []);
      expect(container.innerHTML).toContain("No entries");
    });

    it("escapes HTML in entry titles", () => {
      const data = [
        {
          title: '<script>alert("xss")</script>',
          link: "https://example.com/1",
          summary: "",
          feed_name: "Test",
          published_at: null,
        },
      ];
      rssRender(container, data);
      expect(container.innerHTML).not.toContain("<script>");
    });

    it("handles missing published_at gracefully", () => {
      const data = [
        { title: "Post", link: "https://example.com/1", summary: "", feed_name: "Feed", published_at: null },
      ];
      expect(() => rssRender(container, data)).not.toThrow();
    });

    it("handles non-array data", () => {
      rssRender(container, null);
      expect(container.innerHTML).toContain("No entries");
    });
  });
});
