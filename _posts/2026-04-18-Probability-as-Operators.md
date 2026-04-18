---
title: "Probability as Operators"
date: 2026-04-18
motivation: "I kept rewriting the same linear-algebra-flavored probability arguments: expectations as inner products, conditioning as projection, Bayes as reweighting.  The RKHS embedding view unifies these, but a lot of expositions gloss the fine print.  This is my attempt to keep the unified frame while being honest about where it's schematic and where it's actually a theorem."
background: "Comfortable with Hilbert spaces, bounded/compact operators, and basic probability.  Prior exposure to RKHS is helpful but not required - the reproducing kernel story is recalled as needed."
llm: "Claude"
tags: [seed]
math: true
---

# Probability as Operators

The one-line thesis: a probability measure is a linear functional on a space of observables, and almost every operation you care about - marginalization, conditioning, Bayesian updating, independence, selection - is some linear operator acting on that functional.  Which linear functional, and on which space, is a choice.  Different choices give different pictures (characteristic function, density in $L^2$, kernel mean embedding in an RKHS), each good at different things.

This is a seed, not a textbook.  The goal is to get the unified frame in one place and flag the bits that usually get glossed over.

## 1. The Core Move

Let $X$ be a measurable space and $P$ a probability measure on $X$.  Pick a vector space $V$ of test functions $f: X \to \mathbb{R}$ such that $P[f] := \int f \, dP$ is finite for all $f \in V$.  Then

$$
P: V \to \mathbb{R}, \qquad f \mapsto P[f]
$$

is a linear functional.  Write $P \in V^*$.

That's it.  That's the move.  Different $V$'s give different pictures:

| $V$ | Representation of $P$ | Classical name |
| --- | --- | --- |
| span of $\{e^{it \cdot x}\}_{t \in \mathbb{R}}$ | $\hat{P}(t) = \mathbb{E}[e^{itX}]$ | characteristic function |
| $L^2(\lambda)$ (Lebesgue ref. measure) | density $p \in L^2$ | traditional prob. |
| RKHS $\mathcal{H}_k$ | $\mu_P \in \mathcal{H}_k$ | kernel mean embedding |

Each one gets different structure for free.  The Fourier picture makes convolution clean ($\widehat{P * Q} = \hat P \cdot \hat Q$).  The $L^2$ picture gives you densities and Radon-Nikodym.  The RKHS picture turns linear functionals back into vectors of the space itself via the reproducing property - which, as we'll see, is the move that makes all the operator-algebra magic work.

The price, as always, is that no single $V$ does everything.  Convolution is clean in Fourier and ugly in RKHS.  Conditioning is clean in RKHS and ugly in Fourier.  Moment-sequence representations (as in free probability, where "distribution" means the trace of powers of an operator) give you yet another picture, good for non-commutative things.  Pick the picture, accept its strengths and weaknesses, move on.

## 2. Kernel Mean Embedding, Carefully

Let $k: X \times X \to \mathbb{R}$ be a positive definite kernel with RKHS $\mathcal{H}_k$.  The reproducing property is $f(x) = \langle f, k(x, \cdot) \rangle_{\mathcal{H}}$ for all $f \in \mathcal{H}_k$, $x \in X$.  Write $\varphi(x) := k(x, \cdot)$ for the canonical feature map.

The **kernel mean embedding** of $P$ is

$$
\mu_P \;=\; \mathbb{E}_{x \sim P}[\varphi(x)] \;=\; \mathbb{E}_{x \sim P}[k(x, \cdot)] \;\in\; \mathcal{H}_k.
$$

When it exists (see below), it satisfies

$$
\langle \mu_P, f \rangle_{\mathcal{H}} \;=\; \mathbb{E}_P[f] \qquad \forall f \in \mathcal{H}_k,
$$

i.e. $\mu_P$ is the Riesz representative of the linear functional $f \mapsto \mathbb{E}_P[f]$ on $\mathcal{H}_k$.

### When does $\mu_P$ exist?

This is the part every intro glosses over.  The functional $f \mapsto \mathbb{E}_P[f]$ lives on $\mathcal{H}_k$; Riesz gives you a representative iff the functional is **bounded**.  And

$$
\lvert \mathbb{E}_P[f] \rvert \;=\; \lvert \mathbb{E}_P[\langle f, \varphi(X)\rangle] \rvert \;\le\; \lVert f \rVert_{\mathcal{H}} \cdot \mathbb{E}_P[\lVert \varphi(X) \rVert_{\mathcal{H}}] \;=\; \lVert f \rVert_{\mathcal{H}} \cdot \mathbb{E}_P[\sqrt{k(X,X)}].
$$

