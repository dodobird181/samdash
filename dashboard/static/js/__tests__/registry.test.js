/**
 * Tests for WidgetRegistry (registry.js).
 */
import { describe, it, expect, beforeEach, vi } from "vitest";
import { WidgetRegistry } from "../registry.js";

describe("WidgetRegistry", () => {
  beforeEach(() => {
    // Clear registry between tests by re-importing a fresh instance
    WidgetRegistry._reset();
  });

  describe("registerWidget", () => {
    it("registers a valid plugin", () => {
      const render = vi.fn();
      WidgetRegistry.registerWidget({ type: "gold_price", render });
      expect(WidgetRegistry.hasWidget("gold_price")).toBe(true);
    });

    it("rejects a plugin with no type", () => {
      const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
      WidgetRegistry.registerWidget({ render: vi.fn() });
      expect(WidgetRegistry.listWidgets()).toHaveLength(0);
      consoleSpy.mockRestore();
    });

    it("rejects a plugin with no render function", () => {
      const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
      WidgetRegistry.registerWidget({ type: "gold_price" });
      expect(WidgetRegistry.hasWidget("gold_price")).toBe(false);
      consoleSpy.mockRestore();
    });

    it("rejects null plugin", () => {
      const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
      WidgetRegistry.registerWidget(null);
      expect(WidgetRegistry.listWidgets()).toHaveLength(0);
      consoleSpy.mockRestore();
    });

    it("overwrites existing registration for same type", () => {
      const renderA = vi.fn();
      const renderB = vi.fn();
      WidgetRegistry.registerWidget({ type: "gold_price", render: renderA });
      WidgetRegistry.registerWidget({ type: "gold_price", render: renderB });
      const container = document.createElement("div");
      WidgetRegistry.renderWidget("gold_price", container, {});
      expect(renderB).toHaveBeenCalled();
      expect(renderA).not.toHaveBeenCalled();
    });
  });

  describe("renderWidget", () => {
    it("calls the registered render function with container and data", () => {
      const render = vi.fn();
      WidgetRegistry.registerWidget({ type: "gold_price", render });
      const container = document.createElement("div");
      const data = { x: ["2024-01-01"], y: [1900] };
      WidgetRegistry.renderWidget("gold_price", container, data);
      expect(render).toHaveBeenCalledWith(container, data);
    });

    it("renders error message for unknown widget type", () => {
      const container = document.createElement("div");
      WidgetRegistry.renderWidget("unknown_type", container, {});
      expect(container.innerHTML).toContain("Unknown widget type");
    });

    it("catches render errors and shows error message", () => {
      const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
      WidgetRegistry.registerWidget({
        type: "broken_widget",
        render() { throw new Error("render failed"); },
      });
      const container = document.createElement("div");
      WidgetRegistry.renderWidget("broken_widget", container, {});
      expect(container.innerHTML).toContain("Render error");
      consoleSpy.mockRestore();
    });
  });

  describe("hasWidget", () => {
    it("returns false for unregistered type", () => {
      expect(WidgetRegistry.hasWidget("nope")).toBe(false);
    });

    it("returns true for registered type", () => {
      WidgetRegistry.registerWidget({ type: "silver_price", render: vi.fn() });
      expect(WidgetRegistry.hasWidget("silver_price")).toBe(true);
    });
  });

  describe("listWidgets", () => {
    it("returns empty array initially", () => {
      expect(WidgetRegistry.listWidgets()).toEqual([]);
    });

    it("returns all registered types", () => {
      WidgetRegistry.registerWidget({ type: "a", render: vi.fn() });
      WidgetRegistry.registerWidget({ type: "b", render: vi.fn() });
      expect(WidgetRegistry.listWidgets()).toEqual(expect.arrayContaining(["a", "b"]));
    });
  });
});
