---
title: "Picard-Lefschetz Theory, or: Integration Contours as Linear Algebra"
date: 2026-02-25
motivation: "You know saddle-point approximation works, but which saddle points contribute? Why do the answers jump when you vary parameters? And where does the imaginary part of a metastable partition function come from? The answer is that integration contours form a vector space, and everything else is linear algebra."
background: "Basic complex analysis (Cauchy's theorem, residues, contour deformation). Helpful to have seen steepest descent used informally."
llm: "Claude"
tags: [seed]
math: true
---

# Picard-Lefschetz Theory, or: Integration Contours as Linear Algebra

## The Problem with Saddle Points

Consider the standard asymptotic integral:

$$
I(\lambda) = \int_C e^{-\lambda f(z)} g(z)\, dz
$$

for large $\lambda$, where $f$ and $g$ are holomorphic and $C$ is some contour in the complex plane.  The steepest descent method says: deform $C$ to pass through saddle points of $f$ (where $f'(z_i) = 0$), then each saddle contributes a Gaussian-looking piece to the asymptotic expansion.

This works amazingly well in practice.  But it leaves three questions unanswered:

1. **Which saddle points contribute?**  There might be many saddles of $f$.  The original contour $C$ only "sees" some of them.  Which ones?

2. **What happens at Stokes lines?**  As you vary parameters (say, $\arg(\lambda)$), the set of contributing saddle points can change discontinuously.  The asymptotic expansion *jumps*.  Why?

3. **Where does the imaginary part come from?**  In metastable problems, the partition function $Z = \int e^{-N V(x)} dx$ is a real integral over the real line, so $Z$ is manifestly real.  Yet the decay rate of the metastable state comes from $\text{Im}(Z)$.  How can a real integral have an imaginary part?

Picard-Lefschetz theory answers all three, and the answer is linear algebra on a vector space of integration contours.

## Cauchy's Theorem: The Prototype

Before building the full machine, let's see the idea in a context you already know.

The residue theorem says: for $\oint_C f(z)\, dz$, the answer depends only on which poles are inside $C$, counted with winding numbers.  Small loops $\gamma_i$ around individual poles form a basis, and any closed contour decomposes as

$$
C = \sum_i n_i \gamma_i
$$

where $n_i$ is the winding number of $C$ around pole $i$.  The integral splits accordingly:

$$
\oint_C f(z)\, dz = \sum_i n_i \oint_{\gamma_i} f(z)\, dz = 2\pi i \sum_i n_i \,\text{Res}(f, z_i)
$$

The key structure: contours modulo deformation form a **vector space** (with integer coefficients).  Small loops are a basis.  Winding numbers are coordinates.  The integral is a linear functional on this space.

You can deform $C$ freely as long as you don't cross a pole and you stay in regions where the integrand behaves well at infinity.  Two contours that are deformable into each other give the same integral.  The *topology* of the contour - which poles it encircles - determines the answer.

This is homology, even if nobody called it that the first time you saw it.  The space of "contours modulo allowed deformations" is a vector space, and the elementary loops form a basis.

Picard-Lefschetz theory is exactly this story, upgraded from residue integrals to saddle-point integrals.

## Steepest Descent, Done Right

Write $f = u + iv$ with $u = \text{Re}(f)$ and $v = \text{Im}(f)$.  Since $f$ is holomorphic, $u$ and $v$ are harmonic conjugates.  On any path where $v = \text{const}$, the function $u$ changes monotonically - the integrand $e^{-\lambda u}$ is purely real and exponentially peaked.  No oscillation.

The **steepest descent** paths through a saddle point $z_i$ are exactly the paths of constant $\text{Im}(f)$ emanating from $z_i$ along which $\text{Re}(f)$ increases away from the saddle.  These are the paths of maximum decay for $e^{-\lambda f}$.

From each saddle $z_i$, two distinguished contours emerge:

**The thimble** $\mathcal{J}_i$: the steepest descent contour.  On $\mathcal{J}_i$, $\text{Im}(f) = \text{Im}(f(z_i))$ and $\text{Re}(f) \geq \text{Re}(f(z_i))$, with equality only at the saddle.  The integrand decays in both directions away from $z_i$.  No oscillation, clean Gaussian peak, well-defined integral for large $\lambda$.

**The anti-thimble** $\mathcal{K}_i$: the steepest ascent contour.  Same constant-phase condition, but $\text{Re}(f) \leq \text{Re}(f(z_i))$.  The integrand *grows* away from the saddle.  You would never want to integrate along this contour.  But it plays a crucial role as the "dual basis" - more on this in a moment.

Together, the thimbles and anti-thimbles form a skeleton that organizes the entire complex plane.

### Worked Example: The Cubic

Take $f(z) = z^3/3 - z$.  The saddle points are at $z = \pm 1$, with $f(\pm 1) = \mp 2/3$.

Near $z = +1$, we have $f(z) \approx -2/3 + (z-1)^2 + \cdots$, so the steepest descent direction is along the real axis.  The thimble $\mathcal{J}_+$ starts along the real line near the saddle, then curves off into the complex plane toward the sectors at infinity where $\text{Re}(z^3/3) \to +\infty$.  Near $z = -1$, the same story plays out for $\mathcal{J}_-$.  The anti-thimbles $\mathcal{K}_\pm$ run transversely through each saddle, orthogonal (in the appropriate sense) to the thimbles.

Now consider the integral $\int_{-\infty}^{\infty} e^{-\lambda(z^3/3 - z)} dz$ for real positive $\lambda$.  The real line runs through both saddle points, but which thimbles appear in the decomposition?  You compute the intersection numbers: does the real line cross $\mathcal{K}_+$?  Does it cross $\mathcal{K}_-$?  The answers determine the decomposition, and they depend on $\arg(\lambda)$.

Rotate $\lambda$ in the complex plane and the thimbles deform smoothly.  At a critical angle, the thimble from one saddle runs into the other saddle.  That's a Stokes line.  On one side, both saddles contribute; on the other, only one does.  The integral is the same - the contour hasn't moved - but the asymptotic expansion changes because the basis reshuffled.

## The Vector Space of Cycles

Here's the punchline.

Any valid integration contour $C$ - one that starts and ends in regions where $e^{-\lambda f} \to 0$ - decomposes into thimbles:

$$
C = \sum_i n_i \mathcal{J}_i
$$

The coefficients $n_i$ are **intersection numbers**:

$$
n_i = \langle C, \mathcal{K}_i \rangle \in \mathbb{Z}
$$

This is a signed count of how many times $C$ crosses the anti-thimble $\mathcal{K}_i$.  It's the direct analog of the winding number in the Cauchy case.

The integral decomposes accordingly:

$$
\int_C e^{-\lambda f} g\, dz = \sum_i n_i \int_{\mathcal{J}_i} e^{-\lambda f} g\, dz
$$

Each thimble integral is clean: $\text{Im}(f) = \text{const}$ on $\mathcal{J}_i$, so there's no oscillation.  Each is exponentially dominated by its saddle point, with a straightforward Gaussian expansion for large $\lambda$.  All the hard work is in finding the $n_i$, and that's topology.

This is the **Picard-Lefschetz decomposition**.  The space of valid contours is a vector space.  Thimbles are a basis.  Intersection numbers are coordinates.  The integral is a linear functional.

Here's the dictionary:

| Cauchy (residues) | Picard-Lefschetz (saddles) |
|---|---|
| Poles $z_i$ | Saddle points $z_i$ |
| Small loops $\gamma_i$ | Thimbles $\mathcal{J}_i$ |
| Winding numbers $n_i$ | Intersection numbers $\langle C, \mathcal{K}_i \rangle$ |
| $\oint_C = \sum n_i \oint_{\gamma_i}$ | $\int_C = \sum n_i \int_{\mathcal{J}_i}$ |

The first column is something you've used since undergrad.  The second column is the same structure, one level up.

## Relative Homology: Why "Allowed Wedges"

There's a subtlety the Cauchy analogy glosses over.  For the residue theorem, the contours are closed loops, and they live in the homology $H_1(\mathbb{C} \setminus \{z_i\})$.

For saddle-point integrals, the contour is *not* closed.  It runs from infinity to infinity, and must start and end in regions where $e^{-\lambda f} \to 0$ - i.e., where $\text{Re}(f) \to +\infty$.  These regions are the **allowed wedges** at infinity: sectors in the complex plane determined by the asymptotics of $f$.

The contours live in **relative homology**: $H_1(\mathbb{C}, \mathcal{R})$, where $\mathcal{R}$ is the union of allowed wedges.  "Relative" means we're free to move the endpoints around within $\mathcal{R}$.  As long as the contour starts and ends somewhere in a decay region, we can deform it, and two contours connected by such a deformation give the same integral.

For the cubic $f(z) = z^3/3 - z$, there are three allowed wedges at infinity (the three directions where $\text{Re}(z^3) \to +\infty$), and the relative homology group is two-dimensional - matching the two saddle points.  In general, for a polynomial of degree $d$ with $d-1$ nondegenerate saddle points, the relative homology is $(d-1)$-dimensional.  One basis thimble per saddle, exactly as you'd want.

This is why the Cauchy analogy works at a structural level.  In both cases, you have a vector space of integration cycles, a basis indexed by critical points (poles or saddles), and coordinates given by a topological pairing (winding or intersection).  The "relative" part is just saying: the contour's endpoints live in the decay region, which is the saddle-point analog of closing a contour at infinity.

## Stokes Phenomenon = Change of Basis

As parameters vary - say you rotate $\arg(\lambda)$ - the thimbles $\mathcal{J}_i$ deform continuously.  The original contour $C$ doesn't change (it's a topological object, defined by its intersection numbers with the anti-thimbles).

