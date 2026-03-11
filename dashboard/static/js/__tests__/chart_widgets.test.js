/**
 * Tests for Plotly-based chart widget plugins.
 * Plotly is mocked so tests run without a browser/CDN.
 */
import { describe, it, expect, beforeEach, vi } from "vitest";
import { goldPriceRender } from "../widgets/gold_price/widget.js";
import { silverPriceRender } from "../widgets/silver_price/widget.js";
import { oilPriceRender } from "../widgets/oil_price/widget.js";
import { treasury10yRender } from "../widgets/treasury_10y/widget.js";
import { dowGoldRatioRender } from "../widgets/dow_gold_ratio/widget.js";

// Mock Plotly globally
const mockNewPlot = vi.fn();
global.Plotly = { newPlot: mockNewPlot };

const MOCK_DATA = {
  x: ["2024-01-01", "2024-01-02", "2024-01-03"],
  y: [1900.5, 1910.2, 1905.8],
};

describe("Chart widget plugins", () => {
  let container;

  beforeEach(() => {
    container = document.createElement("div");
    mockNewPlot.mockClear();
  });

  describe("gold_price widget", () => {
    it("calls Plotly.newPlot with correct container and data", () => {
      goldPriceRender(container, MOCK_DATA);
      expect(mockNewPlot).toHaveBeenCalledTimes(1);
      const [calledContainer, traces] = mockNewPlot.mock.calls[0];
      expect(calledContainer).toBe(container);
      expect(traces[0].x).toEqual(MOCK_DATA.x);
      expect(traces[0].y).toEqual(MOCK_DATA.y);
    });

    it("uses gold colour line", () => {
      goldPriceRender(container, MOCK_DATA);
      const trace = mockNewPlot.mock.calls[0][1][0];
      expect(trace.line.color).toBe("#b8860b");
    });

    it("disables the mode bar", () => {
      goldPriceRender(container, MOCK_DATA);
      const config = mockNewPlot.mock.calls[0][3];
      expect(config.displayModeBar).toBe(false);
    });

    it("sets responsive: true", () => {
      goldPriceRender(container, MOCK_DATA);
      const config = mockNewPlot.mock.calls[0][3];
      expect(config.responsive).toBe(true);
    });

    it("sets y-axis title to USD/oz", () => {
      goldPriceRender(container, MOCK_DATA);
      const layout = mockNewPlot.mock.calls[0][2];
      expect(layout.yaxis.title).toBe("USD/oz");
    });
  });

  describe("silver_price widget", () => {
    it("calls Plotly.newPlot with correct data", () => {
      silverPriceRender(container, MOCK_DATA);
      expect(mockNewPlot).toHaveBeenCalledTimes(1);
      const trace = mockNewPlot.mock.calls[0][1][0];
      expect(trace.x).toEqual(MOCK_DATA.x);
    });

    it("uses slate-grey colour", () => {
      silverPriceRender(container, MOCK_DATA);
      const trace = mockNewPlot.mock.calls[0][1][0];
      expect(trace.line.color).toBe("#708090");
    });

    it("disables mode bar", () => {
      silverPriceRender(container, MOCK_DATA);
      expect(mockNewPlot.mock.calls[0][3].displayModeBar).toBe(false);
    });
  });

  describe("oil_price widget", () => {
    it("calls Plotly.newPlot", () => {
      oilPriceRender(container, MOCK_DATA);
      expect(mockNewPlot).toHaveBeenCalledTimes(1);
    });

    it("sets y-axis title to USD/bbl", () => {
      oilPriceRender(container, MOCK_DATA);
      const layout = mockNewPlot.mock.calls[0][2];
      expect(layout.yaxis.title).toBe("USD/bbl");
    });

    it("uses dark grey colour", () => {
      oilPriceRender(container, MOCK_DATA);
      expect(mockNewPlot.mock.calls[0][1][0].line.color).toBe("#4a4a4a");
    });
  });

  describe("treasury_10y widget", () => {
    it("calls Plotly.newPlot", () => {
      treasury10yRender(container, MOCK_DATA);
      expect(mockNewPlot).toHaveBeenCalledTimes(1);
    });

    it("sets y-axis title to Yield (%)", () => {
      treasury10yRender(container, MOCK_DATA);
      const layout = mockNewPlot.mock.calls[0][2];
      expect(layout.yaxis.title).toBe("Yield (%)");
    });

    it("uses navy blue colour", () => {
      treasury10yRender(container, MOCK_DATA);
      expect(mockNewPlot.mock.calls[0][1][0].line.color).toBe("#1a5276");
    });
  });

  describe("dow_gold_ratio widget", () => {
    it("calls Plotly.newPlot", () => {
      dowGoldRatioRender(container, MOCK_DATA);
      expect(mockNewPlot).toHaveBeenCalledTimes(1);
    });

    it("uses purple colour for ratio line", () => {
      dowGoldRatioRender(container, MOCK_DATA);
      const trace = mockNewPlot.mock.calls[0][1][0];
      expect(trace.line.color).toBe("#7d3c98");
    });

    it("sets y-axis title to Ratio", () => {
      dowGoldRatioRender(container, MOCK_DATA);
      const layout = mockNewPlot.mock.calls[0][2];
      expect(layout.yaxis.title).toBe("Ratio");
    });
  });
});
