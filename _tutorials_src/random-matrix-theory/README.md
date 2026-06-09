# A Course in Random Matrix Theory

Quarto + Observable JS tutorial.  Render with `quarto preview` or `quarto render`.

## Files

- `index.qmd` — the tutorial
- `_quarto.yml` — Quarto project config
- `custom.css` — site styling
- `references.bib` — bibliography
- `design.md`, `research.md` — design notes
- `scripts/prepare_data.py` — pre-computes the JSON data files in `data/`
- `data/*.json` — pre-computed numerical results consumed by ojs cells
- `BACKLOG.md` — work queue for the scheduled routine

## Scheduled progress

A scheduled remote agent runs twice daily, picks the topmost item from
`BACKLOG.md`, completes it, and pushes to the `auto-progress` branch.

To pull the latest agent commits: `git fetch origin auto-progress && git log origin/auto-progress`.
