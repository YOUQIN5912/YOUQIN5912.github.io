(() => {
  const stage = document.querySelector('.research-map__stage');
  if (!stage) return;

  const svg = stage.querySelector('svg');
  const nodes = [...stage.querySelectorAll('[data-node]')];
  const byId = new Map(nodes.map(node => [node.dataset.node, node]));
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const compact = matchMedia('(max-width: 45rem)');
  const namespace = 'http://www.w3.org/2000/svg';
  const edges = nodes.flatMap(from => from.dataset.connects.split(' ').filter(Boolean).map(id => {
    const path = document.createElementNS(namespace, 'path');
    path.setAttribute('class', 'research-map__edge');
    svg.append(path);
    return { from, to: byId.get(id), path };
  }));
  let hovered;
  let focused;
  let active;

  function center(node, stageBox) {
    const box = node.getBoundingClientRect();
    return { x: box.left + box.width / 2 - stageBox.left, y: box.top + box.height / 2 - stageBox.top, box };
  }

  function drawEdges() {
    if (compact.matches) return;
    const stageBox = stage.getBoundingClientRect();
    edges.forEach(({ from, to, path }) => {
      const a = center(from, stageBox);
      const b = center(to, stageBox);
      const horizontally = Math.abs(a.y - b.y) < a.box.height / 2;
      if (horizontally) {
        const direction = Math.sign(b.x - a.x);
        const start = a.x + direction * (a.box.width / 2 - 1);
        const end = b.x - direction * (b.box.width / 2 + 2);
        path.setAttribute('d', `M ${start} ${a.y} L ${end} ${b.y}`);
      } else {
        const direction = Math.sign(b.y - a.y);
        const start = a.y + direction * (a.box.height / 2 - 1);
        const end = b.y - direction * (b.box.height / 2 + 2);
        const bend = (start + end) / 2;
        path.setAttribute('d', `M ${a.x} ${start} C ${a.x} ${bend} ${b.x} ${bend} ${b.x} ${end}`);
      }
    });
  }

  function updateActive() {
    if (active) {
      active.classList.remove('is-active');
      active.style.removeProperty('--map-pitch');
      active.style.removeProperty('--map-yaw');
    }
    active = hovered || focused;
    stage.toggleAttribute('data-active', Boolean(active));
    if (active) active.classList.add('is-active');

    edges.forEach(({ from, to, path }) => path.classList.toggle('is-related', active === from || active === to));
    const stageBox = stage.getBoundingClientRect();
    const selected = active && center(active, stageBox);
    nodes.forEach(node => {
      const point = center(node, stageBox);
      const separate = selected && active !== node && !compact.matches && !reducedMotion.matches;
      node.style.setProperty('--map-x', `${separate ? Math.sign(point.x - selected.x) * 5 : 0}px`);
      node.style.setProperty('--map-y', `${separate ? Math.sign(point.y - selected.y) * 5 : 0}px`);
    });
  }

  nodes.forEach(node => {
    node.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse' || !finePointer.matches) return;
      hovered = node;
      updateActive();
    });
    node.addEventListener('pointermove', event => {
      if (hovered !== node || reducedMotion.matches || compact.matches) return;
      const box = node.getBoundingClientRect();
      node.style.setProperty('--map-yaw', `${(event.clientX - box.left - box.width / 2) * 9 / box.width}deg`);
      node.style.setProperty('--map-pitch', `${-(event.clientY - box.top - box.height / 2) * 7 / box.height}deg`);
    });
    node.addEventListener('pointerleave', () => {
      if (hovered !== node) return;
      hovered = null;
      updateActive();
    });
    node.addEventListener('focus', () => { focused = node.matches(':focus-visible') ? node : null; updateActive(); });
    node.addEventListener('blur', () => { focused = null; updateActive(); });
  });

  new ResizeObserver(drawEdges).observe(stage);
  compact.addEventListener('change', updateActive);
  reducedMotion.addEventListener('change', updateActive);
  drawEdges();
})();
