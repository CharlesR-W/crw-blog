---
title: "RKHS and Kernel Learning"
date: 2026-04-18
motivation: "Kernels are the right language for a surprising amount of ML: SVMs, GPs, MMD, HSIC, kernel mean embeddings, even the NTK story.  They're also the cleanest nontrivial example of 'infinite-dimensional linear algebra that you can actually compute with'.  Worth knowing the toolkit cold."
background: "Functional analysis at the level of 'Hilbert spaces, bounded operators, Riesz representation'.  Some ML exposure helps but isn't required.  If you've seen $(X^T X + \\lambda I)^{-1} X^T y$ before, you already know half the story."
llm: "Claude"
tags: [seed]
math: true
---

# RKHS and Kernel Learning

## The Setup

Reproducing kernel Hilbert spaces (RKHS) are what you get when you insist on one thing: in your function space, **point evaluation should be continuous**.  That is, $f \mapsto f(x)$ should be a bounded linear functional for each $x$.

That is a very mild-sounding demand.  $L^2$ doesn't satisfy it (point evaluation isn't even defined there).  But the spaces where it does hold turn out to have a rich structure - every such space has a distinguished "kernel" $k(x,y)$ that encodes everything, and a correspondingly rich computational toolkit.

This is the seed for kernel methods, Gaussian processes, kernel mean embeddings, the NTK regime of deep learning, and half of nonparametric statistics.  We'll set up the toolkit and point at where each piece gets used.

## The Three-Legged Stool

There are three equivalent ways to define an RKHS, and each is useful in different contexts.

**Definition 1: the reproducing property.**  A Hilbert space $\mathcal{H}$ of functions $f : \mathcal{X} \to \mathbb{R}$ is an RKHS if for every $x \in \mathcal{X}$, the evaluation functional $\delta_x : f \mapsto f(x)$ is bounded.  By Riesz representation, there exists $k_x \in \mathcal{H}$ such that

$$
f(x) = \langle f, k_x \rangle_\mathcal{H}.
$$

The function $k(x,y) := k_x(y) = \langle k_x, k_y\rangle$ is the **reproducing kernel**.  It is symmetric and positive definite (the Gram matrix $[k(x_i, x_j)]$ is PSD for any finite sample).

**Definition 2: completion of linear combinations.**  Given a positive definite kernel $k$, form the pre-Hilbert space of finite linear combinations

$$
\mathcal{H}_0 = \left\{ \sum_{i=1}^n c_i k(x_i, \cdot) : n \in \mathbb{N}, c_i \in \mathbb{R}, x_i \in \mathcal{X}\right\}
$$

with inner product $\langle \sum_i c_i k(x_i, \cdot), \sum_j d_j k(y_j, \cdot)\rangle := \sum_{ij} c_i d_j k(x_i, y_j)$.  Completing gives an RKHS whose reproducing kernel is $k$.

**Definition 3: Mercer expansion.**  If $k$ is continuous on a compact domain with finite measure $\nu$, then it admits an eigendecomposition

$$
k(x,y) = \sum_{i=1}^\infty \lambda_i \phi_i(x) \phi_i(y)
$$

where $(\lambda_i, \phi_i)$ are eigenpairs of the integral operator $T_k f(x) = \int k(x,y) f(y)\, d\nu(y)$, the eigenvalues are nonnegative, and the $\phi_i$ are orthonormal in $L^2(\nu)$.  The RKHS is then

$$
\mathcal{H} = \left\{ f = \sum_i a_i \phi_i : \|f\|_\mathcal{H}^2 = \sum_i \frac{a_i^2}{\lambda_i} < \infty \right\}.
$$

Notice: functions whose expansion has weight on small-$\lambda$ components are penalized heavily.  This is where "capacity control" lives.

**Moore-Aronszajn.** These three views are equivalent, and more: any positive definite kernel $k$ on $\mathcal{X} \times \mathcal{X}$ uniquely determines an RKHS $\mathcal{H}_k$ with $k$ as its reproducing kernel.  This is the bridge that lets you treat "kernel" and "RKHS" as two names for the same object.

