---
title: "Information Geometry Basics"
date: 2026-04-18
motivation: "Probability distributions parametrized by some vector $\\theta$ form a manifold. The naive thing is to put the Euclidean metric on $\\theta$ and call it a day. That metric is a lie - it depends on how you picked the coordinates. There's a better one, and it's essentially unique."
background: "Comfortable with Riemannian geometry at the level of 'metric tensor, connection, geodesic'. Comfortable with MLE, KL divergence, exponential families.  The payoff is that a lot of statistics and ML ends up looking like classical mechanics on a very specific manifold."
llm: "Claude"
tags: [seed]
math: true
---

# Information Geometry Basics

## The One-Line Pitch

A family of probability distributions $\{p_\theta\}$ is a manifold.  The Fisher information metric is the right Riemannian metric on it.  Everything else - natural gradient, EM, replicator dynamics, exponential families, MLE asymptotics - is geometry in that metric.

That's the whole seed.  The rest is how to actually use it.

## Why You Can't Just Use Euclidean $\theta$

Start with a simple example.  A Gaussian family $\mathcal{N}(\mu, \sigma^2)$, parametrized by $\theta = (\mu, \sigma)$.  Put the Euclidean metric on $(\mu, \sigma)$ space.  Now ask: is $\mathcal{N}(0, 1)$ "closer" to $\mathcal{N}(0, 2)$ or to $\mathcal{N}(0.5, 1)$?

Euclidean says: same distance, $0.5$ each.  But the distributions themselves are not equally distinguishable.  A one-standard-deviation shift of the mean and a doubling of the variance are completely different operations, and any reasonable notion of "how different are these distributions" should reflect that.

Worse: reparametrize.  Use $\theta' = (\mu, \log \sigma)$ instead.  The Euclidean metric in $\theta'$ coordinates disagrees with the one in $\theta$ coordinates.  Which is "right"?  Neither.  The whole setup is broken because the parametrization is arbitrary - you're measuring the chart, not the manifold.

What you want is a metric that depends only on the distributions, not on how you happen to name them.  Something invariant under reparametrization.

## Fisher Information Metric

Here's the object.  Given a family $p_\theta(x)$, define

$$
g_{ij}(\theta) = \mathbb{E}_{p_\theta}\!\left[ \partial_i \log p_\theta \cdot \partial_j \log p_\theta \right]
$$

where $\partial_i = \partial / \partial \theta^i$.  This is the **Fisher information matrix**, and regarded as a tensor on $\theta$-space it's the **Fisher metric**.

Two other forms of the same object, both useful:

$$
g_{ij} = -\mathbb{E}_{p_\theta}\!\left[ \partial_i \partial_j \log p_\theta \right]
\qquad
g_{ij} = 4 \int \partial_i \sqrt{p_\theta}\, \partial_j \sqrt{p_\theta}\, dx
$$

The first is expected negative Hessian of log-likelihood (equal to the score covariance because the score has mean zero - differentiate $\int p_\theta \, dx = 1$ twice).  The second shows it's the pullback of the round metric on the sphere of $L^2$ functions via $\theta \mapsto \sqrt{p_\theta}$.  That's a nice picture: distributions are points on the unit sphere in $L^2$, and the Fisher metric is the intrinsic geometry inherited from there.

### Where It Comes From: The KL Expansion

Take two nearby distributions $p_\theta$ and $p_{\theta + d\theta}$ and expand the KL divergence.

$$
\mathrm{KL}(p_\theta \lVert p_{\theta + d\theta}) = \int p_\theta \log \frac{p_\theta}{p_{\theta + d\theta}}\, dx
$$

Taylor expand $\log p_{\theta + d\theta} = \log p_\theta + \partial_i \log p_\theta \, d\theta^i + \tfrac{1}{2} \partial_i \partial_j \log p_\theta \, d\theta^i d\theta^j + \ldots$  Take the expectation.  The first-order term $\mathbb{E}[\partial_i \log p_\theta]$ vanishes (score has mean zero).  You're left with

$$
\mathrm{KL}(p_\theta \lVert p_{\theta + d\theta}) = \tfrac{1}{2}\, g_{ij}(\theta)\, d\theta^i d\theta^j + O(d\theta^3).
$$

So the Fisher metric is literally the Hessian of KL at the diagonal.  KL is asymmetric in general, but to second order it's symmetric and positive definite and gives you exactly $g_{ij}$.

This is the cleanest way to remember the definition.  Fisher = $\tfrac{1}{2}$ Hessian of KL at coincident points.

