(() => {
  const stage = document.querySelector('.research-map__stage');
  if (!stage) return;

  const nodes = [...stage.querySelectorAll('[data-node]')];
  const edges = [...stage.querySelectorAll('[data-links]')];
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  let hovered;
  let focused;
  let active;

  function updateActive() {
    if (active) {
      active.classList.remove('is-active');
      active.style.removeProperty('--map-pitch');
      active.style.removeProperty('--map-yaw');
    }
    active = hovered || focused;
    active?.classList.add('is-active');

    edges.forEach(edge => {
      edge.classList.toggle('is-related', Boolean(active && edge.dataset.links.split(' ').includes(active.dataset.node)));
    });
    const selected = active?.getBoundingClientRect();
    nodes.forEach(node => {
      const box = node.getBoundingClientRect();
      const separate = selected && active !== node && !reducedMotion.matches;
      const shiftX = separate ? Math.sign(box.left + box.width / 2 - selected.left - selected.width / 2) * 4 : 0;
      const shiftY = separate ? Math.sign(box.top + box.height / 2 - selected.top - selected.height / 2) * 4 : 0;
      node.style.setProperty('--map-x', shiftX + 'px');
      node.style.setProperty('--map-y', shiftY + 'px');
    });
  }

  nodes.forEach(node => {
    node.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse' || !finePointer.matches) return;
      hovered = node;
      updateActive();
    });
    node.addEventListener('pointermove', event => {
      if (hovered !== node || reducedMotion.matches) return;
      const box = node.getBoundingClientRect();
      node.style.setProperty('--map-yaw', ((event.clientX - box.left - box.width / 2) * 8 / box.width) + 'deg');
      node.style.setProperty('--map-pitch', (-(event.clientY - box.top - box.height / 2) * 6 / box.height) + 'deg');
    });
    node.addEventListener('pointerleave', () => {
      if (hovered !== node) return;
      hovered = null;
      updateActive();
    });
    node.addEventListener('focus', () => {
      focused = node.matches(':focus-visible') ? node : null;
      updateActive();
    });
    node.addEventListener('blur', () => { focused = null; updateActive(); });
  });

  reducedMotion.addEventListener('change', updateActive);

  const canvas = stage.querySelector('canvas');
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  // Ideal cubic ABO3: A on corners, B at the body centre, oxygen on faces.
  const basis = [
    [0, 0, 0, 0], [.5, .5, .5, 1],
    [0, .5, .5, 2], [.5, 0, .5, 2], [.5, .5, 0, 2]
  ];
  const colour = ['138,199,211', '104,170,180', '177,155,218'];

  function drawCrystal() {
    const width = stage.clientWidth;
    const height = stage.clientHeight;
    if (!width || !height) return;
    const ratio = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);

    const step = width / 10;
    const field = ctx.createRadialGradient(width * .51, height * .35, 0, width * .51, height * .35, width * .67);
    field.addColorStop(0, 'rgba(222,247,248,.46)');
    field.addColorStop(1, 'rgba(222,247,248,0)');
    ctx.fillStyle = field;
    ctx.fillRect(0, 0, width, height);

    function project(x, y, z) {
      const horizontal = x * .94 - z * .34;
      const depth = x * .34 + z * .94;
      const vertical = y * .91 - depth * .42;
      const distance = depth * .91 + y * .42;
      const scale = step * 23 / (24 + distance);
      return { x: width * .51 + horizontal * scale, y: height * .48 + vertical * scale, scale, distance };
    }

    const objects = [];
    for (let x = -12; x <= 12; x += 1) {
      for (let y = -9; y <= 9; y += 1) {
        for (let z = 0; z <= 3; z += 1) {
          for (const [dx, dy, dz, type] of basis) {
            const point = project(x + dx, y + dy, z + dz);
            if (point.x < -step || point.x > width + step || point.y < -step || point.y > height + step) continue;
            objects.push({ point, type, layer: z });
            if (type === 1) {
              const bonds = [[1, .5, .5], [0, .5, .5], [.5, 1, .5], [.5, 0, .5], [.5, .5, 1], [.5, .5, 0]];
              for (const [ox, oy, oz] of bonds) objects.push({ point, end: project(x + ox, y + oy, z + oz), layer: z });
            }
          }
        }
      }
    }
    objects.sort((a, b) => b.point.distance - a.point.distance);
    for (const { point, type, end, layer } of objects) {
      const { x, y, scale, distance } = point;
      const fade = Math.max(.12, Math.min(.65, .68 - distance * .052)) * .76 ** layer;
      if (end) {
        ctx.lineCap = 'round';
        ctx.lineWidth = scale * .033;
        ctx.strokeStyle = 'rgba(107,153,186,' + (.43 * fade) + ')';
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(end.x, end.y);
        ctx.stroke();
        ctx.lineWidth = scale * .013;
        ctx.strokeStyle = 'rgba(255,255,255,' + (.65 * fade) + ')';
        ctx.stroke();
        continue;
      }

      const radius = scale * [.115, .087, .066][type];
      const glass = ctx.createRadialGradient(x - radius * .34, y - radius * .38, 0, x, y, radius);
      glass.addColorStop(0, 'rgba(255,255,255,' + (.98 * fade) + ')');
      glass.addColorStop(.3, 'rgba(' + colour[type] + ',' + (.25 * fade) + ')');
      glass.addColorStop(.72, 'rgba(' + colour[type] + ',' + (.6 * fade) + ')');
      glass.addColorStop(.91, 'rgba(99,143,173,' + (.6 * fade) + ')');
      glass.addColorStop(1, 'rgba(249,255,255,' + (.32 * fade) + ')');
      ctx.fillStyle = glass;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  new ResizeObserver(drawCrystal).observe(stage);
})();