### What the RKHS Norm Actually Measures

The norm $\lVert f\rVert_\mathcal{H}$ is a measure of "how complicated" $f$ is, calibrated to the kernel.  For the Gaussian kernel, it roughly counts the high-frequency content of $f$ (in a Sobolev-style way).  For a polynomial kernel of degree $d$, it counts the size of the polynomial coefficients.

Concretely, via Mercer: $\lVert f\rVert_\mathcal{H}^2 = \sum_i a_i^2 / \lambda_i$ where $f = \sum_i a_i \phi_i$.  Components with small eigenvalues are expensive.  A function can live in $L^2$ just fine but have infinite RKHS norm - it uses too much high-frequency content relative to the kernel's spectrum.

So when you regularize with $\lambda \lVert f\rVert_\mathcal{H}^2$, you're telling the optimizer "stay smooth in the sense that this kernel considers smooth".  Different kernels encode different smoothness priors.  This is why kernel choice is the main modeling knob in kernel methods: you're not just picking an algorithm, you're picking a smoothness structure.

## The Feature Map Picture

Define $\varphi : \mathcal{X} \to \mathcal{H}$ by $\varphi(x) = k(x, \cdot)$.  This is the **canonical feature map**.  By the reproducing property,

$$
k(x,y) = \langle \varphi(x), \varphi(y)\rangle_\mathcal{H}.
$$

That's the "kernel trick": you have an implicit embedding of $\mathcal{X}$ into a (possibly infinite-dimensional) Hilbert space, and you can compute inner products there without ever materializing the embedding.  For the RBF kernel the feature space is genuinely infinite-dimensional, and yet $k(x,y) = \exp(-\lVert x - y\rVert^2 / 2\sigma^2)$ takes one line to evaluate.

Any linear method in feature space (regression, classification, PCA, CCA, whatever) that can be written purely in terms of inner products can be "kernelized".  You plug in $k$ wherever you see $\langle \varphi(x), \varphi(y)\rangle$ and you're done.  The price is an $n \times n$ Gram matrix instead of a $d \times d$ covariance - tractable for moderate $n$, a pain for big $n$ (we'll get to approximations).

## The Representer Theorem

Consider regularized empirical risk minimization over $\mathcal{H}$:

$$
\hat{f} = \arg\min_{f \in \mathcal{H}} \; L(f(x_1), \ldots, f(x_n); y_1, \ldots, y_n) + \lambda \lVert f\rVert_\mathcal{H}^2
$$

for any loss $L$ that depends on $f$ only through its values at the training points, and any strictly increasing regularizer of the norm.

**Theorem (Representer):** The minimizer has the form $\hat{f}(x) = \sum_{i=1}^n \alpha_i k(x_i, x)$ for some $\alpha \in \mathbb{R}^n$.

The proof is one line.  Decompose $f = f_\parallel + f_\perp$ where $f_\parallel \in \mathrm{span}\{k(x_i, \cdot)\}$ and $f_\perp$ is orthogonal to this span.  Then $f(x_j) = \langle f, k(x_j, \cdot)\rangle = \langle f_\parallel, k(x_j, \cdot)\rangle = f_\parallel(x_j)$ for each training point, so $L$ only sees $f_\parallel$.  Meanwhile $\lVert f\rVert^2 = \lVert f_\parallel\rVert^2 + \lVert f_\perp\rVert^2$, so any $f_\perp \neq 0$ strictly increases the objective.  Done.

This is huge.  We started with an optimization over an infinite-dimensional function space and ended with an optimization over $n$ coefficients.  SVMs, kernel ridge regression, kernel logistic regression, SVR, support vector novelty detection - they are all finite-dimensional convex programs because of this one argument.

### A Concrete Example

Let's unpack representer with squared loss.  Suppose $\mathcal{X} = \mathbb{R}$, $k(x,y) = \exp(-(x-y)^2/2)$ (Gaussian with bandwidth 1), $n = 3$ data points, $\lambda = 0.1$.  The RKHS is a bona fide infinite-dimensional function space; it contains functions like arbitrary smooth bumps.  But the minimizer of $\sum_i (f(x_i) - y_i)^2 + \lambda \lVert f\rVert^2$ is a specific combination of three Gaussians centered at the data points.  You solve $(K + \lambda I)\alpha = y$ - a $3 \times 3$ linear system - and you're done.

