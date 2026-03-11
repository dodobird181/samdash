/**
 * Widget Registry — plugin pattern.
 *
 * Each widget plugin calls registerWidget({ type, render }).
 * The dashboard calls renderWidget(type, container, data).
 *
 * This file must be loaded before any widget plugins.
 */

const _registryStore = {};

const WidgetRegistry = (() => {
  const _registry = _registryStore;

  /**
   * Register a widget plugin.
   * @param {{ type: string, render: (container: HTMLElement, data: any) => void }} plugin
   */
  function registerWidget(plugin) {
    if (!plugin || !plugin.type || typeof plugin.render !== "function") {
      console.error("[Registry] Invalid plugin:", plugin);
      return;
    }
    _registry[plugin.type] = plugin;
  }

  /**
   * Render a widget into a container element.
   * @param {string} type
   * @param {HTMLElement} container
   * @param {any} data
   */
  function renderWidget(type, container, data) {
    const plugin = _registry[type];
    if (!plugin) {
      container.innerHTML = `<div class="widget-error">Unknown widget type: ${type}</div>`;
      return;
    }
    try {
      plugin.render(container, data);
    } catch (err) {
      console.error(`[Registry] Error rendering widget "${type}":`, err);
      container.innerHTML = `<div class="widget-error">Render error: ${err.message}</div>`;
    }
  }

  /**
   * Check if a widget type is registered.
   * @param {string} type
   * @returns {boolean}
   */
  function hasWidget(type) {
    return Object.prototype.hasOwnProperty.call(_registry, type);
  }

  /**
   * Return a list of all registered widget type names.
   * @returns {string[]}
   */
  function listWidgets() {
    return Object.keys(_registry);
  }

  function _reset() {
    Object.keys(_registry).forEach(k => delete _registry[k]);
  }

  return { registerWidget, renderWidget, hasWidget, listWidgets, _reset };
})();

// Expose globally so widget plugins and dashboard.js can access it.
if (typeof window !== "undefined") {
  window.WidgetRegistry = WidgetRegistry;
  window.registerWidget = WidgetRegistry.registerWidget;
}

export { WidgetRegistry };
export const registerWidget = WidgetRegistry.registerWidget;
