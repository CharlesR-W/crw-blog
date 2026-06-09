# Design notes: RMT tutorial section structure

## Section 1: Why RMT?  The High-D Surprise

**Concept:** The eigenvalues of a sample covariance matrix do not concentrate at the truth in high dimensions, even for iid Gaussian data.
**Motivation:** Reader's classical intuition says $\hat{\Sigma} \to \Sigma$.  Show this is wrong when $p \sim n$.  Hook the reader with the discrepancy before introducing any machinery.
**Prerequisites:** none.
**Figure(s):** Static figure 1 — three eigenvalue histograms of $\hat{\Sigma}$ for $\Sigma = I$, at $\gamma = 0.1, 0.5, 1.0$.
**Performance:** Pre-compute three sample covariance spectra (one per ratio).  Render once at build, cache via `freeze: true`.
**Prose:** ~150 words.  "Suppose you measure $p$ features on $n$ samples..." — set up the high-D regime.  Show the figure.  State the puzzle: why doesn't the eigenvalue spectrum collapse to $\delta(\lambda - 1)$?

## Section 2: Eigenvalue Repulsion is the Key

**Concept:** Hermitian random matrices have an eigenvalue joint density with a Vandermonde-squared factor — eigenvalues repel each other.
**Motivation:** This single fact is what makes RMT not classical probability.  Classical iid samples from a distribution are *unconstrained*; eigenvalues are *correlated by repulsion*.
**Prerequisites:** Section 1.
**Figure(s):** Static figure 2 — side-by-side histograms of nearest-neighbor spacings.  Left: $N$ iid uniform samples (Poisson statistics, exponential spacings).  Right: $N$ GUE eigenvalues (Wigner surmise, $s e^{-c s^2}$ form, vanishing at zero).
**Performance:** Pre-compute both histograms.  Cache.
**Prose:** ~180 words.  Derive the joint density $P(\lambda_1, \ldots, \lambda_N) \propto \prod_{i<j} |\lambda_i - \lambda_j|^2 e^{-N \sum \lambda_i^2 / 2}$ from the Gaussian Unitary Ensemble.  Walk through Vandermonde-from-Jacobian quickly.  Point out the consequence: spacings $s$ between neighboring eigenvalues have $P(s) \to 0$ as $s \to 0$, instead of $P(s) \to$ const for iid.

## Section 3: The Log-Gas

**Concept:** The eigenvalue joint density is exactly the Boltzmann distribution of $N$ classical particles on a line, with quadratic confinement and logarithmic pair repulsion.
**Motivation:** This reframing turns "compute eigenvalue statistics" into "do statistical mechanics," which is a toolkit ML researchers can already use (or recognize).
**Prerequisites:** Section 2.
**Figure(s):** None new; reuse mental model.
**Prose:** ~150 words.  Take the log of the joint density.  $H = N \sum \lambda_i^2 / 2 - 2 \sum_{i<j} \log|\lambda_i - \lambda_j|$.  Note the $N$ in front: it plays the role of inverse temperature, so large $N$ is the "cold" or low-fluctuation limit.

## Section 4: Semicircle from Saddle-Point

**Concept:** In the large-$N$ limit, the eigenvalue density $\rho(\lambda)$ is the minimizer of a free-energy functional.  Solving the variational problem gives the Wigner semicircle.
**Motivation:** Now we get a concrete prediction with no fitting parameters.
**Prerequisites:** Section 3.
**Figure(s):** Observable widget 1 — $N$ slider over $\{20, 50, 100, 500, 2000\}$, shows simulated GUE eigenvalue histogram (precomputed) overlaid with the semicircle prediction.  Learning objective: see convergence is rapid — the semicircle is a useful prediction even at $N = 50$.
**Performance:** Precompute one histogram per $N$, ~5 values, dump as JSON.  Density curve precomputed too.
**Prose:** ~200 words.  Replace sums with integrals over $\rho$, get the variational equation, differentiate to get the Hilbert transform equation.  State (do not derive) the answer: $\rho(\lambda) = \frac{1}{2\pi} \sqrt{4 - \lambda^2}$ on $[-2, 2]$.

## Section 5: Marchenko-Pastur

**Concept:** The same machinery applied to sample covariance gives Marchenko-Pastur, with a single parameter $\gamma = p/n$.
**Motivation:** This is the workhorse of RMT in practice — every PCA-based ML pipeline implicitly assumes either you can ignore MP (low-D) or you correct for it (high-D).
**Prerequisites:** Section 4.
**Figure(s):** Observable widget 2 — $\gamma$ slider $\in [0.05, 1.0]$ sweeping the MP density, with the analytic edges $\lambda_\pm = (1 \pm \sqrt{\gamma})^2$ marked.  Learning objective: the lower edge hits zero exactly at $\gamma = 1$; the bulk is wider for larger $\gamma$.
**Performance:** Precompute MP density curves for ~20 values of $\gamma$, dump as JSON.
**Prose:** ~200 words.  Set up: $X \in \mathbb{R}^{n \times p}$ with iid Gaussian entries; $\hat{\Sigma} = \frac{1}{n} X^T X$.  State the result: eigenvalue density is $\rho_{MP}(\lambda) = \frac{\sqrt{(\lambda_+ - \lambda)(\lambda - \lambda_-)}}{2\pi \gamma \lambda}$ on $[\lambda_-, \lambda_+]$.  Connect back to Section 1's puzzle: that's why $\hat{\Sigma}$ doesn't recover identity.  Mention practical use: spectra outside $[\lambda_-, \lambda_+]$ are signal, inside is noise.

## Section 6: Universality

**Concept:** Local eigenvalue statistics depend only on symmetry class, not on the details of the underlying distribution.
**Motivation:** This is why RMT predictions show up in places that have nothing to do with Gaussian matrices — quantum chaos, zeros of the zeta function, growth of bacterial colonies, KPZ.
**Prerequisites:** Section 4.
**Figure(s):** Observable widget 3 — toggle between $\beta = 1, 2, 4$ ensembles, show the spacing histogram.  Wigner surmises overlay.  Learning objective: stronger repulsion (larger $\beta$) means a bigger gap at zero spacing.
**Performance:** Precompute histograms for each $\beta$ from synthetic GOE/GUE/GSE samples.  ~3 datasets, ~30 KB total.
**Prose:** ~200 words.  State (without derivation) bulk universality (sine kernel) and edge universality (Tracy-Widom).  Tie back to RG: the only "relevant" features at long wavelength are the symmetry and the bulk density; everything else is irrelevant.

## Section 7: When to Reach for RMT

**Concept:** RMT is the right tool whenever you have many generically-coupled degrees of freedom and you care about spectral quantities.
**Motivation:** Convert the math into a recognizable signature.
**Prerequisites:** Sections 5 and 6.
**Figure(s):** None new (or one schematic showing "if your problem looks like X, reach for Y").
**Prose:** ~200 words.  List patterns:
1. Eigenvalues / singular values of any large matrix built from generic data.
2. Compositions of independent random transformations (free probability territory; pointer to companion).
3. Hessian spectra of overparameterized models — bulk + a few outliers.
4. Wigner-style universality wherever there is no special structure (no near-degeneracy, no symmetry beyond the obvious).
End with a one-sentence "what we did not cover" pointer to free probability and Tracy-Widom.

## Total length target

~1,200 words of prose + 5 figures.  Render time budget: <30 seconds (most of that is the precompute script, run once).
