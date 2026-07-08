# Site Modernization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the dark-terminal look with a refined, photography-forward dark design and add project cards + a photo highlights strip to the homepage.

**Architecture:** The existing `md-to-html.py` converter and templates stay in place. We rewrite `styles/default.css` (design tokens + components), add Google Fonts to `templates/head.html`, rewrite `index.md` using raw HTML blocks (same pattern as `photography.md`), and add a progressive-enhancement lightbox injected only on the photography page.

**Tech Stack:** Plain HTML/CSS/vanilla JS, Python `markdown` converter, GitHub Pages.

## Global Constraints

- Fonts: Inter (body/headings) + JetBrains Mono (accents), Google Fonts, `display=swap`, full system fallbacks.
- Palette: bg `#0e1116`, accent `#3ddc84`, off-white text, muted slate secondary (exact tokens in Task 1 CSS).
- All motion gated behind `@media (prefers-reduced-motion: reduce)`.
- CV page: `cv.css` and converter special-casing unchanged. `cv.html` may change ONLY by the added font `<link>` lines from `templates/head.html`.
- Never hand-edit generated `.html`; regenerate via `python md-to-html.py <files>`.
- CI (`convert-markdown.yml`) only regenerates `.md` files changed in a push — template/CSS changes do NOT trigger it. Therefore Task 4 regenerates ALL pages locally and commits the generated HTML.
- No new dependencies, no build tools, no analytics.

---

### Task 1: Design system — fonts, full CSS rewrite, cleanup

**Files:**
- Modify: `templates/head.html`
- Rewrite: `styles/default.css`
- Delete: `default.css` (repo root — stale unreferenced duplicate; verify with grep first)

**Interfaces:**
- Produces CSS classes consumed by later tasks: `.tagline`, `.card-grid`, `.card`, `.card-link`, `.photo-strip`, `.strip-caption` (Task 2); `.lightbox`, `.lightbox-close`, `.lightbox-prev`, `.lightbox-next`, `.lightbox.open` (Task 3).
- Preserves classes used by existing markup/JS: `nav`, `.nav-links`, `.nav-links a.active`, `.hamburger`, `.container`, `.gallery`, `.gallery-col`, `.gallery-item`, `footer`.

- [ ] **Step 1: Confirm root `default.css` is unreferenced**

Run: `grep -rn '"default.css"\|href="default' --include='*.html' --include='*.py' /home/wassu/code/wassupluke.github.io | grep -v styles/`
Expected: no output (every reference is `styles/default.css` via `templates/head.html`). If any file references the root copy, stop and fix the reference instead of deleting.

- [ ] **Step 2: Add font links to `templates/head.html`**

Replace the entire file content with:

```html
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles/{{style}}">
    <link rel="icon" href="static/favicon.svg?v=2" type="image/svg+xml">
```

- [ ] **Step 3: Rewrite `styles/default.css`**

Replace the entire file with:

```css
/* ---------------------------------------------------------------
   wassupluke.com — refined dark, photography-forward
   --------------------------------------------------------------- */

/* Design tokens */
:root {
  --bg: #0e1116;
  --surface: #151b24;
  --surface-hover: #1a2230;
  --border: #232c39;
  --border-strong: #2f3b4c;

  --text: #e8ebf0;
  --text-secondary: #9aa5b5;
  --text-faint: #5f6b7d;

  --accent: #3ddc84;
  --accent-strong: #6ee7a8;
  --accent-soft: rgba(61, 220, 132, 0.13);

  --font-sans: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, Menlo, Monaco, "Courier New", monospace;

  --radius: 10px;
}

/* Global */
html,
body {
  background-color: var(--bg);
  min-height: 100%;
  font-family: var(--font-sans);
  font-size: 17px;
  line-height: 1.7;
  color: var(--text);
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
}

body {
  /* faint green glow bleeding down from the top — atmosphere, not decoration */
  background-image: radial-gradient(
    1100px 500px at 50% -120px,
    rgba(61, 220, 132, 0.07),
    transparent 60%
  );
  background-repeat: no-repeat;
}

::selection {
  background: var(--accent-soft);
  color: var(--accent-strong);
}

:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
  border-radius: 2px;
}

/* Navigation */
nav {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(14, 17, 22, 0.82);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}

.nav-links {
  display: flex;
  gap: 0.25rem;
}

.nav-links a {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--text-secondary);
  padding: 0.9rem 0.8rem 0.75rem;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: color 0.2s ease, border-color 0.2s ease;
}

.nav-links a:visited {
  color: var(--text-secondary);
}

.nav-links a:hover,
.nav-links a:focus-visible {
  color: var(--text);
  border-bottom-color: var(--border-strong);
}

.nav-links a.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.hamburger {
  font-size: 1.4rem;
  color: var(--text);
  background: none;
  border: none;
  cursor: pointer;
  display: none;
  padding: 0.6rem 1rem;
  margin: 0;
}

@media screen and (max-width: 48rem) {
  .hamburger {
    display: block;
  }

  .nav-links {
    display: none;
    flex-direction: column;
    width: 100%;
    background-color: rgba(14, 17, 22, 0.97);
    border-bottom: 1px solid var(--border);
    position: absolute;
    top: 100%;
    left: 0;
  }

  .nav-links.active {
    display: flex;
  }

  .nav-links a {
    padding: 0.85rem 1.25rem;
    border-bottom: none;
    border-left: 2px solid transparent;
  }

  .nav-links a.active {
    border-left-color: var(--accent);
  }
}

/* Layout */
.container {
  margin: 6.5rem auto 2rem;
  max-width: 46rem;
  padding: 0 1.5rem;
  animation: fadeUp 0.5s ease-out;
}

/* Typography */
h1,
h2,
h3,
h4 {
  line-height: 1.25;
  color: var(--text);
}

h1 {
  text-align: center;
  margin: 0 0 0.5rem;
  font-size: clamp(2.4rem, 6vw, 3.4rem);
  font-weight: 800;
  letter-spacing: -0.025em;
  word-wrap: break-word;
}

h2 {
  font-size: 1.7rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 3rem 0 1rem;
  padding-bottom: 0.6rem;
  position: relative;
}

h2::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 2.75rem;
  height: 3px;
  border-radius: 2px;
  background: var(--accent);
}

h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 2rem 0 0.5rem;
}

h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 1.5rem 0 0.5rem;
}

p {
  margin: 0 0 1.2rem;
}

small {
  font-size: 0.85em;
  color: var(--text-secondary);
}

/* Homepage hero bits */
.tagline {
  font-family: var(--font-mono);
  font-size: 0.82rem;
  letter-spacing: 0.14em;
  text-align: center;
  color: var(--text-secondary);
  margin: 0 0 2.5rem;
}

.tagline::before,
.tagline::after {
  content: "—";
  color: var(--text-faint);
  margin: 0 0.6rem;
}

/* Links */
a,
a:visited {
  color: var(--accent);
  text-decoration: underline;
  text-decoration-color: rgba(61, 220, 132, 0.35);
  text-underline-offset: 3px;
  transition: color 0.2s ease, text-decoration-color 0.2s ease;
}

a:hover,
a:focus,
a:active {
  color: var(--accent-strong);
  text-decoration-color: var(--accent-strong);
}

/* Card grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
  gap: 1rem;
  margin: 1.5rem 0 2rem;
}

a.card,
a.card:visited {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem 1.25rem 1.1rem;
  text-decoration: none;
  color: var(--text);
  transition: transform 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
}

a.card:hover,
a.card:focus-visible {
  transform: translateY(-3px);
  border-color: var(--border-strong);
  background: var(--surface-hover);
  color: var(--text);
}

.card h3 {
  margin: 0;
  font-size: 1.05rem;
}

.card p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.card-link {
  margin-top: auto;
  padding-top: 0.6rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
}

/* Photo highlights strip */
.photo-strip {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.6rem;
  margin: 1.5rem 0 0.75rem;
}

.photo-strip a {
  display: block;
  overflow: hidden;
  border-radius: 6px;
  aspect-ratio: 4 / 5;
}

.photo-strip img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.35s ease;
}

.photo-strip a:hover img,
.photo-strip a:focus-visible img {
  transform: scale(1.05);
}

@media screen and (max-width: 48rem) {
  .photo-strip {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 0.5rem;
  }

  .photo-strip a {
    flex: 0 0 60%;
    scroll-snap-align: start;
  }
}

.strip-caption {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  letter-spacing: 0.06em;
}

/* Photography gallery — breaks out of the narrow text column */
.gallery {
  display: flex;
  gap: 0.75rem;
  width: min(66rem, 100vw - 3rem);
  margin-inline: calc((100% - min(66rem, 100vw - 3rem)) / 2);
}

.gallery-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.gallery-item img {
  width: 100%;
  display: block;
  border-radius: 6px;
  transition: opacity 0.25s ease;
}

.gallery-item img:hover {
  opacity: 0.88;
}

/* Lightbox (photography page) */
.lightbox {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: none;
  align-items: center;
  justify-content: center;
  background: rgba(10, 12, 16, 0.93);
  -webkit-backdrop-filter: blur(6px);
  backdrop-filter: blur(6px);
}

.lightbox.open {
  display: flex;
  animation: fadeUp 0.2s ease-out;
}

.lightbox img {
  max-width: 92vw;
  max-height: 86vh;
  border-radius: 4px;
}

.lightbox button {
  position: absolute;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
  padding: 0.75rem;
  transition: color 0.2s ease;
}

.lightbox button:hover,
.lightbox button:focus-visible {
  color: var(--text);
}

.lightbox-close {
  top: 0.75rem;
  right: 1rem;
}

.lightbox-prev {
  left: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
}

.lightbox-next {
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
}

/* Content elements */
img,
canvas,
iframe,
video,
svg,
select,
textarea {
  max-width: 100%;
}

blockquote {
  border-left: 3px solid var(--accent);
  padding: 0.1rem 0 0.1rem 1rem;
  margin: 1.5rem 0;
  color: var(--text-secondary);
}

pre,
code {
  font-family: var(--font-mono);
  font-size: 0.88em;
}

code {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.1em 0.35em;
}

pre {
  padding: 1rem;
  line-height: 1.5;
  overflow-x: auto;
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

pre code {
  background: none;
  border: none;
  padding: 0;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.5rem 0;
  font-size: 0.92rem;
}

th,
td {
  border: 1px solid var(--border);
  padding: 0.5rem 0.75rem;
  text-align: left;
}

th {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-secondary);
}

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2.5rem 0;
}

/* Footer */
footer {
  text-align: center;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  color: var(--text-faint);
  padding: 1.5rem 1rem;
  margin-top: 3rem;
  border-top: 1px solid var(--border);
}

/* Motion */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation: none !important;
    transition: none !important;
  }
}

/* Print */
@media print {
  *,
  *:before,
  *:after {
    background: transparent !important;
    color: #000 !important;
    box-shadow: none !important;
    text-shadow: none !important;
  }

  nav,
  footer {
    display: none;
  }

  a,
  a:visited {
    text-decoration: underline;
  }

  a[href]:after {
    content: " (" attr(href) ")";
  }

  pre,
  blockquote {
    border: 1px solid #999;
    page-break-inside: avoid;
  }

  thead {
    display: table-header-group;
  }

  tr,
  img {
    page-break-inside: avoid;
  }

  img {
    max-width: 100% !important;
  }

  p,
  h2,
  h3 {
    orphans: 3;
    widows: 3;
  }

  h2,
  h3 {
    page-break-after: avoid;
  }
}
```

