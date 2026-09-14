# CRW Blog

Jekyll blog. Posts go in `_posts/` with format `YYYY-MM-DD-Title.md`.

## Writing a post? Invoke the skill first.

**`drafting-crw-blog-posts`** is the entry point for turning CRW's notes into a post.
Invoke it before writing anything — including before asking clarifying questions. It
carries the drafting pipeline, the stub protocol, the source-binding contract, voice
specimens, and the front-matter reference, and it points here for the rest.

Do not draft from `STYLE.md` alone. STYLE.md tells you how the prose *sounds*; the skill
tells you what you are allowed to *assert*, what to stub instead of faking, and how to
mark anything LLM-sourced. Both are required.

`STYLE.md` is iteratively refined — when CRW corrects your writing during a session,
add the correction there so future sessions benefit.

## Repo mechanics

Front matter, tag→page routing, `kind:` badges, and attribution lines are documented in
the skill's `references/templates-and-frontmatter.md`, which is kept in sync with this
repo. Quick version:

```yaml
---
title: "Post Title"   # clean title, no [Prefix] tags
date: YYYY-MM-DD
math: true            # include if post has LaTeX
tags: [seed]          # optional, drives PAGE MEMBERSHIP
kind: musing          # optional, right-side badge only
---
```

`tags:` decides which page a post appears on (one per page):
`seed` -> Curated Tutorial Prompts, `personal` -> Writing, `widget` -> Widgets,
`notes` -> Notes (Claude-written working notes), `nulla-dies` -> hidden page.
Untagged posts land on the Research homepage.

The `long` and `math` badges are computed automatically by `index.md` (from word count
> 3000 and from `math: true`). Never set `long` by hand.

All LLM-assisted posts must carry an attribution line — see the skill for the range of
forms CRW actually uses.

`dev-server.sh` runs the site locally. `BACKLOG.md` is the task queue for the scheduled
tutorial routine, not for post drafting.

## Writing project plans

`~/Documents/Vault/notes/MATS/EAG-writeup-plans.md` — a one-liner, an arc, and the exact
context files to read for each planned post.

## Math in posts: use `$$...$$` everywhere, never a bare `|`

kramdown runs **before** MathJax.  It passes `$$...$$` through verbatim (emitting
`\(...\)` inline and `\[...\]` for display), but it treats single-`$` spans as ordinary
markdown text.  Two failure modes follow, and both are silent — the build succeeds and
the damage is visible only in a browser:

1. **`_` and `*` inside `$...$` become emphasis.**  In `$(H^2 g)_j - \partial_j (H^2 g)_m$`
   the underscores are consumed by an `<em>`, MathJax then cannot parse the span, and the
   raw LaTeX is printed to the page.  Same for `r_*^2`.
2. **A bare `|` inside math is read as a table cell delimiter.**  `$$|f|$$` splits the
   paragraph into `<td>` cells and the math is never rendered.  Use `\vert` and `\Vert`,
   which are typographically identical and contain no pipe.  This applies to `\|...\|`
   norms too.

So: **write all inline math as `$$...$$`**, and keep bare pipes out of math.

Two helpers do the conversion mechanically on an imported draft:

```
python3 ~/Scripts/kramdown-protect-inline-math.py <post.md>   # $...$ -> $$...$$
python3 ~/Scripts/kramdown-escape-math-pipes.py  <post.md>    # |     -> \vert
```

Verify with a real render rather than by eye.  After `bundle exec jekyll build`:

```
bash ~/Scripts/check-mathjax-render.sh _site/<Post-Slug>/index.html /tmp/mjcheck
```

It reports rendered math containers and `mjx-merror` nodes; a healthy post has many
containers and zero errors.  Also check that the `<table>` count in the built HTML equals
the number of `|---|` separator rows in the source — a mismatch means pipes in math.
