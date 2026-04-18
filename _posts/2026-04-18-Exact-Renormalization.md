---
title: "Exact Renormalization from Many Angles"
date: 2026-04-18
motivation: "Renormalization isn't a bag of tricks for curing divergences.  It's a semigroup flow on the space of theories, and there's an exact PDE for that flow.  Once you see it as a flow, the same object keeps showing up in disguise: Fokker-Planck equations, score-based generative models, gradient flows on distribution space, neural network training.  The exact RG is the common spine."
background: "A first course in QFT (you've seen path integrals and one-loop diagrams), some statistical mechanics, comfort with functional derivatives.  No prior exposure to functional RG needed, but it helps if you've at least met Wilsonian RG in some form."
llm: "Claude"
tags: [seed]
math: true
---

# Exact Renormalization from Many Angles

## BLUF

Renormalization is a flow on the space of theories.  There are exact PDEs for that flow.  The two canonical ones are Polchinski's equation (for the Wilsonian effective action) and the Wetterich equation (for the effective average action).  They're Legendre-transform duals of each other.  Both are exact - no perturbative resummation, no diagrammatic approximation.  The perturbative RG you learned in grad school is a projection of these exact flows onto a finite-dimensional subspace of couplings.

Once you have the flow picture, the same mathematical object shows up everywhere: Fokker-Planck equations for diffusion, score-based generative models in ML, gradient flows on distribution space (Otto-Wasserstein), neural network training dynamics.  This seed tours those viewpoints.

I'll flag where things get formal/heuristic.  Some of the ML-physics analogies are more suggestive than rigorous.

## Why Bother With "Exact" RG?

Standard Wilsonian RG tells a story like: "integrate out a momentum shell, rescale, see how the couplings change, read off beta functions".  That's fine and it's how we compute things, but it leaves you wondering what object you're actually flowing through.  In my [earlier musings on running couplings](/2024/10/03/Musings-on-Running-Couplings-and-Invariant-Subspaces.html) I asked the same question from the dynamical-systems side: what IS the space you're flowing on, and when does truncating to a few couplings make sense?

The exact RG answers this cleanly.  The object is the Wilsonian effective action $S_\Lambda[\phi]$ (a functional on field configurations), the flow parameter is the cutoff $\Lambda$ (or $t = \log \Lambda$), and there's a closed PDE for $\partial_\Lambda S_\Lambda$ that makes no perturbative approximation.  Truncating to a finite set of couplings is a projection - sometimes a good one, sometimes a bad one, but at least you now know what you're projecting.

The kicker is that once you have this picture, you discover the same PDE (up to transforms) is the Fokker-Planck equation for a diffusion, is the loss landscape flow of a score-based generative model, is a gradient flow in Wasserstein space.  The physics-ML unification that got trendy in the last few years runs through exact RG.

## The Setup

Start with a scalar QFT (Euclidean, for definiteness).  The partition function with a UV cutoff $\Lambda_0$ is

$$
Z = \int_{\Lambda_0} \mathcal{D}\phi \, e^{-S_0[\phi]}
$$

where the subscript on the measure means "modes with momentum $\lvert p \rvert > \Lambda_0$ are suppressed".  Concretely, split the propagator into a high-mode part and a low-mode part using a smooth cutoff function $K(p^2/\Lambda^2)$:

$$
K(p^2/\Lambda^2) = \begin{cases} 1 & \lvert p \rvert \ll \Lambda \\ 0 & \lvert p \rvert \gg \Lambda \end{cases}
$$

The idea is that we want to integrate out modes with $\lvert p \rvert > \Lambda$ and absorb their contribution into an effective action $S_\Lambda[\phi]$ for the remaining modes.  Exactness means: we do this integration without approximation, and we demand the partition function is invariant under changes in $\Lambda$.

That last condition - $\partial_\Lambda Z = 0$ - is the heart of it.  Differentiating under the integral sign and demanding cancellation gives Polchinski's equation.

## Polchinski's Equation

Here's the canonical form, for a free propagator $G_\Lambda(p) = K(p^2/\Lambda^2) / p^2$ and interaction part $S^{\mathrm{int}}_\Lambda$:

$$
\partial_\Lambda S^{\mathrm{int}}_\Lambda = \tfrac{1}{2} \int \frac{d^d p}{(2\pi)^d} \, \partial_\Lambda G_\Lambda(p) \left( \frac{\delta S^{\mathrm{int}}_\Lambda}{\delta \phi(p)} \frac{\delta S^{\mathrm{int}}_\Lambda}{\delta \phi(-p)} - \frac{\delta^2 S^{\mathrm{int}}_\Lambda}{\delta \phi(p) \delta \phi(-p)} \right)
$$

Let me unpack.  The propagator factor $\partial_\Lambda G_\Lambda(p)$ is localized near $\lvert p \rvert \sim \Lambda$ - that's the "shell" being integrated out.  The two terms in parentheses have clear interpretations:

- **Quadratic term** $(\delta S / \delta \phi)^2$.  This tracks tree-level flow.  If you think diagrammatically, this is joining two external legs into a propagator - sewing tree graphs together.  Leading-order classical flow.

- **Hessian term** $\delta^2 S / \delta \phi \, \delta \phi$.  This tracks loops.  A functional second derivative with the shell propagator closes a loop, which is what integrating out a shell of modes at one-loop actually does.

That's it.  No diagrams truncated, no couplings assumed small.  This is an exact functional PDE and any solution $S^{\mathrm{int}}_\Lambda[\phi]$ tells you the effective action at scale $\Lambda$.

### Why is it tractable?

"Exact" does not mean "solvable".  $S^{\mathrm{int}}_\Lambda$ is a functional on an infinite-dimensional space of field configurations, and the PDE is nonlinear.  In practice you project: expand $S^{\mathrm{int}}_\Lambda$ in some basis (monomials in $\phi$, derivative expansion, etc.), truncate to a finite set of couplings, and turn the functional PDE into ODEs for those couplings.

The value of knowing the exact equation is that you can *check* your truncation, estimate errors, and see what you're leaving out.  Perturbative RG is the truncation where you keep only renormalizable couplings at tree level and ignore the Hessian term beyond one loop.  You can do much better.

### A cautionary note on conventions

Polchinski's equation has about six equivalent forms depending on whether you're flowing the full action or just the interaction, whether you use $\Lambda$ or $t = \log \Lambda$, whether $K$ is a cutoff on the propagator or on the measure, and what sign conventions you picked.  Don't try to memorize the form.  Understand the derivation - $\partial_\Lambda Z = 0$ plus a change of cutoff - and rederive as needed.

## The Wetterich Equation

Polchinski flows the Wilsonian effective action $S^{\mathrm{int}}_\Lambda$.  There's a dual formulation that flows the 1PI (one-particle-irreducible) generating functional, i.e. the effective action $\Gamma_k[\phi]$ where $k$ is an IR cutoff.  The Wetterich equation:

$$
\partial_k \Gamma_k[\phi] = \tfrac{1}{2} \mathrm{Tr}\left[ \left( \Gamma_k^{(2)}[\phi] + R_k \right)^{-1} \partial_k R_k \right]
$$

Here $\Gamma_k^{(2)} = \delta^2 \Gamma_k / \delta \phi \delta \phi$ is the Hessian and $R_k$ is an IR regulator that suppresses modes with $\lvert p \rvert < k$.  The trace is over momenta and any internal indices.

This is sometimes called the "one-loop-exact" form because the RHS has the structure of a one-loop diagram - a trace-log derivative, really - but with the *full* propagator $(\Gamma_k^{(2)} + R_k)^{-1}$ instead of the tree-level one.  All the nonlinearity is hidden in $\Gamma_k^{(2)}$, which depends on the field $\phi$ in arbitrarily complicated ways.

### Polchinski vs. Wetterich

Both are exact.  Both describe the same physics.  They're related by a Legendre transform (schematically: $\Gamma_k$ is the Legendre transform of $W_k = \log Z_k$, and $S^{\mathrm{int}}_\Lambda$ is tied to $W$ in a similar way).

Practical differences:

- **Polchinski** is in "tree-graph form".  The quadratic $(\delta S)^2$ term is explicit, good for seeing flow structure but awkward for truncations.
- **Wetterich** is in "one-loop form".  Cleaner structure, easier to truncate sensibly, used in most modern functional RG (FRG) work.

If you only have patience to learn one, learn Wetterich.  It's the one practitioners use.

## Stochastic-Process View

Here's where things get fun.  The exact RG equation has the structure of a Fokker-Planck equation.

