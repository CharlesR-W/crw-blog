---
title: "Otto Calculus and Wasserstein"
date: 2026-04-18
motivation: "The space of probability measures has a natural Riemannian-ish structure, and a bunch of PDEs you already know are gradient flows in it.  Fokker-Planck is literally just downhill motion for free energy, measured with the right ruler.  Once you see this, you get a free-energy landscape on distribution space and a bunch of functional inequalities fall out almost by accident."
background: "Multivariable calculus (gradient, divergence, integration by parts), some exposure to Fokker-Planck or Langevin diffusion, and enough comfort with functional derivatives that $\\delta F / \\delta \\mu$ doesn't scare you.  No need to have seen optimal transport before."
llm: "Claude"
tags: [seed]
math: true
---

# Otto Calculus and Wasserstein

## TL;DR

There's a geometry on the space of probability measures where:

- distances come from optimal transport ($W_2$),
- tangent vectors at $\mu$ are gradient fields $\nabla \phi$,
- and a whole zoo of PDEs you know - Fokker-Planck, heat equation, porous medium - are gradient flows of recognizable functionals (entropy, free energy, etc.).

Otto calculus is the "physicist's dictionary" for this geometry.  It is formal - making every step fully rigorous is a career - but formally it is light, and the payoff is large.  You basically only need gradient, divergence, and $W_2^2$.

I wrote a previous post on [KL vs optimal transport](/2025/07/11/KL-Divergence-Geometric-Naturalness-and-Optimal-Transport) which is the natural prequel to this one.  Go read it if "why $W_2$ at all" isn't already obvious.  This post is about the differential geometry that $W_2$ gives you once you accept it.

## A physicist's orientation

The geometric picture is going to feel more plausible if you think of it like this.  In thermodynamics, a state of a gas is a point in some low-dimensional parameter space (temperature, pressure, volume, whatever).  The free energy is a scalar function on that parameter space.  Equilibrium is where free energy is minimized.  Approach to equilibrium is downhill motion.

Now up the ante: the "state" is a full distribution $\mu$ on microstates, not a handful of macroscopic observables.  The free energy is still a scalar function, $F[\mu]$, defined on the much-bigger space of distributions.  Equilibrium (the Gibbs distribution) is still where $F$ is minimized.  And approach to equilibrium is still downhill motion - but now you need a sensible notion of "downhill" on the space of distributions.

KL doesn't give you that, because it's not a metric (asymmetric, triangle inequality fails, etc.).  Information geometry uses Fisher information as a Riemannian metric on finite-parameter families and it's a great tool, but it doesn't scale to the infinite-dimensional $\mathcal{P}_2$ in a natural way.  Wasserstein does.  And once you have the metric, "gradient flow" has a meaning, "geodesics" have a meaning, and the physical intuition of downhill motion on a free-energy landscape is not just an analogy - it's literally what's happening.

That's the payoff.  You already think in terms of free energy minimization for macroscopic systems.  Otto calculus lets you do the same for distributions, with the same mathematical structure, just upgraded to an infinite-dimensional manifold.

## Why you might care

Here's the one-sentence sell: **the Fokker-Planck equation is gradient descent of free energy on a Riemannian-ish manifold of probability measures, where the metric is $W_2$.**  This was the Jordan-Kinderlehrer-Otto (JKO) observation in 1998, cleaned up geometrically by Otto in 2001.

Why that matters:

- It gives free-energy landscapes on distribution space.  You can talk about "downhill" for a PDE the same way you do for a particle in a potential.
- Convergence rates of stochastic dynamics (Langevin, MALA, ULA, diffusion models) become curvature statements.  "Log-Sobolev" = "the free energy is uniformly convex along transport geodesics".
- A lot of functional inequalities (HWI, Talagrand, log-Sobolev, Poincaré) are just different cross-sections of one geometric story.
- Displacement interpolation gives you an honest notion of "straight line between two distributions" that respects the geometry of the underlying space.  KL does not.

If any of that sounds like the kind of thing you'd want to understand before touching score-based diffusion models or mean-field sampling, you're in the right place.

## The object: $W_2$

Quick recap.  Given two probability measures $\mu, \nu$ on $\mathbb{R}^d$, the Wasserstein-2 distance is

$$
W_2^2(\mu, \nu) = \inf_{\pi \in \Pi(\mu, \nu)} \int \lVert x - y \rVert^2 \, d\pi(x, y),
$$

where $\Pi(\mu, \nu)$ is the set of joint distributions with marginals $\mu, \nu$.  Think: sand pile $\mu$ gets rearranged into sand pile $\nu$, and you pay squared distance per unit mass moved.  The infimum is the minimum transport cost.

Two things worth knowing:

**Kantorovich duality.**  The minimization has a dual:

$$
W_2^2(\mu, \nu) = \sup_{\varphi, \psi} \left[ \int \varphi \, d\mu + \int \psi \, d\nu \right]
$$

over pairs $(\varphi, \psi)$ satisfying $\varphi(x) + \psi(y) \le \lVert x - y \rVert^2$.  The potentials $\varphi, \psi$ are the Kantorovich potentials.  Duality buys you a way to estimate $W_2$ from samples without ever writing down the transport plan.

**Brenier.**  Under mild conditions (e.g. $\mu$ absolutely continuous), the optimal plan is deterministic and given by a map $T: \mathbb{R}^d \to \mathbb{R}^d$, which is itself the gradient of a convex function:

$$
T(x) = \nabla u(x), \quad u \text{ convex}, \quad T_\# \mu = \nu.
$$

This is the Brenier theorem, and it's why $W_2$ has such nice geometric structure - optimal transport is potential flow.

## The Riemannian-ish structure (Otto, 2001)

Here is where we put on the physicist hat and ignore some analysts' polite coughing.

**Tangent vectors.**  A curve $t \mapsto \mu_t$ in the space of measures is a family of densities (say).  What's a tangent vector at $\mu$?  You need a "direction to perturb $\mu$ in".  The right answer, from continuity, is: a tangent vector is a velocity field.  Pick $\phi: \mathbb{R}^d \to \mathbb{R}$; the velocity field $v = \nabla \phi$ advects $\mu$ via the continuity equation

$$
\partial_t \mu + \nabla \cdot (\mu \, \nabla \phi) = 0.
$$

So tangent vectors at $\mu$ are gradients $\nabla \phi$.  Why gradients and not general vector fields?  Because curl-free vector fields are the ones with minimal kinetic energy that produce a given $\partial_t \mu$ - this is the variational content of Otto's identification.  Any solenoidal (divergence-free when weighted by $\mu$) piece transports no mass and is "gauge".

Quick derivation of the continuity equation if you haven't seen it: let $\mu_t$ be the pushforward of $\mu_0$ under the flow $\Phi_t$ of $v$, i.e. each particle at $x_0$ goes to $\Phi_t(x_0)$.  Mass conservation in the integrated form is $\int_{\Phi_t(A)} \mu_t = \int_A \mu_0$ for any region $A$.  Differentiating in $t$ and applying the divergence theorem gives $\partial_t \mu_t + \nabla \cdot (\mu_t v) = 0$.  That's continuity.  The "$v = \nabla \phi$" restriction is an additional assumption, justified by the minimum-kinetic-energy argument above.

**Inner product.**  The $W_2$ inner product on tangent vectors at $\mu$ is

$$
\langle \nabla \phi_1, \nabla \phi_2 \rangle_\mu = \int \nabla \phi_1 \cdot \nabla \phi_2 \, d\mu.
$$

This is weighted $L^2$.  The corresponding norm $\lVert \nabla \phi \rVert_\mu^2 = \int \lVert \nabla \phi \rVert^2 \, d\mu$ is the kinetic energy of the velocity field $\nabla \phi$ against $\mu$.

There's a quick sanity check that "gradients only" is the right tangent space.  Hodge decomposition on $\mathbb{R}^d$: any vector field splits as $v = \nabla \phi + v^\perp$ with $\nabla \cdot (\mu v^\perp) = 0$.  The orthogonal piece $v^\perp$ transports no mass (because it has no divergence against $\mu$), so for the purpose of moving $\mu$ around, it's redundant.  Among all vector fields $v$ producing a given $\partial_t \mu$, the gradient $\nabla \phi$ has the minimum kinetic energy $\int \lVert v \rVert^2 \mu$ - this is just the Pythagorean theorem for the Hodge decomposition.  So gradients are the "efficient" tangent vectors, and identifying tangent space with gradients modulo constants is natural.

**Why this is $W_2$.**  The geodesic distance induced by this metric (integrate $\sqrt{\text{kinetic energy}}$ along paths, minimize) is exactly $W_2$.  That's the Benamou-Brenier dynamic formulation, which we'll hit in a moment.  Taking this seriously, the space of probability measures $\mathcal{P}_2(\mathbb{R}^d)$ is an (infinite-dimensional, ill-behaved, formally) Riemannian manifold.

**Honest moment.**  "Ill-behaved" is doing work.  The tangent space is a weighted $L^2$ closure of gradients, the manifold is not a manifold in any standard sense, singular measures make things weird, and when $\mu$ has zero density somewhere you lose uniqueness.  A lot of the calculus below is formal.  It still gives correct answers, in the sense that the resulting PDEs and inequalities are true theorems.  Ambrosio-Gigli-Savaré is where you go if you want this made rigorous; it's a book and a half of work.

### A cartoon of the identification

If you want a toy case to anchor the formal manipulations: restrict to $d = 1$ and consider absolutely continuous measures $\mu(x) \, dx$.  Then the cumulative distribution function $F_\mu(x) = \int_{-\infty}^x \mu$ is monotone, and it turns out

$$
W_2^2(\mu, \nu) = \int_0^1 \lVert F_\mu^{-1}(q) - F_\nu^{-1}(q) \rVert^2 \, dq.
$$

So in 1D, $W_2$ is just the $L^2$ distance between quantile functions.  That's as concrete as it gets.  All the Otto-calculus machinery in this case reduces to ordinary calculus on quantile functions.  In higher dimensions there's no such slick coordinate chart - you have to do it abstractly - but the 1D picture keeps the formalism honest.

## Wasserstein gradient and gradient flow

Given a functional $F: \mathcal{P}_2 \to \mathbb{R}$, the variational derivative $\delta F / \delta \mu$ is the thing satisfying

$$
\left. \frac{d}{d\epsilon} F[\mu + \epsilon \eta] \right\vert_{\epsilon=0} = \int \frac{\delta F}{\delta \mu}(x) \, \eta(x) \, dx
$$

for test perturbations $\eta$ with $\int \eta = 0$.  This is the "Euclidean" functional derivative - what you'd compute by pretending $\mu(x)$ is an independent variable for each $x$.