The "infinite-dimensional optimization" happens only conceptually.  The actual compute is cubic in $n$, independent of the dimension of the feature space.  This is why the representer theorem is the central computational fact of kernel methods: it collapses functional optimization into matrix algebra.

## Kernel Ridge Regression

Apply representer to squared loss $L = \sum_i (f(x_i) - y_i)^2$.  Substituting $f = \sum_j \alpha_j k(x_j, \cdot)$ and using $f(x_i) = \sum_j \alpha_j k(x_i, x_j) = (K\alpha)_i$ with $K_{ij} = k(x_i, x_j)$:

$$
\hat{\alpha} = \arg\min_\alpha \lVert K\alpha - y\rVert^2 + \lambda \alpha^T K \alpha.
$$

The optimum $\hat\alpha = (K + \lambda I)^{-1} y$, and the prediction at a new point is

$$
\boxed{\hat f(x) = k(x, X) (K + \lambda I)^{-1} y}
$$

where $k(x, X) \in \mathbb{R}^n$ is the row vector of kernel evaluations between the test point and the training set.

This is the **kernel ridge regression** estimator.  Compare to ordinary ridge $\hat w = (X^T X + \lambda I)^{-1} X^T y$ - same structure, different inner products.  For a linear kernel they coincide.

### Connection to Gaussian Processes

Put a Gaussian process prior $f \sim \mathcal{GP}(0, k)$ on the function, observe $y = f(X) + \epsilon$ with $\epsilon \sim \mathcal{N}(0, \sigma^2 I)$, and compute the posterior.  The posterior mean is

$$
\mathbb{E}[f(x) \mid y] = k(x, X) (K + \sigma^2 I)^{-1} y
$$

which is **exactly** the KRR estimator with $\lambda = \sigma^2$.  Same math, different story.  KRR says "regularize with an RKHS norm"; GP says "put a Gaussian prior with covariance $k$ and condition on data".  You end up in the same place because the RKHS norm and the Gaussian log-density differ by a constant.

Worth noting: the GP posterior also gives you a variance

$$
\mathrm{Var}[f(x) \mid y] = k(x,x) - k(x, X)(K + \sigma^2 I)^{-1} k(X, x)
$$

which KRR doesn't give you directly.  If you want uncertainty, GP is the way.  If you only want the point estimate, they are the same computation.

(n.b. the "kernel mean" in the GP prior is whatever you set; the posterior mean is what gets reshaped by the data.  If your prior mean is $m(x) \neq 0$, replace $y$ with $y - m(X)$ above and add $m(x)$ back at the end.)

## Gaussian Processes, Slightly Less Briefly

A Gaussian process $f \sim \mathcal{GP}(m, k)$ is a distribution over functions such that any finite collection $(f(x_1), \ldots, f(x_n))$ is jointly Gaussian with mean $(m(x_1), \ldots, m(x_n))$ and covariance $[k(x_i, x_j)]$.  The kernel is the covariance function; the RKHS norm penalizes "rough" functions relative to this covariance.

Draws from a GP almost surely do **not** lie in the RKHS (the RKHS is a "thin" subset of the support of the prior - a measure-zero set in general).  This is a famous confusion point.  The RKHS is where the posterior mean lives; the draws themselves are rougher.  The relation between the two involves Cameron-Martin style stuff that I will leave as an exercise.

## The Kernel Zoo

Your choice of kernel determines everything about the resulting RKHS.  Here are the big ones.

**RBF / Gaussian:** $k(x,y) = \exp(-\lVert x-y\rVert^2 / 2\sigma^2)$.  Infinitely smooth, universal, characteristic (defined below).  The default for "I don't know what I want".  Bandwidth $\sigma$ controls locality.

**Matérn:** a family parameterized by smoothness $\nu > 0$:

$$
k_\nu(x,y) = \frac{2^{1-\nu}}{\Gamma(\nu)}\left(\frac{\sqrt{2\nu}\, r}{\ell}\right)^\nu K_\nu\left(\frac{\sqrt{2\nu}\, r}{\ell}\right), \quad r = \lVert x - y\rVert
$$

where $K_\nu$ is a modified Bessel function.  Functions in $\mathcal{H}_\nu$ are $\lceil\nu\rceil - 1$ times differentiable.  As $\nu \to \infty$, Matérn $\to$ RBF.  Use Matérn when you care about the smoothness assumption.  Popular: $\nu = 3/2$ (once differentiable), $\nu = 5/2$ (twice).

**Polynomial:** $k(x,y) = (\langle x,y\rangle + c)^d$.  Feature space is degree-$\leq d$ polynomials.  Finite-dimensional RKHS, not universal.

**Linear:** $k(x,y) = \langle x,y\rangle$.  Kernel ridge with linear kernel = ordinary ridge.

**String, graph, and structured kernels:** defined on non-Euclidean domains.  Convolution kernels on strings for NLP, Weisfeiler-Lehman or random-walk kernels on graphs, diffusion kernels on manifolds.  The machinery is the same as long as you can write down a PSD kernel.

### Building Kernels from Other Kernels

Positive definiteness is preserved under a surprising number of operations, which means you can build bespoke kernels from simpler ones.  If $k_1, k_2$ are PSD kernels, then so are:

- $k_1 + k_2$ (sum),
- $k_1 \cdot k_2$ (pointwise product),
- $\alpha k_1$ for $\alpha \geq 0$,
- $f(x) k_1(x,y) f(y)$ for any $f : \mathcal{X} \to \mathbb{R}$,
- $k_1(\psi(x), \psi(y))$ for any map $\psi$,
- $\exp(k_1)$ (from the series representation),
- $\lim_n k_n$ if the limit exists pointwise and the $k_n$ are PSD.

These let you compose kernels for structured data: e.g. a kernel on sequences-of-vectors by summing an RBF kernel over pairs of elements.  This is the "kernel engineering" side of the subject, and it is genuinely useful when your data is not just a flat vector in $\mathbb{R}^d$.

### Universal and Characteristic

Two properties you often want your kernel to have:

- **Universal:** $\mathcal{H}_k$ is dense in $C(\mathcal{X})$ (continuous functions on a compact set).  Means you can approximate any continuous function arbitrarily well in sup-norm.  Required for consistency of kernel regression.
- **Characteristic:** the kernel mean embedding $P \mapsto \mu_P := \mathbb{E}_{X \sim P}[k(X, \cdot)]$ is injective on probability measures.  Means MMD is a proper metric on distributions (not just a pseudometric).

RBF and Matérn are both universal and characteristic on $\mathbb{R}^d$.  Polynomial kernels are neither.  The precise conditions (Steinwart-Christmann) come down to the kernel's Fourier transform having full support.

## The Spectral Picture

Mercer gives us $k(x,y) = \sum_i \lambda_i \phi_i(x) \phi_i(y)$ with $\lambda_1 \geq \lambda_2 \geq \ldots \geq 0$.  The eigenvalue decay rate controls almost everything about the learning problem.

- **Polynomial decay** $\lambda_i \sim i^{-\beta}$: typical for Matérn with finite $\nu$; gives minimax rates for learning that depend on $\beta$.
- **Exponential decay** $\lambda_i \sim e^{-ci}$: typical for RBF; gives very fast rates but also "spectral bias" - the method has strong implicit preferences for low-index eigenfunctions.

The $\phi_i$ are not arbitrary.  For a translation-invariant kernel on $\mathbb{R}^d$, they are essentially Fourier modes, and $\lambda_i$ is the Fourier transform of $k$.  So RBF's exponential decay means high-frequency components are crushed.

This is **spectral bias** - the recent-ish NTK literature observed that wide neural networks trained with gradient descent behave like kernel regression with a specific kernel (the NTK), and this kernel has eigenfunctions that are approximately Legendre-like polynomials with fast-decaying eigenvalues.  Low-frequency parts of the target function are learned first; high-frequency parts last.  Same phenomenon as in kernel ridge.