### Chentsov's Theorem (The Uniqueness)

Chentsov (1972) proved: on finite discrete probability simplices, the Fisher information metric is the **unique** (up to scale) Riemannian metric that is invariant under sufficient statistics (equivalently: under Markov morphisms, or reparametrizations that preserve information).

The moral is strong: if you want a metric on distributions that doesn't depend on the coordinate system and behaves nicely under coarse-graining, you don't have a choice.  Up to a multiplicative constant, Fisher is it.  The proof is combinatorial and not enlightening; I'm happy to skip it and just use the result.

There are extensions to continuous families (Ay-Jost-Le-Schwachhöfer) with some extra technical hypotheses but the same moral: Fisher is canonical.  Fight me if you disagree, but bring Chentsov's ghost.

## Exponential Families: The Canonical Setting

An **exponential family** is

$$
p_\theta(x) = h(x)\, \exp\!\left( \theta^i T_i(x) - \psi(\theta) \right)
$$

where $T_i$ are sufficient statistics, $\theta^i$ are the **natural parameters**, and $\psi(\theta)$ is the log-partition (normalizer).  This swallows most of the distributions you care about: Gaussians, Bernoullis, Poissons, categoricals, Boltzmann machines, exponential random graph models, etc.

The log-partition does the heavy lifting.  Differentiate twice:

$$
\partial_i \psi = \mathbb{E}[T_i] =: \eta_i
\qquad
\partial_i \partial_j \psi = \mathrm{Cov}(T_i, T_j) = g_{ij}(\theta).
$$

First line: the gradient of $\psi$ is the **expectation parameters** $\eta$.  Second line: the Hessian of $\psi$ is the Fisher metric.  One scalar function, $\psi$, generates both the parametrization map and the metric.  Exponential families are the flat geometries of information geometry.

The Legendre dual of $\psi$ is another convex function $\phi$ with $\phi(\eta) + \psi(\theta) = \theta^i \eta_i$ and $\nabla \phi = \theta$.  You now have two coordinate systems on the same manifold:

- $\theta$: natural parameters
- $\eta$: expectation parameters

connected by $\eta = \nabla \psi(\theta)$ and inversely $\theta = \nabla \phi(\eta)$.  These are **dual affine coordinates** in a sense I'll make precise in a moment.

### Why MLE Is So Nice Here

Given iid data $x_1, \ldots, x_N$, the log-likelihood is

$$
\ell(\theta) = \theta^i \sum_n T_i(x_n) - N \psi(\theta) + \text{const}.
$$

$\nabla_\theta \ell = 0$ gives $\nabla \psi(\theta) = \tfrac{1}{N} \sum_n T(x_n)$, i.e. the MLE is the $\theta$ whose expected sufficient statistic equals the sample sufficient statistic.  Match the moments.

The Hessian of $-\ell$ is $N \cdot g_{ij}(\theta)$ - the Fisher metric.  So **MLE by Newton's method is gradient descent in the Fisher metric**.  More on this in the natural gradient section.

## Dual Connections and the Alpha-Family

Here's where it gets a little weird and a lot beautiful.  On a generic Riemannian manifold there's a unique torsion-free metric-compatible connection, the Levi-Civita connection.  Information geometry has Levi-Civita, but it's usually *not* the connection you want.  Instead there's a whole one-parameter family of connections indexed by $\alpha \in \mathbb{R}$, with two special values.

Define the **alpha-connection** $\nabla^{(\alpha)}$ by

$$
\Gamma^{(\alpha)}_{ij,k}(\theta) = \mathbb{E}\!\left[\left(\partial_i \partial_j \log p + \frac{1 - \alpha}{2}\, \partial_i \log p\, \partial_j \log p\right)\partial_k \log p\right].
$$

The two special values:

- $\alpha = 1$: the **e-connection** (exponential).  Its geodesics in an exponential family are straight lines in $\theta$-coordinates.  Mixtures of $\log p$ are geodesic.
- $\alpha = -1$: the **m-connection** (mixture).  Geodesics are straight lines in $\eta$-coordinates.  Convex combinations $t p_1 + (1-t) p_2$ are m-geodesic.

Neither is Levi-Civita (that would be $\alpha = 0$).  Both are **flat** on exponential families - their curvature vanishes - but in different coordinate systems.  They are **dual** with respect to the Fisher metric:

$$
X \langle Y, Z \rangle = \langle \nabla^{(e)}_X Y, Z \rangle + \langle Y, \nabla^{(m)}_X Z \rangle.
$$

This is the defining equation of a **dually flat** structure.  Compare to Levi-Civita compatibility $X\langle Y, Z\rangle = \langle \nabla_X Y, Z\rangle + \langle Y, \nabla_X Z\rangle$ - there you use the same connection on both sides; here you use two different ones that are dual partners.  Amari was the one who systematized all this.

### Generalized Pythagoras

The payoff: in a dually flat manifold with divergence $D$ (which turns out to be KL for exponential families), if $p$, $q$, $r$ are three points such that the e-geodesic from $q$ to $p$ is perpendicular (in Fisher metric) to the m-geodesic from $q$ to $r$, then

$$
D(p \lVert r) = D(p \lVert q) + D(q \lVert r).
$$

Pythagoras, but for KL.  This is the engine behind information projections: when you project a distribution onto a submanifold, the residual divergence and the projected divergence add.  EM is alternating Pythagorean projections (e-projection onto the posterior, m-projection onto the model).  Variational inference is an m-projection onto a tractable family.  Maximum entropy is an e-projection from the uniform.

You pick up a lot of algorithms by noticing that they're Pythagorean.

## Bregman Divergences

Let $\phi: \Omega \to \mathbb{R}$ be strictly convex and differentiable.  The **Bregman divergence** is

$$
D_\phi(p \lVert q) = \phi(p) - \phi(q) - \langle \nabla \phi(q), p - q \rangle.
$$

Geometrically: the gap between $\phi(p)$ and its linear approximation around $q$ evaluated at $p$.  By convexity this is non-negative and zero iff $p = q$.  It's not a metric (asymmetric, doesn't satisfy triangle inequality), but it's a legitimate notion of "distance" for many purposes.

Examples:

- $\phi(p) = \tfrac{1}{2}\lVert p \rVert^2$: $D_\phi = \tfrac{1}{2}\lVert p - q \rVert^2$, squared Euclidean.
- $\phi(p) = \sum_i p_i \log p_i$ (negative entropy on the simplex): $D_\phi = \mathrm{KL}(p \lVert q)$.  This is the big one.
- $\phi(p) = -\sum_i \log p_i$ (Burg entropy, positive reals): $D_\phi$ = Itakura-Saito, used in audio.

The KL-as-Bregman observation is the geometric heart of exponential families.  Recall $\phi$ is Legendre dual to the log-partition $\psi$.  Write the KL between two exponential-family distributions in expectation parameters:

$$
\mathrm{KL}(p_{\eta_1} \lVert p_{\eta_2}) = \phi(\eta_1) - \phi(\eta_2) - \langle \nabla \phi(\eta_2), \eta_1 - \eta_2 \rangle = D_\phi(\eta_1 \lVert \eta_2).
$$

KL in expectation parameters is Bregman with potential $\phi$.  By duality, KL in natural parameters is Bregman with potential $\psi$, but with the arguments swapped: $\mathrm{KL}(p_{\theta_1} \lVert p_{\theta_2}) = D_\psi(\theta_2 \lVert \theta_1)$.  The swap of arguments is what the e-m duality looks like at the level of divergences.

Every dually flat structure arises from a Bregman divergence, and vice versa.  That's a theorem of Amari-Nagaoka.  So "dually flat manifold" and "Bregman divergence" are the same animal viewed from two angles.

## Natural Gradient

Vanilla gradient descent on a loss $L(\theta)$ updates $\theta \leftarrow \theta - \epsilon \nabla L$.  The gradient $\nabla L$ is a covector, a one-form.  To turn it into a vector (a direction to move in) you need a metric.  Vanilla GD implicitly uses the Euclidean metric in $\theta$-coordinates, which, as we established, is a lie.

The **natural gradient** uses the Fisher metric:

$$
\tilde{\nabla} L = g^{-1} \nabla L.
$$

Steepest descent under the constraint that the infinitesimal step has fixed KL-length, not fixed Euclidean-length.  Equivalently: reparametrization-invariant.  If you change coordinates, the natural gradient transforms as a vector and $g^{-1}$ transforms oppositely so that the update is intrinsic.

### Why It's Actually Newton's Method In Disguise (For Exp Fams)

Recall for an exponential family MLE, the Hessian of negative log-likelihood is the Fisher information.  Newton's method updates

$$
\theta \leftarrow \theta - H^{-1} \nabla L = \theta - g^{-1} \nabla L = \theta - \tilde{\nabla} L.
$$