Usually this is uneventful.  But at special parameter values, a thimble from saddle $i$ hits saddle $j$.  When this happens, the thimble "picks up" the other thimble:

$$
\mathcal{J}_i \to \mathcal{J}_i + n_{ij} \mathcal{J}_j
$$

where $n_{ij} = \pm\langle \mathcal{J}_i, \mathcal{K}_j \rangle$ is the intersection number at the critical moment.

The contour $C$ hasn't moved.  But the basis changed, so the decomposition $C = \sum n_i \mathcal{J}_i$ picks up different coefficients.  Before the Stokes line, maybe saddle $j$ doesn't contribute.  After crossing it, saddle $j$ enters the decomposition (or drops out).

This is the **Stokes phenomenon**: a change of basis in the space of integration cycles.  The integral hasn't changed - same contour, same integrand.  But the saddle-point *expansion* changes because the thimble decomposition has reshuffled.

If you've read [Asymptotics, Borel, and Stokes], this is the same phenomenon described there in the language of Borel summation and lateral resummation.  The exponentially small terms that appear and disappear across Stokes lines correspond exactly to saddle points entering and leaving the thimble decomposition.  The Picard-Lefschetz framework makes the mechanism geometric: nothing mysterious happens to the series.  The basis of integration cycles rotates, and the coordinates of the contour in the new basis are different from the old ones.