Note: the old `.video-embed` and body-font-size media queries are intentionally dropped (no page uses the video embed after Task 2; the new type scale is static).

- [ ] **Step 4: Delete the stale root stylesheet**

Run: `git rm default.css`

- [ ] **Step 5: Regenerate a page and eyeball the design system**

Run: `cd /home/wassu/code/wassupluke.github.io && python md-to-html.py nursing.md athlete.md && python -m http.server 8000 &` then open `http://localhost:8000/nursing.html`.
Check: fonts load (Inter body, mono nav), nav underline hover, accent h2 bars, blockquote styling, mobile hamburger at narrow width. Kill the server after.

- [ ] **Step 6: Commit**

```bash
git add templates/head.html styles/default.css default.css nursing.html athlete.html
git commit -m "Redesign: dark photography-forward design system"
```

---

### Task 2: Homepage — intro, project cards, photo highlights strip

**Files:**
- Rewrite: `index.md`

**Interfaces:**
- Consumes CSS classes from Task 1: `.tagline`, `.card-grid`, `.card`, `.card-link`, `.photo-strip`, `.strip-caption`.

- [ ] **Step 1: Rewrite `index.md`**

Replace the entire file with:

```markdown
# Luke Wass

<p class="tagline">nurse · endurance athlete · photographer · developer</p>

I live in the data-and-details end of everything I do. I'm a [nurse](nursing.html), [endurance athlete](athlete.html), [photographer](photography.html), and [developer](https://github.com/wassupluke/). When I'm not at the bedside, you'll find me racing bikes on [Zwift](https://www.zwift.com/why-zwift), coaching athletes through [Intervals.icu](https://intervals.icu/athlete/i75079/), building mid-century modern furniture, or building things like this site.

## Things I've built

<div class="card-grid">
  <a class="card" href="https://wassupluke.com/six-second-stemi" target="_blank" rel="noopener noreferrer">
    <h3>Six Second STEMI</h3>
    <p>A STEMI-recognition practice app for residents, students, and nurses who want reps reading 12-leads.</p>
    <span class="card-link">wassupluke.com/six-second-stemi</span>
  </a>
  <a class="card" href="https://wassupluke.com/recipe-emailer/" target="_blank" rel="noopener noreferrer">
    <h3>Recipe Emailer</h3>
    <p>Weekly meal planning that picks recipes and lands them in your inbox, grocery list included.</p>
    <span class="card-link">wassupluke.com/recipe-emailer</span>
  </a>
  <a class="card" href="https://intervals.icu/athlete/i75079/" target="_blank" rel="noopener noreferrer">
    <h3>Endurance Coaching</h3>
    <p>Data-driven training plans and race-performance analysis for cyclists and runners on Intervals.icu.</p>
    <span class="card-link">intervals.icu</span>
  </a>
  <a class="card" href="https://github.com/wassupluke/wassupluke.github.io" target="_blank" rel="noopener noreferrer">
    <h3>This Site</h3>
    <p>Markdown in, website out — a tiny Python pipeline that auto-builds every page with GitHub Actions.</p>
    <span class="card-link">github.com/wassupluke</span>
  </a>
</div>

## Photo highlights

<div class="photo-strip">
  <a href="photography.html"><img src="images/photography/teton-rainbow.jpg" alt="Rainbow over the Teton Range in a storm" loading="lazy"></a>
  <a href="photography.html"><img src="images/photography/alaska-glacier-valley.jpg" alt="Glacier flowing between Alaska mountain ridges" loading="lazy"></a>
  <a href="photography.html"><img src="images/photography/frost-covered-trees.jpg" alt="Frost-covered trees in winter fog" loading="lazy"></a>
  <a href="photography.html"><img src="images/photography/portland-head-light-wide.jpg" alt="Portland Head Light on a rocky coast" loading="lazy"></a>
  <a href="photography.html"><img src="images/photography/loon-wings-spread.jpg" alt="Loon spreading its wings on a lake" loading="lazy"></a>
</div>

<p class="strip-caption"><a href="photography.html">See the full gallery →</a></p>
```

