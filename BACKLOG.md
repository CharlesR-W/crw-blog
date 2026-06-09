# Backlog

Master task queue for the scheduled routine.  The routine reads this file, picks the **first unchecked item under "Open"**, completes it, moves the entry to "Done" with a date, builds the affected tutorial, commits, and pushes to `auto-progress`.

Add new tasks at the bottom of "Open".  Be specific about what tutorial each task targets.

## Convention

Each open task starts with a `[tag]` indicating the tutorial slug (or `[meta]` for repo-wide work):

- `[rmt]` -> work in `_tutorials_src/random-matrix-theory/`
- `[free-probability]` -> create or extend `_tutorials_src/free-probability/`
- `[meta]` -> repo-level changes

Source material for each tutorial is in `seeds/blog-posts/` (one post per topic) or `seeds/turbulence/` (the 7 chapters).  When creating a new tutorial from a seed, set up a fresh Quarto project at `_tutorials_src/<slug>/` mirroring the structure of `random-matrix-theory/`: `index.qmd`, `_quarto.yml`, `data/` for pre-computed JSON, `scripts/prepare_data.py` if interactive widgets need data, `references.bib`.

## Open

### Tier 1: high-momentum continuation

- [ ] `[rmt]` Verify all derivations in §3-§5.  Re-derive the saddle-point equation for the semicircle, the Stieltjes inversion, and the Marchenko-Pastur self-consistent equation.  If any step has a gap or sign error, fix it and add a one-line callout-warning noting the subtle point.

- [ ] `[rmt]` Add three new exercises with solutions: one in §3 (log-gas energy at the saddle), one in §6 (Wigner surmise from a 2x2 GOE), one in §7 (BBP transition critical value).

- [ ] `[rmt]` Add orthogonal-polynomial section.  Hermite polynomials for GUE, Laguerre for Wishart.  Insert as new §6 (between Marchenko-Pastur and Universality).  ~250 words plus a static figure showing first few Hermite polynomials evaluated near the spectral edge.

- [ ] `[rmt]` Add Tracy-Widom asymptotics callout.  Right tail decays like exp(-c xi^{3/2}), left tail like exp(-c |xi|^3).  Currently §7 only shows the histogram; add a callout-note with the asymptotic formulas and why they differ.

- [ ] `[rmt]` Polish §8 (When to reach for RMT).  Expand "Hessians of trained networks" with the concrete bulk + outliers picture, and add one citation each.

- [ ] `[rmt]` Add references.bib entries.  Mehta (2004), Tao (2012 lectures), Pennington & Worah (2017).

### Tier 2: convert seed posts to interactive Quarto tutorials

For each task: read the seed post in `seeds/blog-posts/<file>.md`, set up `_tutorials_src/<slug>/`, write `index.qmd` that expands the seed into a full interactive tutorial with at least 2 Observable widgets, pre-compute any data via `scripts/prepare_data.py`, run `bash build.sh <slug>` from repo root, verify it renders, commit.

- [ ] `[free-probability]` From `seeds/blog-posts/2026-01-21-Free-Probability.md`.  Slug: `free-probability`.  Widgets: free additive convolution of two semicircle distributions; large-N limit of independent random matrix products.

- [ ] `[extreme-value-theory]` From `seeds/blog-posts/2026-01-21-Extreme-Value-Theory.md`.  Slug: `extreme-value-theory`.  Widgets: GEV density vs xi parameter (Gumbel/Frechet/Weibull); empirical max convergence to GEV.

- [ ] `[wkb]` From `seeds/blog-posts/2026-01-21-WKB-and-Matched-Asymptotics.md`.  Slug: `wkb-matched-asymptotics`.  Widgets: WKB wavefunction near a turning point with Airy matching; boundary-layer thickness vs epsilon.

- [ ] `[principal-symbols]` From `seeds/blog-posts/2026-01-21-Principal-Symbols-and-Singularity-Propagation.md`.  Slug: `principal-symbols`.  Widget: characteristic curves and singularity propagation.

- [ ] `[manifolds]` From `seeds/blog-posts/2026-01-21-Manifolds-for-the-Anti-Mathematician.md`.  Slug: `manifolds`.  Widget: tangent vectors as derivations; chart-overlap visualization.

### Tier 3: turbulence series upgrade to Quarto

The 7 chapters in `seeds/turbulence/` are already substantial markdown.  Each task lifts one chapter into a full Quarto interactive tutorial.

- [ ] `[turbulence-k41]` From `seeds/turbulence/01-kolmogorov-1941-theory.md`.  Slug: `turbulence-k41`.  Widget: spectrum E(k) ~ k^{-5/3} with adjustable Reynolds number; structure-function exponents.

- [ ] `[turbulence-cascade]` From `seeds/turbulence/02-richardson-cascade-and-scaling.md`.  Slug: `turbulence-cascade`.  Widget: cascade picture animation; eddy-scale energy distribution.

- [ ] `[turbulence-intermittency]` From `seeds/turbulence/03-intermittency-experiments-and-exact-constraints.md`.  Slug: `turbulence-intermittency`.  Widget: structure-function exponents zeta_p with the K41 prediction overlaid against measured anomalies.

- [ ] `[turbulence-multifractal]` From `seeds/turbulence/04-multifractal-models.md`.  Slug: `turbulence-multifractal`.  Widget: f(alpha) singularity spectrum.

- [ ] `[turbulence-shell]` From `seeds/turbulence/05-dissipation-cascades-shell-models.md`.  Slug: `turbulence-shell`.  Widget: GOY shell-model cascade run live in JS (or pre-computed time series).

- [ ] `[turbulence-closure]` From `seeds/turbulence/06-closure-renormalization.md`.  Slug: `turbulence-closure`.  Widget: closure approximations comparison.

- [ ] `[turbulence-2d]` From `seeds/turbulence/07-two-dimensional-turbulence.md`.  Slug: `turbulence-2d`.  Widget: dual cascade in 2D, energy and enstrophy spectra.

### Tier 4: Alon systems biology (blocked: needs your chapter notes in seeds/alon/)

- [ ] `[alon-motifs]` BLOCKED until `seeds/alon/ch03-network-motifs.md` exists.  Then: tutorial on transcription network motifs (FFL, autoreg, etc.) with widgets showing the input-output behavior of each motif.

- [ ] `[alon-autoreg]` BLOCKED until `seeds/alon/ch04-autoregulation.md` exists.

## Done

(nothing yet)