Newton = natural gradient with step 1, when $L$ is the NLL of an exponential family.  This is why natural gradient converges so fast on these problems - it's second-order without having to compute a separate Hessian.  For general (non-exponential-family) losses it's not exactly Newton, but it's still a principled second-order-ish step.

### Why It Matters Beyond MLE

Policy gradient in RL: the loss surface depends wildly on policy parametrization.  Natural policy gradient (Kakade, then TRPO, then PPO as a heuristic approximation) uses Fisher in policy space.

Neural networks: the Fisher matrix for an NN is the NTK-adjacent object that Amari and others pushed.  K-FAC approximates it block-diagonally.  In practice this is expensive and modern practice uses preconditioners (Adam's diagonal) that approximate a diagonal Fisher, which is why Adam-family optimizers work better than SGD on many problems.

Bayesian updating: the posterior is an m-projection (or e-projection, depending on formulation) onto a constrained family.  Natural gradient steps are geometrically natural updates.

## The Replicator Bridge (Preview)

Here's a teaser that I'll develop in the natural-selection seed.  Consider the probability simplex $\Delta^{n-1}$ with coordinates $p_i$ ($\sum p_i = 1$).  Equip it with the **Shahshahani metric**, which is the Fisher metric for the categorical family:

$$
g_{ij}(p) = \frac{\delta_{ij}}{p_i}.
$$

Suppose each $p_i$ is the frequency of type $i$ in a population, and fitness of type $i$ is $f_i(p)$ with mean fitness $\bar{f}(p) = \sum_i p_i f_i(p)$.  The **replicator equation** is

$$
\dot{p}_i = p_i (f_i - \bar{f}).
$$

Types above average grow, types below average shrink.  Classic evolutionary dynamics.

The claim: **the replicator equation is natural gradient ascent on mean fitness $\bar{f}$ in the Shahshahani/Fisher metric.**  Explicitly, if $L(p) = -\bar{f}(p)$ then $-g^{-1}(p) \nabla L = p_i(f_i - \bar{f})$ (with appropriate handling of the simplex constraint).

Selection is gradient ascent.  The "gradient" is with respect to the one metric that knows $p$ is a probability distribution.  And everything you know about replicator dynamics - Fisher's fundamental theorem, Lyapunov functions, the entropic flow - is information geometry in disguise.

More in the selection seed.

## What's Next

A bunch of loose threads to pull on, depending on where you want to go.

- **Information projections and EM.**  EM is alternating e- and m-projections.  The E-step is an m-projection of the joint onto $p(z \vert x)$; the M-step is an e-projection onto the model family.  Clean and geometric.  Csiszár's alternating minimization theorem is the general statement.

- **Cramér-Rao as a geometric bound.**  The Cramér-Rao inequality $\mathrm{Cov}(\hat{\theta}) \succeq g^{-1}$ is the statement that the Fisher metric is the minimal covariance of any unbiased estimator.  Geometrically: you can't estimate parameters better than the intrinsic distinguishability of the distributions allows.

- **Second-order optimizers.**  K-FAC, Shampoo, natural gradient variants all approximate $g^{-1}$ in different ways.  The design space is: how do you cheaply invert / factor the Fisher.

- **Quantum information geometry.**  Replace classical distributions with density matrices, KL with quantum relative entropy, Fisher metric with a family of quantum Fisher metrics (Bures, Kubo-Mori, etc.).  Chentsov-style uniqueness fails - there's a whole zoo of quantum Fisher metrics, parametrized by operator monotone functions (Petz classification).  The lack of uniqueness is itself informative.

- **Wasserstein geometry as an alternative.**  Fisher cares about pointwise likelihood ratios; Wasserstein cares about transport cost.  Different answers to "how far apart are these distributions".  For smooth distributions on $\mathbb{R}^n$, they give genuinely different geometries and different gradient flows (the Fokker-Planck equation is Wasserstein gradient flow of free energy; replicator is Fisher gradient flow of mean fitness).

- **$\alpha$-divergences and Rényi entropy.**  The alpha-connections come with a family of divergences that interpolate between KL and reverse-KL; Rényi-$\alpha$ is in the same family.  Useful when you want to tune how aggressively a projection "mode-matches" vs. "mean-matches".

***

Fisher metric, exponential families, dual connections, Bregman divergences, natural gradient.  If you know these five things and how they fit, you know information geometry basics.  The rest is applications and generalizations.

Please clap.

*Written with Claude.*