- [ ] **Step 2: Regenerate and verify**

Run: `cd /home/wassu/code/wassupluke.github.io && python md-to-html.py index.md && python -m http.server 8000 &` then open `http://localhost:8000/index.html`.
Check: centered name + mono tagline, about paragraph renders as markdown (links work), 2×2 card grid on desktop / single column narrow, five-photo strip (horizontal scroll on mobile width), card hover lift. Kill the server after.
Also run: `grep -c 'class="card"' index.html` — Expected: `4`.

- [ ] **Step 3: Commit**

```bash
git add index.md index.html
git commit -m "Redesign homepage: intro, project cards, photo highlights"
```

---

### Task 3: Gallery lightbox

**Files:**
- Create: `static/js/lightbox.js`
- Modify: `md-to-html.py` (the `javascript = ...` line in `main()`)

**Interfaces:**
- Consumes: `.gallery-item img` markup in `photography.html`; `.lightbox*` CSS classes from Task 1 (overlay shown by toggling the `open` class).
- Produces: `static/js/lightbox.js`, injected only into `photography.html`.

- [ ] **Step 1: Create `static/js/lightbox.js`**

```javascript
// Dependency-free lightbox for the photography gallery.
(function () {
    const thumbs = Array.from(document.querySelectorAll('.gallery-item img'));
    if (!thumbs.length) return;

    const overlay = document.createElement('div');
    overlay.className = 'lightbox';
    overlay.innerHTML =
        '<button class="lightbox-close" aria-label="Close">&times;</button>' +
        '<button class="lightbox-prev" aria-label="Previous photo">&#8249;</button>' +
        '<img alt="">' +
        '<button class="lightbox-next" aria-label="Next photo">&#8250;</button>';
    document.body.appendChild(overlay);

    const fullImg = overlay.querySelector('img');
    let index = 0;

    function show(i) {
        index = (i + thumbs.length) % thumbs.length;
        fullImg.src = thumbs[index].src;
        fullImg.alt = thumbs[index].alt;
        overlay.classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    function close() {
        overlay.classList.remove('open');
        fullImg.removeAttribute('src');
        document.body.style.overflow = '';
    }

    thumbs.forEach((img, i) => {
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', () => show(i));
    });

    overlay.addEventListener('click', (e) => {
        if (e.target === overlay || e.target.classList.contains('lightbox-close')) close();
    });
    overlay.querySelector('.lightbox-prev').addEventListener('click', () => show(index - 1));
    overlay.querySelector('.lightbox-next').addEventListener('click', () => show(index + 1));

    document.addEventListener('keydown', (e) => {
        if (!overlay.classList.contains('open')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowLeft') show(index - 1);
        if (e.key === 'ArrowRight') show(index + 1);
    });
})();
```