The effective dimension $N(\lambda) := \sum_i \lambda_i / (\lambda_i + \lambda)$ quantifies how many eigenfunctions you can "resolve" given regularization $\lambda$.  It replaces the raw dimension $d$ in generalization bounds.  For RBF, $N(\lambda)$ grows polylogarithmically in $1/\lambda$; for Matérn, polynomially.

### Bias-Variance in the Spectral Basis

Here's the spectral picture of KRR in one paragraph.  Write the target function as $f^*(x) = \sum_i a_i \phi_i(x)$ and the estimator as $\hat f = \sum_i \hat a_i \phi_i$.  In expectation over the noise, $\hat a_i = \frac{\lambda_i}{\lambda_i + \lambda/n} a_i$ (approximately, for large $n$).  Components with $\lambda_i \gg \lambda/n$ are retained; components with $\lambda_i \ll \lambda/n$ are zeroed out.  The regularizer $\lambda$ acts as a cutoff in the eigenbasis.  Bias comes from the low-$\lambda_i$ components being crushed; variance comes from noise bleeding into the kept components.  Minimize the sum and you get the classical bias-variance trade-off expressed spectrally.

This is also the cleanest view of why KRR's implicit bias matches gradient descent on wide networks: both perform "soft-thresholded" recovery in an eigenbasis, with eigenvalues determined by the kernel.

## Kernel Mean Embeddings of Distributions

Given a distribution $P$ on $\mathcal{X}$, its **kernel mean embedding** is

$$
\mu_P := \mathbb{E}_{X \sim P}[k(X, \cdot)] \in \mathcal{H}.
$$

Because $\mathcal{H}$ is a Hilbert space, $\mu_P$ is an honest-to-god vector, and you can do linear algebra with distributions.  For example:

**MMD (Maximum Mean Discrepancy):** $\mathrm{MMD}(P,Q) := \lVert \mu_P - \mu_Q\rVert_\mathcal{H}$.  This is a distance between distributions, and is computable from samples:

$$
\widehat{\mathrm{MMD}}^2 = \frac{1}{n^2}\sum_{ij} k(x_i, x_j) + \frac{1}{m^2}\sum_{ij} k(y_i, y_j) - \frac{2}{nm}\sum_{ij} k(x_i, y_j).
$$

Two-sample tests, generative modeling (MMD-GANs), distribution regression - all built on this.

**HSIC (Hilbert-Schmidt Independence Criterion):** kernel-based independence test.  Embed the joint distribution $P_{XY}$ and the product $P_X \otimes P_Y$ as elements of a tensor-product RKHS, take the squared distance.  Zero iff $X \perp Y$ (for characteristic kernels).

This is the kernel toolkit for comparing distributions.  There is a much longer story here - see the "Probability as Operators" seed for how this generalizes to operator-valued embeddings, conditional mean embeddings, and the whole machinery of kernelized Bayesian inference.

### Sanity Check: What the Embedding Buys You

Why does it help to think of a distribution as a vector?  Because once it is a vector, every linear operation is on the table.  Differences, projections, least-squares fits, orthogonal decompositions - all of classical Hilbert-space geometry now applies to distributions.

Concretely: MMD gives you a distance that is computable from samples at $O(n^2)$ cost and is a proper metric when the kernel is characteristic.  HSIC gives you an independence test with no parametric assumptions.  Kernel-based two-sample and independence tests routinely beat their classical competitors on real data because they are sensitive to all moments, not just the first two.

The trade-off: the kernel choice matters, and you need enough samples to estimate the embedding.  There is no free lunch, but the lunch is pretty good.

## Kernels from Neural Networks

Two regimes where neural networks become kernel machines:

**NTK (Neural Tangent Kernel):** in the infinite-width limit with appropriate scaling, a neural network trained by gradient flow is equivalent to kernel regression with the kernel $k_\mathrm{NTK}(x,y) = \langle \nabla_\theta f(x), \nabla_\theta f(y)\rangle$ evaluated at initialization.  The kernel is **constant throughout training** (the "lazy regime").

