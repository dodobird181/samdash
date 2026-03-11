/**
 * Tests for Dashboard bootstrap (dashboard.js).
 */
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";

vi.mock("../registry.js", () => ({
  WidgetRegistry: { renderWidget: vi.fn() },
  registerWidget: vi.fn(),
}));

vi.mock("../shortcuts.js", () => ({
  ShortcutSystem: { load: vi.fn(), _reset: vi.fn() },
}));

import { Dashboard } from "../dashboard.js";
import { WidgetRegistry } from "../registry.js";
import { ShortcutSystem } from "../shortcuts.js";

describe("Dashboard", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div class="widget-cell" id="widget-gold_price" data-type="gold_price" data-endpoint="/api/gold-price/" data-refresh="300">
        <div class="widget-body" id="body-gold_price"><div class="widget-loading">Loading...</div></div>
      </div>
      <div class="widget-cell" id="widget-rss_feed" data-type="rss_feed" data-endpoint="/api/rss/entries/" data-refresh="0">
        <div class="widget-body" id="body-rss_feed"></div>
      </div>
    `;

    vi.clearAllMocks();
    Dashboard._reset();
  });

  afterEach(() => {
    Dashboard._clearTimers();
    vi.restoreAllMocks();
    document.body.innerHTML = "";
  });

  describe("init", () => {
    it("fetches data for each widget cell", async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ x: [], y: [] }),
      });
      await Dashboard.init();
      expect(fetch).toHaveBeenCalledWith("/api/gold-price/");
      expect(fetch).toHaveBeenCalledWith("/api/rss/entries/");
    });

    it("calls renderWidget for each successfully loaded widget", async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ x: ["2024-01-01"], y: [1900] }),
      });
      await Dashboard.init();
      expect(WidgetRegistry.renderWidget).toHaveBeenCalledTimes(2);
    });

    it("shows error in widget body when fetch fails", async () => {
      global.fetch = vi.fn().mockRejectedValue(new Error("Network error"));
      await Dashboard.init();
      const body = document.getElementById("body-gold_price");
      expect(body.innerHTML).toContain("Error");
    });

    it("shows error when HTTP response is not ok", async () => {
      global.fetch = vi.fn().mockResolvedValue({ ok: false, status: 500 });
      await Dashboard.init();
      const body = document.getElementById("body-gold_price");
      expect(body.innerHTML).toContain("Error");
    });

    it("calls ShortcutSystem.load after widgets are loaded", async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({}),
      });
      await Dashboard.init();
      expect(ShortcutSystem.load).toHaveBeenCalled();
    });
  });

  describe("refreshWidget", () => {
    it("re-fetches data for a specific widget", async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ x: [], y: [] }),
      });
      await Dashboard.refreshWidget("gold_price");
      expect(fetch).toHaveBeenCalledWith("/api/gold-price/");
    });

    it("does nothing for unknown widget id", async () => {
      global.fetch = vi.fn();
      await Dashboard.refreshWidget("nonexistent");
      expect(fetch).not.toHaveBeenCalled();
    });
  });
});
