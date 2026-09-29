/* Apply the saved theme before CSS paints; first-time visitors see light mode. */
(() => {
  'use strict';
  const key = 'junqiao-theme';
  const root = document.documentElement;
  let button;

  function applyTheme(value) {
    const dark = value === 'dark';
    root.dataset.theme = dark ? 'dark' : 'light';
    document.querySelector('meta[name="theme-color"]').content = dark ? '#151c24' : '#ffffff';
    if (button) {
      const action = dark ? 'Switch to light mode' : 'Switch to dark mode';
      button.setAttribute('aria-label', action);
      button.title = action;
      button.querySelector('.theme-label').textContent = dark ? 'Light' : 'Dark';
    }
  }

  try { applyTheme(localStorage.getItem(key)); }
  catch { applyTheme('light'); }

  document.addEventListener('DOMContentLoaded', () => {
    button = document.getElementById('theme-toggle');
    button.hidden = false;
    applyTheme(root.dataset.theme);
    button.addEventListener('click', () => {
      const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      applyTheme(theme);
      try { localStorage.setItem(key, theme); }
      catch { /* Switching still works when browser storage is unavailable. */ }
    });
  });

  window.addEventListener('storage', (event) => {
    if (event.key === key || event.key === null) applyTheme(event.newValue);
  });
})();