So a sufficient (and essentially necessary, for Bochner-integrability of $\varphi(X)$) condition is

$$
\boxed{\; \mathbb{E}_P\!\left[\sqrt{k(X,X)}\right] \;<\; \infty \;}
$$

For bounded kernels (RBF, Laplacian, anything with $k(x,x) \le M$) this is automatic and people stop worrying about it.  For unbounded kernels (polynomial, linear on $\mathbb{R}^n$) it's a real integrability constraint - linear kernel on $\mathbb{R}^n$ needs $\mathbb{E}\lVert X \rVert < \infty$, polynomial of degree $d$ needs $\mathbb{E}\lVert X\rVert^d < \infty$, etc.  Heavy-tailed $P$ plus unbounded $k$: be careful, your embedding might not even be a Hilbert space element.

### Characteristic kernels

The map $P \mapsto \mu_P$ is injective on probability measures iff $k$ is **characteristic**.  Gaussian RBF on $\mathbb{R}^n$: characteristic.  Matérn: characteristic.  Linear kernel: emphatically not (it only sees the mean).  Polynomial kernel of degree $d$: sees moments up to order $d$, so two distributions agreeing on first $d$ moments are indistinguishable.  If $k$ isn't characteristic, $\mu_P$ discards information, and you're working with a lossy summary.

The characterization (Sriperumbudur et al. 2010): a bounded, continuous, translation-invariant $k$ on $\mathbb{R}^n$ is characteristic iff the support of its Fourier transform (a finite measure by Bochner) is all of $\mathbb{R}^n$.  The RBF kernel qualifies because $\hat k$ is a Gaussian, strictly positive everywhere.  "Characteristic" is really "spectral support is big enough to separate measures."

### Fourier as a special case

A nice consistency check: the characteristic-function picture is an RKHS embedding in disguise.  Take $X = \mathbb{R}$ and the kernel $k(x, y) = e^{-(x-y)^2/2\sigma^2}$ (RBF).  By Bochner, $k(x, y) = \int e^{i t(x - y)} d\Lambda(t)$ for a finite measure $\Lambda$ (here a scaled Gaussian).  The RKHS $\mathcal{H}_k$ can be realized as

$$
\mathcal{H}_k \;\cong\; \left\{ f(x) = \int e^{itx} \tilde f(t) \, d\Lambda(t) \,:\, \int \lvert \tilde f \rvert^2 d\Lambda < \infty \right\},
$$

i.e. $L^2(\Lambda)$ pulled back via inverse Fourier.  The kernel mean embedding $\mu_P$ corresponds to the function $\hat P \, \sqrt{d\Lambda/d t}$, which is the characteristic function windowed by the kernel's spectral density.  MMD squared is then $\int \lvert \hat P - \hat Q\rvert^2 d\Lambda$ - a spectrally-weighted $L^2$ distance of characteristic functions.  So kernel embeddings are characteristic-function embeddings, just with a choice of spectral weighting.  Characteristic kernels = spectral weighting has full support = you can recover $\hat P$ (hence $P$) from the windowed version.  This is the cleanest way I know to see why "characteristic kernel" is the right condition for injectivity.

## 3. MMD and HSIC

Given the embedding, two obvious things to do.

### Distance: Maximum Mean Discrepancy

$$
\mathrm{MMD}(P, Q) \;=\; \lVert \mu_P - \mu_Q \rVert_{\mathcal{H}}.
$$

Expanding:

$$
\mathrm{MMD}(P,Q)^2 = \mathbb{E}_{x,x' \sim P} k(x,x') - 2\mathbb{E}_{x\sim P, y\sim Q} k(x,y) + \mathbb{E}_{y,y'\sim Q} k(y,y').
$$

For characteristic $k$, MMD is a metric on probability measures: $\mathrm{MMD}(P,Q) = 0 \iff P = Q$.  This gives you a Hilbert-space geometry on distributions - very useful if you're trying to do gradient descent in the space of distributions (kernel Stein, kernel exponential families, MMD-GANs, etc.).

There's also an integral-probability-metric reading:

$$
\mathrm{MMD}(P, Q) \;=\; \sup_{\lVert f \rVert_{\mathcal{H}} \le 1} \lvert \mathbb{E}_P f - \mathbb{E}_Q f \rvert.
$$