The **Wasserstein gradient** is obtained by pushing this through the metric identification.  A quick version: we want $\text{grad}_W F$ such that for any tangent vector $\nabla \phi$,

$$
\left. \frac{d}{dt} F[\mu_t] \right\vert_{t=0} = \langle \text{grad}_W F, \nabla \phi \rangle_\mu
$$

where $\mu_t$ solves $\partial_t \mu + \nabla \cdot (\mu \nabla \phi) = 0$.  Computing the left side via $\delta F / \delta \mu$ and integration by parts,

$$
\frac{d}{dt} F[\mu_t] = \int \frac{\delta F}{\delta \mu} \partial_t \mu = -\int \frac{\delta F}{\delta \mu} \nabla \cdot (\mu \nabla \phi) = \int \nabla \frac{\delta F}{\delta \mu} \cdot \nabla \phi \, d\mu.
$$

Comparing to the inner product, we read off

$$
\boxed{\text{grad}_W F = \nabla \frac{\delta F}{\delta \mu}.}
$$

This is the Otto dictionary.  The gradient in Wasserstein space is the spatial gradient of the variational derivative.

**The gradient flow** of $F$ is then

$$
\partial_t \mu = -\text{grad}_W F[\mu] \quad \text{(in the manifold)}
$$

which, translated back to a PDE via the continuity equation, reads

$$
\boxed{\partial_t \mu = \nabla \cdot \left(\mu \, \nabla \frac{\delta F}{\delta \mu}\right).}
$$

This is the master equation of Otto calculus.  Everything below is special cases.

**The JKO scheme.**  Why should you believe this is really a gradient flow?  Because you can construct it as the limit of a proximal algorithm.  Define

$$
\mu^{n+1} = \arg\min_{\mu} \left[ F[\mu] + \frac{1}{2\tau} W_2^2(\mu, \mu^n) \right]
$$

with time step $\tau$.  This is just "move to decrease $F$, but don't move too far in Wasserstein".  As $\tau \to 0$, JKO iterates converge to solutions of $\partial_t \mu = \nabla \cdot (\mu \nabla \delta F / \delta \mu)$.  Jordan-Kinderlehrer-Otto 1998.  The JKO scheme is the discrete analog of gradient descent; the PDE is its continuum limit.

Sanity check this reduces to the familiar thing in finite dimensions: on $\mathbb{R}^n$ with Euclidean metric, the proximal step is

$$
x^{n+1} = \arg\min_x \left[ f(x) + \frac{1}{2\tau} \lVert x - x^n \rVert^2 \right],
$$

whose stationarity condition is $0 = \nabla f(x^{n+1}) + (x^{n+1} - x^n)/\tau$, i.e. $x^{n+1} = x^n - \tau \nabla f(x^{n+1})$ - implicit Euler for $\dot x = -\nabla f$.  JKO is exactly this recipe with $\lVert \cdot \rVert^2$ replaced by $W_2^2$ and $\nabla f$ replaced by the Otto gradient.  Same structure, fancier manifold.

## Fokker-Planck as gradient flow of free energy

Now the payoff.  Consider the free energy functional

$$
F[\mu] = \int \mu \log \mu \, dx + \int V \mu \, dx.
$$

The first term is negative entropy (relative to Lebesgue), the second is potential energy.  Standard physics: free energy = internal energy minus temperature times entropy, with $k_B T = 1$ absorbed.  Compute the variational derivative:

$$
\frac{\delta F}{\delta \mu} = \log \mu + 1 + V.
$$

Plug into the master equation:

$$
\partial_t \mu = \nabla \cdot (\mu \nabla (\log \mu + 1 + V)) = \nabla \cdot (\mu \nabla \log \mu) + \nabla \cdot (\mu \nabla V).
$$

The first term simplifies: $\mu \nabla \log \mu = \nabla \mu$, so $\nabla \cdot (\mu \nabla \log \mu) = \Delta \mu$.  Therefore

$$
\boxed{\partial_t \mu = \Delta \mu + \nabla \cdot (\mu \nabla V).}
$$

That's the Fokker-Planck equation for the overdamped Langevin SDE

$$
dX_t = -\nabla V(X_t) \, dt + \sqrt{2} \, dW_t.
$$

Four lines.  Fokker-Planck is literally gradient descent of free energy, measured in $W_2$.  Please clap.

A few small sanity checks:

- $V = 0$: $\partial_t \mu = \Delta \mu$, the heat equation.  Heat flow is gradient flow of entropy in Wasserstein.  (This was my earlier post's punchline.)
- Stationary point: $\nabla (\log \mu + V) = 0$, so $\mu \propto e^{-V}$, the Gibbs measure.  Of course.
- The "potential" pushing $\mu$ around is $\log \mu + V$, which you can read as "log-probability penalty + external potential" - it's the effective potential felt by a probability fluid.

### Other PDEs from other functionals

Different $F$, different PDE.  A small menagerie:

**Porous medium equation.**  Take $F[\mu] = \frac{1}{m-1} \int \mu^m \, dx$ for $m > 1$.  Then $\delta F / \delta \mu = \frac{m}{m-1} \mu^{m-1}$, and

$$
\partial_t \mu = \nabla \cdot (\mu \nabla \mu^{m-1}) \propto \Delta (\mu^m).
$$

The porous medium equation.  Describes e.g. gas percolating through a porous solid.  It's gradient flow of a Rényi-ish entropy in Wasserstein.

**McKean-Vlasov / interaction energy.**  Take $F[\mu] = \frac{1}{2} \int\int W(x - y) \mu(x) \mu(y) \, dx \, dy$ for a symmetric interaction kernel $W$.  Then $\delta F / \delta \mu(x) = \int W(x - y) \mu(y) \, dy = (W \ast \mu)(x)$, and

$$
\partial_t \mu = \nabla \cdot (\mu \nabla (W \ast \mu)).
$$

Aggregation equation.  Used in swarming models, chemotaxis, opinion dynamics, mean-field limits of interacting particle systems.  Adding diffusion (so $F = \int \mu \log \mu + \frac{1}{2} \int\int W \mu \mu$) gives you McKean-Vlasov.

**Keller-Segel-ish.**  For chemotaxis you combine entropic diffusion with an attractive interaction.  Same Otto-calculus recipe; the only novel part is that the interaction can overwhelm diffusion and you get finite-time blow-up.

**Kinetic Fokker-Planck.**  If you include velocity as well as position ($\mathbb{R}^{2d}$ phase space) and your drift is Hamiltonian plus friction, you get the kinetic Fokker-Planck equation.  This isn't quite a plain Wasserstein gradient flow - the Hamiltonian part conserves free energy rather than decreasing it - but it fits into a "GENERIC" framework (General Equation for Non-Equilibrium Reversible-Irreversible Coupling) that combines Wasserstein gradient flow with symplectic flow.  If you've ever puzzled over why underdamped Langevin converges *faster* than overdamped, this is roughly why: it has a conservative piece that mixes directions that pure gradient flow can't.

In each case, you write down $F$, compute $\delta F / \delta \mu$, plug in, and read off a PDE.  The physical interpretation (what "free energy" means) depends on $F$, but the formal machinery is uniform.  This unification is a lot of what makes the Otto framework useful.

## Free energy decrease and Fisher information

The whole point of gradient flow is that it decreases the functional.  Let's check.

$$
\frac{dF}{dt} = \int \frac{\delta F}{\delta \mu} \partial_t \mu \, dx = \int (\log \mu + V) \nabla \cdot (\mu \nabla (\log \mu + V)) \, dx.
$$

Integrate by parts:

$$
\frac{dF}{dt} = -\int \mu \, \lVert \nabla (\log \mu + V) \rVert^2 \, dx.
$$

This is manifestly $\le 0$.  The quantity on the right has a name: **relative Fisher information** $I(\mu \mid e^{-V})$.  So

$$
\frac{dF}{dt} = -I(\mu \mid e^{-V}) \le 0.
$$

In Wasserstein terms, this is $\dot F = -\lVert \text{grad}_W F \rVert_\mu^2$, which is the standard gradient-flow identity.  Free energy strictly decreases along Fokker-Planck until we reach the Gibbs measure.

### Bakry-Émery and exponential convergence

If $F$ is uniformly convex along Wasserstein geodesics (roughly: Hessian $\ge \lambda > 0$ in the Otto sense), then you get exponential decay to equilibrium with rate $2\lambda$.  The condition for our free energy to have this property is

$$
\text{Hess } V \succeq \lambda I,
$$

i.e. the potential $V$ is $\lambda$-convex.  This is the **Bakry-Émery criterion**.  It is equivalent to the **log-Sobolev inequality** with constant $\lambda$:

$$
\text{Ent}(\mu \mid e^{-V}) \le \frac{1}{2\lambda} I(\mu \mid e^{-V}).
$$

Entropy is bounded by Fisher information.  Combined with $\dot F = -I$, you get $F(t) - F_\infty \le e^{-2\lambda t} (F_0 - F_\infty)$.

Why this is nice: a PDE convergence rate (Fokker-Planck equilibration) is a geometric statement (convexity of free energy) is a functional inequality (log-Sobolev).  Three faces of one thing.

### Worked example: Ornstein-Uhlenbeck

Make it concrete.  Take $V(x) = \frac{1}{2} \lVert x \rVert^2$ on $\mathbb{R}^d$.  Then $\text{Hess } V = I$, so $\lambda = 1$.  Bakry-Émery gives log-Sobolev with constant $1$, and Fokker-Planck is the Ornstein-Uhlenbeck process $dX = -X \, dt + \sqrt{2} \, dW$, whose stationary distribution is standard Gaussian $\mathcal{N}(0, I)$.

Starting from any initial distribution with finite second moment, the KL to the Gaussian equilibrium decays as

$$
\text{KL}(\mu_t \mid\mid \mathcal{N}(0, I)) \le e^{-2t} \text{KL}(\mu_0 \mid\mid \mathcal{N}(0, I)).
$$

Wasserstein-2 decay follows from Talagrand's inequality (which also follows from log-Sobolev): $W_2^2 \le 2 \text{KL}$, so $W_2(\mu_t, \mathcal{N}) \le e^{-t} W_2(\mu_0, \mathcal{N})$ times a constant.

This is the toy model.  For ML applications, "$\nabla^2 V$ bounded below" is roughly "target distribution is log-concave".  That's restrictive; most practical distributions aren't, and a lot of the modern story is about weaker convexity-like conditions (local log-Sobolev, modified Bakry-Émery, etc.) that still give useful bounds.

## Geodesics and displacement interpolation

Here's another consequence of the geometry: there's a natural notion of "straight line between distributions", due to McCann.

Given $\mu_0$ and $\mu_1$, let $T: \mathbb{R}^d \to \mathbb{R}^d$ be the Brenier map ($T = \nabla u$) with $T_\# \mu_0 = \mu_1$.  Define

$$
\mu_t = \left[ (1-t) \text{Id} + t T \right]_\# \mu_0, \quad t \in [0, 1].
$$

This is the **displacement interpolation** (or McCann interpolation).  Each mass element $x$ travels along the straight line $(1-t)x + tT(x)$; the distribution $\mu_t$ is the pushforward.  It's the geodesic between $\mu_0$ and $\mu_1$ in Wasserstein.

Compare this to the "linear interpolation" $\mu_t = (1-t)\mu_0 + t \mu_1$, which is the straight line in the affine simplex of measures.  The two are dramatically different.  Take $\mu_0 = \delta_0$ and $\mu_1 = \delta_1$:

- Linear: $\mu_{1/2} = \frac{1}{2}\delta_0 + \frac{1}{2}\delta_1$ - two spikes.
- Displacement: $\mu_{1/2} = \delta_{1/2}$ - a single spike halfway.

Displacement interpolation respects the geometry of $\mathbb{R}^d$.  The affine one doesn't know there is one.

Another easy example: $\mu_0 = \mathcal{N}(m_0, \Sigma_0)$, $\mu_1 = \mathcal{N}(m_1, \Sigma_1)$.  The Brenier map is affine, the displacement interpolant is again Gaussian, and the parameters interpolate as

$$
m_t = (1-t) m_0 + t m_1, \quad \Sigma_t^{1/2} = (1-t) \Sigma_0^{1/2} + t \Sigma_1^{1/2}
$$

(in the commuting case; otherwise use the matrix-geometric-mean generalization).  Note that it's the square roots that interpolate linearly.  This is the "Bures geodesic" on the cone of positive-definite matrices, and it's a useful mental model.

### Displacement convexity

A functional $F$ is **displacement convex** if $t \mapsto F[\mu_t]$ is convex along displacement interpolations.  McCann's theorem: on $\mathbb{R}^d$, the entropy $\int \mu \log \mu$ is displacement convex for all $d \ge 1$.  The internal energy $\int U(\mu) \, dx$ is displacement convex iff $s \mapsto s^d U(s^{-d})$ is convex and non-increasing - a weird-looking but important condition.

Displacement convexity is the "right" convexity for transport-based inequalities.  It's what gives you the Brunn-Minkowski inequality, concentration of measure, and half of the log-Sobolev zoo.  One unifying principle: convexity of entropy along geodesics of probability space.  When someone says "Ricci curvature bounded below is equivalent to displacement convexity of entropy" (Lott-Sturm-Villani), this is what they mean.

Quick concrete example.  Take $d = 1$, $\mu_0 = \text{Uniform}(0, 1)$, $\mu_1 = \text{Uniform}(1, 2)$.  Both have the same entropy (zero, with appropriate normalization).  What about the midpoint?

- Affine midpoint: $\mu_{1/2}^{\text{aff}} = \frac{1}{2} \text{Unif}(0,1) + \frac{1}{2} \text{Unif}(1,2) = \frac{1}{2} \text{Unif}(0, 2)$.  Entropy is $\log 2 > 0$.
- Displacement midpoint: $\mu_{1/2}^{\text{disp}} = \text{Unif}(1/2, 3/2)$.  Entropy is zero.

Under affine interpolation, entropy went up.  Under displacement interpolation, entropy stayed put.  In general, displacement interpolation cannot increase entropy more than linearly in $t$ (that's displacement convexity of $-$entropy, which is the convention people use).  This is the microscopic content of "transport respects geometry".

## Benamou-Brenier: the action principle

I claimed earlier that Wasserstein is the geodesic distance from the Otto metric.  Here is the precise statement, and it's essentially an action principle:

$$
W_2^2(\mu_0, \mu_1) = \inf_{(\mu_t, v_t)} \int_0^1 \int \lVert v_t(x) \rVert^2 \mu_t(x) \, dx \, dt
$$

subject to $\partial_t \mu_t + \nabla \cdot (\mu_t v_t) = 0$, $\mu(0) = \mu_0$, $\mu(1) = \mu_1$.  This is the **Benamou-Brenier formulation** (2000).

The inner integral is kinetic energy (mass times speed squared).  The constraint is conservation of probability.  So $W_2^2$ is the minimum "total kinetic energy" needed to morph $\mu_0$ into $\mu_1$ in unit time, integrated over space and time.

Why this is useful:

- Conceptually, $W_2$ is literally an action in the Lagrangian sense.  Euler-Lagrange gives you the geodesic equation on $\mathcal{P}_2$.
- Computationally, it turns a high-dimensional optimization (over plans $\pi$) into a PDE-constrained optimal control (over velocity fields).  For low-dimensional problems this is actually tractable.
- Conceptually again, the optimizer is a pressureless Euler flow: $\partial_t v + (v \cdot \nabla) v = 0$.  Geodesics are free-particle motions on the underlying space.  Consistent with Brenier's theorem.

The "action principle" framing is worth sitting with.  Fermat, Lagrange, Hamilton, Feynman - all of physics is action principles.  Optimal transport is yet another one: minimize kinetic energy subject to boundary conditions and a conservation law.  The fact that this particular action defines a distance with good geometric properties is, in retrospect, almost unsurprising.  It would be weird if it didn't.

## Applications and connections

A partial tour:

**Langevin samplers (MALA, ULA).**  Overdamped Langevin is Fokker-Planck is gradient flow of free energy.  Discretizing gives ULA (unadjusted Langevin); adding a Metropolis step gives MALA.  Convergence guarantees come from log-Sobolev / Bakry-Émery.  The right way to think about Langevin MCMC is "Wasserstein gradient descent on free energy".  The step size $\tau$ plays the role of the JKO timestep, and a lot of the sharp convergence results for ULA (Vempala-Wibisono, etc.) are proved by comparing ULA to exact JKO and then to exact Fokker-Planck.

**WGAN.**  Wasserstein-1 distance as a loss, via Kantorovich-Rubinstein duality.  $W_1$ is the supremum of $\mathbb{E}_\mu[f] - \mathbb{E}_\nu[f]$ over 1-Lipschitz $f$; approximate $f$ with a neural net and you get WGAN.  $W_2$ is cleaner geometrically, but $W_1$ has the cleaner dual for training.

**Score-based diffusion.**  Diffusion models run a forward SDE (turning data into noise) and learn a reverse SDE.  The reverse is driven by the score $\nabla \log p_t$.  This is exactly the gradient of the variational derivative of entropy - the Wasserstein gradient.  Diffusion models are, in a real sense, doing Otto calculus on the data distribution.  Specifically: the Fokker-Planck evolution is the heat-flow-plus-drift gradient flow described above, and the reverse-time SDE has velocity field $\nabla \log p_t$ because the entropy part of the free energy contributes exactly that to the Wasserstein gradient.  Score matching is "learn the Wasserstein gradient of entropy from samples".

**MMD vs Wasserstein in ML.**  MMD ($O(1/\sqrt{n})$ sample complexity) is cheaper than $W_2$ ($O(n^{-1/d})$ - cursed in high $d$), but is geometry-blind in a similar way to KL.  Different tools for different jobs.

**Stein's method and KSD.**  Kernelized Stein Discrepancy is a geometric cousin of Fisher information, relating to log-Sobolev-like inequalities via Stein operators.  Related geometric story, different metric.

**Neural gradient flows.**  Parameterize $\mu_\theta$ by a neural net and do Wasserstein gradient flow on $\theta$ - this is what "neural ODE samplers" and some continuous-time normalizing flows are morally doing.

**Training dynamics of neural nets.**  The "mean-field" limit of a very wide two-layer network replaces the finite collection of neurons with a distribution over neuron parameters, and SGD on the neurons becomes a Wasserstein gradient flow on that distribution.  This has been genuinely useful for proving convergence in the overparameterized regime - loss landscapes that look non-convex in parameter space are displacement-convex in distribution space.

**Natural gradient.**  Amari's natural gradient uses Fisher information as the metric on parameter space.  That's the information-geometric cousin of Wasserstein: same template (give parameter space a Riemannian structure derived from distributions), different metric.  Fisher corresponds to relative entropy; Wasserstein corresponds to transport cost.  Both are "geometry-aware" in the relevant sense.

## Entropic regularization and Sinkhorn

Practically, computing $W_2$ is expensive.  A standard fix: add an entropic penalty.

$$
W_\epsilon^2(\mu, \nu) = \inf_{\pi \in \Pi(\mu, \nu)} \left[ \int \lVert x - y \rVert^2 d\pi + \epsilon \, \text{KL}(\pi \mid\mid \mu \otimes \nu) \right].
$$

The $\text{KL}$ term penalizes "overly deterministic" plans.  As $\epsilon \to 0$, you recover $W_2$; as $\epsilon \to \infty$, you get the product distribution.  The effect is to smear out optimal plans and make the problem strictly convex.

**Sinkhorn.**  The regularized problem has a closed-form structure: optimal $\pi$ factors as $\pi(x, y) = a(x) b(y) k(x, y)$ with $k(x,y) = \exp(-\lVert x - y\rVert^2 / \epsilon)$.  Finding $a, b$ reduces to alternating rescaling of the rows and columns of the Gibbs kernel $k$ to match the marginals.  This is the **Sinkhorn-Knopp algorithm**, and it converges linearly.

Costs:

- Fast: $O(n^2)$ per iteration for $n$-point distributions, and the iteration count is roughly $O(\log(1/\text{tol}) / \epsilon)$.
- Differentiable: great for ML pipelines.
- Biased: $W_\epsilon$ is not the true $W_2$.  For $\mu = \nu$, $W_\epsilon(\mu, \mu) \ne 0$.  You want the **Sinkhorn divergence** $S_\epsilon(\mu, \nu) = W_\epsilon(\mu, \nu) - \frac{1}{2} W_\epsilon(\mu, \mu) - \frac{1}{2} W_\epsilon(\nu, \nu)$ to kill the bias.

For practical OT in ML, Sinkhorn divergences are the workhorse.  For theory, use $W_2$ directly.

There's also a cute theoretical interpretation.  The entropic OT problem is equivalent to a **Schrödinger bridge**: find the law of a Brownian-bridge-like diffusion that goes from $\mu$ at $t = 0$ to $\nu$ at $t = 1$ with minimal KL from a Brownian reference.  The small-noise limit of the Schrödinger bridge is optimal transport.  So entropic OT is not just a computational hack - it's a distinct, interpretable object that has its own physics (stochastic bridges) and its own limit (classical OT).  This connection is why Schrödinger bridges keep showing up in diffusion-model papers.

## The HWI inequality: a geometric unification

Since we're at the summit, one glimpse of what all this geometry buys you on the functional-inequality side.

Let $\nu = e^{-V}$ be our reference measure.  Define:

- $H(\mu) = \text{KL}(\mu \mid\mid \nu)$, the relative entropy (Boltzmann $H$-function, hence the name).
- $W = W_2(\mu, \nu)$, Wasserstein distance to the reference.
- $I(\mu) = \int \mu \lVert \nabla \log (\mu/\nu) \rVert^2$, relative Fisher information.

Under $\lambda$-convexity of $V$ (so Bakry-Émery applies), the **HWI inequality** says

$$
H(\mu) \le W(\mu) \sqrt{I(\mu)} - \frac{\lambda}{2} W(\mu)^2.
$$

This is a two-parameter generalization of both:

- **Log-Sobolev** ($\lambda > 0$, bounding $H$ by $I$): take the inequality, use $ab \le \frac{1}{2\lambda} a^2 + \frac{\lambda}{2} b^2$ on the first term with $a = \sqrt{I}$, $b = W$: $H \le \frac{I}{2\lambda}$.  Done.
- **Talagrand** ($\lambda > 0$, bounding $W$ by $H$): this is the $I = 0$ limit, roughly.  $W^2 \le \frac{2H}{\lambda}$.

The geometric picture: $F[\mu] = H(\mu)$ is $\lambda$-geodesically-convex on $\mathcal{P}_2$, and HWI is Taylor's theorem for that along the geodesic from $\mu$ to $\nu$.  One inequality, several specializations, all coming from one convexity.

That's the tip of the functional-inequality iceberg.  A whole zoo (Poincaré, modified log-Sobolev, Beckner, etc.) drops out of varying choices of $F$ and convexity hypotheses.  And all of it has a transport / Otto-calculus face.

## Mean-field games briefly

If you've seen Hamilton-Jacobi-Bellman in classical control, the mean-field-games version is HJB on $\mathcal{P}_2$.  Roughly: in a game with a continuum of identical players, each player solves an HJB problem where the running cost depends on the distribution $\mu_t$ of the other players; $\mu_t$ itself evolves by a Fokker-Planck equation driven by the players' optimal controls.  The equilibrium is a coupled forward-backward system: Fokker-Planck forward in time for the density, HJB backward in time for the value function.

The "master equation" of MFG packages both into a single PDE on $\mathcal{P}_2$ whose well-posedness relies on the Otto-calculus machinery.  It's the cleanest way I know to think about population-scale control in stochastic systems, and it's increasingly used in economic modeling, swarm robotics, and large-scale RL.

## What's next

Otto calculus is the entry point to a bigger story.  Some natural continuations:

**HWI and functional inequalities.**  The HWI inequality relates entropy ($H$), Wasserstein distance ($W$), and Fisher information ($I$), and under displacement convexity it implies log-Sobolev and Talagrand's transport inequality.  It's the "master inequality" of the Otto picture.

**Wasserstein-information geometry (Li-Otto, etc).**  There's a natural Hessian geometry on $\mathcal{P}_2$, and Fisher information is, roughly, the squared norm of the Wasserstein gradient of entropy.  This is a geometric unification of information geometry (Amari) and optimal transport.  The "Wasserstein Fisher" and "classical Fisher" disagree off the tangent space of statistical models, which is part of what makes the unification interesting.

**Mean-field games.**  Equilibria of large-population games live on $\mathcal{P}_2$, and the master equation is a Hamilton-Jacobi-Bellman on Wasserstein space.  Carmona-Delarue is the reference.  The Otto framework is essential here.

**Schrödinger bridges.**  The entropic regularization above has an interpretation as a stochastic control problem: find a diffusion that transports $\mu_0$ to $\mu_1$ with minimal KL from a reference Brownian motion.  This is the Schrödinger bridge, and it's closely tied to diffusion models.  In the zero-noise limit you recover optimal transport.

**Curvature and $\text{RCD}(K, \infty)$ spaces.**  "Ricci curvature bounded below" on metric measure spaces is defined via displacement convexity of entropy.  Lott-Sturm-Villani.  The definition makes sense on singular spaces and gives a notion of curvature for fractals, graphs, etc.

Any one of these is a seed for another post.

**A reading path if you want to go deeper.**  Villani's *Topics in Optimal Transportation* (2003) is the friendly entry point; *Optimal Transport: Old and New* (2008) is the definitive (but enormous) reference.  Santambrogio's *Optimal Transport for Applied Mathematicians* (2015) is the practical, less-scary book.  Ambrosio-Gigli-Savaré's *Gradient Flows in Metric Spaces* is the rigor-heavy treatment of Otto calculus.  For the ML side, Peyré-Cuturi's *Computational Optimal Transport* covers Sinkhorn and modern algorithms with code.  All are excellent.

## A recap in one page

Before the caveats section, here's the whole story in condensed form, so you have something to point at.

1. **Problem.**  You want to do calculus on probability measures.  KL is not a metric and ignores the geometry of the underlying space; Fisher information gives you a Riemannian metric on finite-parameter families but doesn't scale.  We want a global metric on $\mathcal{P}_2$.

2. **Metric.**  $W_2^2(\mu, \nu)$ = minimum cost of rearranging $\mu$ into $\nu$ with squared-distance cost.  Concrete, interpretable, respects geometry of $\mathbb{R}^d$.

3. **Geometry.**  Otto (2001): $\mathcal{P}_2$ with $W_2$ is formally Riemannian, with tangent space at $\mu$ = $\{\nabla \phi\}$ and inner product $\int \nabla \phi_1 \cdot \nabla \phi_2 \, d\mu$.  Geodesics are McCann displacement interpolations.

4. **Calculus.**  For $F: \mathcal{P}_2 \to \mathbb{R}$, the Wasserstein gradient is $\nabla (\delta F / \delta \mu)$, and gradient flow reads $\partial_t \mu = \nabla \cdot (\mu \nabla \delta F / \delta \mu)$.

5. **Physics.**  Free energy $F = \int \mu \log \mu + \int V \mu$ gives Fokker-Planck $\partial_t \mu = \Delta \mu + \nabla \cdot (\mu \nabla V)$.  Different $F$, different PDE.

6. **Convergence.**  Bakry-Émery: if $V$ is $\lambda$-convex, Fokker-Planck converges exponentially at rate $2\lambda$.  Equivalent to log-Sobolev inequality with constant $\lambda$.  Equivalent to $\lambda$-displacement-convexity of $F$.

7. **Dynamic formulation.**  Benamou-Brenier: $W_2^2$ is the minimum kinetic energy subject to the continuity equation.  An action principle.

8. **Applications.**  Langevin MCMC, diffusion models, WGAN, mean-field games, neural-net training dynamics, curvature on metric measure spaces.

That's the whole post in eight bullets.  Use it as a cheat sheet.

## An aside on "formal vs rigorous"

I've been waving hands a lot.  Some of the waving is essential, some is lazy, and it's worth flagging the difference.

**Essentially formal (where rigor is available but obnoxious):** the $\mathcal{P}_2$ space is not a manifold in the differentiable sense, but it is an Alexandrov space of curvature bounded below in the sense of length spaces, and the Otto inner product has a rigorous interpretation as the metric derivative of absolutely continuous curves.  The "tangent vectors as gradients" statement is precise modulo closures.  The "gradient of $F$" is precise.  None of this is merely formal - it's just notationally expensive to make fully rigorous.

**Formal and not clearly fixable:** the second-order geometry (Hessians, sectional curvature) is genuinely tricky and not uniformly convergent with what a finite-dimensional Riemannian manifold does.  "Displacement convexity" is the right substitute for geodesic convexity in many arguments, but statements about the Ricci tensor on $\mathcal{P}_2$ are modality-dependent (Lott-Sturm-Villani vs Villani's earlier formulation, etc.).  When people say "Wasserstein manifold has Ricci curvature bounded below by the Ricci curvature of the base space" there's a careful theorem behind it, but there's no computation of a Ricci tensor.

**Formal and load-bearing:** some of the manipulations in this post (integration by parts with $\mu$ vanishing, etc.) need non-trivial regularity assumptions to go through.  For smooth log-concave $V$ you're fine.  For distributions with compact support, with atoms, or with singular behavior, extra work.

For a physicist I think the right attitude is: the formal manipulations give correct answers on the problems you care about, and when they don't, it's usually obvious in retrospect (e.g. at a shock in a hyperbolic problem you lose classical solutions, and that's a physics fact, not an artifact of the formalism).  Compute first, worry about regularity second.  The mathematicians will find you if you get it wrong.

## Summary

- $W_2$ makes probability space a Riemannian-ish manifold.
- Tangent vectors at $\mu$ are gradient fields $\nabla \phi$, with inner product $\int \nabla \phi_1 \cdot \nabla \phi_2 \, d\mu$.
- Wasserstein gradient: $\text{grad}_W F = \nabla (\delta F / \delta \mu)$.
- Gradient flow: $\partial_t \mu = \nabla \cdot (\mu \nabla \delta F / \delta \mu)$.  Master equation.
- Fokker-Planck is gradient flow of free energy $\int \mu \log \mu + \int V \mu$.
- Free energy decreases at rate = Fisher information.  Bakry-Émery / log-Sobolev controls the rate.
- Geodesics are displacement interpolations (McCann).  Straight lines in transport space.
- Benamou-Brenier: $W_2^2$ is an action (kinetic energy along a continuity-equation-constrained path).

All you really need to carry out of this post: gradient, divergence, $W_2^2$, and the single formula

$$
\partial_t \mu = \nabla \cdot \left( \mu \, \nabla \frac{\delta F}{\delta \mu} \right).
$$

Everything else is mnemonic.

If you internalize one thing: **distributions have geometry, and the right metric to use depends on whether you care about labels or positions**.  For categorical labels (words, classes), KL is fine.  For positions (distributions on metric spaces, continuous latents, densities of matter or probability), $W_2$ is the move, and Otto calculus is the toolkit.  The switch from KL to $W_2$ is the same move as switching from "count-based" to "geometry-aware" statistics, and it's what makes all the beautiful PDE-gradient-flow connections possible.  Please clap.

***

*See also: [KL Divergence, Geometric Naturalness, and Optimal Transport](/2025/07/11/KL-Divergence-Geometric-Naturalness-and-Optimal-Transport), [Small Zoo of Natural Norms and Metrics](/2026/01/24/Small-Zoo-of-Natural-Norms-and-Metrics).*

*Written with Claude.*
