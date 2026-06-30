# LiuCMU.github.io

Personal blog built with [Hugo](https://gohugo.io/) and the
[Paige](https://github.com/willfaught/paige) theme, deployed to GitHub Pages.

## Local development

Prerequisites (already installed on this machine): Hugo extended, Go, Dart Sass.

```sh
# Live preview with drafts at http://localhost:6789
hugo server --buildDrafts --port 6789

# Production build into ./public
hugo --gc --minify
```

## Light/dark mode toggle

`color_scheme = "light"` in `hugo.toml` compiles Bootstrap in data-attribute
mode. Two project hooks add a manual toggle button (the theme is not forked):

- `layouts/partials/paige/head-last.html` — applies the saved theme (or the
  visitor's OS preference on first visit) before paint, to avoid a flash.
- `layouts/partials/paige/site-header-last.html` — the sun/moon toggle button
  and its click handler; the choice is remembered in `localStorage`.

## Writing a new post

```sh
hugo new posts/my-post-title/index.md
```

Edit the new file, set `draft = false` (or remove it) when ready, then commit
and push. The GitHub Actions workflow builds and deploys automatically.

## How publishing works

- Pushing to `main`/`master` triggers `.github/workflows/hugo.yml`.
- The workflow installs Hugo + Go + Dart Sass, builds the site, and deploys to
  GitHub Pages.
- In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Updating the theme

```sh
hugo mod get github.com/willfaught/paige@latest
hugo mod tidy
```