"Worst-case expectation gap over the unit ball of the RKHS" - which says MMD is the $\mathcal{H}$-flavored Wasserstein / Kantorovich-Rubinstein dual.  For the Gaussian RBF, the unit ball of $\mathcal{H}$ is a dense subset of very smooth functions, so MMD measures distributional differences a smoothness-weighted way.  That's sometimes what you want (smooth test functions, nice concentration) and sometimes not (you might prefer Wasserstein's transport-cost reading for OT applications).

### Independence: HSIC

Let $(X, Y) \sim P_{XY}$, with kernels $k$ on $X$ and $l$ on $Y$, feature maps $\varphi, \psi$.  The **cross-covariance operator** is

$$
C_{XY} \;=\; \mathbb{E}[(\varphi(X) - \mu_X) \otimes (\psi(Y) - \mu_Y)] : \mathcal{H}_l \to \mathcal{H}_k.
$$

Its Hilbert-Schmidt norm is

$$
\mathrm{HSIC}(X, Y) \;=\; \lVert C_{XY} \rVert_{\mathrm{HS}}^2.
$$

For characteristic $k$ and $l$ (and appropriate integrability), $\mathrm{HSIC}(X,Y) = 0 \iff X \perp Y$.  This is genuinely beautiful: **independence in probability = zero-ness of an operator in Hilbert space**.

HSIC is what you want whenever you'd reach for a correlation coefficient but suspect nonlinear dependence.  And since you can estimate it from samples in $O(n^2)$ (or $O(n)$ with Nyström / Random Fourier Features), it's computationally live.

## 4. Conditioning as an Operator - Read the Fine Print

This is where the source note I was working from glossed the most.  The picture is real, but the formulas that get thrown around are either the population-level object (with invertibility assumptions) or the regularized empirical estimator (with a $\lambda$), and conflating them leads to confusion.  Let me be careful.

### 4.1 What we want

For each $x$, $P(Y \mid X=x)$ is a probability measure on $Y$; its embedding is $\mu_{Y \mid x} = \mathbb{E}_{Y \mid x}[\psi(Y)]$.  We want an operator $\mathcal{U}_{Y \mid X}: \mathcal{H}_k \to \mathcal{H}_l$ such that

$$
\mathcal{U}_{Y \mid X} \, \varphi(x) \;=\; \mu_{Y \mid x}
$$

for all (or a.e.) $x$.  Think of $\mathcal{U}_{Y\mid X}$ as "the conditional distribution, compiled into a linear map on features."

### 4.2 Population formula and its fine print

The Song-Huang-Smola-Fukumizu (2009) result, in clean form: if

$$
\mathbb{E}[g(Y) \mid X = \cdot] \in \mathcal{H}_k \quad \text{for all } g \in \mathcal{H}_l,
$$

then $\mathcal{U}_{Y \mid X} = C_{YX} C_{XX}^{-1}$ in the sense that $\mathcal{U}_{Y\mid X} C_{XX} = C_{YX}$.  The issue is that $C_{XX}$ is typically not invertible on all of $\mathcal{H}_k$ (it's compact, positive, with spectrum accumulating at zero), so $C_{XX}^{-1}$ has to be read as a pseudo-inverse on the range of $C_{XX}$, and the "for all $g \in \mathcal{H}_l$" assumption is not innocent - for universal kernels it's essentially saying $\mathcal{H}_k$ is closed under a lot of conditional-expectation operations.

Klebanov-Schuster-Sullivan and others have cleaned up the statement: you can make sense of $\mathcal{U}_{Y\mid X}$ as a densely-defined unbounded operator without the strong assumption, but then composition becomes delicate.

The **empirical, regularized** version is what everyone actually uses:

$$
\hat{\mathcal{U}}_{Y \mid X} \;=\; \hat C_{YX}\,(\hat C_{XX} + \lambda I)^{-1}.
$$

This is what's computable from data (it's kernel ridge regression on feature maps, with Gram matrices doing all the work).  It's a **regularized estimator of the population operator**, and $\lambda$ has to go to zero at a controlled rate for consistency.  Writing "$\mathcal{U}_{Y\mid X} = C_{YX}(C_{XX} + \lambda I)^{-1}$" without the hat is a common abuse that makes the operator look like a closed-form object when it's actually an estimator.

### 4.3 Why this is still useful

Even with the caveats, the picture

$$
\text{conditioning} \;=\; \text{kernel ridge regression in RKHS}
$$

is a real theorem in the right regime, and operationally it says: to condition, you solve a (regularized) linear system.  That's the payoff.  You can compute $\mu_{Y\mid x}$ from samples, get consistency rates, and chain conditional operators to handle more complex inference.

