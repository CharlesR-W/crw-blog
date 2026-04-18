---
title: "Mean Field Theory"
date: 2026-04-18
motivation: "Mean field is the same idea wearing two hats.  Physicists use it to solve the Ising model and find phase transitions; ML people use it to approximate posteriors and derive the ELBO.  The unifying fact is that mean field is the best product-form approximation to a distribution, in KL.  Once you see that, the Curie-Weiss equation and coordinate-ascent variational inference stop looking like separate subjects."
background: "Undergrad statistical mechanics (partition functions, free energy) and a passing acquaintance with variational inference or graphical models.  If you've seen the ELBO once, or you've done an Ising model homework, you have enough background.  If you've done both, even better - this post is about seeing that they were the same thing all along."
llm: "Claude"
tags: [seed]
math: true
---

# Mean Field Theory

## The Idea in One Line

Replace a many-body interaction with a one-body problem in an effective field you determine self-consistently.  That's it.  Everything else - Curie-Weiss, the Bethe approximation, variational inference, the ELBO, mean-field games - is this one move, specialized.

I want to unify the two big traditions here.  Physicists meet mean field through the Ising model and phase transitions.  ML people meet it through variational inference.  These look different on the surface, but they're the same variational principle: the best product-form approximation to an intractable distribution, measured by KL.  Once you see that, the Curie-Weiss self-consistency equation and coordinate-ascent VI are literally the same algorithm.

## Ising and Curie-Weiss

Start with the canonical physics example.  Ising spins $s_i \in \\{-1, +1\\}$ on some graph, Hamiltonian

$$
H(s) = -J \sum_{\langle i,j \rangle} s_i s_j - h \sum_i s_i
$$

and Gibbs measure $p(s) \propto e^{-\beta H(s)}$.  The pair interaction $s_i s_j$ is what makes this hard.  Mean field says: fix a site $i$, and replace each neighbor $s_j$ by its expectation $m = \langle s_j \rangle$.  Then site $i$ sees an effective field

$$
h_{\text{eff}} = h + J z m
$$

where $z$ is the coordination number (number of neighbors).  Each spin is now independent, feeling a one-body field $h_{\text{eff}}$.  A single spin in a field $h_{\text{eff}}$ has magnetization $\tanh(\beta h_{\text{eff}})$.  But this is supposed to equal $m$, because we assumed every site has the same expectation.  So:

$$
\boxed{\,m = \tanh\!\big(\beta (h + J z m)\big)\,}
$$

That's the Curie-Weiss equation.  It's self-consistent: $m$ is an input (through $h_{\text{eff}}$) and an output (through $\langle s \rangle$), and the solution is wherever they agree.

### Phase Transition

Set $h = 0$ and look for solutions.  $m = 0$ is always one.  For small $\beta$ (high $T$), it's the only one - the curve $\tanh(\beta J z m)$ has slope $\beta J z < 1$ at the origin and crosses the line $y = m$ only once.  At $\beta_c J z = 1$, the slope hits 1, and for $\beta > \beta_c$ two new solutions appear at $\pm m_0 \ne 0$.  The $m = 0$ solution is still there but becomes unstable.

So mean field predicts a ferromagnetic phase transition at $T_c = J z / k_B$.  Above $T_c$, the magnet is disordered; below, the $\mathbb{Z}_2$ symmetry $s \to -s$ spontaneously breaks and the system picks one of the two minima.  The order parameter $m$ grows from zero as $(T_c - T)^{1/2}$ near criticality - you get this by Taylor expanding $\tanh(x) = x - x^3/3 + \ldots$ in the Curie-Weiss equation.

### Mean-Field Exponents (And Where They Fail)

Same Taylor expansion gives you the rest of the critical exponents:

- $m \sim (T_c - T)^{1/2}$, so $\beta = 1/2$
- $\chi \sim \vert T - T_c \vert^{-1}$, so $\gamma = 1$
- $m \sim h^{1/3}$ at $T_c$, so $\delta = 3$
- specific heat has a jump discontinuity, so $\alpha = 0$

These are the **mean-field exponents**.  They're wrong for the 2D and 3D Ising model.  Real 2D Ising has $\beta = 1/8$; 3D Ising has $\beta \approx 0.326$.  Mean field is exact only in the limit of infinite coordination number (or equivalently, infinite dimension).

The rule of thumb is the **upper critical dimension** $d_c$.  For Ising, $d_c = 4$: above four dimensions, mean-field exponents are correct, because fluctuations are suppressed enough that the naive approximation works.  Below $d_c$, fluctuations dominate near the critical point and you need the renormalization group to get the right exponents.  The Ginzburg criterion quantifies when mean field is self-consistent; it basically fails wherever the neglected fluctuations are comparable to the mean.

