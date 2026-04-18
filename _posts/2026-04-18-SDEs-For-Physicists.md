---
title: "SDEs for Physicists"
date: 2026-04-18
motivation: "Stochastic calculus has a reputation for heavy machinery. The measure theory is real, but physicists almost never need it. What you actually need: Brownian motion as a tool, Itô's lemma, Fokker-Planck, and a few named tricks (Girsanov, Doob, Onsager-Machlup) that all turn out to be the same move in different costumes."
background: "Comfort with ODEs, basic probability, and the idea of a path integral.  No measure theory.  If you've written down the Langevin equation and waved your hands about white noise, that's the right starting point."
llm: "Claude"
tags: [seed]
math: true
---

# SDEs for Physicists

## What This Is

Stochastic differential equations are how physicists write down noisy dynamics.  The Langevin equation is the paradigm: a deterministic force plus a kick.  Under the hood there's a lot of measure theory that probabilists care about and you probably don't.

This is the minimum viable curriculum.  You'll be able to compute things, translate between conventions, and read the literature.  You will not become a Kallenberg-wielding martingale theorist.  That's fine.

The payoff: once you have Itô's lemma and Fokker-Planck, a surprising number of named tools (Girsanov, Doob h-transform, Onsager-Machlup, Feynman-Kac, Freidlin-Wentzell) all turn into easy manipulations.

## The Langevin Paradigm

Before formalism, the physical picture.  Put a heavy particle in a fluid.  The fluid molecules batter it; averaged, they produce friction; fluctuating, they produce a random force.  The equation of motion:

$$
m\ddot x = -\gamma\dot x - V'(x) + \eta(t)
$$

with $\eta$ a "random force" of zero mean and correlation $\langle \eta(t)\eta(s)\rangle = 2\gamma k_B T\,\delta(t-s)$.  That's the **Langevin equation**.  The strength of the noise is fixed by the temperature via the **fluctuation-dissipation theorem** - dissipation and fluctuation come from the same microscopic bath.

The overdamped limit (ignore inertia, $m \to 0$):

$$
\gamma\dot x = -V'(x) + \eta(t)
$$

or, dividing through:

$$
dx = -\frac{V'(x)}{\gamma}\,dt + \sqrt{\frac{2 k_B T}{\gamma}}\,dW
$$

where I've absorbed the noise into a Wiener differential.  This is an SDE.  The translation "$\eta(t)\,dt = \sigma\,dW_t$" with $\sigma = \sqrt{2\gamma k_B T}$ gets you from physics notation to math notation.

Physicists tend to write $\xi(t)$ for "white noise" and treat it as a function.  It isn't.  But in most calculations you can proceed by computing moments ($\langle\xi\xi\rangle = \delta$, products involving $\xi$ are Gaussian, etc.), and the answer agrees with the rigorous SDE treatment, provided you've picked a convention (Itô or Stratonovich) and stuck with it.

## Brownian Motion: The Rules You Need

A standard Brownian motion (Wiener process) $W_t$ is a random function of time with:

1. $W_0 = 0$
2. Independent increments: $W_t - W_s$ is independent of everything that happened before time $s$
3. Gaussian increments: $W_t - W_s \sim \mathcal{N}(0, t-s)$
4. Continuous sample paths

That last property is subtle.  The paths are continuous, but nowhere differentiable.  If you try to write $dW/dt$, you get "white noise" $\xi(t)$ with $\langle \xi(t)\xi(s)\rangle = \delta(t-s)$, which is not a function in any classical sense.  It's a distribution.

The operational rule you will use constantly:

$$
dW^2 = dt
$$

Not "approximately $dt$".  Equal to $dt$.  This isn't quite a rigorous statement, but it's the right heuristic: $dW$ is of size $\sqrt{dt}$, so $dW^2$ is of size $dt$, and its fluctuations (which are of size $dt$) are negligible compared to $dt$ itself in the limit.  The quadratic variation of $W$ over $[0,T]$ is exactly $T$, almost surely.

Everything else is a consequence.  $dW \cdot dt = 0$ (higher order).  $dt^2 = 0$ (higher order).  $dW_1 \cdot dW_2 = 0$ if $W_1, W_2$ are independent.

That's it.  That's Brownian motion for the working physicist.

A couple of scaling facts worth internalizing:

- **Self-similarity.** $W_{ct}$ has the same distribution as $\sqrt{c}\,W_t$.  Brownian motion is scale-invariant between space and time with exponent $1/2$.  This is where the $\sqrt{t}$ in diffusion ($\langle x^2\rangle \sim t$) comes from.
- **Time inversion.** $t\cdot W_{1/t}$ (with $0$ at $t = 0$) is another Brownian motion.  Useful for relating behavior at $t \to 0$ and $t \to \infty$.
- **Reflection principle.** The probability that a Brownian motion exceeds level $a > 0$ by time $T$ is twice the probability that $W_T > a$.  This is one of the few tractable exit-time calculations you can do by hand.

## The Naive Integral Breaks

Here's a test case.  What is $\int_0^T W\,dW$?

If $W$ were a smooth function, ordinary calculus gives $\tfrac{1}{2} W(T)^2 - \tfrac{1}{2} W(0)^2 = \tfrac{1}{2} W(T)^2$.  You'd expect the same here.

But "integral" now requires a convention.  Partition $[0,T]$ and sum $W(t_i^*) (W(t_{i+1}) - W(t_i))$.  Where do we evaluate the integrand: left endpoint, midpoint, right endpoint?  For a smooth integrand these all agree in the limit.  For $W$ they don't.

Left endpoint (Itô):

$$
\int_0^T W\,dW = \tfrac{1}{2} W(T)^2 - \tfrac{1}{2} T
$$

There's an extra $-T/2$.  Where did it come from?  From $dW^2 = dt$.  Write $W(t_{i+1}) = W(t_i) + dW$ and expand $W(t_{i+1})^2 - W(t_i)^2 = 2 W(t_i)\, dW + dW^2$.  Summing, the $dW^2$ terms add up to $T$, not $0$.

Midpoint (Stratonovich):

$$
\int_0^T W \circ dW = \tfrac{1}{2} W(T)^2
$$

The $\circ$ denotes Stratonovich.  The midpoint rule averages over the endpoints and cancels the $-T/2$.  Ordinary calculus holds.

So we have a choice.  Both are consistent mathematical objects, but they define different integrals.  The physics literature uses both, often without telling you which.

## Itô vs. Stratonovich: What's the Difference

**Itô.** Evaluate the integrand before the increment:

$$
\int_0^T f(W_t)\,dW_t = \lim \sum_i f(W_{t_i}) (W_{t_{i+1}} - W_{t_i})
$$

This is the "non-anticipating" choice: the integrand doesn't peek at the future.  Its huge advantage: **the Itô integral is a martingale**.  Mean zero, no systematic drift from the noise.  That makes it the right tool for probabilistic arguments (filtering, optimal control, pricing theory).

**Stratonovich.** Evaluate at the midpoint:

$$
\int_0^T f(W_t) \circ dW_t = \lim \sum_i f(\tfrac{W_{t_i} + W_{t_{i+1}}}{2})(W_{t_{i+1}} - W_{t_i})
$$

The integrand does peek (a little) at the future.  Huge advantage: **ordinary calculus works**.  Chain rule, change of variables, substitution, all the familiar moves.  Geometric / coordinate-invariant.  Also what you get as the smooth-noise limit (Wong-Zakai theorem): if your "noise" is actually a high-frequency smooth process that you've idealized as white, you should use Stratonovich.

**Converting between them.** For an SDE

$$
dX = b(X)\,dt + \sigma(X)\,dW \qquad \text{(Itô)}
$$

the equivalent Stratonovich equation has a shifted drift:

$$
dX = \left[b(X) - \tfrac{1}{2}\sigma(X)\sigma'(X)\right] dt + \sigma(X) \circ dW
$$

Read it the other way for Stratonovich to Itô.  For additive noise ($\sigma$ constant), there's no difference.  For multiplicative noise, it matters.

The physics literature is a trap.  Sometimes "$\sqrt{2D}\,\xi$" means Itô, sometimes Stratonovich.  When in doubt, ask.  Or look for giveaways: any time you see a chain rule applied naively (e.g.  to get the equation for $\log X$), the author is using Stratonovich.

Here's the rule of thumb I use.  **If the noise is idealized white noise replacing a real physical fluctuation, use Stratonovich.**  This is the Wong-Zakai theorem: smooth noise converging to white noise produces Stratonovich SDEs in the limit.  Physical noise has a finite correlation time; when you idealize away that scale, you land in Stratonovich.  **If the noise is exogenous and "non-anticipating" (information arrives, you react; finance, filtering), use Itô.**  The martingale property is what you want.

When in doubt, do the conversion and see if the drift correction looks physical.  The extra term $-\tfrac{1}{2}\sigma\sigma'$ often has a clean interpretation ("noise-induced drift" or "Stratonovich correction").

## Itô's Lemma

This is the single most useful formula in the subject.  It's the chain rule in Itô calculus.

Suppose $X$ satisfies the Itô SDE $dX = b\,dt + \sigma\,dW$ and $f(t, x)$ is smooth.  Then:

$$
\boxed{\;df = \partial_t f\,dt + \partial_x f\,dX + \tfrac{1}{2} \partial_x^2 f\,\sigma^2\,dt\;}
$$

Compare to ordinary calculus, which would give you the first two terms only.  The extra piece $\tfrac{1}{2} \partial_x^2 f\,\sigma^2\,dt$ is the **Itô correction**.

The derivation is a one-liner.  Taylor expand:

$$
df = \partial_t f\,dt + \partial_x f\,dX + \tfrac{1}{2} \partial_x^2 f\,dX^2 + \cdots
$$

Now use $dX^2 = \sigma^2 dW^2 = \sigma^2 dt$ (cross terms and $dt^2$ drop out) and keep only $O(dt)$ terms.  Done.

Intuitively: $X$ moves by $\sqrt{dt}$ amounts, so the second-order term $dX^2$ contributes at the same order as $dt$.  You can't drop it like you would in ordinary calculus.

### Worked Example: Geometric Brownian Motion

The SDE for a stock price (or any multiplicatively-driven positive quantity):

$$
dX = \mu X\,dt + \sigma X\,dW
$$

What does $\log X$ satisfy?  Apply Itô to $f(x) = \log x$: $f' = 1/x$, $f'' = -1/x^2$.

$$
d(\log X) = \frac{dX}{X} - \tfrac{1}{2}\frac{1}{X^2}\sigma^2 X^2\,dt = (\mu - \tfrac{1}{2}\sigma^2)\,dt + \sigma\,dW
$$

Additive noise in $\log X$.  So $\log X_t - \log X_0$ is Gaussian with mean $(\mu - \tfrac{1}{2}\sigma^2) t$ and variance $\sigma^2 t$:

$$
X_t = X_0 \exp\left[(\mu - \tfrac{1}{2}\sigma^2) t + \sigma W_t\right]
$$

Note the $-\tfrac{1}{2}\sigma^2$.  If you'd done the calculation naively (no Itô correction), you'd get $X_t = X_0 e^{\mu t + \sigma W_t}$, which has mean $X_0 e^{(\mu + \sigma^2/2)t}$.  The correct answer has mean $X_0 e^{\mu t}$.  The volatility drag is real: the log-mean is below the log-of-mean by exactly $\tfrac{1}{2}\sigma^2 t$.  This is Jensen's inequality made concrete by Itô.

Please clap.

### Multidimensional Itô

In $n$ dimensions with $dX^i = b^i\,dt + \sigma^i_\alpha\,dW^\alpha$ (summed over noise index $\alpha$), the lemma generalizes to:

$$
df = \partial_t f\,dt + \partial_i f\,dX^i + \tfrac{1}{2}(\sigma\sigma^T)^{ij}\,\partial_i\partial_j f\,dt
$$

The Itô correction uses the diffusion matrix $D^{ij} = (\sigma\sigma^T)^{ij}/2$, which is the covariance per unit time of the increments $dX^i dX^j$.  This is what shows up in the multidimensional Fokker-Planck equation too.  The noise index $\alpha$ doesn't enter the final formula - only the physically observable covariance $\sigma\sigma^T$ does.  A gauge redundancy: $\sigma \to \sigma O$ for $O$ orthogonal leaves everything invariant.

## Fokker-Planck: The Density

The SDE is a statement about sample paths.  The **Fokker-Planck equation** is the corresponding statement about the probability density $p(x, t)$ of $X_t$.

Starting from the Itô SDE $dX = b\,dt + \sigma\,dW$, Itô's lemma gives us $d\langle f(X)\rangle/dt$ for any test function $f$:

$$
\frac{d}{dt}\langle f(X_t)\rangle = \langle b\,\partial_x f + \tfrac{1}{2}\sigma^2\,\partial_x^2 f\rangle = \int p\,(b\partial_x f + \tfrac{1}{2}\sigma^2 \partial_x^2 f)\,dx
$$

(the $dW$ term has mean zero: martingale property).  Integrate by parts on the right:

$$
\int p\,b\,\partial_x f\,dx = -\int f\,\partial_x(b p)\,dx, \qquad \int p\,\sigma^2 \partial_x^2 f\,dx = \int f\,\partial_x^2(\sigma^2 p)\,dx
$$

Since this holds for all $f$, and also equals $\int f\,\partial_t p\,dx$:

$$
\boxed{\;\partial_t p = -\partial_x(b p) + \tfrac{1}{2}\partial_x^2(\sigma^2 p)\;}
$$

That's Fokker-Planck.  Drift term plus diffusion term.  The operator on the right is the adjoint of the **backward generator** $L = b\,\partial_x + \tfrac{1}{2}\sigma^2\,\partial_x^2$, which acts on test functions.  More on $L$ in a moment.

### Worked Example: Ornstein-Uhlenbeck

$$
dX = -\gamma X\,dt + \sigma\,dW
$$

Linear drift pulling toward zero, additive noise.  Fokker-Planck:

$$
\partial_t p = \gamma\partial_x(x p) + \tfrac{1}{2}\sigma^2 \partial_x^2 p
$$

Equilibrium: set $\partial_t p = 0$.  Divide by $p$ and integrate: $\gamma x + \tfrac{1}{2}\sigma^2 \partial_x \log p = \text{const}$, which gives

$$
p_{\text{eq}}(x) \propto \exp\left(-\frac{\gamma x^2}{\sigma^2}\right)
$$

A Gaussian with variance $\sigma^2/(2\gamma)$.  Fluctuation-dissipation: the equilibrium width is set by noise strength over damping rate.  Classic.

The time-dependent solution starting from $X_0 = x_0$ is also Gaussian, with mean $x_0 e^{-\gamma t}$ and variance $(\sigma^2/2\gamma)(1 - e^{-2\gamma t})$.  Relaxation to equilibrium on timescale $1/\gamma$.

### Overdamped Langevin and the Gibbs Measure

One reason physicists like overdamped Langevin dynamics: the equilibrium distribution is the Gibbs measure you expected.

$$
dx = -\nabla V(x)\,dt + \sqrt{2 k_B T}\,dW
$$

Fokker-Planck:

$$
\partial_t p = \nabla\cdot(\nabla V\,p) + k_B T\,\Delta p = \nabla\cdot[p\,\nabla V + k_B T\,\nabla p]
$$

The expression in brackets is the probability current $J$.  Set $J = 0$ (equilibrium, no net flow): $p\,\nabla V + k_B T\,\nabla p = 0$, solved by $p \propto e^{-V/k_B T}$.  Boltzmann.

The fact that this works is basically the reason MCMC-for-continuous-distributions is a thing.  Simulating Langevin dynamics and averaging over long time is the same as sampling from $e^{-V/k_B T}$.  (Metropolis-adjusted Langevin algorithm, Hamiltonian Monte Carlo, etc.  all descend from this.)

## Reversibility and Detailed Balance

One more observation physicists care about.  The overdamped Langevin SDE $dx = -\nabla V\,dt + \sqrt{2T}\,dW$ is **reversible**: running the dynamics backward in time (at equilibrium) produces a process statistically indistinguishable from the forward one.

Concretely: the equilibrium time-reversed generator equals the forward generator.  The condition is that the drift be a gradient of a potential.  If you instead write $dx = F(x)\,dt + \sqrt{2T}\,dW$ with $F$ **not** a gradient (i.e., $\nabla\times F \ne 0$ in some sense), the equilibrium state still exists (if confining) but has **nonzero probability current**: $J_{\text{eq}} \ne 0$.  You get a nonequilibrium steady state (NESS) with persistent circulation.

This is where the stochastic-thermodynamics / active-matter crowd lives.  The "nonconservative" drift is what separates equilibrium from driven dynamics.  Same SDE formalism, very different physics.

The reversal of a general SDE $dx = b\,dt + \sigma\,dW$ under its own invariant measure $\pi$ has drift $\tilde b = -b + \sigma^2 \nabla\log\pi$.  Forward-reverse symmetry requires $\tilde b = b$, which gives $b = \tfrac{1}{2}\sigma^2\nabla\log\pi$: the drift must be exactly the score of the invariant density (times $\sigma^2/2$).  For Langevin $dx = -\nabla V\,dt + \sqrt{2T}\,dW$: $\pi \propto e^{-V/T}$, $\nabla\log\pi = -\nabla V/T$, and indeed the drift is $\tfrac{1}{2}(2T)(-\nabla V/T) = -\nabla V$.  Checks out.

This identity (drift = $\tfrac{1}{2}\sigma^2 \times$ score) is, incidentally, the cornerstone of score-based generative modeling.  A diffusion model is literally a reverse-time Langevin SDE where the score function is learned by a neural net.  Same machinery, applied to image generation instead of molecular dynamics.

## Backward Operator and Feynman-Kac

The generator $L = b\,\partial_x + \tfrac{1}{2}\sigma^2\,\partial_x^2$ acts on observables, not densities.  If $u(x, t) = \mathbb{E}_x[f(X_t)]$ is the expected value of $f(X_t)$ given $X_0 = x$, then:

$$
\partial_t u = L u, \qquad u(x, 0) = f(x)
$$

This is the **backward Kolmogorov equation**.  It's dual to Fokker-Planck: $\partial_t p = L^* p$.

The **Feynman-Kac formula** generalizes this with a potential $V(x)$:

$$
u(x, 0) = \mathbb{E}_x\left[\exp\left(-\int_0^T V(X_s)\,ds\right) f(X_T)\right]
$$

solves $\partial_t u = L u - V u$ with final condition $u(x, T) = f(x)$.

One line, one of the most useful formulas in mathematical physics.  Schrödinger in imaginary time (with $L = \tfrac{1}{2}\Delta$) has exactly this form.  The stochastic path integral *is* the Feynman path integral.

### Worked Example: Harmonic Oscillator Ground State

Take $L = \tfrac{1}{2}\partial_x^2$ (Brownian) and $V(x) = \tfrac{1}{2}\omega^2 x^2$.  Then $\partial_t u = \tfrac{1}{2}\partial_x^2 u - \tfrac{1}{2}\omega^2 x^2 u$ is the imaginary-time Schrödinger equation for a harmonic oscillator.

Feynman-Kac says:

$$
u(x, 0) = \mathbb{E}_x\left[e^{-\tfrac{1}{2}\omega^2 \int_0^T W_s^2\,ds} f(W_T)\right]
$$

At large $T$, this projects onto the ground state: $u(x, 0) \sim e^{-E_0 T}\psi_0(x)\langle\psi_0, f\rangle$ with $E_0 = \omega/2$, $\psi_0(x) \propto e^{-\omega x^2/2}$.  You've computed the ground state energy by averaging $e^{-\tfrac{1}{2}\omega^2\int W^2}$ over Brownian paths and reading off the exponential decay rate.  This is diffusion Monte Carlo in miniature.  And it's the cleanest motivation for the Euclidean path integral.

## Girsanov: Changing the Drift

Here is the setup.  You have two SDEs on the same Brownian:

$$
\text{P:}\ dX = b\,dt + \sigma\,dW, \qquad \text{Q:}\ dX = (b + \sigma\theta)\,dt + \sigma\,d\tilde{W}
$$

Same diffusion, different drifts.  Under $P$, the process is driven by $W$.  Under $Q$, there's an extra drift $\sigma\theta$, and a different Brownian $\tilde{W} = W - \int \theta\,dt$ is the driver.

**Girsanov's theorem** says the two laws are absolutely continuous, and the Radon-Nikodym derivative (likelihood ratio) on paths up to time $T$ is:

$$
\boxed{\;\frac{dQ}{dP} = \exp\left(\int_0^T \theta_s\,dW_s - \tfrac{1}{2}\int_0^T \theta_s^2\,ds\right)\;}
$$

Two terms.  The first is the naive likelihood ratio you'd guess for shifting the mean of a Gaussian.  The second is a normalizing Itô correction.  Note that the exponent is itself an SDE whose log is a martingale (mean zero under $P$).

Why you care:

- **Importance sampling.** Want to sample trajectories under $Q$ but can only simulate $P$?  Weight by $dQ/dP$.
- **Filtering / likelihood.** Parameter estimation from observed paths: the log-likelihood is the Girsanov exponent.
- **Mathematical finance.** Risk-neutral pricing is Girsanov shifting from the real-world to risk-neutral measure.
- **Path integral reweighting.** In sampling applications (molecular dynamics, sampling rare trajectories), this is how you bias and reweight.

The heuristic derivation: think of the probability of a path under $P$ as $\prod_i \exp(-(\Delta W_i)^2 / 2\Delta t)$ (Gaussian increments).  Under $Q$, increments are $\Delta \tilde{W}_i = \Delta W_i - \theta_i \Delta t$, so the density is $\prod_i \exp(-(\Delta W_i - \theta_i \Delta t)^2 / 2\Delta t)$.  Take the ratio, expand, and take the continuum limit.  The $\theta\,dW$ and $\tfrac{1}{2}\theta^2\,dt$ terms fall out.

### Worked Example: Constant Drift

The simplest Girsanov.  $P$: standard Brownian motion, $dX = dW$.  $Q$: Brownian with drift $\mu$, $dX = \mu\,dt + d\tilde W$.  Then $\theta = \mu$ constant, and:

$$
\frac{dQ}{dP} = \exp\left(\mu W_T - \tfrac{1}{2}\mu^2 T\right)
$$

Check: compute $\mathbb{E}_P[dQ/dP]$.  This should be $1$.  It is, because $\mathbb{E}[e^{\mu W_T}] = e^{\mu^2 T/2}$ for Gaussian $W_T$, and the two factors cancel.

Sanity: under $Q$, the mean of $X_T$ should be $\mu T$.  Compute via importance sampling: $\mathbb{E}_Q[X_T] = \mathbb{E}_P[X_T \cdot dQ/dP]$.  With $X_T = W_T$ under $P$ and explicit Gaussian moments, you get $\mu T$.  Works.

This is also the foundation of **likelihood-based parameter estimation**: given a path and a parametric family of SDEs, the Girsanov exponent is the log-likelihood, and you maximize over parameters.

**Technical caveat**: Girsanov requires $\theta$ to satisfy the Novikov condition $\mathbb{E}[\exp(\tfrac{1}{2}\int_0^T \theta^2\,dt)] < \infty$, which ensures the exponential is a genuine density (integrates to $1$).  If $\theta$ grows too fast, the change of measure fails: the two laws become mutually singular.  In practice this matters when $\theta$ is unbounded, e.g.  state-dependent with linear growth.  For bounded $\theta$ you're always fine.  The failure mode when Novikov fails is real: you can't actually reweight the path measure because the "likelihood ratio" isn't a probability density.  This is one of the measure-theoretic points physicists do need to know about, at least enough to recognize.

## Onsager-Machlup: Path Probability

Related but distinct: Girsanov compares two path measures; Onsager-Machlup writes down an action for a single path measure relative to pure Brownian.

Roughly (up to Jacobian subtleties that are actually important and I'll flag):

$$
P[\text{path}\ x(\cdot)] \propto \exp\left(-\tfrac{1}{2}\int_0^T \frac{(\dot x - b(x))^2}{\sigma^2}\,dt\right)
$$

The action $S[x] = \tfrac{1}{2}\int (\dot x - b(x))^2 / \sigma^2 \,dt$ is **Onsager-Machlup**.  Its minimizer is the "most probable path".

This is suggestive.  It looks just like a Feynman path integral with a Lagrangian $\mathcal{L} = \tfrac{1}{2}(\dot x - b)^2 / \sigma^2$.  In the small-noise limit, the most probable path dominates: this is the Freidlin-Wentzell large deviation framework (see [Instantons in Statistical Physics]).

### Caveat: The Jacobian

Be careful.  "Most probable path" isn't quite what you think, because what you're maximizing is not a probability of a path (paths have probability zero) but a density with respect to a reference measure.  The reference matters.

The honest statement is a small-tube probability: the probability of staying within an $\epsilon$-tube of a given path $\phi$ is

$$
P[\text{tube}_\epsilon(\phi)] \asymp \exp\left(-\frac{1}{2}\int (\dot \phi - b)^2/\sigma^2\,dt - \tfrac{1}{2}\int \partial_x b(\phi)\,dt\right)
$$

as $\epsilon \to 0$.  That second term (the Jacobian / divergence term) is often dropped in the physics literature, but it matters when comparing paths at the same exponent.  See Graham's work (1977) and follow-ups.

Also: in the Stratonovich convention (midpoint rule), the Jacobian term is symmetric and has a different form than the Itô one.  The "most probable path" can shift under conventions.  Not a physical disagreement, but a real bookkeeping headache.

tl;dr the action is the right idea, the most probable path is a useful concept, the prefactors matter more than you might initially think.

## Doob h-Transform: Conditioning on the Future

Suppose you have the SDE $dX = b\,dt + \sigma\,dW$ and you want to condition on some event in the future: the process survives in a region, hits a target, reaches $x_1$ at time $T$, etc.

The conditioned process is also a Markov process, driven by a modified SDE.  The modification is a drift shift.

**Doob's h-transform.** Let $h(x, t)$ be a positive harmonic function of the backward generator: $\partial_t h + L h = 0$, with boundary conditions encoding the conditioning.  Then the conditioned dynamics is:

$$
dX = \left(b + \sigma^2\,\partial_x \log h\right)dt + \sigma\,dW
$$

An extra drift term $\sigma^2 \partial_x \log h$ pushes the process toward regions where the conditioning is more likely to be satisfied.

### Why This Is Useful

Rare-event simulation.  Suppose you want trajectories that reach a rare target.  Naive simulation has you sampling forever waiting for the rare event.  Doob's construction tells you the optimal biased dynamics that produces exactly those conditioned trajectories.  In practice you'd use an approximation to $h$ (the "committor" function in the chemistry literature) since solving the PDE exactly is as hard as the original rare-event problem.  But even approximate Doob transforms speed things up dramatically.

### Brownian Bridge

Canonical example.  Condition Brownian motion on hitting zero at time $T$: $W_0 = 0$, $W_T = 0$.  The conditional density at the target is a Gaussian kernel, and the harmonic function is:

$$
h(x, t) = \frac{1}{\sqrt{2\pi(T-t)}} e^{-x^2/2(T-t)}
$$

Compute $\partial_x \log h = -x/(T-t)$.  The conditioned SDE:

$$
dX = -\frac{X}{T-t}\,dt + dW
$$

A time-dependent OU process with restoring force that blows up as $t \to T$.  This pulls the process back to zero in the nick of time.  This is the Brownian bridge.

Doob's framework works for any conditioning: survival in a domain ($h$ = first eigenfunction of the killed generator), reaching a specific target, conditioning on a rare trajectory.  The move is always the same: solve a linear PDE for $h$, add $\sigma^2 \nabla \log h$ to the drift.

This is also how you get dynamics for rare-event simulation, optimal transport over paths, and conditional Langevin samplers.  Very worth having in your toolbox.

## Large Deviations and Instantons

A quick pointer, since there's a whole other seed on this.

In the small-noise limit $\sigma \to 0$ (or $\epsilon \to 0$ after rescaling $\sigma \to \sqrt{\epsilon}\sigma$), path probabilities concentrate.  The **Freidlin-Wentzell** theorem says:

$$
P[\text{path near}\ \phi] \asymp \exp\left(-\frac{1}{\epsilon}\cdot\tfrac{1}{2}\int (\dot\phi - b(\phi))^2/\sigma^2\,dt\right)
$$

The exponent is the Onsager-Machlup action (without the Jacobian, since the Jacobian is $O(1)$ and the action is $O(1/\epsilon)$: the Jacobian is subleading).  Rare events are dominated by the minimizing path, the **instanton**.

This is the framework for rare-event asymptotics in SDE systems: Kramers escape, noise-induced transitions, extreme fluctuations.  The instanton is the classical trajectory of the effective Lagrangian $\mathcal{L} = \tfrac{1}{2}(\dot x - b)^2/\sigma^2$.  See [Instantons in Statistical Physics] for the worked machinery, and [From Witten to Kramers] for the connection to topology.

## Numerical Simulation: Euler-Maruyama

You probably want to actually compute something.  The dumb default:

$$
X_{n+1} = X_n + b(X_n)\,\Delta t + \sigma(X_n)\sqrt{\Delta t}\,Z_n
$$

where $Z_n \sim \mathcal{N}(0,1)$ i.i.d.  This is **Euler-Maruyama** and it's the Itô discretization.  Note the $\sqrt{\Delta t}$ scaling of the noise: a time step of $\Delta t$ produces an $\mathcal{N}(0, \Delta t)$ increment, matching $dW$.  If you accidentally write $\sigma\,\Delta t\,Z$, your noise is too small by a factor of $\sqrt{\Delta t}$.  Classic bug.

Strong convergence order $1/2$: $\mathbb{E}[\vert X_T^{\text{exact}} - X_T^{\text{EM}}\vert] = O(\sqrt{\Delta t})$.  Weak convergence (for expectations of observables) is order $1$.

**Milstein** improves the strong order to $1$ by adding the leading $\sigma\sigma'$ correction:

$$
X_{n+1} = X_n + b\,\Delta t + \sigma\sqrt{\Delta t}\,Z_n + \tfrac{1}{2}\sigma\sigma'\,\Delta t\,(Z_n^2 - 1)
$$

The $(Z_n^2 - 1)$ factor is the Itô correction in discrete form.  For additive noise ($\sigma' = 0$), Milstein and Euler-Maruyama coincide.

Higher-order schemes exist (stochastic Runge-Kutta) but are annoying in multiple dimensions because you need iterated integrals $\int\int dW^i dW^j$ that don't reduce to simple quadratic variation.  For most physics applications, Euler-Maruyama with a small time step is fine.

**Stratonovich EM** replaces $\sigma(X_n)$ with $\sigma(X_n + \tfrac{1}{2}\sigma\sqrt{\Delta t}\,Z_n)$ (midpoint).  Or, equivalently, do the conversion to Itô first and then use the standard scheme.

## The Named Tools, Unified

Look back at what we did.  Several of the named tools are the same move:

- **Girsanov** shifts the drift from $b$ to $b + \sigma\theta$, and the price is the exponent $\int \theta\,dW - \tfrac{1}{2}\int \theta^2\,dt$.
- **Doob h-transform** shifts the drift from $b$ to $b + \sigma^2 \nabla \log h$.  This is Girsanov with $\theta = \sigma \nabla \log h$.
- **Onsager-Machlup** is the log-density of paths, which is the Girsanov exponent with $\theta = \dot x / \sigma - b/\sigma$ (comparing against pure Brownian motion).
- **Freidlin-Wentzell** is Onsager-Machlup in the small-noise limit, i.e.  Laplace's method on path integrals.

All of these are manipulations of the same path-space Radon-Nikodym derivative.  Once you see it, the names collapse into one operation: shift the drift, pay an Itô-corrected exponent.

Once you see it, rare-event sampling, variational inference on paths, stochastic control, and instanton theory all look like the same subject with different terminology.  That's the real payoff of having Girsanov in your head: it's not an arcane theorem, it's the thing every path-measure manipulation secretly is.

## What's Next

A short pointer list.  Each of these deserves its own seed.

- **Multidimensional / manifold SDEs.** Itô's lemma in $\mathbb{R}^n$ picks up a covariance matrix and a Hessian.  On manifolds you need to worry about coordinate covariance: Stratonovich is natural, Itô requires a connection.  Brownian motion on a Riemannian manifold is generated by $\tfrac{1}{2}\Delta_g$ where $\Delta_g$ is the Laplace-Beltrami operator.  Stratonovich notation commutes with coordinate changes; Itô notation requires extra Christoffel-symbol terms to do the same.  The rolling-without-slipping construction (Itô's intrinsic definition) is beautiful and worth the detour.
- **Stroock-Varadhan.** Martingale problems as a rigorous foundation for SDEs: characterize the law of the process by which functions of it are martingales.  Cleaner than pathwise definitions when the coefficients are rough.
- **Malliavin calculus.** Differentiation on Wiener space.  Lets you compute sensitivities of path-functionals, integration by parts on path space, density smoothness.  Practical use: Greeks in finance, adjoints in filtering.
- **Rough paths.** Terry Lyons' framework.  Extends SDE theory to non-Brownian drivers (fractional Brownian, signal processing, neural networks).  Makes sense of "$\int f\,dx$" for very irregular $x$.
- **Jump processes.** Lévy processes, SDEs with jumps, Poisson stochastic integrals.  The analogue of Itô's lemma includes a jump term $\sum [f(X + \Delta X) - f(X)]$.  The drift-diffusion-jump trichotomy is exhaustive for Markov processes with independent increments.
- **Stochastic control and BSDEs.** Backward stochastic differential equations.  Dual to forward SDEs, arise in optimal control, finance, and (recently) in the theory of neural network training.  The Hamilton-Jacobi-Bellman equation is to SDE control what the classical HJB is to deterministic control, with an Itô term.  Neat connection: variational characterizations of free energy via stochastic control (Fleming-Sheu, Boué-Dupuis).
- **Numerical methods.** Euler-Maruyama is the dumb default and converges at $O(\sqrt{\Delta t})$ in strong sense.  Milstein fixes the strong order to $O(\Delta t)$.  Higher-order methods (Runge-Kutta for SDEs) exist but are finicky because of the non-commuting noise terms.

## Summary

- Brownian motion is characterized by $dW^2 = dt$ and you mostly don't need to know anything else.
- Itô calculus has a non-trivial chain rule (Itô's lemma) with a second-derivative term.
- Stratonovich obeys ordinary calculus but loses the martingale property.
- Fokker-Planck evolves densities; backward Kolmogorov evolves observables.  They are adjoint.
- Feynman-Kac is one line and recovers Schrödinger-in-imaginary-time.
- Girsanov, Doob, Onsager-Machlup, Freidlin-Wentzell are all drift-shift manipulations of path measures.  Same move, different framing.
- Rare events are dominated by instantons: minimizers of the Onsager-Machlup action in the small-noise limit.

That's enough stochastic calculus to read most of the literature.  If you need the measure theory, Kallenberg is on the shelf.  If you need to compute something, you probably don't.

One parting thought.  Physicists already have a path integral formulation of stochastic dynamics in the form of Martin-Siggia-Rose / Janssen / De Dominicis response-field theory.  That's essentially Onsager-Machlup with auxiliary fields, set up so that perturbation theory (diagrammatics, renormalization) works cleanly.  If you come from QFT, MSRJD is the bridge: the same math as above, reorganized into Feynman rules.  See [Instantons in Statistical Physics] for the small-noise / saddle-point version.

***

*See also: [Instantons in Statistical Physics], [From Witten to Kramers], [Asymptotics, Borel, and Stokes].*

Written with Claude.
