# Site Modernization Design

**Date:** 2026-07-08
**Scope:** Visual redesign of wassupluke.github.io plus a richer homepage. The markdown → HTML pipeline (`md-to-html.py` + GitHub Actions) is unchanged in concept; only templates, styles, and content change.

## Goals

- Replace the dated dark-terminal look (Courier everywhere, neon green links, purple heading bars) with a refined, photography-forward dark design.
- Make the homepage engaging: project cards and a photo highlights strip.
- Keep the site dependency-light, fast, and maintainable through the existing converter.

## Non-goals

- No static-site-generator migration, no blog/posts system.
- CV page (`cv.md` / `cv.css`) is untouched.
- No analytics, no build-tool additions.

## Design system

**Typography**
- Body & headings: Inter (Google Fonts), fallback `system-ui, sans-serif`.
- Accents (nav labels, eyebrows, footer, code): JetBrains Mono, fallback existing mono stack.
- Headings lose the purple background bars; `h2` gets a short accent underline treatment instead (pseudo-element bar beneath the heading).

**Color**
- Background: near-black blue-gray `#0e1116` (page), slightly lighter surface `#161b22`-family for cards/nav.
- Text: soft off-white primary, muted slate secondary.
- Single accent: refined green in the `#3ddc84` family (desaturated evolution of the current `#01ff70`), used for links, active nav underline, eyebrows, focus states.

**Motion**
- Keep page fade-in. Add card hover lift and gentle image hover ease.
- All motion gated behind `prefers-reduced-motion: reduce`.

## Components

**Navbar** (`templates/navbar.html` + CSS)
- Same links and order. Sticky, translucent background with `backdrop-filter: blur`, mono uppercase labels, accent underline on hover/active. Hamburger behavior unchanged (`static/js/nav.js` stays as-is).

**Footer**
- Same content, restyled to match (muted, mono, subtle top border).

**Homepage** (`index.md`, using raw HTML blocks — same pattern as `photography.md`)
1. **Intro:** Name + one-line identity ("nurse · endurance athlete · photographer · developer") + tightened version of the current about paragraph. Text only, no photo backdrop. The YouTube embed section is removed. The "Future improvements" section is removed.
2. **"Things I've built" card grid:** Six Second STEMI, Recipe Emailer, this site, coaching via Intervals.icu. Each card: title, one-line blurb, link. Grid collapses to one column on mobile.
3. **Photo highlights strip:** 5 hand-picked shots from `images/photography/` (candidates: teton-rainbow, alaska-glacier-valley, frost-covered-trees, portland-head-light-wide, loon-wings-spread), displayed as a horizontal band linking to `photography.html`.

**Gallery lightbox** (`photography.html`)
- New dependency-free `static/js/lightbox.js`: click image to open full-size overlay; close via Esc, backdrop click, or close button; navigate with arrow keys.
- Converter tweak in `md-to-html.py`: inject the lightbox script only for `photography.md` (same special-casing pattern already used for `cv.md`).

## File changes

| File | Change |
|-|-|
| `styles/default.css` | Full rewrite implementing the design system |
| `templates/head.html` | Add Google Fonts preconnect + stylesheet links |
| `templates/navbar.html` | Markup tweaks if needed for new nav styling |
| `index.md` | Rewrite: intro, project cards, photo strip |
| `static/js/lightbox.js` | New file |
| `md-to-html.py` | Inject lightbox script on photography page |
| `default.css` (repo root) | Delete — stale unreferenced duplicate |
| Generated `.html` | Regenerated locally for verification; commit only `.md`/assets and let CI auto-commit HTML |

## Error handling / edge cases

- Fonts: `font-display: swap` and full system fallbacks so the site renders fine if Google Fonts is unreachable.
- Lightbox: pure progressive enhancement — without JS the gallery behaves exactly as today.
- Mobile: nav hamburger unchanged; card grid and photo strip stack/scroll gracefully at narrow widths.

## Testing / verification

- Run `python md-to-html.py index.md nursing.md athlete.md photography.md` and inspect each generated page in a browser (desktop + narrow viewport) for layout, nav, hover states, and lightbox behavior.
- Confirm `cv.html` output is byte-identical (no regressions from converter change).
- Check `prefers-reduced-motion` and keyboard navigation (nav links, lightbox Esc/arrows, focus visibility).