The Picard-Lefschetz formula $n_{ij} = \pm\langle \mathcal{J}_i, \mathcal{K}_j \rangle$ tells you exactly *how* the expansion jumps.  The intersection number at the Stokes line controls the size of the jump.  This is a computable integer, not a free parameter.  The seemingly mysterious discontinuities in asymptotic expansions are completely determined by the topology of how thimbles and anti-thimbles intersect.

## The Imaginary Part: Payoff

Now for the question that started this whole discussion.

Consider a metastable system with partition function:

$$
Z = \int_{-\infty}^{\infty} e^{-N V(x)}\, dx
$$

where $V(x)$ has a local minimum at $x_0$ (the metastable "false vacuum") and a global minimum somewhere else, separated by a barrier with saddle point at $x_s$.

This is a real integral over the real line.  It's manifestly real and positive.  So how can the decay rate of the metastable state involve $\text{Im}(Z)$?

Analytically continue $V$ into the complex plane and decompose the real-line contour into thimbles.  The perturbative saddle at $x_0$ (the local minimum, $V''(x_0) > 0$) has a thimble $\mathcal{J}_0$ that stays on the real axis.  Its contribution to $Z$ is real and positive.  This is the naive partition function of the metastable phase.

The barrier saddle at $x_s$ has a **negative mode**: $V''(x_s) < 0$.  The steepest descent direction from $x_s$ for the function $N V(z)$ is in the *imaginary* direction (because the negative second derivative means the real axis is the steepest *ascent*).  So the thimble $\mathcal{J}_s$ goes off into the complex plane.  On this thimble, $\text{Im}(V) \neq 0$, and the contribution to $Z$ is complex.

