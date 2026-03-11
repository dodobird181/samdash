/**
 * Dow / Gold Ratio widget plugin.
 * Renders a Plotly line chart from /api/dow-gold-ratio/ data.
 */
import { registerWidget } from "../../registry.js";

function dowGoldRatioRender(container, data) {
  const trace = {
    x: data.x,
    y: data.y,
    type: "scatter",
    mode: "lines",
    name: "Dow/Gold Ratio",
    line: { color: "#7d3c98", width: 1.5 },
  };

  const layout = {
    margin: { t: 4, r: 8, b: 40, l: 52 },
    paper_bgcolor: "#f4f6f8",
    plot_bgcolor: "#f4f6f8",
    font: { family: "Verdana, Tahoma, sans-serif", size: 9 },
    yaxis: { title: "Ratio", gridcolor: "#d0d8e0" },
    xaxis: { gridcolor: "#d0d8e0" },
    showlegend: false,
  };

  const config = { displayModeBar: false, responsive: true };
  Plotly.newPlot(container, [trace], layout, config);
}

registerWidget({ type: "dow_gold_ratio", render: dowGoldRatioRender });

export { dowGoldRatioRender };