Think of $e^{-S_\Lambda[\phi]}$ as a probability distribution over field configurations.  As $\Lambda$ decreases, this distribution evolves.  The evolution equation is linear in the distribution (because $S$ is in the exponent and we can recast in terms of $P = e^{-S}$):

$$
\partial_t P_t[\phi] = -\partial_\phi (\mu[\phi] P_t) + \tfrac{1}{2} \partial_\phi^2 (D[\phi] P_t)
$$

where $t = -\log \Lambda$ (flowing toward IR), $\mu$ is a drift, and $D$ is a diffusion.  That's literally a Fokker-Planck equation for a diffusion process on field space.

What's the diffusion?  It's Gaussian noise at scale $\Lambda$ - the smooth cutoff $K$ generates Gaussian fluctuations that wash out modes as $\Lambda$ shrinks.  The drift comes from the gradient of the action.

So the exact RG flow of an action is equivalent to a diffusion process on field configurations.  The stationary point of the diffusion (a fixed point of the flow) is where drift and diffusion balance.

This is the bridge to everything that follows.

## Diffusion Models and Score Matching

Now the ML angle, which I find genuinely striking.

Score-based generative models (diffusion models, DDPM, etc.) work like this: take your data distribution $p_{\mathrm{data}}(x)$, add Gaussian noise progressively over "time" to get a family $p_t(x)$ that interpolates between data ($t=0$) and pure noise ($t=T$).  Train a neural network to learn the **score** $\nabla_x \log p_t(x)$.  Then sample by running the reverse-time SDE, which uses the score to denoise.

The forward noising process is *exactly* the kind of Fokker-Planck flow we just described.  And the score is *exactly* the gradient of the log-probability, which in RG language is $-\nabla_\phi S_t[\phi]$ (minus the gradient of the effective action).

Cash out the analogy:

| Physics (RG) | ML (diffusion models) |
|---|---|
| Cutoff $\Lambda$ (or $t = \log \Lambda$) | Noise time $t$ |
| Field configuration $\phi$ | Data point $x$ |
| Effective action $S_\Lambda[\phi]$ | $-\log p_t(x)$ |
| Score $-\nabla S$ | $\nabla \log p_t$ |
| Fokker-Planck for $P_t = e^{-S_\Lambda}$ | Forward SDE for $p_t$ |
| "Integrating out UV modes" | "Adding noise" |

The reverse-time sampling in diffusion models is, up to transposing the arrow, running RG backward - regenerating UV structure from IR data.  The NN learns the effective-action gradient, which is exactly what you'd want if you were doing variational RG.

Is this a deep coincidence or a shallow one?  Honestly, I think it's genuinely deep.  Both are doing coarse-graining on distributions, and the exact math is the same.  Whether this leads anywhere in either direction (better RG from ML, better ML from RG) is an open research question with plenty of papers in the last two years.  Cohen-Gur-Ari, Beny, and others have been pushing various versions of this.

## Information-Geometric View

The exact RG is a flow on the space of probability distributions $P_\Lambda[\phi] = e^{-S_\Lambda[\phi]} / Z$.  That space has structure: the Fisher information metric, relative entropy (KL divergence), the full apparatus of information geometry.

A natural question: is the Wetterich flow a *gradient* flow in some metric?

The answer is "kinda, formally".  There's work by Polonyi, Shalaby, and others arguing that exact RG is a gradient flow of relative entropy with respect to a Fisher-information-like metric on theory space.  The details are tricky - the metric isn't canonical, the gradient structure depends on what you call "conjugate variables", and some of the cleaner statements are formal.  But the spirit is right.

This connects directly to the [Otto-Wasserstein picture](/2026/04/18/Otto-Calculus-and-Wasserstein.html): there too, Fokker-Planck is a gradient flow of free energy in the Wasserstein metric on probability measures.  The exact RG is playing the same game, just on the infinite-dimensional space of field-theoretic probability measures.

Cash out: exact RG flow might be characterized variationally as

$$
\partial_t P_t = -\mathrm{grad}_{g} F[P_t]
$$

for some free energy $F$ and some metric $g$ on distribution space.  If you get the right $F$ and $g$, gradient flow reproduces Wetterich.  There are multiple candidate pairs.  The flag: nobody has a fully satisfying derivation that's both general and rigorous.  Ongoing.