**NNGP (Neural Network Gaussian Process):** a randomly initialized infinite-width neural network defines a GP on its outputs, with a specific kernel you can compute recursively layer by layer.

The NTK story explains a lot about wide neural networks - generalization, spectral bias, the implicit bias of SGD.  It does not explain finite-width feature learning, which is where the "not kernel" part of deep learning happens.  The interesting question is when you leave the kernel regime, and why.

One quick way to see the connection: at initialization, $f_\theta(x) \approx f_{\theta_0}(x) + \langle \nabla_\theta f_{\theta_0}(x), \theta - \theta_0\rangle$.  Gradient flow on squared loss makes $\theta - \theta_0$ stay small in the wide limit (the "lazy" regime), so this linearization is accurate throughout training.  Gradient flow on the linearized model is just kernel gradient flow with kernel $k_\mathrm{NTK}$.  Plug in $t = \infty$ with $\ell_2$ regularization and you get kernel ridge.

What breaks down in feature-learning regimes: the parameter movement is no longer small, and $\nabla_\theta f_\theta(x)$ actually evolves during training.  The kernel moves, which is exactly the claim that features are being learned.  Understanding this transition is one of the active frontiers.

More on this in a future seed on NTK / feature learning transitions.

## What's Next

The basic RKHS toolkit unlocks a whole district of ML.  Things I haven't covered but that follow naturally:

- **Nyström and random Fourier features:** how to scale kernel methods to large $n$ by approximating the Gram matrix (Nyström: low-rank subsample; RFF: Monte Carlo sample from the Fourier representation).  The key trick for making kernel methods work beyond $n = 10^4$.
- **Kernel PCA:** do PCA in feature space.  The resulting "principal components" are nonlinear features of your data.
- **Kernel CCA, kernel ICA, kernel $k$-means:** you can kernelize any method that only uses inner products.
- **Conditional mean embeddings:** $\mu_{Y\mid X=x}$ as an element of $\mathcal{H}_Y$.  Lets you do regression-of-distributions, kernel Bayes rule, and kernelized reinforcement learning.
- **Kernel mean shift:** nonparametric mode-finding using kernel density estimation.  The seed of a bunch of clustering and tracking methods.
- **Operator-valued kernels:** for vector-valued regression.  Multi-task learning, structured prediction.
- **Koopman operator analysis:** dynamical systems viewed through observables in an RKHS.  DMD, EDMD, kernel DMD - a very productive corner of applied math right now.
- **Geometric kernels:** kernels on manifolds, graphs, Lie groups.  You pick the kernel to respect the symmetry of your domain.
- **Deep kernels:** kernels parameterized by neural networks.  The NTK of a finite-width net, or a learned kernel in a composite GP.  The current frontier.

## tl;dr

- **RKHS:** a Hilbert space of functions where point evaluation is continuous.  Every such space has a reproducing kernel $k(x,y) = \langle k_x, k_y\rangle$.  Moore-Aronszajn: PSD kernels $\leftrightarrow$ RKHSs, bijectively.
- **Kernel trick:** compute inner products in feature space without materializing the features.  $k(x,y) = \langle\varphi(x), \varphi(y)\rangle$.
- **Representer theorem:** regularized ERM over $\mathcal{H}$ is solved in the span of the training kernels.  Infinite-dim optimization $\to$ $n$-dim optimization.
- **KRR = GP posterior mean:** same math, different story.  GP also gives variance.
- **Spectral picture:** Mercer decomposition; eigenvalue decay controls capacity and rates.  Spectral bias is just "low-$i$ eigenfunctions get learned first".
- **Kernel mean embeddings:** distributions as vectors in $\mathcal{H}$.  MMD, HSIC, the kernel toolkit for distribution-level objects.
- **Neural nets:** infinite-width nets are kernel machines (NTK, NNGP); finite-width ones aren't.

Please clap.

***

*See also: [Probability as Operators], [Spectral Theory for ML], [Random Features and Nyström].*

*Written with Claude.*
