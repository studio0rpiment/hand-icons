import json
import pathlib
REPO = pathlib.Path(__file__).resolve().parent.parent
LIB = str(REPO / "build" / "lib")
sprite = open(f"{LIB}/hand-icons.svg").read()
manifest = open(f"{LIB}/hand-icons.json").read()

page = r'''<title>Hand Icons</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* layout: sticky toolbar (filters) over a grid of icon cards; each card = one icon with its direction siblings */
:root {
  --paper: #f3f3f0; --paper-2: #e9e9e4; --ink: #17181a; --ink-2: #5d5f63; --rule: #cfd0ca;
  --accent: #1f4fd8; --accent-fg: #ffffff; --chip: #ffffff;
  --sans: "Public Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --preview-bg: #ffffff; --preview-fg: #17181a;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #1b1c1e; --paper-2: #242527; --ink: #ececea; --ink-2: #a3a39e; --rule: #3a3b3e;
  --accent: #7ea0ff; --accent-fg: #0d1326; --chip: #2a2b2e; --preview-bg: #0f1012; --preview-fg: #f2f2ef; color-scheme: dark } }
:root[data-theme="dark"] {
  --paper: #1b1c1e; --paper-2: #242527; --ink: #ececea; --ink-2: #a3a39e; --rule: #3a3b3e;
  --accent: #7ea0ff; --accent-fg: #0d1326; --chip: #2a2b2e; --preview-bg: #0f1012; --preview-fg: #f2f2ef; color-scheme: dark }
:root[data-preview="dark"] { --preview-bg: #0f1012; --preview-fg: #f2f2ef; }
:root[data-preview="light"] { --preview-bg: #ffffff; --preview-fg: #17181a; }

* { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink); font: 400 0.95rem/1.5 var(--sans);
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--paper); }
header { padding-block: 1.5rem 0.75rem; display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.5rem 1.25rem; }
h1 { font-size: 1.35rem; font-weight: 600; margin: 0; letter-spacing: -0.01em; }
header p { margin: 0; color: var(--ink-2); font-size: 0.85rem; }
.hi { display: inline-block; width: 1em; height: 1em; vertical-align: -0.125em; color: inherit; flex: none; }

.bar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--paper); border-bottom: 1px solid var(--rule);
  display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; align-items: center; padding-block: 0.6rem; }
.seg { display: inline-flex; border: 1px solid var(--rule); border-radius: 0.4rem; overflow: hidden; background: var(--chip); }
.seg button { appearance: none; border: 0; background: transparent; color: var(--ink-2); font: 500 0.8rem/1 var(--sans); padding: 0.5rem 0.7rem; cursor: pointer; letter-spacing: 0.02em; text-transform: uppercase; }
.seg button[aria-pressed="true"] { background: var(--accent); color: var(--accent-fg); }
.seg button:focus-visible, .card:focus-visible, input:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
input[type=search] { font: inherit; padding: 0.45rem 0.6rem; border: 1px solid var(--rule); border-radius: 0.4rem; background: var(--chip); color: var(--ink); min-width: 0; width: 11rem; }
.spacer { flex: 1; }
.count { color: var(--ink-2); font-size: 0.8rem; font-variant-numeric: tabular-nums; }

main { padding-block: 1rem 3rem; display: grid; gap: 2rem; }
section h2 { font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-2); margin: 0 0 0.75rem; display: flex; gap: 0.6rem; align-items: baseline; }
section h2 small { font-weight: 400; letter-spacing: 0; text-transform: none; font-variant-numeric: tabular-nums; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(17rem, 1fr)); gap: 0.75rem; }
.card { background: var(--preview-bg); color: var(--preview-fg); border: 1px solid var(--rule); border-radius: 0.5rem; padding: 0.75rem; display: grid; gap: 0.5rem; text-align: left; cursor: default; }
.card .row { display: flex; gap: 0.25rem; }
.card .tile { flex: 1; aspect-ratio: 1; max-width: 100%; display: grid; place-items: center; border-radius: 0.35rem; border: 1px solid transparent; background: transparent; color: inherit; cursor: pointer; padding: 0; position: relative; }
.card .tile:hover, .card .tile[aria-pressed="true"] { border-color: var(--accent); }
.card .tile .hi { font-size: 3.2rem; }
.card .tile small { position: absolute; left: 0.3rem; bottom: 0.15rem; font: 400 0.6rem/1 var(--mono); opacity: 0.55; }
.card .meta { display: flex; justify-content: space-between; align-items: baseline; gap: 0.5rem; font-size: 0.8rem; }
.card .meta .num { font-family: var(--mono); opacity: 0.6; }
.card .meta .name { font-weight: 500; }
.card .id { font: 400 0.7rem/1.4 var(--mono); opacity: 0.7; overflow-wrap: anywhere; min-width: 0; }

.toast { position: fixed; left: 50%; bottom: calc(1rem + env(safe-area-inset-bottom, 0px)); transform: translateX(-50%); background: var(--ink); color: var(--paper); font: 500 0.8rem/1 var(--mono); padding: 0.6rem 0.9rem; border-radius: 0.4rem; opacity: 0; transition: opacity 0.15s; pointer-events: none; max-width: calc(100vw - 2rem); overflow-wrap: anywhere; }
.toast.show { opacity: 1; }
.panel { background: var(--paper-2); border: 1px solid var(--rule); border-radius: 0.5rem; padding: 0.9rem 1rem; display: grid; gap: 0.5rem; font-size: 0.85rem; }
.panel code, .panel pre { font-family: var(--mono); font-size: 0.78rem; }
.panel pre { margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; }
.panel .k { color: var(--ink-2); }
@media (prefers-reduced-motion: reduce) { .toast { transition: none; } }
</style>
''' + sprite + r'''
<header>
  <h1>Hand Icons</h1>
  <p>29 marker drawings as one SVG sprite · line &amp; fill · rotated siblings · <code>currentColor</code>. Click a tile to copy its snippet.</p>
</header>
<div class="bar">
  <div class="seg" role="group" aria-label="Variant">
    <button id="v-line" aria-pressed="true" data-variant="line">line</button>
    <button id="v-fill" aria-pressed="false" data-variant="fill">fill</button>
  </div>
  <div class="seg" role="group" aria-label="Preview background">
    <button id="p-light" aria-pressed="true" data-preview="light">on light</button>
    <button id="p-dark" aria-pressed="false" data-preview="dark">on dark</button>
  </div>
  <div class="seg" role="group" aria-label="Snippet format">
    <button id="f-html" aria-pressed="true" data-format="html">html</button>
    <button id="f-react" aria-pressed="false" data-format="react">react</button>
    <button id="f-id" aria-pressed="false" data-format="id">id</button>
  </div>
  <input id="q" type="search" placeholder="search name or kind" aria-label="Search icons">
  <span class="spacer"></span>
  <span class="count" id="count"></span>
</div>
<main id="main"></main>
<div class="toast" id="toast" role="status"></div>
<script>
const M = ''' + manifest + r''';
const root = document.documentElement;
const state = { variant: "line", preview: "light", format: "html", q: "" };
try { Object.assign(state, JSON.parse(localStorage.getItem("hi-cat") || "{}")); } catch (e) {}
const save = () => { try { localStorage.setItem("hi-cat", JSON.stringify(state)); } catch (e) {} };

function symId(icon, dir) { return `hi-${icon.name}-${state.variant}${dir === "base" ? "" : "-" + dir}`; }
function snippet(icon, dir) {
  const id = symId(icon, dir);
  if (state.format === "id") return id;
  if (state.format === "react") return `<Icon name="${icon.name}" variant="${state.variant}"${dir === "base" ? "" : ` direction="${dir}"`} />`;
  return `<svg class="hi"><use href="#${id}"/></svg>`;
}

function render() {
  root.dataset.preview = state.preview;
  for (const b of document.querySelectorAll("[data-variant]")) b.setAttribute("aria-pressed", b.dataset.variant === state.variant);
  for (const b of document.querySelectorAll("[data-preview]")) b.setAttribute("aria-pressed", b.dataset.preview === state.preview);
  for (const b of document.querySelectorAll("[data-format]")) b.setAttribute("aria-pressed", b.dataset.format === state.format);
  const q = state.q.trim().toLowerCase();
  const main = document.getElementById("main");
  main.textContent = "";
  let shown = 0;
  for (const kind of M.kinds) {
    const icons = M.icons.filter(i => i.kind === kind && (!q || i.name.includes(q) || i.kind.includes(q) || String(i.number).padStart(2, "0").includes(q)));
    if (!icons.length) continue;
    const sec = document.createElement("section");
    const h = document.createElement("h2"); h.textContent = kind; const sm = document.createElement("small"); sm.textContent = icons.length; h.append(sm);
    const grid = document.createElement("div"); grid.className = "grid";
    for (const icon of icons) {
      shown++;
      const card = document.createElement("div"); card.className = "card";
      const row = document.createElement("div"); row.className = "row";
      for (const dir of icon.directions) {
        const t = document.createElement("button"); t.className = "tile"; t.type = "button";
        t.title = `copy ${symId(icon, dir)}`; t.setAttribute("aria-label", `${icon.name} ${dir}`);
        t.innerHTML = `<svg class="hi" aria-hidden="true"><use href="#${symId(icon, dir)}"/></svg>` + (dir === "base" ? "" : `<small>${dir}</small>`);
        t.addEventListener("click", () => copy(snippet(icon, dir), t));
        row.append(t);
      }
      const meta = document.createElement("div"); meta.className = "meta";
      meta.innerHTML = `<span class="name">${icon.name}</span><span class="num">${String(icon.number).padStart(2, "0")}</span>`;
      const id = document.createElement("div"); id.className = "id"; id.textContent = snippet(icon, "base");
      card.append(row, meta, id);
      grid.append(card);
    }
    sec.append(h, grid); main.append(sec);
  }
  document.getElementById("count").textContent = `${shown} of ${M.icons.length}`;
  if (!shown) { const p = document.createElement("p"); p.className = "count"; p.textContent = "No icon matches that search."; main.append(p); }
}

let toastT;
function copy(text, el) {
  const done = () => {
    const t = document.getElementById("toast"); t.textContent = "copied  " + text; t.classList.add("show");
    clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("show"), 1600);
    document.querySelectorAll(".tile[aria-pressed]").forEach(x => x.removeAttribute("aria-pressed")); el.setAttribute("aria-pressed", "true");
  };
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done).catch(() => fallback(text, done));
  else fallback(text, done);
}
function fallback(text, done) {
  const ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
  document.body.append(ta); ta.select(); try { document.execCommand("copy"); } catch (e) {} ta.remove(); done();
}

document.querySelector(".bar").addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  for (const k of ["variant", "preview", "format"]) if (b.dataset[k]) state[k] = b.dataset[k];
  save(); render();
});
const qEl = document.getElementById("q"); qEl.value = state.q;
qEl.addEventListener("input", () => { state.q = qEl.value; save(); render(); });
render();
</script>
'''
open(f"{LIB}/catalog.html", "w").write(page)
# standalone document for GitHub Pages (the artifact publisher adds its own skeleton; Pages needs ours)
import re
head = re.findall(r'<title>.*?</title>|<link rel="stylesheet"[^>]*>', page)
body = page
for b in head: body = body.replace(b, "", 1)
body = body.replace('<meta name="claude:viewport-fit-sides" content="cover">', "", 1)
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + "\n".join(head) + '\n</head>\n<body>\n' + body.strip() + '\n</body>\n</html>\n')
open(f"{LIB}/catalog-standalone.html", "w").write(doc)
print("catalog", len(page) // 1024, "KB")
