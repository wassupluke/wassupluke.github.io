# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal portfolio/website hosted on GitHub Pages. Content is authored in Markdown and auto-converted to HTML.

## Build System

**Local conversion:** `python md-to-html.py <file1.md> [file2.md ...]`
- Requires: `pip install markdown`
- Converts `.md` files to `.html` with template wrapping

**CI:** GitHub Actions workflow (`.github/workflows/convert-markdown.yml`) runs `md-to-html.py` on any pushed `.md` changes and auto-commits the generated HTML. Can also be triggered manually via `workflow_dispatch`.

## Architecture

- **Content pages:** Root-level `.md` files (index, cv, meals, nursing, athlete) are the source of truth. Never edit `.html` files directly — they are generated.
- **Converter (`md-to-html.py`):** Reads markdown, converts with `markdown.extensions.tables`, wraps in an HTML template with navbar, styles, and footer.
- **CV exception:** `cv.md` gets `cv.css` and no navbar/JS injection. All other pages get `default.css`, the navbar template, and `nav.js`.
- **Templates:** `templates/navbar.html` — shared navigation bar injected into non-CV pages.
- **Styles:** `styles/default.css`, `styles/cv.css`.
- **JS:** `static/js/nav.js` — responsive hamburger nav toggle.

## Key Conventions

- To add a new page: create `newpage.md`, add a link in `templates/navbar.html`, run the converter.
- Page titles are derived from the filename (uppercased, `.md` stripped).
