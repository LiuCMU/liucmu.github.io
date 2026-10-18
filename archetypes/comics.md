---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
# Optional: name the image file in this bundle to use as the comic.
# Omit it and the first image resource in the bundle is used.
image: ""
---

<!-- Drop the comic image in this bundle, then replace this comment with one
     paragraph of explanation (aim for under 125 words). No H1 heading. -->
