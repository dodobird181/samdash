/**
 * Keyboard Shortcut System.
 *
 * Loads shortcut definitions from /api/shortcuts/ and registers
 * them as keydown listeners. All configuration is server-driven —
 * no shortcuts are hardcoded here.
 */

const ShortcutSystem = (() => {
  let _shortcuts = [];
  let _focusedIndex = 0;

  const _widgetCells = () =>
    Array.from(document.querySelectorAll(".widget-cell"));

  function _focusWidget(type) {
    const el = document.getElementById(`widget-${type}`);
    if (!el) return;
    _widgetCells().forEach(w => w.classList.remove("focused"));
    el.classList.add("focused");
    el.scrollIntoView?.({ behavior: "smooth", block: "nearest" });
  }

  function _expandWidget(type) {
    const el = document.getElementById(`widget-${type}`);
    if (!el) return;
    el.classList.toggle("expanded");
  }

  function _refreshWidget(type) {
    if (window.Dashboard && window.Dashboard.refreshWidget) {
      window.Dashboard.refreshWidget(type);
    }
  }

  function _nextWidget() {
    const cells = _widgetCells();
    if (!cells.length) return;
    _focusedIndex = (_focusedIndex + 1) % cells.length;
    cells.forEach(w => w.classList.remove("focused"));
    cells[_focusedIndex].classList.add("focused");
    cells[_focusedIndex].scrollIntoView?.({ behavior: "smooth", block: "nearest" });
  }

  function _previousWidget() {
    const cells = _widgetCells();
    if (!cells.length) return;
    _focusedIndex = (_focusedIndex - 1 + cells.length) % cells.length;
    cells.forEach(w => w.classList.remove("focused"));
    cells[_focusedIndex].classList.add("focused");
    cells[_focusedIndex].scrollIntoView?.({ behavior: "smooth", block: "nearest" });
  }

  const _actions = {
    focus_widget: (s) => _focusWidget(s.target_widget),
    expand_widget: (s) => _expandWidget(s.target_widget),
    refresh_widget: (s) => _refreshWidget(s.target_widget),
    next_widget: () => _nextWidget(),
    previous_widget: () => _previousWidget(),
  };

  function _handleKey(event) {
    // Don't fire shortcuts when typing in inputs
    if (["INPUT", "TEXTAREA", "SELECT"].includes(event.target.tagName)) return;

    const match = _shortcuts.find(s => s.key === event.key);
    if (!match) return;

    const action = _actions[match.action_type];
    if (action) {
      event.preventDefault();
      action(match);
    }
  }

  async function load() {
    try {
      const res = await fetch("/api/shortcuts/");
      if (!res.ok) return;
      _shortcuts = await res.json();
      document.addEventListener("keydown", _handleKey);
      console.log(`[Shortcuts] Loaded ${_shortcuts.length} shortcuts.`);
    } catch (err) {
      console.warn("[Shortcuts] Failed to load:", err);
    }
  }

  function _reset() {
    _shortcuts = [];
    _focusedIndex = 0;
    document.removeEventListener("keydown", _handleKey);
  }

  return { load, _reset };
})();

if (typeof window !== "undefined") {
  window.ShortcutSystem = ShortcutSystem;
}

export { ShortcutSystem };
