# assets/scripts

Small maintenance scripts for the blog. These are **authoring/build-time tools**,
not site assets — Hugo only publishes files under `assets/` when they're pulled in
via `resources.Get`, so nothing here ships to the built site.

## manage_refs.py

Maintains the reference apparatus of a post that uses the repo's ACS citation
convention (in-text `<sup>` citations + a numbered `## References` list).

It prunes references that are no longer cited, renumbers the survivors 1..N in
order of first appearance, and rewrites each in-text citation superscript to link
directly to its source URL and open in a new tab
(`target="_blank" rel="noopener noreferrer"`). It reads citations in either the
authoring form `[N](#ref-N)` or the already-linkified form (`data-ref="N"`), so
it is safe to re-run after edits.

```sh
# dry run: report cited count + orphaned references
python3 assets/scripts/manage_refs.py --check content/posts/agent/index.md

# apply: prune, renumber, linkify (edits the file in place)
python3 assets/scripts/manage_refs.py content/posts/agent/index.md
```

Run it after adding/removing citations in a post. Commit the resulting `index.md`
change alongside your edits.
