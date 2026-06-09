# Research notes: Random Matrix Theory tutorial

## Source material

- Primary: `~/Programming/Claude/tutorials/tutorial_rmt-tour.md` (206 lines)
- Supplemental: `~/Programming/Claude/conversations/raw/2026-01-30_non-iid-phenomena-through-random-matrix-theory.md`

## Audience and goal

ML researchers who know linear algebra and basic probability but have not derived the semicircle law or used Marchenko-Pastur in practice.  Goal: build the intuition that RMT is the natural language for "many generically-coupled degrees of freedom," with the semicircle law and Marchenko-Pastur as the worked examples.  Reader should leave able to recognize when RMT applies and what universality buys them.

## Scope decisions (narrowing)

The source covers 10+ topics.  Cutting:

- 't Hooft diagrammatics / ribbon graphs (genuinely beautiful, but tangential for the ML audience and adds a whole category of prerequisites).
- Free probability (companion topic, covered in `tutorials/free-probability.md` already).
- Determinantal point processes, orthogonal polynomial methods, β-ensembles for non-classical β.

Keeping:

- Eigenvalue repulsion and the log-gas picture.
- Semicircle law via saddle-point on the log-gas.
- Marchenko-Pastur and the high-D covariance picture.
- Universality (bulk = sine kernel, edge = Tracy-Widom), but at intuition level only.
- ML applications: PCA / spectrum thresholding, NN initialization spectra.

## Concept Dependency Graph

### Prerequisites (assumed known)
- Linear algebra: eigenvalues, Hermitian matrices, traces, the spectral theorem.
- Probability: distributions, expectations, the central limit theorem.
- Calculus: enough to do a saddle-point / variational calculation.

### Core Ideas (the tutorial teaches these)
1. **Eigenvalue repulsion** — depends on: prerequisites.  The Vandermonde squared makes eigenvalues repel; this is the single fact that makes RMT non-classical.
2. **Log-gas analogy** — depends on: idea 1.  The joint density is a Boltzmann distribution on $N$ particles with quadratic confinement and logarithmic repulsion.
3. **Semicircle from saddle-point** — depends on: idea 2.  Large-$N$ minimization gives the Wigner semicircle.
4. **Marchenko-Pastur** — depends on: idea 3 (analogous derivation).  Sample covariance eigenvalues spread along the MP density even when the true covariance is identity.
5. **Universality** — depends on: ideas 1, 3.  Bulk and edge statistics are the same across symmetry class regardless of the underlying distribution.
6. **When to reach for RMT** — depends on: ideas 4, 5.  ML applications: noise thresholding in PCA, spectra of products of weight matrices, Hessian spectra of trained networks.

### Advanced Topics (mentioned, not derived)
- Tracy-Widom edge distribution — stated, not derived.
- Free probability and DNN spectra — pointer to companion tutorial.
- Sine kernel for bulk correlations — stated.

## Five Key Visualizations

| # | Type | What it shows | Learning objective |
|---|------|---------------|--------------------|
| 1 | Static | Eigenvalue histograms of sample covariance with $\Sigma = I$, three values of $\gamma = p/n$ | "Even iid Gaussian features don't give you eigenvalues at 1 — they spread along Marchenko-Pastur" |
| 2 | Static | Side-by-side: nearest-neighbor spacing histograms for Poisson vs GUE eigenvalues | "Eigenvalues repel each other; this is qualitatively unlike classical samples" |
| 3 | Observable widget | $N$ slider over $\{20, 50, 100, 500, 2000\}$, shows GUE eigenvalue histogram converging to semicircle | "The semicircle is a large-$N$ asymptotic, and convergence is fast" |
| 4 | Observable widget | $\gamma$ slider $\in [0.05, 1]$ sweeping Marchenko-Pastur density | "Concentration ratio shifts the bulk and the edge; at $\gamma = 1$ the lower edge hits zero" |
| 5 | Observable widget | $\beta$ toggle (1, 2, 4) for the three Gaussian ensembles, showing repulsion strength via spacing histogram | "Symmetry class is the only piece of the underlying distribution that survives universality" |

All densities and histograms precomputed in Python and dumped to JSON.  No live numerics in the browser.
