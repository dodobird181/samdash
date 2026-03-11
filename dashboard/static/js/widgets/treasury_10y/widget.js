/**
 * US 10Y Treasury Yield widget plugin.
 * Renders a Plotly line chart from /api/treasury-10y/ data.
 */
import { registerWidget } from "../../registry.js";

function treasury10yRender(container, data) {
  const trace = {
    x: data.x,
    y: data.y,
    type: "scatter",
    mode: "lines",
    name: "US 10Y Yield (%)",
    line: { color: "#1a5276", width: 1.5 },
  };

  const layout = {
    margin: { t: 4, r: 8, b: 40, l: 52 },
    paper_bgcolor: "#f4f6f8",
    plot_bgcolor: "#f4f6f8",
    font: { family: "Verdana, Tahoma, sans-serif", size: 9 },
    yaxis: { title: "Yield (%)", gridcolor: "#d0d8e0" },
    xaxis: { gridcolor: "#d0d8e0" },
    showlegend: false,
  };

  const config = { displayModeBar: false, responsive: true };
  Plotly.newPlot(container, [trace], layout, config);
}

registerWidget({ type: "treasury_10y", render: treasury10yRender });

export { treasury10yRender };