Concretely, given samples $\{(x_i, y_i)\}_{i=1}^n$ from $P_{XY}$, let $K$ be the $n \times n$ Gram matrix on $X$ ($K_{ij} = k(x_i, x_j)$) and $\Psi = (\psi(y_1), \ldots, \psi(y_n))$.  The empirical conditional mean embedding is

$$
\hat \mu_{Y \mid x} \;=\; \Psi (K + n\lambda I)^{-1} k_x, \qquad k_x = (k(x_1, x), \ldots, k(x_n, x))^\top.
$$

This is kernel ridge regression with the "labels" being feature-map-valued.  Tests against $g \in \mathcal{H}_l$ give the standard kernel ridge regression formula $\hat g(x) = g_Y^\top (K + n\lambda I)^{-1} k_x$ where $g_Y = (g(y_1), \ldots, g(y_n))$.  So the abstract conditional-embedding operator and the concrete kernel ridge regressor are the same object, just written differently.

## 5. Bayes as Operator, With Caveats

Set prior $P(\theta)$, likelihood $P(D \mid \theta)$, posterior $P(\theta \mid D)$.  In operator form:

$$
\mu_{\theta \mid d} \;=\; \mathcal{U}_{\theta \mid D}\, \psi(d), \qquad \mathcal{U}_{\theta \mid D} = C_{\theta D}\,(C_{DD} + \lambda I)^{-1}.
$$

Two caveats the source note glossed:

1. **Means, not distributions.** $\mu_{\theta \mid d}$ is the *embedding* of the posterior - which is the full posterior distribution if $k_\theta$ is characteristic, and merely the posterior's mean-under-$k_\theta$-features otherwise.  "Bayes-as-regression" gives you conditional *means* in the first instance; characteristic-kernel injectivity is what upgrades that to full conditional *distributions*.  Drop the characteristic assumption and you're doing something weaker than Bayes.

2. **Same regularization story as §4.2.** Population $\mathcal{U}_{\theta\mid D}$ needs invertibility / range conditions; the $\lambda I$ version is the empirical estimator.  Don't squint at the formula and conclude "Bayes is just linear algebra" - Bayes is a linear map between *embeddings*, which is a real statement, not the same as saying posteriors are always computable by Gram-matrix inversion.

With those caveats, the picture is genuinely unifying: prior → posterior is a bounded linear map between points in RKHS.  You can compose conditional operators, do sequential Bayesian updating as composition, and get nonparametric Bayes-like behavior without ever writing down a density.

### 5.1 Why the kernel picture is actually useful for Bayes

Three things it gives you that classical Bayes struggles with:

1. **No likelihood required.**  If you can sample from the joint $(\theta, D)$, you can estimate $\hat C_{\theta D}$ and $\hat C_{DD}$ empirically.  No need to write down $P(D \mid \theta)$ as a density.  This is the "likelihood-free" regime people reach for ABC (approximate Bayesian computation) in - kernel methods let you condition without a tractable likelihood, trading density estimation for kernel ridge regression.

2. **Composable updating.**  Sequential inference: posterior under data $d_1$ becomes prior for $d_2$.  If the posterior embedding is a linear map applied to the likelihood-embedding, composition just chains operators.  Numerical stability and regularization do real work here - don't compose fifty of these without thinking - but conceptually clean.

3. **Nonparametric posterior samples.**  From $\hat \mu_{\theta \mid d}$ you can recover posterior mean predictions, and with some work (Kanagawa, Sriperumbudur, et al. on "kernel herding" and related), approximate posterior samples.

What you *don't* get for free: full posterior distributions (only their embeddings - see caveat 1 above), calibrated uncertainty intervals, and anything that requires you to integrate against priors you don't have samples from.  It's Bayes-as-regression, not Bayes-as-density.

## 6. Operations Table (With Flags)

A compact summary.  Marked with $\ast$ are the ones that are cleaner in another picture, or need care.

