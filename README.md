# LiuCMU.github.io

Personal blog built with [Hugo](https://gohugo.io/) and the
[Paige](https://github.com/willfaught/paige) theme, deployed to GitHub Pages.

## Local development

Prerequisites (already installed on this machine): Hugo extended, Go, Dart Sass.

```sh
# Live preview with drafts at http://localhost:1313
hugo server --buildDrafts

# Production build into ./public
hugo --gc --minify
```

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