The real-line contour decomposes as:

$$
\mathbb{R} = \mathcal{J}_0 + n_s \mathcal{J}_s + \cdots
$$

The intersection number $n_s$ is nonzero when the real line crosses the barrier's anti-thimble - which it does, because the real line has to pass through the barrier region.  The barrier's complex contribution gives:

$$
\text{Im}(Z) \propto e^{-N(V(x_s) - V(x_0))}
$$

This is the Langer/Callan-Coleman result, and now we understand where the imaginary part comes from.  It's not from any hand-wavy "analytic continuation to imaginary time."  It's from the topology of the thimble decomposition: the barrier saddle's thimble goes into the complex plane because the negative mode makes the steepest descent direction imaginary, and the real contour has nonzero intersection number with the barrier's anti-thimble, so the barrier saddle contributes.  Its contribution is complex.

(See [Instantons in Statistical Physics] for the instanton perspective on the same physics.  The instanton there is this barrier saddle; Picard-Lefschetz tells you *why* it contributes and *why* its contribution is complex.)

## The Bigger Picture

The Picard-Lefschetz framework has deep generalizations that each deserve their own treatment.

**Monodromy.**  Loop around a singularity in parameter space - take $\lambda$ around a path where two saddle values coincide - and the saddle points permute.  This induces a linear transformation on the space of thimbles.  The collection of all such transformations is the **monodromy group**, and it encodes the global topology of the parameter space.

**Gauss-Manin connection.**  The thimble basis "parallel transports" as parameters vary.  This transport defines a flat connection on the vector bundle of cycle spaces over parameter space.  Its singularities are the Stokes lines.  If you want to track how saddle-point expansions change with parameters - not just the jumps, but the smooth evolution between jumps - this is the right language.

**Period integrals and Picard-Fuchs equations.**  The thimble integrals $\int_{\mathcal{J}_i} e^{-\lambda f} g\, dz$ are "periods" - integrals of a fixed form over varying cycles.  They satisfy a system of linear ODEs in the parameters (the Picard-Fuchs equations).  This connects the asymptotic analysis to algebraic geometry and the theory of D-modules.

Each of these is its own rabbit hole.  The point for now is that the vector-space-of-cycles perspective isn't just a nice repackaging of steepest descent.  It's the entry point to a genuinely richer structure where ideas from algebraic geometry, differential equations, and representation theory all converge on the same object: the bundle of integration cycles over parameter space.

## Summary

- Integration contours modulo deformation form a **vector space** with integer coefficients
- **Thimbles** $\mathcal{J}_i$ (steepest descent contours through saddle points) are a basis
- **Intersection numbers** $n_i = \langle C, \mathcal{K}_i \rangle$ with anti-thimbles are the coordinates, telling you **which saddle points contribute**
- The **Stokes phenomenon** is a change of basis: thimbles reshuffle at Stokes lines, changing which saddles appear in the decomposition
- The **imaginary part** of a metastable partition function comes from the barrier saddle's thimble going into the complex plane (negative mode makes the steepest descent direction imaginary)
- Everything is a direct generalization of the residue theorem: poles → saddles, loops → thimbles, winding numbers → intersection numbers

---

*See also: [Asymptotics, Borel, and Stokes], [Instantons in Statistical Physics], [WKB and Matched Asymptotics].*

*Written with Claude.*
