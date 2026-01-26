---
title: "Lie Groups and Haar Measure"
date: 2026-01-21
tags: [seed, math, physics]
motivation: "Symmetries are groups. Continuous symmetries are Lie groups. But what's the 'right' way to integrate over a group? And why does that even make sense?"
background: "Basic group theory, comfort with linear algebra. Helpful to have seen rotation matrices or unitary transformations. The Haar measure question becomes natural once you want to 'average over all rotations' and realize you need a measure to do that."
llm: "Claude"
---

# Lie Groups and Haar Measure

## What's a Lie Group?

A **Lie group** is a group that's also a manifold, where the group operations (multiplication, inverse) are smooth.

**Translation:** A continuous family of symmetries that you can differentiate.

### Examples

- $\mathbb{R}$ under addition: translations on a line
- $SO(3)$: rotations in 3D
- $SU(2)$: unitary $2 \times 2$ matrices with determinant 1 (spin rotations)
- $GL(n)$: invertible $n \times n$ matrices
- $U(N)$: unitary $N \times N$ matrices

These aren't just abstract groups—they're smooth manifolds. $SO(3)$ is diffeomorphic to $\mathbb{RP}^3$. $SU(2)$ is diffeomorphic to $S^3$ (the 3-sphere). You can do calculus on them.

## The Lie Algebra

Near the identity element $e$ of a Lie group $G$, infinitesimal group elements look like:

$$
g \approx e + \epsilon X
$$

where $X$ is in the **Lie algebra** $\mathfrak{g} = T_e G$.

The Lie algebra is a vector space with an extra operation: the **Lie bracket** $[X, Y]$.

For matrix groups: $[X, Y] = XY - YX$ (the commutator).

**Punchline:** The Lie algebra is the "linearization" of the Lie group near the identity. You can often work with the algebra (linear!) instead of the group (nonlinear).

### Exponential Map

You go from algebra to group via the **exponential map**:

$$
\exp(tX) = \text{the group element you get by flowing in direction } X \text{ for time } t
$$

For matrices: this is literally $\exp(tX) = \sum_{n=0}^\infty \frac{(tX)^n}{n!}$.

**Example:** For $SO(3)$, the Lie algebra is antisymmetric $3 \times 3$ matrices. $\exp(t J_z)$ where $J_z$ is the generator of rotation about $z$, gives you rotation by angle $t$ about the $z$-axis.

### Why Physicists Care

Noether's theorem: continuous symmetries $\leftrightarrow$ conservation laws.

The symmetries form a Lie group. The conserved quantities are related to the Lie algebra generators.

Angular momentum operators $J_x, J_y, J_z$? They're the Lie algebra of $SO(3)$, with $[J_i, J_j] = i\epsilon_{ijk} J_k$.

---

## Haar Measure: The "Right" Way to Integrate Over a Group

Here's the fundamental question: if I want to "average over all rotations" or "integrate over all unitaries," how do I do it?

I need a measure on the group. But not just any measure—I want one that respects the group structure.

### Left-Invariance

A measure $\mu$ on $G$ is **left-invariant** if:

$$
\mu(gS) = \mu(S)
$$

for all $g \in G$ and measurable sets $S$.

Here $gS = \{gh : h \in S\}$ is the set $S$ "translated" by $g$.

In words: the measure of a set doesn't change if you multiply every element by a fixed group element.

**Example:** On $(\mathbb{R}, +)$, Lebesgue measure is left-invariant: $\mu([a,b]) = \mu([a+c, b+c])$ for any $c$.

**Example:** On $(\mathbb{R}_{>0}, \times)$, the measure $d\mu = dx/x$ is left-invariant: if you scale by $c$, then $\mu([a,b]) = \int_a^b dx/x = \ln(b/a)$ and $\mu([ca, cb]) = \int_{ca}^{cb} dx/x = \ln(cb/ca) = \ln(b/a)$.

### The Haar Theorem

**Theorem (Haar):** On any locally compact topological group $G$, there exists a nonzero left-invariant measure, and it is **unique up to overall scale**.

This is remarkable. The group structure essentially *determines* the measure. You don't choose it—it's forced on you by the symmetry.

For compact groups (like $SO(3)$, $SU(N)$), you can normalize to have total measure 1:

$$
\int_G d\mu(g) = 1
$$

This is the **normalized Haar measure**.

### Right-Invariance and Unimodularity

Similarly, you can define **right-invariant** measures: $\mu(Sg) = \mu(S)$.

Left and right Haar measures don't always coincide. But on:
- Compact groups
- Abelian groups
- Semisimple Lie groups

they do. Such groups are called **unimodular**.

For non-unimodular groups (like the affine group $ax + b$), left and right Haar measures differ by a factor called the **modular function**.

### Computing Haar Measure

For matrix Lie groups, there are standard formulas.