- [ ] **Step 2: Inject the script for the photography page in `md-to-html.py`**

Change:

```python
    javascript = f'<script src="static/js/nav.js"></script>' if filename != "cv.md" else ""
```

to:

```python
    javascript = '<script src="static/js/nav.js"></script>' if filename != "cv.md" else ""
    if filename == "photography.md":
        javascript += '\n  <script src="static/js/lightbox.js"></script>'
```

- [ ] **Step 3: Regenerate and verify injection is photography-only**

Run: `cd /home/wassu/code/wassupluke.github.io && python md-to-html.py photography.md && grep -l 'lightbox.js' *.html`
Expected output: `photography.html` (only).

- [ ] **Step 4: Verify behavior in browser**

Run: `python -m http.server 8000 &` then open `http://localhost:8000/photography.html`.
Check: click a photo → overlay opens with full image; Esc / backdrop click / × closes; ←/→ cycle photos; page scroll locked while open. Kill the server after.

- [ ] **Step 5: Commit**

```bash
git add static/js/lightbox.js md-to-html.py photography.html
git commit -m "Add dependency-free lightbox to photography gallery"
```

---

### Task 4: Full regeneration, CV guard, final verification

**Files:**
- Regenerate: `index.html`, `nursing.html`, `athlete.html`, `photography.html`, `cv.html`

**Interfaces:**
- Consumes: everything above. Produces the final deployable site.

- [ ] **Step 1: Regenerate every page**

Run: `cd /home/wassu/code/wassupluke.github.io && python md-to-html.py index.md nursing.md athlete.md photography.md cv.md`
Expected: five "has been converted" messages, no traceback.

- [ ] **Step 2: CV guard — confirm cv.html changed only by font links**

Run: `git diff cv.html`
Expected: the ONLY changes are the three added `<link rel="preconnect"...>` / Google Fonts lines in `<head>`. Any other diff (navbar, styles, scripts) is a bug in the converter special-casing — stop and fix.

- [ ] **Step 3: Full visual pass**

Run: `python -m http.server 8000 &` and check every page at desktop and ~375px width: nav active-state per page, hamburger open/close, homepage cards + strip, gallery + lightbox, nursing/athlete content pages, cv.html unchanged visually. Also verify keyboard: Tab shows focus rings, lightbox Esc/arrows work. Kill the server after.

- [ ] **Step 4: Commit generated HTML**

```bash
git add index.html nursing.html athlete.html photography.html cv.html
git commit -m "Regenerate HTML for redesign"
```

(Committing HTML directly is required here: CI only regenerates `.md` files changed in the push, so template/CSS-driven HTML changes must be committed locally.)

- [ ] **Step 5: Push (only if user has approved pushing)**

```bash
git push
```

Note: the push touches `.md` files, so the workflow will re-run the converter on them; its output should match the committed HTML (idempotent), resulting in "No changes to commit".
