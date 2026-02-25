---
title: "Morse Theory"
date: 2026-02-25
motivation: "A smooth function's critical points encode the topology of the underlying manifold.  Morse theory makes this precise: count critical points, track gradient flow, build a chain complex."
background: "Multivariable calculus, basic linear algebra, comfort with manifolds at the level of 'Manifolds for the Anti-Mathematician'.  No algebraic topology prerequisites - we build what we need."
llm: "Claude"
tags: [seed]
math: true
---

# Morse Theory

## The Central Claim

Take a smooth function on a compact manifold.  Look at its critical points - the places where the derivative vanishes.  Classify them by how many "downhill directions" they have (the **index**).

Claim: this is enough to recover the topology.

That's surprising.  A single generic function, defined purely locally (value at each point), somehow encodes global information - the number of holes, the connectivity, the Euler characteristic.  Morse theory is the machine that makes this precise.

The running example throughout: the height function on a torus.

## Morse Functions and Critical Points

Let $M$ be a compact smooth manifold and $f: M \to \mathbb{R}$ a smooth function.  A point $p \in M$ is **critical** if $df_p = 0$ - the differential vanishes.  In coordinates, all partial derivatives $\partial f / \partial x^i$ are zero at $p$.

At a critical point, the **Hessian** is well-defined as a symmetric bilinear form on $T_p M$:

$$
H_p(u, v) = \frac{\partial^2 f}{\partial x^i \partial x^j}\, u^i v^j
$$

