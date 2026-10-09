/* Stratum — site interactions. No dependencies. */
(() => {
  "use strict";
  const doc = document.documentElement;
  doc.classList.add("js");
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { /* ignore */ } },
  };

  /* ------------------------------------------------------------------
     Header: scrolled state, mega menus, drawer
  ------------------------------------------------------------------ */
  const header = $(".site-header");
  const drawer = $(".drawer");
  const burger = $(".burger");
  // The header stays pinned; it only gains a solid background once the page scrolls.
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const y = window.scrollY;
      header.classList.toggle("is-scrolled", y > 12);
      toTop && toTop.classList.toggle("is-on", y > 900);
      ticking = false;
    });
  };

  const megaTriggers = $$("[data-mega]");
  let closeTimer;
  const closeMegas = (except) => {
    megaTriggers.forEach((t) => {
      if (t === except) return;
      t.setAttribute("aria-expanded", "false");
      $("#" + t.dataset.mega)?.classList.remove("is-open");
    });
  };
  let openedAt = 0;
  const openMega = (t) => {
    clearTimeout(closeTimer);
    if (t.getAttribute("aria-expanded") !== "true") openedAt = performance.now();
    closeMegas(t);
    t.setAttribute("aria-expanded", "true");
    const m = $("#" + t.dataset.mega);
    m.classList.add("is-open");
    if (m.classList.contains("mega--resources")) {
      const r = t.getBoundingClientRect();
      const host = header.querySelector(".container").getBoundingClientRect();
      const w = m.offsetWidth;
      let left = r.left - host.left - 40;
      left = Math.min(left, host.width - w - 20);
      m.style.left = Math.max(20, left) + "px";
    }
  };
  megaTriggers.forEach((t) => {
    const m = $("#" + t.dataset.mega);
    const item = t.closest(".nav__item");
    t.addEventListener("click", (e) => {
      e.preventDefault();
      // A hover may have just opened it; only a deliberate second click closes.
      const open = t.getAttribute("aria-expanded") === "true";
      open && performance.now() - openedAt > 450 ? closeMegas() : openMega(t);
    });
    const hoverable = window.matchMedia("(hover: hover)").matches;
    if (hoverable) {
      item.addEventListener("mouseenter", () => openMega(t));
      item.addEventListener("mouseleave", () => { closeTimer = setTimeout(() => closeMegas(), 180); });
      m.addEventListener("mouseenter", () => clearTimeout(closeTimer));
      m.addEventListener("mouseleave", () => { closeTimer = setTimeout(() => closeMegas(), 180); });
    }
  });
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".nav__item") && !e.target.closest(".mega")) closeMegas();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const open = megaTriggers.find((t) => t.getAttribute("aria-expanded") === "true");
    closeMegas();
    open?.focus();
    if (header.classList.contains("is-open")) toggleDrawer(false);
  });

  const toggleDrawer = (force) => {
    const open = force ?? !header.classList.contains("is-open");
    header.classList.toggle("is-open", open);
    drawer.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.style.overflow = open ? "hidden" : "";
    drawer.toggleAttribute("inert", !open);
  };
  burger?.addEventListener("click", () => toggleDrawer());
  drawer?.setAttribute("inert", "");
  window.addEventListener("resize", () => { if (window.innerWidth > 1060 && header.classList.contains("is-open")) toggleDrawer(false); });

  const toTop = $(".to-top");
  toTop?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" }));
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ------------------------------------------------------------------
     Topographic contour engine (value noise + marching squares)
  ------------------------------------------------------------------ */
  const hash3 = (x, y, z, s) => {
    let h = Math.imul(x, 374761393) ^ Math.imul(y, 668265263) ^ Math.imul(z, 1274126177) ^ Math.imul(s, 2246822519);
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    h ^= h >>> 16;
    return (h >>> 0) / 4294967295;
  };
  const fade = (t) => t * t * (3 - 2 * t);
  const lerp = (a, b, t) => a + (b - a) * t;
  const noise3 = (x, y, z, s) => {
    const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z);
    const xf = x - xi, yf = y - yi, zf = z - zi;
    const u = fade(xf), v = fade(yf), w = fade(zf);
    const c = (dx, dy, dz) => hash3(xi + dx, yi + dy, zi + dz, s);
    return lerp(
      lerp(lerp(c(0, 0, 0), c(1, 0, 0), u), lerp(c(0, 1, 0), c(1, 1, 0), u), v),
      lerp(lerp(c(0, 0, 1), c(1, 0, 1), u), lerp(c(0, 1, 1), c(1, 1, 1), u), v),
      w
    );
  };
  const fbm = (x, y, z, s) => noise3(x, y, z, s) * 0.62 + noise3(x * 2.03, y * 2.03, z * 1.4 + 7, s) * 0.28 + noise3(x * 4.1, y * 4.1, z * 1.8 + 3, s) * 0.1;

  const PALETTES = {
    light: { line: "rgba(16,39,32,0.12)", index: "rgba(31,90,70,0.42)", accent: "rgba(234,164,60,0.95)" },
    dark: { line: "rgba(238,240,230,0.09)", index: "rgba(167,194,163,0.35)", accent: "rgba(212,234,124,0.9)" },
    cover: { line: "rgba(238,240,230,0.16)", index: "rgba(212,234,124,0.55)", accent: "rgba(234,164,60,0.95)" },
    mist: { line: "rgba(16,39,32,0.12)", index: "rgba(31,90,70,0.35)", accent: "rgba(234,164,60,0.8)" },
  };

  class Topo {
    constructor(canvas, opts) {
      this.c = canvas;
      this.ctx = canvas.getContext("2d");
      this.o = Object.assign({ palette: "light", cell: 11, scale: 0.0026, levels: 13, speed: 0.00006, seed: 1, mouse: true, animate: true, accentLevel: 7 }, opts);
      this.pal = PALETTES[this.o.palette] || PALETTES.light;
      this.t = Math.random() * 100;
      this.m = { x: -9999, y: -9999, tx: -9999, ty: -9999, s: 0, ts: 0 };
      this.visible = true;
      this.resize();
      new ResizeObserver(() => { this.resize(); if (!this.running) this.draw(); }).observe(canvas.parentElement);
      if (this.o.mouse && !reduced && window.matchMedia("(hover: hover)").matches) {
        const host = canvas.closest("section, header, .cta, .calc__out, .notfound") || canvas.parentElement;
        host.addEventListener("pointermove", (e) => {
          const r = this.c.getBoundingClientRect();
          this.m.tx = e.clientX - r.left; this.m.ty = e.clientY - r.top; this.m.ts = 1;
          if (this.m.x < -999) { this.m.x = this.m.tx; this.m.y = this.m.ty; }
        });
        host.addEventListener("pointerleave", () => { this.m.ts = 0; });
      }
      if (this.o.animate && !reduced) {
        new IntersectionObserver(([en]) => { this.visible = en.isIntersecting; if (this.visible && !this.running) this.loop(); }, { rootMargin: "100px" }).observe(canvas);
      } else {
        this.draw();
      }
    }
    resize() {
      const r = this.c.parentElement.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      this.w = Math.max(1, r.width); this.h = Math.max(1, r.height);
      this.c.width = Math.round(this.w * dpr); this.c.height = Math.round(this.h * dpr);
      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      this.cols = Math.ceil(this.w / this.o.cell) + 1;
      this.rows = Math.ceil(this.h / this.o.cell) + 1;
      this.field = new Float32Array(this.cols * this.rows);
    }
    sample() {
      const { cols, rows, field } = this, { cell, scale, seed } = this.o, z = this.t;
      const m = this.m, r2 = 170 * 170;
      for (let j = 0; j < rows; j++) {
        for (let i = 0; i < cols; i++) {
          const x = i * cell, y = j * cell;
          let v = fbm(x * scale, y * scale, z, seed);
          if (m.s > 0.01) {
            const dx = x - m.x, dy = y - m.y;
            v += 0.22 * m.s * Math.exp(-(dx * dx + dy * dy) / r2);
          }
          field[j * cols + i] = v;
        }
      }
    }
    draw() {
      this.sample();
      const { ctx, cols, rows, field } = this, cell = this.o.cell, L = this.o.levels;
      ctx.clearRect(0, 0, this.w, this.h);
      for (let l = 0; l < L; l++) {
        const th = 0.18 + (l / (L - 1)) * 0.66;
        const isAccent = l === this.o.accentLevel;
        const isIndex = !isAccent && l % 4 === 1;
        ctx.beginPath();
        for (let j = 0; j < rows - 1; j++) {
          for (let i = 0; i < cols - 1; i++) {
            const a = field[j * cols + i], b = field[j * cols + i + 1], c = field[(j + 1) * cols + i + 1], d = field[(j + 1) * cols + i];
            let idx = 0;
            if (a > th) idx |= 8; if (b > th) idx |= 4; if (c > th) idx |= 2; if (d > th) idx |= 1;
            if (idx === 0 || idx === 15) continue;
            const x = i * cell, y = j * cell;
            const top = () => [x + cell * ((th - a) / (b - a)), y];
            const right = () => [x + cell, y + cell * ((th - b) / (c - b))];
            const bottom = () => [x + cell * ((th - d) / (c - d)), y + cell];
            const left = () => [x, y + cell * ((th - a) / (d - a))];
            const seg = (p, q) => { ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); };
            switch (idx) {
              case 1: case 14: seg(left(), bottom()); break;
              case 2: case 13: seg(bottom(), right()); break;
              case 3: case 12: seg(left(), right()); break;
              case 4: case 11: seg(top(), right()); break;
              case 5: seg(left(), top()); seg(bottom(), right()); break;
              case 6: case 9: seg(top(), bottom()); break;
              case 7: case 8: seg(left(), top()); break;
              case 10: seg(left(), bottom()); seg(top(), right()); break;
            }
          }
        }
        ctx.strokeStyle = isAccent ? this.pal.accent : isIndex ? this.pal.index : this.pal.line;
        ctx.lineWidth = isAccent ? 1.6 : isIndex ? 1.3 : 1;
        if (isAccent) ctx.setLineDash([7, 9]); else ctx.setLineDash([]);
        ctx.stroke();
      }
      ctx.setLineDash([]);
    }
    loop() {
      this.running = true;
      let last = 0;
      const frame = (now) => {
        if (!this.visible) { this.running = false; return; }
        if (now - last > 33) {
          const dt = Math.min(now - last, 60); last = now;
          this.t += this.o.speed * dt;
          const m = this.m;
          m.x += (m.tx - m.x) * 0.08; m.y += (m.ty - m.y) * 0.08; m.s += (m.ts - m.s) * 0.05;
          this.draw();
        }
        requestAnimationFrame(frame);
      };
      requestAnimationFrame(frame);
    }
  }
  $$("canvas[data-topo]").forEach((c, i) => {
    const d = c.dataset;
    new Topo(c, {
      palette: d.topo || "light",
      seed: +(d.seed || i + 1),
      animate: d.animate !== "false",
      mouse: d.mouse !== "false",
      cell: +(d.cell || 11),
      scale: +(d.scale || 0.0026),
      levels: +(d.levels || 13),
      accentLevel: d.accent ? +d.accent : 7,
    });
  });

  /* ------------------------------------------------------------------
     Reveal on scroll + word splitting
  ------------------------------------------------------------------ */
  $$("[data-split]").forEach((el) => {
    let i = 0;
    const walk = (node) => {
      [...node.childNodes].forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            const w = document.createElement("span"); w.className = "w";
            const s = document.createElement("span"); s.textContent = part; s.style.setProperty("--i", i++);
            w.appendChild(s); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== "BR") walk(n);
      });
    };
    el.setAttribute("aria-label", el.textContent.replace(/\s+/g, " ").trim());
    walk(el);
    $$(".w", el).forEach((w) => w.setAttribute("aria-hidden", "true"));
    el.classList.add("split-words");
  });
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add("in-view");
      io.unobserve(en.target);
    });
  }, { threshold: 0.14, rootMargin: "0px 0px -6% 0px" });
  $$("[data-reveal], .split-words, .meter, [data-inview]").forEach((el) => io.observe(el));
  $$("[data-stagger]").forEach((p) => {
    const step = +(p.dataset.stagger || 0.08);
    [...p.children].forEach((c, i) => { c.setAttribute("data-reveal", c.dataset.reveal || ""); c.style.setProperty("--d", (i * step).toFixed(2) + "s"); io.observe(c); });
  });

  /* ------------------------------------------------------------------
     Counters
  ------------------------------------------------------------------ */
  const fmt = (n, dec) => n.toLocaleString("en-GB", { minimumFractionDigits: dec, maximumFractionDigits: dec });
  const cio = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      cio.unobserve(en.target);
      const el = en.target, to = parseFloat(el.dataset.count), dec = +(el.dataset.decimals || 0);
      if (reduced) { el.textContent = fmt(to, dec); return; }
      const dur = 1800, t0 = performance.now();
      const tick = (now) => {
        const p = Math.min(1, (now - t0) / dur);
        const e = 1 - Math.pow(1 - p, 4);
        el.textContent = fmt(to * e, dec);
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }, { threshold: 0.5 });
  $$("[data-count]").forEach((el) => { el.textContent = "0"; cio.observe(el); });

  /* ------------------------------------------------------------------
     Tabs (WAI-ARIA)
  ------------------------------------------------------------------ */
  $$("[data-tabs]").forEach((root) => {
    const tabs = $$('[role="tab"]', root);
    const select = (tab, focus) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        const p = $("#" + t.getAttribute("aria-controls"));
        if (!p) return;
        if (on) { p.hidden = false; p.classList.remove("is-entering"); void p.offsetWidth; p.classList.add("is-entering"); }
        else p.hidden = true;
      });
      if (focus) tab.focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener("click", () => select(t));
      t.addEventListener("keydown", (e) => {
        let n = null;
        if (e.key === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === "Home") n = tabs[0];
        if (e.key === "End") n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
  });

  /* ------------------------------------------------------------------
     Carousel (quotes)
  ------------------------------------------------------------------ */
  $$("[data-carousel]").forEach((root) => {
    const slides = $$("[data-slide]", root);
    const dotsWrap = $(".dots", root);
    const dur = +(root.dataset.interval || 8000);
    root.style.setProperty("--dur", dur + "ms");
    let idx = 0, timer;
    const dots = slides.map((_, i) => {
      const b = document.createElement("button");
      b.type = "button"; b.setAttribute("aria-label", `Show testimonial ${i + 1} of ${slides.length}`);
      b.addEventListener("click", () => go(i));
      dotsWrap.appendChild(b); return b;
    });
    const go = (i) => {
      idx = (i + slides.length) % slides.length;
      slides.forEach((s, k) => {
        if (k === idx) { s.hidden = false; s.classList.remove("is-entering"); void s.offsetWidth; s.classList.add("is-entering"); }
        else s.hidden = true;
      });
      restart();
    };
    // Re-triggers the progress fill on the active dot and schedules the next slide.
    const restart = () => {
      clearTimeout(timer);
      dots.forEach((d) => d.setAttribute("aria-current", "false"));
      void dotsWrap.offsetWidth;
      dots[idx].setAttribute("aria-current", "true");
      if (!reduced && !root.classList.contains("is-paused")) timer = setTimeout(() => go(idx + 1), dur);
    };
    $("[data-prev]", root)?.addEventListener("click", () => go(idx - 1));
    $("[data-next]", root)?.addEventListener("click", () => go(idx + 1));
    root.addEventListener("mouseenter", () => { root.classList.add("is-paused"); clearTimeout(timer); });
    root.addEventListener("mouseleave", () => { root.classList.remove("is-paused"); restart(); });
    root.addEventListener("focusin", () => { root.classList.add("is-paused"); clearTimeout(timer); });
    root.addEventListener("focusout", () => { root.classList.remove("is-paused"); restart(); });
    go(0);
  });

  /* ------------------------------------------------------------------
     Scroll stepper (procurement process)
  ------------------------------------------------------------------ */
  $$("[data-stepper]").forEach((root) => {
    const steps = $$(".step", root);
    const btns = $$(".stepper__nav button", root);
    const bar = $(".stepper__progress i", root);
    const setActive = (i) => {
      steps.forEach((s, k) => s.classList.toggle("is-active", k === i));
      btns.forEach((b, k) => { b.classList.toggle("is-active", k === i); b.setAttribute("aria-current", k === i ? "step" : "false"); });
      if (bar) bar.style.width = ((i + 1) / steps.length) * 100 + "%";
    };
    const sio = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) setActive(steps.indexOf(en.target)); });
    }, { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach((s) => sio.observe(s));
    btns.forEach((b, i) => b.addEventListener("click", () => steps[i].scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" })));
    setActive(0);
  });

  /* ------------------------------------------------------------------
     Live RFP mock (hero)
  ------------------------------------------------------------------ */
  $$("[data-live-rfp]").forEach((root) => {
    const list = $(".bids", root);
    const kBids = $("[data-k=bids]", root), kAvg = $("[data-k=avg]", root), kSave = $("[data-k=save]", root);
    const pool = [
      ["Mangrove restoration", "Indonesia · Blue carbon", "AA", 31.4, "#a7c2a3"],
      ["Improved forest mgmt.", "Canada · IFM", "A", 18.9, "#d4ea7c"],
      ["Biochar facility", "Brazil · Removal", "AA", 128.0, "#f3c064"],
      ["Agroforestry", "Kenya · ARR", "A+", 24.6, "#a7c2a3"],
      ["Clean cookstoves", "Rwanda · Household", "BBB", 9.8, "#9fc4c9"],
      ["Peatland rewetting", "Scotland · Removal", "AA", 42.1, "#d4ea7c"],
      ["Native reforestation", "Panama · ARR", "AA", 36.2, "#a7c2a3"],
      ["Enhanced weathering", "India · Removal", "A", 248.0, "#f3c064"],
      ["Grassland restoration", "Uruguay · Soil", "A", 21.5, "#9fc4c9"],
    ];
    let n = 0, bids = +kBids.textContent, avg = 27.4, save = 21.4;
    const render = (b, isNew) => {
      const li = document.createElement("li");
      li.className = "bid" + (isNew ? " is-new" : "");
      li.innerHTML = `<span class="bid__ico" style="background:${b[4]}">${b[0][0]}</span><span class="bid__name">${b[0]}<span>${b[1]}</span></span><span class="bid__score">${b[2]}</span><span class="bid__price">$${b[3].toFixed(2)}</span>`;
      return li;
    };
    pool.slice(0, 4).forEach((b) => list.appendChild(render(b)));
    n = 4;
    if (reduced) return;
    let visible = true;
    new IntersectionObserver(([en]) => { visible = en.isIntersecting; }).observe(root);
    setInterval(() => {
      if (!visible || document.hidden) return;
      const b = pool[n++ % pool.length];
      const li = render(b, true);
      li.style.opacity = "0"; li.style.transform = "translateY(-8px)";
      list.prepend(li);
      requestAnimationFrame(() => { li.style.transition = "opacity .5s, transform .6s cubic-bezier(.2,.7,.1,1), background 1.6s"; li.style.opacity = "1"; li.style.transform = "none"; });
      setTimeout(() => li.classList.remove("is-new"), 1800);
      while (list.children.length > 4) list.lastElementChild.remove();
      bids += 1; avg = Math.max(18, Math.min(34, avg + (Math.random() - 0.55) * 0.8)); save = Math.max(18, Math.min(26, save + (Math.random() - 0.4) * 0.5));
      kBids.textContent = bids; kAvg.textContent = "$" + avg.toFixed(1); kSave.textContent = save.toFixed(1) + "%";
    }, 3200);
  });

  /* ------------------------------------------------------------------
     Savings calculator
  ------------------------------------------------------------------ */
  $$("[data-calc]").forEach((root) => {
    const vol = $("#calc-volume", root), price = $("#calc-price", root), yrs = $("#calc-years", root);
    const money = (v) => "$" + (v >= 1e6 ? (v / 1e6).toFixed(v >= 1e7 ? 1 : 2) + "m" : v >= 1e3 ? Math.round(v / 1e3) + "k" : Math.round(v));
    const paint = (r) => r.style.setProperty("--p", ((r.value - r.min) / (r.max - r.min)) * 100 + "%");
    const update = () => {
      [vol, price, yrs].forEach(paint);
      const v = +vol.value, p = +price.value, y = +yrs.value, rate = 0.2;
      $("[data-o=volume]", root).textContent = fmt(v, 0) + " t";
      $("[data-o=price]", root).textContent = "$" + p + "/t";
      $("[data-o=years]", root).textContent = y + (y > 1 ? " years" : " year");
      const spend = v * p, sAnnual = spend * rate;
      $("[data-o=big]", root).textContent = money(sAnnual * y);
      $("[data-o=spend]", root).textContent = money(spend) + " / yr";
      $("[data-o=annual]", root).textContent = money(sAnnual) + " / yr";
      $("[data-o=total]", root).textContent = money(spend * (1 - rate) * y);
    };
    [vol, price, yrs].forEach((r) => r.addEventListener("input", update));
    update();
  });

  /* ------------------------------------------------------------------
     Price benchmark chart (illustrative data)
  ------------------------------------------------------------------ */
  $$("[data-chart]").forEach((root) => {
    const svgNS = "http://www.w3.org/2000/svg";
    const W = 880, H = 360, P = { l: 44, r: 16, t: 16, b: 34 };
    const months = [];
    for (let y = 2023; y <= 2026; y++) for (let m = 0; m < 12; m++) { if (y === 2026 && m > 8) break; months.push([y, m]); }
    const M = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const rnd = (s) => () => (s = (s * 16807) % 2147483647) / 2147483647;
    const mk = (start, drift, vol, seed) => { const r = rnd(seed); let v = start; return months.map((_, i) => (v = Math.max(2, v + drift + (r() - 0.5) * vol + Math.sin(i / 5) * vol * 0.1))); };
    const series = [
      { k: "Nature-based removals", c: "#1f5a46", d: mk(17, 0.32, 1.6, 11) },
      { k: "Avoided deforestation", c: "#eaa43c", d: mk(9.5, -0.03, 1.1, 23) },
      { k: "Cookstoves", c: "#6aa0a8", d: mk(6.2, 0.04, 0.6, 37) },
      { k: "Renewable energy", c: "#a7c2a3", d: mk(3.1, -0.02, 0.35, 51) },
    ];
    const max = Math.ceil(Math.max(...series.flatMap((s) => s.d)) / 10) * 10;
    const x = (i) => P.l + (i / (months.length - 1)) * (W - P.l - P.r);
    const y = (v) => H - P.b - (v / max) * (H - P.t - P.b);
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", "Illustrative line chart of average carbon credit prices by project type, 2023 to 2026");
    let g = "";
    for (let v = 0; v <= max; v += max / 5) g += `<line class="grid-line" x1="${P.l}" x2="${W - P.r}" y1="${y(v)}" y2="${y(v)}"/><text class="axis-label" x="${P.l - 10}" y="${y(v) + 4}" text-anchor="end">$${v}</text>`;
    months.forEach(([yr, m], i) => { if (m === 0) g += `<text class="axis-label" x="${x(i)}" y="${H - 10}" text-anchor="middle">${yr}</text>`; });
    let defs = "<defs>";
    series.forEach((s, si) => { defs += `<linearGradient id="g${si}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="${s.c}" stop-opacity=".18"/><stop offset="1" stop-color="${s.c}" stop-opacity="0"/></linearGradient>`; });
    defs += "</defs>";
    let paths = "";
    series.forEach((s, si) => {
      const pts = s.d.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`);
      paths += `<path class="area" data-s="${si}" d="M${pts[0]} L${pts.join(" L")} L${x(s.d.length - 1)},${y(0)} L${x(0)},${y(0)} Z" fill="url(#g${si})"/>`;
      paths += `<path class="series" data-s="${si}" d="M${pts.join(" L")}" stroke="${s.c}"/>`;
    });
    svg.innerHTML = defs + g + paths + `<line class="cursor-line" y1="${P.t}" y2="${H - P.b}" x1="-10" x2="-10"/>` + series.map((s, si) => `<circle class="dot" data-s="${si}" r="5" fill="${s.c}" cx="-10" cy="-10"/>`).join("");
    const box = $(".chart", root);
    box.appendChild(svg);
    const tip = document.createElement("div"); tip.className = "chart-tip"; box.appendChild(tip);
    // draw-in animation
    $$(".series", svg).forEach((p) => {
      const len = p.getTotalLength(); p.style.strokeDasharray = len; p.style.strokeDashoffset = reduced ? 0 : len;
    });
    new IntersectionObserver(([en], ob) => {
      if (!en.isIntersecting) return; ob.disconnect();
      $$(".series", svg).forEach((p, i) => { p.style.transition = `stroke-dashoffset 2.2s ${i * 0.15}s cubic-bezier(.2,.7,.1,1)`; p.style.strokeDashoffset = 0; });
    }, { threshold: 0.3 }).observe(svg);
    const on = series.map(() => true);
    $$(".legend-btn", root).forEach((b, i) => {
      b.addEventListener("click", () => {
        if (on.filter(Boolean).length === 1 && on[i]) return;
        on[i] = !on[i]; b.setAttribute("aria-pressed", String(on[i]));
        $$(`[data-s="${i}"]`, svg).forEach((el) => el.classList.toggle("is-off", !on[i]));
      });
    });
    const cursor = $(".cursor-line", svg);
    const move = (clientX) => {
      const r = svg.getBoundingClientRect();
      const sx = ((clientX - r.left) / r.width) * W;
      const i = Math.max(0, Math.min(months.length - 1, Math.round(((sx - P.l) / (W - P.l - P.r)) * (months.length - 1))));
      cursor.setAttribute("x1", x(i)); cursor.setAttribute("x2", x(i));
      $$(".dot", svg).forEach((d, si) => { d.setAttribute("cx", x(i)); d.setAttribute("cy", y(series[si].d[i])); });
      tip.innerHTML = `<b>${M[months[i][1]]} ${months[i][0]}</b>` + series.map((s, si) => on[si] ? `<div><span><i style="--c:${s.c}"></i>${s.k}</span><strong>$${s.d[i].toFixed(2)}</strong></div>` : "").join("");
      const px = (x(i) / W) * r.width;
      tip.style.left = Math.min(r.width - tip.offsetWidth, Math.max(0, px + (px > r.width / 2 ? -tip.offsetWidth - 16 : 16))) + "px";
      tip.style.top = "10px";
      tip.classList.add("is-on");
    };
    svg.addEventListener("pointermove", (e) => move(e.clientX));
    svg.addEventListener("pointerleave", () => { tip.classList.remove("is-on"); cursor.setAttribute("x1", -10); cursor.setAttribute("x2", -10); $$(".dot", svg).forEach((d) => d.setAttribute("cx", -10)); });
  });

  /* ------------------------------------------------------------------
     Insights filter + search
  ------------------------------------------------------------------ */
  $$("[data-filter]").forEach((root) => {
    const chips = $$(".chip", root);
    const input = $("input[type=search]", root);
    const items = $$("[data-cat]", root);
    const empty = $(".empty", root);
    const count = $("[data-count-out]", root);
    let cat = "all";
    const apply = () => {
      const q = (input?.value || "").trim().toLowerCase();
      let shown = 0;
      items.forEach((it) => {
        const ok = (cat === "all" || it.dataset.cat === cat) && (!q || it.textContent.toLowerCase().includes(q));
        it.hidden = !ok; if (ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      if (count) count.textContent = `${shown} ${shown === 1 ? "result" : "results"}`;
    };
    chips.forEach((c) => c.addEventListener("click", () => {
      cat = c.dataset.value; chips.forEach((x) => x.setAttribute("aria-pressed", String(x === c))); apply();
    }));
    input?.addEventListener("input", apply);
    const pre = new URLSearchParams(location.search).get("type");
    if (pre) { const c = chips.find((x) => x.dataset.value === pre); c?.click(); }
    apply();
  });

  /* ------------------------------------------------------------------
     Forms
  ------------------------------------------------------------------ */
  const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  $$("form[data-form]").forEach((form) => {
    const validate = (field) => {
      const wrap = field.closest(".field");
      if (!wrap) { const v = field.checkValidity(); field.setAttribute("aria-invalid", String(!v)); return v; }
      let ok = field.checkValidity();
      if (ok && field.type === "email") ok = EMAIL.test(field.value.trim());
      wrap.classList.toggle("has-error", !ok);
      field.setAttribute("aria-invalid", String(!ok));
      return ok;
    };
    $$("input, select, textarea", form).forEach((f) => {
      f.addEventListener("blur", () => { if (f.value) validate(f); });
      f.addEventListener("input", () => { if (f.closest(".field")?.classList.contains("has-error")) validate(f); });
    });
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fields = $$("input[required], select[required], textarea[required]", form);
      const bad = fields.filter((f) => !validate(f));
      if (bad.length) { bad[0].focus(); return; }
      const btn = $("button[type=submit]", form);
      const label = btn.innerHTML;
      btn.disabled = true; btn.innerHTML = "Sending…";
      await new Promise((r) => setTimeout(r, 900));
      form.classList.add("is-sent");
      btn.disabled = false; btn.innerHTML = label;
      $(".form__success", form)?.focus();
    });
    $("[data-reset]", form)?.addEventListener("click", () => { form.reset(); form.classList.remove("is-sent"); });
  });
  $$("form[data-newsletter]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const input = $("input", form), msg = form.parentElement.querySelector(".newsletter-msg");
      if (!EMAIL.test(input.value.trim())) { msg.textContent = "Please enter a valid work email."; input.focus(); return; }
      msg.textContent = "Thanks — you're on the list. First edition lands next Tuesday.";
      form.reset();
    });
  });
  // Preselect contact role via ?role=
  const role = new URLSearchParams(location.search).get("role");
  if (role) { const r = $(`input[name=role][value="${role}"]`); if (r) r.checked = true; }

  /* ------------------------------------------------------------------
     Parallax images (subtle)
  ------------------------------------------------------------------ */
  const par = $$("[data-parallax]");
  if (par.length && !reduced) {
    const tickP = () => {
      const vh = window.innerHeight;
      par.forEach((el) => {
        const r = el.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        const p = (r.top + r.height / 2 - vh / 2) / vh;
        el.style.transform = `translate3d(0, ${(p * -40 * (+el.dataset.parallax || 1)).toFixed(1)}px, 0) scale(1.1)`;
      });
    };
    window.addEventListener("scroll", () => requestAnimationFrame(tickP), { passive: true });
    tickP();
  }

  /* ------------------------------------------------------------------
     Cookie banner
  ------------------------------------------------------------------ */
  const cookie = $(".cookie");
  if (cookie && !store.get("ab-consent")) {
    setTimeout(() => cookie.classList.add("is-on"), 1400);
    $$("[data-consent]", cookie).forEach((b) => b.addEventListener("click", () => {
      store.set("ab-consent", b.dataset.consent);
      cookie.classList.remove("is-on");
    }));
  }

  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
