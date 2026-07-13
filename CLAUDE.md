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
- `content/_index.md` is the homepage; `content/about.md` is the About page.
- Post front matter fields come from `archetypes/default.md`: `title`, `date`,
  `draft`, `authors`, `tags`, `summary`.