(At non-critical points, the Hessian depends on the coordinate choice.  At critical points, it doesn't.  Good exercise to check.)

The critical point is **non-degenerate** if $\det H_p \neq 0$, and the **index** $\lambda(p)$ is the number of negative eigenvalues of $H_p$.  Index 0 means "all directions go up" (a minimum).  Index $n = \dim M$ means "all directions go down" (a maximum).  Anything in between is a saddle.

A function $f$ is **Morse** if all its critical points are non-degenerate.  This is a generic condition - Morse functions form an open dense set in $C^\infty(M)$.  Almost every smooth function is Morse.

### The Torus

Stand a torus upright on a table and let $f$ be the height function.  There are exactly four critical points:

| Point | Type | Index | Height |
|-------|------|-------|--------|
| $p$ | Minimum (bottom) | 0 | Lowest |
| $q$ | Saddle (inner) | 1 | Lower-middle |
| $r$ | Saddle (outer) | 1 | Upper-middle |
| $s$ | Maximum (top) | 2 | Highest |

So $c_0 = 1$ minimum, $c_1 = 2$ saddles, $c_2 = 1$ maximum.  The index counts downhill directions: a minimum has none (index 0), a saddle on a surface has one (index 1), a maximum has two (index 2).

If you want an explicit formula: on the flat torus $T^2 = (\mathbb{R}/2\pi\mathbb{Z})^2$, use $f(\theta, \phi) = -\cos\theta - 2\cos\phi$.  The factor of 2 makes all four critical values distinct.  Critical points at $(\theta, \phi) \in \{0, \pi\}^2$, with indices matching the table above.

## The Morse Lemma

Near a non-degenerate critical point, things are simpler than you'd expect.

**Morse Lemma.**  If $p$ is a non-degenerate critical point of index $\lambda$, there exist local coordinates $(y^1, \ldots, y^n)$ centered at $p$ such that:

$$
f(y) = f(p) - (y^1)^2 - \cdots - (y^\lambda)^2 + (y^{\lambda+1})^2 + \cdots + (y^n)^2
$$

Locally, every Morse function looks quadratic.  No cubic terms, no higher-order corrections.  The Hessian *is* the full local picture, up to coordinate change.  Call it "diagonalization for critical points."

The Morse Lemma is why non-degeneracy is the right condition.  A degenerate critical point (like $f(x) = x^3$ at the origin) can't be put in this normal form, and its topology-changing behavior is messier.

This will come back: the Witten Laplacian localizes at critical points, and the Morse Lemma tells us the local model is a harmonic oscillator (see [The Witten Deformation]).

## Gradient Flow

Pick a Riemannian metric $g$ on $M$.  The **negative gradient flow** is the ODE:

$$
\dot{x} = -\nabla f(x)
$$

This is "roll downhill" dynamics.  Every trajectory flows from a critical point of higher $f$-value toward one of lower $f$-value (on a compact manifold, trajectories can't escape to infinity).

For each critical point $p$, define:
- **Stable manifold**: $W^s(p) = \lbrace x \in M : \phi_t(x) \to p \text{ as } t \to +\infty \rbrace$ (points that flow *to* $p$)
- **Unstable manifold**: $W^u(p) = \lbrace x \in M : \phi_t(x) \to p \text{ as } t \to -\infty \rbrace$ (points that flow *from* $p$)

By the Morse Lemma, near $p$ the unstable manifold is tangent to the negative eigenspace of the Hessian:

$$
\dim W^u(p) = \operatorname{index}(p)
$$

The unstable manifold of a saddle of index 1 is a curve.  The unstable manifold of a maximum (index $n$) is $n$-dimensional.  Minima (index 0) have zero-dimensional unstable manifolds - they're attractors.

**Connection to instantons.**  A gradient flow line from critical point $q$ (above) down to $p$ (below) follows the steepest descent.  Now reverse time: the path from $p$ *up* to $q$ follows $\dot{x} = +\nabla f$.  In the Langevin dynamics with noise, this uphill path is the instanton - the most probable transition path between metastable states (see [Instantons in Statistical Physics]).  Same curves, opposite direction.  The instanton climbs; the gradient flow descends.

## The Morse Complex

Here's the payoff.

Define a chain complex.  The chain groups are free abelian groups generated by critical points of each index:

$$
C_k = \bigoplus_{\operatorname{index}(p)=k} \mathbb{Z}\langle p \rangle
$$

So $C_k$ has one copy of $\mathbb{Z}$ for each index-$k$ critical point.  For the torus: $C_0 = \mathbb{Z}\langle p\rangle$, $C_1 = \mathbb{Z}\langle q, r\rangle$, $C_2 = \mathbb{Z}\langle s\rangle$.

The boundary operator $\partial_k: C_k \to C_{k-1}$ counts gradient flow lines:

$$
\partial_k(q) = \sum_{\operatorname{index}(p)=k-1} n(q, p)\, p
$$

where $n(q, p)$ is the *signed* count of gradient flow lines from $q$ down to $p$.  (The sign comes from comparing orientations of unstable manifolds.)

**The key property:** $\partial^2 = 0$.

Why?  Consider the space of gradient flow lines from $q$ (index $k$) down to $p$ (index $k-2$), passing through no intermediate critical point.  This is a 1-dimensional manifold.  A 1-manifold's boundary consists of pairs of endpoints that cancel: each boundary point corresponds to a **broken flow line** - a flow from $q$ to some intermediate $r$ (index $k-1$), then from $r$ to $p$.  These are exactly the terms in $\partial^2$, and they cancel because the boundary of a compact 1-manifold has signed count zero.

A topological argument, not an algebraic accident.

**Morse Homology Theorem.**  The homology of the Morse complex equals the singular homology of $M$:

$$
H_k(C_*, \partial) \cong H_k(M; \mathbb{Z})
$$

### Torus Computation

For the height function on the torus, the gradient flow from each saddle leads down to the unique minimum via two flow lines that go "around" in opposite directions.  The signed counts cancel: $\partial_1 q = 0$, $\partial_1 r = 0$.  Similarly, $\partial_2 s = 0$.

The homology is just the chain groups themselves:

$$
H_0 = \mathbb{Z}, \quad H_1 = \mathbb{Z}^2, \quad H_2 = \mathbb{Z}
$$

One connected component ($b_0 = 1$), two independent loops ($b_1 = 2$), one 2-cycle ($b_2 = 1$).  This matches $H_*(T^2)$.  The Morse function recovered the topology.

When all boundary maps vanish, the Morse function is called **perfect**: $c_k = b_k$ for every $k$.  Not every Morse function is perfect, but the torus height function is.

## Morse Inequalities

Even when the Morse function isn't perfect, the critical point counts constrain the topology.

**Weak Morse inequalities.**  For each $k$:

$$
c_k \geq b_k
$$

where $c_k$ is the number of index-$k$ critical points and $b_k = \dim H_k(M; \mathbb{R})$ is the $k$-th Betti number.  This is immediate from the chain complex: $b_k = \dim(\ker\partial_k / \operatorname{im}\partial_{k+1}) \leq \dim C_k = c_k$.

You can't have fewer critical points than Betti numbers.  Critical points can be "redundant" (they contribute to $\ker\partial$ but also to $\operatorname{im}\partial$), but you can't have too few.

**Strong Morse inequalities.**  For each $m$:

$$
\sum_{k=0}^{m} (-1)^{m-k} c_k \geq \sum_{k=0}^{m} (-1)^{m-k} b_k
$$

Setting $m = \dim M$ gives equality:

$$
\boxed{\sum_{k} (-1)^k c_k = \sum_{k} (-1)^k b_k = \chi(M)}
$$

The alternating sum of critical point counts equals the Euler characteristic.  Always.  For the torus: $1 - 2 + 1 = 0 = \chi(T^2)$.

## Handle Decomposition

There's a geometric way to see why critical points control topology.

Consider the **sublevel set** $M^a = \lbrace x \in M : f(x) \leq a \rbrace$.  As $a$ increases from $-\infty$ to $+\infty$, $M^a$ grows from empty to all of $M$.

If the interval $[a, b]$ contains no critical values, then $M^b \cong M^a$ (diffeomorphic).  The gradient flow provides the diffeomorphism - just "push" the boundary uphill.

When $a$ crosses a critical value with an index-$k$ critical point, you attach a **$k$-handle**: a thickened $k$-disk $D^k \times D^{n-k}$.

For the torus:
1. Below $p$: empty set
2. Past $p$ (index 0): a disk appears (0-handle = new connected component)
3. Past $q$ (index 1): attach a 1-handle (a bridge).  The disk becomes a cylinder.
4. Past $r$ (index 1): attach another 1-handle.  Now a punctured torus.
5. Past $s$ (index 2): cap off the remaining hole (2-handle = glue a disk over the boundary).  Full torus.

Each critical point contributes one handle, and the handle type is determined by the index.  The manifold is assembled from these handles, giving it the structure of a CW complex.  This is why the Morse complex computes cellular homology.

## The Morse-Smale Condition

One condition we've been sweeping under the rug: for gradient flow line counts to be well-defined and finite, we need transversality.

The **Morse-Smale condition** requires that for every pair of critical points $p, q$, the unstable manifold $W^u(p)$ and stable manifold $W^s(q)$ intersect transversally.  When this holds, the space of flow lines from $p$ to $q$ is a smooth manifold of dimension $\operatorname{index}(p) - \operatorname{index}(q) - 1$.  When the index difference is 1, flow lines are isolated and countable.

Good news: for a generic metric, the Morse-Smale condition holds.  You can always perturb slightly to make everything transverse.  The resulting homology doesn't depend on the generic metric chosen.

## Summary

| Concept | What it is |
|---------|------------|
| Morse function | Smooth function, all critical points non-degenerate |
| Index | Number of negative Hessian eigenvalues |
| Morse Lemma | Local quadratic normal form at critical points |
| Gradient flow | $\dot{x} = -\nabla f$, connects critical points high-to-low |
| Morse complex | Chains on critical points, $\partial$ counts flow lines |
| Morse inequalities | $c_k \geq b_k$, alternating sum gives $\chi(M)$ |
| Handle decomposition | Build $M$ by attaching one handle per critical point |

A Morse function gives you a combinatorial/dynamical skeleton of the manifold.  Critical points are the vertices, gradient flow lines are the edges, and the chain complex they form computes the homology.

Next: the Witten deformation gives an analytical proof of the Morse Homology Theorem - and connects all of this to Fokker-Planck dynamics and supersymmetry.  See [The Witten Deformation].

---

*See also: [Manifolds for the Anti-Mathematician], [Instantons in Statistical Physics], [The Witten Deformation].*

Written with Claude.
