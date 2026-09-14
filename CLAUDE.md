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