| Operation | Operator form | Note |
| --- | --- | --- |
| $\mathbb{E}_P[f]$ | $\langle \mu_P, f \rangle_{\mathcal{H}}$ | needs $\mathbb{E}\sqrt{k(X,X)} < \infty$ |
| Mixture $\alpha P + (1-\alpha)Q$ | $\alpha \mu_P + (1-\alpha)\mu_Q$ | linear, clean |
| Product $P \otimes Q$ | $\mu_P \otimes \mu_Q \in \mathcal{H}_k \otimes \mathcal{H}_l$ | tensor-product RKHS |
| Marginalization$^\ast$ | partial trace on tensor-product embedding | needs Hilbert-Schmidt structure; see below |
| Conditioning$^\ast$ | $\hat C_{YX}(\hat C_{XX} + \lambda I)^{-1}$ | regularized, empirical |
| Independence | $\lVert C_{XY}\rVert_{\mathrm{HS}} = 0?$ | needs characteristic $k, l$ |
| Pushforward $Y = g(X)$ | $\mathbb{E}[\psi(g(X))]$ | linear in $\mu_P$ only in special cases |
| Convolution$^\ast$ | no clean formula in RKHS | use Fourier |

### On "marginalization = partial trace"

This one deserves a flag.  If $\mu_{XY} \in \mathcal{H}_k \otimes \mathcal{H}_l$ is the joint embedding (feature map $\varphi(x) \otimes \psi(y)$), then "marginalize out $Y$" is the partial-trace-like operation of pairing with a functional that integrates $\psi(y)$ against $P_Y$.  Making this rigorous requires treating $\mu_{XY}$ as a Hilbert-Schmidt operator $\mathcal{H}_l \to \mathcal{H}_k$ and reading marginalization as applying it to the constant function - and the constant function isn't always in the RKHS (e.g., on $\mathbb{R}^n$ with Gaussian RBF, constants are not in $\mathcal{H}_k$, only in its closure).  The slogan is right, the mechanics need care.  Schematic picture, not drop-in formula.

