(() => {
  const panels = [...document.querySelectorAll('.diagram-panel')];
  const choices = [...document.querySelectorAll('[data-view]')];
  const theme = document.querySelector('#theme');
  const media = matchMedia('(prefers-color-scheme: dark)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const play = document.querySelector('#play');
  const step = document.querySelector('#step');
  const reset = document.querySelector('#reset');
  const status = document.querySelector('#step-status');
  const labels = ['Select or reuse methods for this task.', 'Check only changed prerequisites.', 'Execute within the approved scope.', 'Verify behavior and required reviews.', 'Record evidence, limits and next action.', 'Continue to the next approved, dependency-ready task.'];
  let current = -1;
  let timer;
  function stop() { clearInterval(timer); timer = undefined; play.textContent = 'Play'; play.setAttribute('aria-pressed', 'false'); }
  function showStep(index) {
    current = index;
    document.querySelectorAll('#task-loop [data-step]').forEach(node => node.classList.toggle('active-step', Number(node.dataset.step) === index));
    status.textContent = index < 0 ? 'Complete loop shown. Choose Play or Next step to explore.' : `Step ${index + 1} of 6 · ${labels[index]}`;
  }
  function select(name) {
    if (!panels.some(panel => panel.id === name)) name = 'ownership';
    stop(); panels.forEach(panel => { panel.hidden = panel.id !== name; });
    choices.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === name)));
  }
  function applyTheme() {
    const dark = theme.value === 'dark' || (theme.value === 'system' && media.matches);
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    document.querySelectorAll('[data-download]').forEach(link => { link.href = `diagrams/${link.dataset.download}-${dark ? 'dark' : 'light'}.svg`; });
  }
  function applyMotion() {
    stop(); play.disabled = reduced.matches;
    document.querySelector('#motion-note').textContent = reduced.matches ? 'Reduced motion is on. Use Next step; the complete diagram remains visible.' : 'Playback illustrates the method; it does not start agents or repeat automatically.';
  }
  choices.forEach(button => button.addEventListener('click', () => {
    history.replaceState(null, '', '#' + button.dataset.view);
    select(button.dataset.view);
  }));
  window.addEventListener('hashchange', () => select(location.hash.slice(1)));
  play.addEventListener('click', () => {
    if (timer) { stop(); return; }
    if (reduced.matches) return;
    if (current === 5 || current < 0) showStep(0);
    play.textContent = 'Pause'; play.setAttribute('aria-pressed', 'true');
    timer = setInterval(() => { if (current >= 5) { stop(); return; } showStep(current + 1); }, 900);
  });
  step.addEventListener('click', () => { stop(); showStep((current + 1) % labels.length); });
  reset.addEventListener('click', () => { stop(); showStep(-1); });
  theme.addEventListener('change', applyTheme); media.addEventListener('change', applyTheme); reduced.addEventListener('change', applyMotion);
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  document.querySelector('.controls').hidden = false;
  document.querySelector('.playback').hidden = false;
  applyTheme(); applyMotion(); showStep(-1); select(location.hash.slice(1));
})();
