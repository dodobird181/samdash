/**
 * Dashboard bootstrap.
 *
 * Reads widget cells from the DOM, fetches data from each widget's
 * API endpoint, and hands off rendering to the plugin registry.
 * Also sets up auto-refresh timers.
 */
import { WidgetRegistry } from "./registry.js";
import { ShortcutSystem } from "./shortcuts.js";

const Dashboard = (() => {
  const _timers = {};

  async function _loadWidget(cell) {
    const type = cell.dataset.type;
    const endpoint = cell.dataset.endpoint;
    const body = document.getElementById(`body-${type}`);
    if (!body || !endpoint) return;

    body.innerHTML = '<div class="widget-loading">Loading...</div>';

    try {
      const res = await fetch(endpoint);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      body.innerHTML = "";
      WidgetRegistry.renderWidget(type, body, data);
    } catch (err) {
      body.innerHTML = `<div class="widget-error">Error: ${err.message}</div>`;
      console.error(`[Dashboard] Failed to load widget "${type}":`, err);
    }
  }

  function refreshWidget(type) {
    const cell = document.getElementById(`widget-${type}`);
    if (cell) _loadWidget(cell);
  }

  function _scheduleRefresh(cell) {
    const type = cell.dataset.type;
    const interval = parseInt(cell.dataset.refresh, 10) * 1000;
    if (!interval || interval <= 0) return;

    if (_timers[type]) clearInterval(_timers[type]);
    _timers[type] = setInterval(() => _loadWidget(cell), interval);
  }

  async function init() {
    const cells = Array.from(document.querySelectorAll(".widget-cell"));

    // Load all widgets in parallel
    await Promise.allSettled(cells.map(_loadWidget));

    // Schedule auto-refresh
    cells.forEach(_scheduleRefresh);

    // Boot shortcut system
    ShortcutSystem.load();
  }

  function _reset() {
    // For test isolation
  }

  function _clearTimers() {
    Object.values(_timers).forEach(clearInterval);
    Object.keys(_timers).forEach(k => delete _timers[k]);
  }

  return { init, refreshWidget, _reset, _clearTimers };
})();

if (typeof window !== "undefined") {
  window.Dashboard = Dashboard;

  // Global helpers called from inline onclick attributes in the template
  window.refreshWidget = (type) => Dashboard.refreshWidget(type);
  window.expandWidget = (type) => {
    const el = document.getElementById(`widget-${type}`);
    if (el) el.classList.toggle("expanded");
  };

  document.addEventListener("DOMContentLoaded", () => Dashboard.init());
}

export { Dashboard };