Fine.  Mean field gets the qualitative picture - there's a transition, there's spontaneous symmetry breaking, there's an order parameter - and the quantitative details wrong below $d_c$.  That's still a lot.

## The Variational View (Here's the Bridge)

Now the move that unifies everything.  Given a distribution $p(x) \propto e^{-\beta H(x)}$ we can't sample, what's the best product-form approximation?  "Best" measured how?  Use KL divergence:

$$
q^* = \arg\min_{q \in \mathcal{Q}_{\text{prod}}} \mathrm{KL}(q \,\Vert\, p)
$$

where $\mathcal{Q}_{\text{prod}} = \\{q : q(x) = \prod_i q_i(x_i)\\}$.  You want to minimize $\mathrm{KL}(q \,\Vert\, p)$ rather than $\mathrm{KL}(p \,\Vert\, q)$ because the former is tractable (expectations under $q$, which factorizes) and the latter is not (expectations under $p$, which is what you're trying to avoid).

Write it out:

$$
\mathrm{KL}(q \,\Vert\, p) = \mathbb{E}_q[\log q] - \mathbb{E}_q[\log p] = -H[q] + \beta \mathbb{E}_q[H] + \log Z
$$

Dropping the $\log Z$ constant, minimizing KL is the same as minimizing the **variational free energy**

$$
F[q] = \mathbb{E}_q[H] - \frac{1}{\beta} H[q]
$$

which is exactly the physicist's (Helmholtz) free energy $F = U - TS$, evaluated at a trial distribution $q$.  The true $p$ is the $q$ that minimizes $F$.  Any product-form $q$ gives an upper bound on the true free energy (Gibbs-Bogoliubov inequality).

**This is the bridge.**  The ML derivation and the physics derivation are the same variational principle.  Minimize $F[q]$ over product distributions - you get mean field.

### Naive Mean Field as Coordinate Ascent

For each factor $q_i$, take the derivative of $F[q]$ (with Lagrange multiplier for normalization) and set to zero.  You get

$$
q_i^*(x_i) \propto \exp\!\big(\mathbb{E}_{q_{-i}}[\log p(x)]\big)
$$

where $q_{-i} = \prod_{j \ne i} q_j$.  Each factor is the exponential of the expected log-joint with the other factors held fixed.  Iterate: update $q_1$ holding $q_{2}, \ldots$ fixed, then $q_2$, then $q_3$, etc.  Coordinate ascent.  It converges (monotonically decreases $F$) but typically to a local minimum.

Apply this to Ising.  $q_i(s_i) = \frac{1}{2}(1 + m_i s_i)$ for $s_i \in \\{-1, +1\\}$.  Plug in, do the coordinate update:

$$
q_i^*(s_i) \propto \exp\!\Big(\beta s_i \big(h + J \sum_{j \sim i} m_j\big)\Big)
$$

which is a spin in an effective field $h + J \sum_{j \sim i} m_j$.  Its magnetization is $\tanh$ of that field times $\beta$.  If we further assume homogeneity $m_i = m$, we recover Curie-Weiss exactly.

So: Curie-Weiss is coordinate-ascent variational inference on the Ising Gibbs measure, with a homogeneity assumption.  The kicker is that these weren't ever separate methods.

### ELBO

In ML, the same computation gets packaged as evidence lower bound.  You have latent $z$, observed $x$, joint $p(x, z)$, and want the posterior $p(z \vert x)$.  Write

$$
\log p(x) = \mathrm{KL}(q(z) \,\Vert\, p(z \vert x)) + \mathcal{L}[q]
$$

where

$$
\mathcal{L}[q] = \mathbb{E}_q[\log p(x, z)] - \mathbb{E}_q[\log q(z)]
$$

is the ELBO.  Since KL is nonneg, $\mathcal{L}[q] \le \log p(x)$, with equality when $q = p(z \vert x)$.  Maximizing ELBO over $q$ is the same as minimizing $\mathrm{KL}(q \,\Vert\, p(z \vert x))$, i.e., finding the best approximation to the posterior.

Restrict to $q(z) = \prod_i q_i(z_i)$ and you're doing naive mean-field VI.  The coordinate updates are

$$
q_i^*(z_i) \propto \exp\!\big(\mathbb{E}_{q_{-i}}[\log p(x, z)]\big)
$$

Exact same formula.  The physicists' "minus free energy" is the statisticians' "ELBO" up to a constant.

## Where Naive MF Fails

Naive mean field underestimates the entropy of $p$ and misses correlations.  Factorizing $q(x) = \prod q_i(x_i)$ forces zero correlation among variables that are correlated under $p$.  The $\mathrm{KL}(q \,\Vert\, p)$ objective also has a **mode-seeking** bias: $q$ will concentrate on a single mode of $p$ and ignore others, because putting mass where $p$ is small costs a lot (the $\log q / p$ blows up where $p \to 0$).  This is why naive MF on a bimodal posterior typically picks one mode and calls it a day.

In physics language: naive MF misses fluctuation-fluctuation correlations.  Below the upper critical dimension, those correlations are what drive the critical behavior, and the critical exponents come out wrong.

## Bethe / Bethe-Peierls: The Next Step

The next order of approximation is to treat pairs (or small clusters) instead of single sites.  Bethe-Peierls (1935) does this on the Ising model: consider a central spin and all its neighbors as a cluster, treat interactions inside the cluster exactly, and parametrize the field from outside the cluster self-consistently.  This captures nearest-neighbor correlations that naive MF throws away, and gives better (though still imperfect) critical exponents.

The clean modern statement is via the **Bethe free energy**, which is exact on trees.  Write the joint on a tree as

$$
p(x) = \frac{\prod_{(i,j) \in E} p_{ij}(x_i, x_j)}{\prod_i p_i(x_i)^{d_i - 1}}
$$

where $d_i$ is the degree of $i$.  The Bethe free energy is the corresponding variational functional in the marginals $q_i, q_{ij}$.  Minimizing it subject to consistency constraints gives fixed-point equations that, on trees, coincide with **belief propagation** (BP).

On a loopy graph, the factorization above is not exact, but you can still write down the Bethe free energy and minimize it.  This is **loopy BP**, and its fixed points are stationary points of the Bethe free energy (Yedidia-Freeman-Weiss).  It's a much better approximation than naive MF whenever there's local tree-like structure, which is most of the time.

In the variational-inference world, the corresponding upgrade is **expectation propagation** and related "structured" approximations - give $q$ more structure than full factorization, at the cost of more expensive updates.

## Replica and Cavity (Briefly)

For disordered systems - spin glasses, random constraint satisfaction - the replica trick and the cavity method are the standard tools.  Replica computes $\overline{\log Z}$ via $\overline{Z^n}$ for integer $n$, analytically continues to $n \to 0$, and ends up with an optimization over overlap matrices $Q_{ab}$ between replicas.  Replica-symmetric solutions are essentially mean field on the disorder-averaged problem.  Breaking replica symmetry captures the hierarchical structure of glassy minima.

The cavity method is the "physical" version of the same thing: remove a variable, compute the effective field on it from the rest of the system, self-consistently.  On tree-like random graphs, cavity $=$ BP.  On denser graphs, the Thouless-Anderson-Palmer (TAP) equations give the cavity corrections to naive MF.

I won't derive any of this here.  The point is just that these are all elaborations of the same core move: replace an interacting problem with a self-consistent one-body problem, with whatever small-cluster corrections you can afford.

## Where To Go Next

Two active directions that mean field opens onto, one sentence each.

**Mean-field games.**  Lasry-Lions and Huang-Caines-Malhame.  Take $N$ interacting agents, send $N \to \infty$, replace pairwise interactions by interaction with the population density.  You get a coupled Hamilton-Jacobi-Bellman / Fokker-Planck system that is the continuum limit of the game.  Same move as Ising mean field, now for strategic agents.

**Neural networks at infinite width.**  NTK (neural tangent kernel) is a mean-field limit where the network stays close to initialization and training becomes kernel regression.  The "mean-field scaling" (as opposed to NTK scaling) keeps the features plastic and gives a nontrivial Wasserstein-gradient-flow dynamics on the distribution of neurons.  Different parametrizations, different regimes, same basic fact: in the $N \to \infty$ limit of a many-body interacting system (the neurons), the problem becomes a one-body problem in an effective field (the population distribution of features).

## tl;dr

Mean field is one idea, three times:

- Physicists: self-consistent one-body field on the Ising Gibbs measure $\to$ Curie-Weiss, phase transition, mean-field exponents, breaks down below $d_c$.
- ML: best factorized approximation to a posterior $\to$ coordinate-ascent VI, ELBO.
- The bridge: both are minimizing $\mathrm{KL}(q \,\Vert\, p)$ over product distributions.  Same variational problem, different applications.

Upgrades: Bethe for correlations, loopy BP on graphs, replica/cavity for disordered systems.  Generalizations: mean-field games, infinite-width neural networks.  The common thread is the $N \to \infty$ limit that collapses a many-body problem into an effective one-body problem coupled to its own statistics.

Written with Claude.
