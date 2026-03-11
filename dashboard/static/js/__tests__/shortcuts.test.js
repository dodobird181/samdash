/**
 * Tests for ShortcutSystem (shortcuts.js).
 */
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { ShortcutSystem } from "../shortcuts.js";

describe("ShortcutSystem", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div class="widget-cell" id="widget-gold_price" data-type="gold_price"></div>
      <div class="widget-cell" id="widget-silver_price" data-type="silver_price"></div>
    `;
    ShortcutSystem._reset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    document.body.innerHTML = "";
  });

  describe("load", () => {
    it("fetches shortcuts from /api/shortcuts/", async () => {
      const mockShortcuts = [
        { key: "g", action_type: "focus_widget", target_widget: "gold_price" },
      ];
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockShortcuts),
      });

      await ShortcutSystem.load();
      expect(fetch).toHaveBeenCalledWith("/api/shortcuts/");
    });

    it("attaches keydown listener after load", async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve([]),
      });
      const addSpy = vi.spyOn(document, "addEventListener");
      await ShortcutSystem.load();
      expect(addSpy).toHaveBeenCalledWith("keydown", expect.any(Function));
    });

    it("handles fetch failure gracefully", async () => {
      global.fetch = vi.fn().mockRejectedValue(new Error("Network error"));
      const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});
      await expect(ShortcutSystem.load()).resolves.not.toThrow();
      warnSpy.mockRestore();
    });

    it("handles non-ok response gracefully", async () => {
      global.fetch = vi.fn().mockResolvedValue({ ok: false });
      await expect(ShortcutSystem.load()).resolves.not.toThrow();
    });
  });

  describe("keyboard actions", () => {
    async function loadWith(shortcuts) {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(shortcuts),
      });
      await ShortcutSystem.load();
    }

    it("focus_widget adds focused class to matching widget", async () => {
      await loadWith([{ key: "g", action_type: "focus_widget", target_widget: "gold_price" }]);
      document.dispatchEvent(new KeyboardEvent("keydown", { key: "g" }));
      expect(document.getElementById("widget-gold_price").classList.contains("focused")).toBe(true);
    });

    it("does not fire when typing in an input", async () => {
      await loadWith([{ key: "g", action_type: "focus_widget", target_widget: "gold_price" }]);
      const input = document.createElement("input");
      document.body.appendChild(input);
      input.dispatchEvent(new KeyboardEvent("keydown", { key: "g", bubbles: true }));
      expect(document.getElementById("widget-gold_price").classList.contains("focused")).toBe(false);
    });

    it("next_widget cycles through widget cells", async () => {
      await loadWith([{ key: "n", action_type: "next_widget", target_widget: "" }]);
      document.dispatchEvent(new KeyboardEvent("keydown", { key: "n" }));
      const cells = document.querySelectorAll(".widget-cell");
      const hasFocused = Array.from(cells).some(c => c.classList.contains("focused"));
      expect(hasFocused).toBe(true);
    });

    it("previous_widget cycles backward", async () => {
      await loadWith([{ key: "p", action_type: "previous_widget", target_widget: "" }]);
      document.dispatchEvent(new KeyboardEvent("keydown", { key: "p" }));
      const cells = document.querySelectorAll(".widget-cell");
      const hasFocused = Array.from(cells).some(c => c.classList.contains("focused"));
      expect(hasFocused).toBe(true);
    });

    it("ignores unknown action types gracefully", async () => {
      await loadWith([{ key: "z", action_type: "unknown_action", target_widget: "" }]);
      expect(() => {
        document.dispatchEvent(new KeyboardEvent("keydown", { key: "z" }));
      }).not.toThrow();
    });
  });
});
