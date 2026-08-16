#!/usr/bin/env python3
"""
manage_refs.py — maintain the reference apparatus of a blog post.

What it does, given a Markdown post that has a `## References` section whose
entries look like:

    <a id="ref-1"></a>[1] Author, A. Title; Venue, Year. https://url (accessed ...).

1. PRUNE  — drop any reference entry that is never cited in the body.
2. RENUMBER — renumber the surviving references 1..N in order of first
   appearance in the body (ACS convention), rewriting both the in-text
   citations and the reference list.
3. LINKIFY — rewrite each in-text citation superscript so it links directly to
   the reference's source URL and opens in a new tab:
       <sup><a href="URL" target="_blank" rel="noopener noreferrer"
              data-ref="N">N</a></sup>
   (The numbered `## References` list is kept as the full bibliography.)

It recognizes citations in EITHER form, so it is idempotent / re-runnable:
   - authoring form:  [N](#ref-N)
   - linkified form:  ... data-ref="N" ...>N</a>

Usage:
    python3 assets/scripts/manage_refs.py content/posts/agent/index.md
    python3 assets/scripts/manage_refs.py --check content/posts/<slug>/index.md
"""
import re, sys

MARKER = "\n## References\n"
ENTRY_RE = re.compile(r'<a id="ref-(\d+)"></a>\[(\d+)\]\s+(.*)')
CITE_RE  = re.compile(r'\[(\d+)\]\(#ref-\d+\)|data-ref="(\d+)"')
URL_RE   = re.compile(r'https?://[^\s)]+')

def process(path, check_only=False):
    s = open(path, encoding="utf-8").read()
    if MARKER not in s:
        raise SystemExit(f"no '## References' section in {path}")
    body, refs = s.split(MARKER, 1)

    content = {int(m.group(1)): m.group(3).strip() for m in ENTRY_RE.finditer(refs)}
    if not content:
        raise SystemExit("no reference entries parsed")

    def url_of(n):
        m = URL_RE.search(content.get(n, ""))
        return m.group(0) if m else "#"

    # citations in order of first appearance
    order, seen = [], set()
    for m in CITE_RE.finditer(body):
        n = int(m.group(1) or m.group(2))
        if n not in seen:
            seen.add(n); order.append(n)

    missing = [n for n in order if n not in content]
    if missing:
        raise SystemExit(f"cited but undefined: {missing}")
    removed = sorted(set(content) - set(order))
    newnum = {old: i + 1 for i, old in enumerate(order)}

    if check_only:
        print(f"{path}: {len(order)} cited, {len(removed)} orphaned -> {removed}")
        return

    def repl(m):
        old = int(m.group(1) or m.group(2)); nn = newnum[old]
        return (f'<a href="{url_of(old)}" target="_blank" rel="noopener noreferrer" '
                f'data-ref="{nn}">{nn}</a>')
    body2 = CITE_RE.sub(repl, body)

    entries = [f'<a id="ref-{newnum[old]}"></a>[{newnum[old]}] {content[old]}' for old in order]
    out = body2 + MARKER + "\n\n".join(entries) + "\n"
    open(path, "w", encoding="utf-8").write(out)
    print(f"{path}: kept {len(order)} refs, pruned {len(removed)} {removed}")

if __name__ == "__main__":
    args = sys.argv[1:]
    chk = "--check" in args
    files = [a for a in args if not a.startswith("--")]
    if not files:
        raise SystemExit(__doc__)
    for fpath in files:
        process(fpath, check_only=chk)
