# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal blog (Zhen Liu) built with [Hugo](https://gohugo.io/) using the
[Paige](https://github.com/willfaught/paige) theme, deployed to GitHub Pages.
Content is Markdown; there is no application code.

## Commands

```sh
# Live preview with drafts at http://localhost:6789
hugo server --buildDrafts --port 6789

# Production build into ./public
hugo --gc --minify

# New post (creates content/posts/<slug>/index.md from archetypes/default.md)
hugo new posts/my-post-title/index.md

# New comic (creates content/comics/<slug>/index.md from archetypes/comics.md)
hugo new comics/my-comic-title/index.md

# Update the theme
hugo mod get github.com/willfaught/paige@latest && hugo mod tidy
```

Prerequisites: Hugo **extended**, Go (required — Paige is consumed as a Hugo/Go
module, see `go.mod`), and Dart Sass.

## Publishing

Pushing to `main` or `master` triggers `.github/workflows/hugo.yml`, which builds
with Hugo extended and deploys to GitHub Pages. `main` is the working branch.
`/public` and `/resources/_gen/` are build output — gitignored, never edited by hand.
New posts go live only when `draft = false` (the archetype sets `draft = true`).

## Architecture notes

The theme is **not forked**. Customizations live in two places, and this is the
main thing to understand before changing site behavior:

- `hugo.toml` — site config, menu, and Paige params. Key detail:
  `color_scheme = "light"` is deliberately set so Bootstrap compiles in
  data-attribute mode (`[data-bs-theme]`), which is what makes the manual
  light/dark toggle possible. `markup.goldmark.renderer.unsafe = true` allows raw
  HTML in Markdown.
- `layouts/partials/paige/*.html` — Hugo overrides Paige's partials of the same
  name. Two hooks implement the light/dark toggle without touching the theme:
  - `head-last.html` — applies the saved/OS theme before paint (avoids flash) and
    holds a small `<style>` block for responsive content images and the homepage
    banner (`img[alt="Homepage banner"]`).
  - `site-header-last.html` — JS that injects the sun/moon toggle button into the
    nav and persists the choice in `localStorage` (`paige-theme`).

To override any other Paige template, add a file at the matching path under
`layouts/` rather than editing the module.

## Content conventions

- Posts are page bundles: `content/posts/<slug>/index.md` with co-located images
  referenced by relative path.
- Site-wide assets go in `static/` and are referenced from root (e.g.
  `/homepage_background.jpeg`).
- `content/_index.md` is the homepage; `content/about.md` is the About page
  (intentionally blank — title only).
- Post front matter fields come from `archetypes/default.md`: `title`, `date`,
  `draft`, `authors`, `tags`, `summary`. Every post **must** have full front
  matter and **no leading `# H1`** — Paige renders the title from front matter,
  so a top-level heading in the body duplicates it.
- Each post should ship a **`toc.png`** in its bundle, used as the homepage /
  Posts card thumbnail. Make it **3:2 (e.g. 1536×1024)** so it fills the card's
  image area with no letterboxing; posts without one fall back to a 📝 tile.
- `summary` is what shows as the card preview text — keep it to ~1–2 sentences.

### Comics (`content/comics/`)

A second, deliberately minimal content section — no tags, summary, authors, word
count or reading time.

- Each comic is a page bundle: `content/comics/<slug>/index.md` with the comic
  image co-located in the same folder. Front matter comes from
  `archetypes/comics.md`: `title`, `date`, `draft`, and optional `image`.
- **Image resolution** (`layouts/partials/comic-image.html`): the file named by
  front matter `image` (e.g. `image: "panel.png"`), else the **first image
  resource in the bundle**. So a bundle with one image needs no `image` field.
  A comic with no image falls back to a 🗯️ tile on its card.
- **Image sizing** (`layouts/partials/comic-sized.html`): source comics are
  often 2000px+ and multiple MB, so Hugo resizes and converts them to **WebP**
  (a modern image format, much smaller than JPEG at the same quality) — 900px
  wide for the card, 1600px for the single page. Drop in the full-resolution
  original; don't pre-shrink it. Two guards in that partial: **SVG** (a vector
  format with no pixel dimensions) is passed through, since `.Resize` can't
  process it, and an image already narrower than the target is passed through
  rather than upscaled. The guards are nested `if`s, not one `and` — `and`
  would evaluate `.Width` on an SVG and break the build.