**On $U(N)$:** The Haar measure can be written in terms of eigenvalues $\{e^{i\theta_j}\}$:

$$
d\mu(U) \propto \prod_{j < k} |e^{i\theta_j} - e^{i\theta_k}|^2 \cdot \prod_j d\theta_j
$$

That Vandermonde factor $\prod_{j<k}|e^{i\theta_j} - e^{i\theta_k}|^2$ is eigenvalue repulsion—the same factor that appears in random matrix theory!

**On $SO(3)$:** Using axis-angle parametrization, the Haar measure is:

$$
d\mu \propto \sin^2(\theta/2) \, d\theta \, d\hat{n}
$$

where $\theta$ is the rotation angle and $\hat{n}$ is the axis (a point on $S^2$).

### Why Haar Measure Matters

1. **Averaging over symmetries**: If you want to compute "the average of $f$ over all rotations," you need Haar measure:
   $$\langle f \rangle = \int_{SO(3)} f(R) \, d\mu(R)$$

2. **Random matrix theory**: A "uniformly random" unitary or orthogonal matrix means Haar-distributed. This is the starting point for random matrix theory.

3. **Representation theory**: Peter-Weyl theorem says $L^2(G)$ (with Haar measure) decomposes into irreducible representations. Orthogonality of characters uses Haar measure.

4. **Physics**: Gauge theory uses Haar measure for path integrals over gauge configurations. Lattice QCD integrates over $SU(3)$ at each link.

---

## The Weyl Integration Formula

For compact Lie groups, there's a beautiful formula that reduces integration over the whole group to integration over a maximal torus.

Let $G$ be a compact connected Lie group with maximal torus $T$ (e.g., diagonal unitaries in $U(N)$). Let $W$ be the Weyl group (permutations of eigenvalues, for $U(N)$).

**Weyl Integration Formula:**

$$
\int_G f(g) \, d\mu(g) = \frac{1}{|W|} \int_T f(t) \, |\Delta(t)|^2 \, d\mu_T(t)
$$

where $\Delta(t)$ is the Weyl denominator—a product over positive roots that encodes the Jacobian from $G$ to $T$.

For $U(N)$, this is:

$$
\int_{U(N)} f(U) \, dU = \frac{1}{N!} \int_{[0,2\pi]^N} f(\text{diag}(e^{i\theta_1}, \ldots, e^{i\theta_N})) \prod_{j<k} |e^{i\theta_j} - e^{i\theta_k}|^2 \frac{d\theta_1 \cdots d\theta_N}{(2\pi)^N}
$$

The Vandermonde determinant is doing all the work.

---

## Invariant Vector Fields and the Maurer-Cartan Form

On a Lie group, there's a canonical way to define vector fields: **left-invariant vector fields**.

Given $X \in \mathfrak{g}$ (a tangent vector at the identity), define a vector field $\tilde{X}$ on all of $G$ by:

$$
\tilde{X}_g = (L_g)_* X
$$

where $L_g: h \mapsto gh$ is left multiplication and $(L_g)_*$ is its pushforward.

This is left-invariant: $\tilde{X}_{gh} = (L_g)_* \tilde{X}_h$.

**Maurer-Cartan form:** The dual notion. A left-invariant 1-form $\omega$ on $G$ with values in $\mathfrak{g}$:

$$
\omega_g(v) = (L_{g^{-1}})_* v
$$

It satisfies the **Maurer-Cartan equation**:

$$
d\omega + \frac{1}{2}[\omega, \omega] = 0
$$

This is the infinitesimal version of the group axioms, and it's fundamental for gauge theory.

---

## Connection to Random Matrix Theory

When we say "random unitary matrix," we mean Haar-distributed. This is the unique measure that treats all unitaries "the same."

The eigenvalue repulsion factor $\prod_{j<k}|e^{i\theta_j} - e^{i\theta_k}|^2$ in the Haar measure is exactly why random matrices exhibit level repulsion. It's not put in by hand—it comes from the geometry of the group.

The Weyl integration formula says: **integrating over the group = integrating over eigenvalues with a Jacobian**. That Jacobian is the source of all the interesting random matrix statistics.

---

## Summary

| Concept | What It Is |
|---------|------------|
| Lie group | Smooth group (symmetries you can differentiate) |
| Lie algebra | Tangent space at identity; infinitesimal symmetries |
| Exponential map | Goes from algebra to group |
| Haar measure | Unique (up to scale) invariant measure on a group |
| Unimodular | Left = right Haar (true for compact, abelian, semisimple) |
| Weyl formula | Reduces group integration to torus + Jacobian |

**The philosophy:** Group structure determines the measure. When you average over symmetries, there's essentially one right way to do it.

---

*See also: [Manifolds for the Anti-Mathematician], [Random Matrix Theory Tour].*
