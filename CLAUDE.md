# CRW Blog

Jekyll blog. Posts go in `_posts/` with format `YYYY-MM-DD-Title.md`.

## Writing Style

**Read `STYLE.md` in this directory before writing any post.** It contains CRW's voice, vocabulary, structural patterns, and a NEVER list. Follow it closely.

The style file is iteratively refined — when CRW corrects your writing during a session, update STYLE.md with the correction so future sessions benefit.

## Front Matter

Posts use YAML front matter:
```yaml
---
title: "Post Title"   # clean title, no [Prefix] tags
date: YYYY-MM-DD
math: true        # include if post has LaTeX
tags: [seed]       # optional, drives PAGE MEMBERSHIP
kind: musing       # optional, shows as a right-side badge
---
```

`tags:` decides which page a post appears on (one per page):
`seed` -> Curated Tutorial Prompts, `personal` -> Writing, `widget` -> Widgets,
`notes` -> Notes (Claude-written working notes), `nulla-dies` -> hidden page.
Untagged posts land on the Research homepage.

`kind:` is a content-type badge only (no page effect): `musing`, `poetry`,
`latin`, `linkpost`, etc.  Never put `[Prefix]` inside the title; use `kind:`.

## Attribution

All Claude-assisted posts must include attribution (e.g. "Written with Claude." or "Revised with Claude.") — see STYLE.md for details.

## EAG Writeup Plans

Current writing project plans are at `~/Documents/Vault/MATS/EAG-writeup-plans.md`. Each post has a list of context files to read before starting work.