- The Markdown **body is the explanation** — one paragraph, aim for under 125
  words, and **no leading `# H1`** (same rule as posts: the title comes from
  front matter). Do *not* embed the image in the body; `layouts/comics/single.html`
  places it between the title and the explanation.
- `content/comics/_index.md` uses a `cascade` block to disable Paige's authors /
  reading time / word count on every comic page.
- Comics are excluded from the homepage post cards and the Tags taxonomy simply
  because those queries filter on `Section` / use tags, which comics don't set.

### References / citations (see `content/posts/auth/index.md`)

- Cite in-text as superscripts: `<sup>[n](#ref-n)</sup>` (raw HTML works because
  `markup.goldmark.renderer.unsafe = true`).
- The References list uses matching anchors: `<a id="ref-n"></a>[n] ...`.
- Format entries in **ACS style**; number them in **order of first appearance**
  in the text.
- Manual numbering is deliberate (Goldmark footnotes are *not* used) so the
  "References" heading and ACS layout stay under our control.

## Homepage and post cards

- Post preview **cards** are rendered by `layouts/partials/post-cards.html`
  (context = a page collection), shared by `layouts/home.html` and
  `layouts/posts/list.html` so both pages look identical.
- Card structure: **title on top** (full width), a **middle row** of the
  `toc.png` thumbnail (~32% width, inset in a padded frame) beside the intro
  (`.Summary`), then a **meta row** at the bottom (tags · date · words · reading
  time). The whole card is a single `<a>`, so tags are rendered as **plain text**
  there (nested `<a>` would be invalid HTML); clickable tags live on the post /
  tag pages.
- Comic cards are rendered by `layouts/partials/comic-cards.html` and used by
  `layouts/comics/list.html`. Same card frame as a post card, but **title on top
  and the comic image below it — nothing else**. The image is shown whole
  (bounded by `max-width: 100%` / `max-height: 34rem`, never cropped), so any
  aspect ratio previews cleanly. An empty section renders "No comics yet."
- `layouts/comics/single.html` replaces Paige's `single.html` for comics:
  Paige's page header (title + date), then the comic at full content width
  (`.paige-comic-full`), then the Markdown body as the explanation.
- Homepage **stats** are in `layouts/partials/home-stats.html`: three tiles,
  **Posts** and **Comics** (build-time counts) and **Readers** (from
  `data/stats.json`). The grid is a fixed 3 columns at every width, with a
  `@media (max-width: 480px)` block that shrinks the tiles rather than letting
  them wrap 2 + 1. Reading time / word count are shown on cards and post pages,
  **not** as a homepage page-level figure.
- **Custom CSS lives in the `<style>` block of
  `layouts/partials/paige/head-last.html`** (cards, stats, banner, responsive
  images). Use Bootstrap CSS variables (`var(--bs-border-color)`,
  `--bs-body-bg`, `--bs-secondary-color`, `--bs-tertiary-bg`) so light and dark
  modes both work automatically.
- Nav order is set by `weight` in `hugo.toml`'s `[[menu.main]]` entries:
  Home 1 · Posts 2 · Comics 3 · About 4 · Tags 5.
- Nav: **Home** is a menu item in `hugo.toml`; breadcrumbs are disabled
  (`paige.site.disable_breadcrumbs`). The per-post table-of-contents outline is
  disabled site-wide (`paige.pages.disable_toc = true`).

## Analytics (GoatCounter)

- Site code **`zhenliu`** (`params.goatcounter` in `hugo.toml`); the tracking
  script is injected from `head-last.html` and ignores localhost.
- The deploy workflow (`.github/workflows/hugo.yml`) fetches
  `/api/v0/stats/total` with the repo secret **`GOATCOUNTER_TOKEN`** (Read
  statistics scope) and writes `data/stats.json` before each build; a daily
  `schedule` cron refreshes it without a commit.
- **GoatCounter tracks a single visitor metric only** — there is no separate
  pageviews number in its API. "Readers" = visitors. True pageviews would
  require switching analytics (e.g. Umami/Plausible).