## Perturbative RG as a Projection

How does the one-loop beta function you learned in grad school fall out of this machinery?

Take Wetterich.  Make the **local potential approximation (LPA)**: assume the effective action has the form

$$
\Gamma_k[\phi] = \int d^d x \left[ \tfrac{1}{2} (\partial \phi)^2 + U_k(\phi) \right]
$$

i.e. only a potential, no field-dependent kinetic term, no higher-derivative terms.  Plug into Wetterich.  You get an ODE for $U_k(\phi)$ as a function of $k$ and $\phi$.  For a polynomial ansatz $U_k(\phi) = \sum_n g_n(k) \phi^{2n} / (2n)!$, you get ODEs for the couplings $g_n(k)$.

Truncate to $\phi^4$ only and Taylor-expand the Wetterich trace.  Reading off the leading term, you recover the one-loop beta function:

$$
\beta_{g_4} \sim \frac{3 g_4^2}{16 \pi^2} + \cdots
$$

(modulo scheme-dependent constants; the coefficient $3$ is correct, symmetry factor and all).  Higher orders in the derivative expansion give you **LPA'** (adds wavefunction renormalization) and so on.

The point: **every perturbative RG scheme you've seen is a projection of the exact flow onto a finite-dimensional subspace of couplings.**  Wilson-Fisher, epsilon expansion, minimal subtraction - all projections.  The exact flow knows more than any of them, and if you trust your truncation you can compute non-perturbative things (like the Wilson-Fisher fixed point in $d = 3$ directly, without expanding in $\epsilon$).

Modern FRG practice is exactly this: pick a clever ansatz for $\Gamma_k$, plug into Wetterich, solve the resulting ODEs numerically.  This gives quantitatively good critical exponents for the 3D Ising universality class without any perturbation theory.  Please clap.

## Fixed Points and Critical Exponents

A fixed point of the exact RG flow is a scale-invariant theory: $\partial_t \Gamma_t^\star = 0$ where $t = \log k$ in dimensionless variables.  The basic ones:

- **Gaussian fixed point**: free theory, $\Gamma^\star$ quadratic.  Trivially scale-invariant.
- **Wilson-Fisher fixed point**: interacting, exists for $d < 4$, describes critical Ising.  Nontrivial.

Linear stability analysis around a fixed point: write $\Gamma_t = \Gamma^\star + \delta \Gamma_t$, linearize the flow in $\delta \Gamma$, and diagonalize.  The eigenvalues are the **critical exponents**.  Relevant perturbations (positive eigenvalue, grow in the IR) are the ones you need to tune to reach the fixed point.  Irrelevant ones die off.

### A toy computation

At the Wilson-Fisher fixed point in $d = 4 - \epsilon$, the leading critical exponent $\nu$ satisfies

$$
\nu = \tfrac{1}{2} + \tfrac{1}{12} \epsilon + O(\epsilon^2)
$$

You can get this from perturbative RG at one loop, or from LPA Wetterich (gives a slightly different but nearby answer), or from full FRG with derivative expansion (gives the best answer).  All three are approximations to the same exact flow evaluated at the same fixed point.

The exact flow has a spectrum; the critical exponents are eigenvalues of the linearized flow operator.  You can think of renormalization as spectral theory for a particular operator on theory space.  (c.f. my older musing on [invariant subspaces](/2024/10/03/Musings-on-Running-Couplings-and-Invariant-Subspaces.html) - the "running couplings" approximation is asking when the flow admits a finite-dimensional invariant subspace around the fixed point, which happens when only finitely many couplings are relevant or marginal.)

## Scheme Dependence and Physical Content

Here's the part that's genuinely confusing even to experts, and I want to flag it clearly.

The effective action $S_\Lambda[\phi]$ (or $\Gamma_k[\phi]$) depends on the cutoff scheme $K$ (or $R_k$).  Different choices give different flows, different intermediate values of couplings, different trajectories in theory space.

**But physical observables do not depend on the scheme.**  1PI $n$-point functions at physical momenta (i.e. in the limit $k \to 0$ for Wetterich, or similar) are scheme-independent.  S-matrix elements, critical exponents at fixed points, free energies - all independent of $K$ up to the approximations you make.