What *is* clean: if $f \in \mathcal{H}_k$ only (doesn't depend on $y$), then

$$
\mathbb{E}_{XY}[f(X)] \;=\; \langle \mu_{XY}, f \otimes \mathbf{1}\rangle_{\mathcal{H}_k \otimes \mathcal{H}_l}
$$

reduces to $\langle \mu_X, f \rangle_{\mathcal{H}_k}$ when you pair correctly.  This is the "marginalize" semantic for observables that only look at $X$.  But if you want to *obtain* $\mu_X$ as an operation applied to $\mu_{XY}$, the partial-trace slogan needs that constant-function move, with the caveat above.

## 7. Transfer Operators: Koopman and Perron-Frobenius

Same abstract move, in dynamical systems.  Let $T: X \to X$ be a measurable map.

- **Koopman operator** $\mathcal{K}: (\mathcal{K} f)(x) = f(T(x))$.  Acts on observables (functions).  Linear even if $T$ is horrendously nonlinear; the tradeoff is that $\mathcal{K}$ lives on an infinite-dimensional function space.
- **Perron-Frobenius operator** $\mathcal{P}$: dual of $\mathcal{K}$, acts on measures/densities.  If $P$ has density $p$ and $T$ is nice, $\mathcal{P}p$ is the density of $T_\# P$.

In the kernel picture, $\mathcal{P}$ is the pushforward of embeddings: $\mu_P \mapsto \mu_{T_\# P}$.  Given data $(x_t, x_{t+1})_{t=1}^N$, the natural estimator of $\mathcal{K}$ (restricted to $\mathcal{H}_k$) is

$$
\hat{\mathcal{K}} \;=\; \hat C_{X_{t+1}, X_t} (\hat C_{X_t, X_t} + \lambda I)^{-1}.
$$

Same shape as the conditional embedding.  No coincidence: learning the Koopman operator from data **is** learning the conditional distribution $P(X_{t+1} \mid X_t)$.  For deterministic $T$ the conditional distribution is a point mass, and $\hat{\mathcal{K}}$ estimates the usual Koopman operator; for stochastic dynamics it estimates the stochastic Koopman operator (expected-value-of-future-observable).  Extended Dynamic Mode Decomposition (EDMD), in its kernelized form, is exactly this.  This is a clean, compact way to say what kernel-EDMD is doing.

Caveats inherited from §4: regularization matters, spectral estimation of $\mathcal{K}$ from $\hat{\mathcal{K}}$ is delicate (eigenvalues of $\hat{\mathcal{K}}$ are consistent only under strong conditions, and spurious eigenvalues are common), and for mixing dynamics you need to be careful about which stationary measure the embedding is with respect to.  The cleanest statements are in Klus et al. and in the subsequent literature on consistency of kernel Koopman estimators.

## 8. Selection, Bayes, and the Price Equation in RKHS

The connection I find most fun.

### 8.1 Selection as reweighting

Population distribution $P$, fitness $f: X \to \mathbb{R}_+$.  One generation of selection:

$$
dP' / dP \;\propto\; f, \qquad P'(A) = \frac{\int_A f \, dP}{\int f \, dP}.
$$

Selection is a Radon-Nikodym reweight by fitness.

### 8.2 Bayes is selection

Posterior $\propto$ likelihood $\times$ prior.  Set $f(\theta) = P(D \mid \theta)$ and $P = $ prior.  Same formula.

This isn't a metaphor or a vibes-based connection - it's equality of operations.  The replicator dynamic and Bayesian updating are the same abstract reweighting; Harper (2009) works this out cleanly, and Campbell (2015) does the philosophical framing.

### 8.3 Kernel embedding of one selection step

If $f \in \mathcal{H}_k$ (so fitness is a well-behaved observable in the RKHS), the embedding of the post-selection distribution is

$$
\mu_{P'} \;=\; \frac{\mathbb{E}_P[f(X)\, \varphi(X)]}{\mathbb{E}_P[f(X)]} \;=\; \frac{C_P f + \mu_P \langle \mu_P, f\rangle}{\langle \mu_P, f\rangle},
$$

using $\mathbb{E}_P[f(X) \varphi(X)] = C_P f + \mu_P \mathbb{E}_P[f]$.  Selection is a closed-form nonlinear map on embeddings when fitness is in the RKHS.  It's affine plus normalization - not linear, but close.

### 8.4 Price equation, kernelized

Continuous-time replicator:

$$
\dot p_i \;=\; p_i\big(f_i - \bar f\big), \qquad \bar f = \sum_j p_j f_j.
$$

Compute $\dot \mu_P$ assuming $f \in \mathcal{H}_k$ so that $\mathbb{E}_P[f] = \langle \mu_P, f\rangle$:

$$
\dot \mu_P \;=\; \frac{d}{dt} \mathbb{E}_P[\varphi(X)] \;=\; \mathbb{E}_P\!\left[\big(f(X) - \mathbb{E}_P[f]\big)\, \varphi(X)\right].
$$

Recognize the right-hand side as the covariance operator applied to $f$:

$$
C_P f \;=\; \mathbb{E}_P[(\varphi(X) - \mu_P) \otimes (\varphi(X) - \mu_P)] \, f \;=\; \mathbb{E}_P[(f(X) - \langle \mu_P, f\rangle) (\varphi(X) - \mu_P)].
$$

A line of algebra shows these are equal, so

$$
\boxed{\; \dot \mu_P \;=\; C_P f \;}
$$

This is the Price equation "change in trait = covariance of fitness and trait" upgraded to an operator statement: change in *embedding* equals the covariance *operator* applied to fitness.  Pair with any $g \in \mathcal{H}_k$ and you recover $\frac{d}{dt}\mathbb{E}_P[g] = \mathrm{Cov}_P(f, g)$.  Please clap.

### 8.5 Info-geometric gloss

Here's where the source note had the formula wrong, so let me fix it.  For fitness-weighted $P' \propto f P$,

$$
\mathrm{KL}(P' \,\lVert\, P) \;=\; \int \log\frac{dP'}{dP} \, dP' \;=\; \int \left(\log f - \log \mathbb{E}_P[f]\right) dP' \;=\; \mathbb{E}_{P'}[\log f] - \log \mathbb{E}_P[f].
$$

Note $\mathbb{E}_{P'}$ on the first term, not $\mathbb{E}_P$.  (If you use $\mathbb{E}_P[\log f]$ you get $\mathrm{KL}(P \,\lVert\, P')$ up to a sign, which is the reverse direction.  Easy to confuse.)  By Jensen, $\log \mathbb{E}_P[f] \ge \mathbb{E}_P[\log f]$, so

$$
\mathrm{KL}(P' \,\lVert\, P) \;=\; \mathbb{E}_{P'}[\log f] - \log \mathbb{E}_P[f] \;\ge\; 0,
$$

with equality iff $f$ is $P$-a.s. constant.  Good.

**Natural-gradient framing.**  In an exponential family $P_\eta \propto \exp(\eta \cdot T) P_0$ with log-partition $A(\eta)$, a multiplicative update $P \to P \cdot \exp(\varepsilon g)$ is, to first order in $\varepsilon$, a step $\eta \to \eta + \varepsilon \delta\eta$ where $\delta\eta$ is chosen so that $\delta\eta \cdot T$ best matches $g$ in $L^2(P)$.  The update direction, in the natural (canonical) parameters $\eta$, is the Fisher-preconditioned gradient of $\mathbb{E}_P[g]$: natural gradient ascent on mean fitness with step size $\varepsilon$.  So one infinitesimal generation of selection with fitness $e^{\varepsilon g}$ is an $\varepsilon$-step of natural gradient ascent on $\mathbb{E}_P[g]$ in the exp-family log-parametrization.

Caveats worth flagging: (i) this is a *local* / exp-family statement - outside exponential families the "natural gradient" name requires the Fisher metric, which you still have, but the clean $P \propto e^{\eta T}$ trick doesn't apply verbatim; (ii) discrete-time selection by $f$ (not by $\exp(\varepsilon g)$) is an exact multiplicative update, not an $\varepsilon$-step - the natural-gradient picture is the infinitesimal limit.  See my info-geom seed for the full story.

### 8.6 Putting it together

Selection, Bayes, and replicator dynamics are the same linear-algebraic object seen from three angles.  In the RKHS, the object is $\dot \mu_P = C_P f$.  In info geometry, it's natural-gradient ascent of mean fitness in exp-family coordinates.  In classical probability, it's reweighting.  Pick your favorite picture.

## 9. Worked Mini-Example: Two Gaussians on $\mathbb{R}$

Let $P = \mathcal{N}(0, 1)$, $Q = \mathcal{N}(\theta, 1)$ on $\mathbb{R}$, RBF kernel $k(x,y) = \exp(-(x-y)^2 / 2\sigma^2)$.  Then $\mu_P(z) = \mathbb{E}_{X \sim P}[k(X, z)]$, and by Gaussian convolution,

$$
\mu_P(z) \;=\; \frac{\sigma}{\sqrt{\sigma^2 + 1}} \exp\!\left(-\frac{z^2}{2(\sigma^2 + 1)}\right).
$$

A Gaussian, but broader than the kernel.  $\mu_Q$ is the same shape centered at $\theta$.  MMD squared:

$$
\mathrm{MMD}^2 = \lVert \mu_P - \mu_Q\rVert^2 \;=\; \frac{\sigma}{\sqrt{\sigma^2 + 2}}\left(2 - 2 \exp\!\left(-\frac{\theta^2}{2(\sigma^2 + 2)}\right)\right).
$$

Two sanity checks.  $\theta = 0$: MMD squared is zero.  Good.  $\theta \to \infty$: MMD squared $\to 2\sigma/\sqrt{\sigma^2 + 2}$, saturating at a finite value.  That's a feature, not a bug - MMD under a bounded kernel is bounded, unlike KL or Wasserstein.  The kernel bandwidth $\sigma$ sets a scale: for $\theta \ll \sigma$, MMD is linear in $\theta$ (detection scales as separation); for $\theta \gg \sigma$, MMD saturates (you know the means differ but can't measure how much).

Moral: pick $\sigma$ on the scale of the distributional differences you care about.  This is also why RFF / multi-bandwidth MMDs (sum of MMDs at several $\sigma$'s) are the practical default - they cover multiple scales.

## 10. What This Picture Is Bad At

Honest accounting, because overselling a frame makes people mistrust it.

- **Convolution.**  Addition of independent variables is beautiful in Fourier ($\hat P \cdot \hat Q$) and awful in RKHS - no clean closed form in terms of $\mu_P, \mu_Q$ for generic translation-invariant kernels.  If you need convolutions, embed differently or stay in Fourier.

- **No universal embedding.**  There isn't one $V$ that makes all operations linear and clean.  Fourier is great for convolution and translation; $L^2$ is great for densities and Radon-Nikodym; RKHS is great for conditioning, independence, and kernel geometry; moment sequences are great for positive-support things and for non-commutative generalizations.  You pick your kernel (/ space) based on what operation you need to be linear.

- **Infinite-dim concentration.**  Empirical estimators of $\mu_P$, $C_{XY}$, etc. concentrate at parametric rates ($n^{-1/2}$) for bounded kernels, but constants depend on effective dimension, and spectral quantities (eigenvalues of $\hat C_{XX}$) concentrate more slowly.  If you're doing spectral kernel methods, read the concentration literature carefully.  The operator picture is clean on the board; the estimator picture has more knobs.

- **Characteristic kernel assumption isn't free.**  Most "$\mu_P$ encodes $P$" claims require it, and on non-compact spaces with unbounded kernels the assumption interacts non-trivially with moment conditions.  Some settings don't admit a characteristic kernel at all (discrete finite $X$ with $k = \delta_{xy}$ is characteristic but trivial; the embedding is just the probability vector).

- **Conditional embeddings need the regularized / empirical reading.**  Writing $C_{YX} C_{XX}^{-1}$ makes the object look like a formula when it's really a regularized estimator of a potentially-unbounded population operator.  See §4.

- **No good high-dimensional geometric intuition.**  The geometry of $\mu_P$ in an infinite-dim RKHS doesn't match standard intuitions from finite-dim.  Two distributions can have MMD close to zero while their supports are disjoint (kernel bandwidth mismatch), and the "distance between distributions" reading of MMD can be misleading if you forget the kernel is doing smoothing.

## 11. Exercises / Things to Chew On

- Show that for the linear kernel $k(x,y) = x \cdot y$ on $\mathbb{R}^n$, $\mu_P = \mathbb{E}[X]$ and MMD measures only mean differences.  HSIC with linear $k, l$ reduces to what?  (Answer: squared Frobenius norm of the cross-covariance *matrix* $\mathbb{E}[XY^\top] - \mathbb{E}[X]\mathbb{E}[Y]^\top$.  Classic multivariate covariance.)

- Derive the empirical HSIC formula in terms of Gram matrices: $\mathrm{HSIC} = \frac{1}{n^2} \mathrm{tr}(K H L H)$ with $H = I - \frac{1}{n} \mathbf{1}\mathbf{1}^\top$ the centering matrix.  This is what everyone actually computes.

- For a characteristic kernel with $C_{XX}$ trace-class, show $\mathrm{MMD}^2(P, Q) = \sum_i (\langle \mu_P - \mu_Q, e_i\rangle)^2$ in an eigenbasis of $C_{XX}$.  Think about what happens as you truncate - this is kernel PCA of distributions.

- Work out $\dot \mu_P = C_P f$ directly from $\dot p_i = p_i(f_i - \bar f)$ in the discrete case.  Where does the covariance operator come from?  (Hint: $\frac{d}{dt}\mathbb{E}[\varphi(X)] = \mathbb{E}[\dot p(x) \varphi(x)]$, then plug in.)

## 12. Recap in One Breath

Probability measures are linear functionals on function spaces.  Pick the space and you pick the picture.  In an RKHS $\mathcal{H}_k$ with $\mathbb{E}\sqrt{k(X,X)} < \infty$, the measure $P$ has a Riesz representative $\mu_P = \mathbb{E}\,\varphi(X) \in \mathcal{H}_k$; characteristic $k$ makes $P \mapsto \mu_P$ injective.  MMD is the embedding distance, HSIC is the Hilbert-Schmidt norm of cross-covariance, independence is a zero-operator statement.  Conditioning, Bayes, and the Koopman operator are all the same regularized kernel ridge regression $\hat C_{YX}(\hat C_{XX} + \lambda I)^{-1}$ - with the honest caveat that this is an empirical estimator of a population operator that needs care to define.  Selection is Bayes is replicator dynamics is $\dot \mu_P = C_P f$, which is the Price equation lifted to an operator, and infinitesimally it's natural-gradient ascent on mean fitness.  Convolution is where this picture is bad; use Fourier.

See also: my info-geom seed for the natural-gradient framing; my seed on free probability for the non-commutative analog (where "distribution" means moments of an operator, and the Cauchy / R-transforms play the role of Fourier).

## References

- Muandet, Fukumizu, Sriperumbudur, Schölkopf (2017), *Kernel Mean Embedding of Distributions: A Review and Beyond*.  The comprehensive survey; has the existence / boundedness conditions spelled out.
- Song, Huang, Smola, Fukumizu (2009), *Hilbert Space Embeddings of Conditional Distributions*.  Original conditional-embedding paper; read carefully for the assumptions.
- Klebanov, Schuster, Sullivan and co-authors, various, on cleaner formulations of conditional mean embeddings (the $C_{YX} C_{XX}^{-1}$ story without the strong "$\mathbb{E}[g(Y)\mid X] \in \mathcal{H}_k$" assumption).
- Gretton, Borgwardt, Rasch, Schölkopf, Smola (2012), *A Kernel Two-Sample Test*.  MMD statistical theory.
- Gretton et al. on HSIC; Fukumizu et al. on characteristic kernels.
- Williams and Rowley, *A Data-Driven Approximation of the Koopman Operator*; Klus et al. on kernel-EDMD.
- Harper (2009), *The Replicator Equation as an Inference Dynamic*.
- Campbell (2015), *Universal Darwinism as a Process of Bayesian Inference*.

Written with Claude.