Why is this confusing?  Because truncations break scheme independence.  If you truncate the flow to a finite set of couplings, the truncated flow's predictions *will* depend on $K$.  A popular way to check truncations is to vary $K$ and see how much your predictions change.  The variation bounds your truncation error.

(An aside: this is structurally identical to scheme-dependence in perturbative QCD - MS vs MS-bar vs momentum subtraction.  Physical observables don't care; intermediate quantities do.  The exact RG just makes the scheme choice more explicit as a choice of cutoff function.)

## ML Tie-In: NN Training as RG?

Brief pointer to active research.  The claim: training a neural network (gradient descent on weights) can be viewed as an RG flow on the distribution of weights, or equivalently on the induced distribution over functions.

Two regimes:

- **NTK / lazy / infinite-width**.  The network behaves like a linear model in some feature space.  Training is a linear flow in function space, which has very clean RG-like structure.  You can identify modes with eigenvalues of the NTK and ask which ones are relevant/irrelevant.
- **Feature learning / finite-width**.  The feature representations themselves evolve.  This is where the analogy to RG gets richer - features being "discovered" during training look a lot like effective degrees of freedom emerging as you integrate out scales.

Is this a rigorous equivalence?  No, not fully.  But the mathematical structures overlap substantially: diffusion equations for weight distributions in large-width limits, kernel structure at infinite width, hierarchical feature emergence.  Papers by Roberts-Yaida, Halverson, and others have tried to make the correspondence sharp.  Big if true - a unified framework for both could inform both sides.  (I am somewhat skeptical about how much physicists' RG intuition will port cleanly.  Time will tell.)

## Things To Read / What's Next

Once you have exact RG in hand, there's a ton of adjacent stuff:

- **Batalin-Vilkovisky (BV) formalism**.  Handles gauge theories and generalized symmetries.  Exact RG generalizes cleanly into BV - "flow equations" become flows on $L_\infty$-algebras, roughly.  Costello's book is the reference.
- **Algebraic / homotopical RG**.  Costello-Gwilliam treat renormalization as a problem in homotopical algebra.  Makes precise what the "space of theories" is and what "flow" means categorically.  Hard but clarifying.
- **Stochastic quantization**.  Parisi-Wu: quantize by running a Langevin process and taking the stationary distribution.  The Langevin process is basically RG in reverse (noise going from IR to UV).  Connects directly to diffusion models.
- **Lattice exact RG / block-spin**.  Luscher-Weiss, Kadanoff's original picture.  Discrete analog of what we've been doing.
- **RG monotones**.  Zamolodchikov's $c$-theorem in 2D, $a$-theorem in 4D, $F$-theorem in 3D.  Quantities that decrease monotonically along RG flow.  Strong constraints on possible flows.  Related to information-theoretic quantities along the flow.
- **Asymptotic safety for gravity**.  Weinberg's program: gravity as a nonperturbatively renormalizable QFT via a nontrivial UV fixed point in FRG.  Active research, partial evidence, some skepticism warranted.  Reuter-Saueressig's review is the entry point.
- **Critical phenomena & conformal bootstrap**.  Exact RG gives you fixed points; the bootstrap pins them down with unitarity + crossing.  Two complementary windows on the same scale-invariant theories.

***

## Summary

- Exact RG: a functional PDE for the effective action, derived from $\partial_\Lambda Z = 0$, with no perturbative approximation.
- Polchinski (tree-graph form) and Wetterich (one-loop form) are the two canonical versions, related by Legendre transform.
- The flow is structurally a Fokker-Planck equation on field space.  This bridges to diffusion models (score = gradient of effective action), to Otto-Wasserstein gradient flow, and to information geometry on theory space.
- Perturbative RG is a projection onto finite-dimensional coupling space.  LPA Wetterich reproduces one-loop beta functions as a first approximation.
- Fixed points are scale-invariant theories; critical exponents are eigenvalues of the linearized flow.
- Scheme dependence of the effective action is real; scheme dependence of physical observables isn't (modulo truncation).
- The whole apparatus generalizes into gauge theories (BV), gravity (asymptotic safety), and possibly into machine learning (NN training as RG).

If this seed works the way it's supposed to, you now have a mental home for a lot of disparate-looking objects: beta functions, diffusion models, Fokker-Planck, gradient flows on distribution space.  They're all the same flow, seen from different angles.

Written with Claude.
