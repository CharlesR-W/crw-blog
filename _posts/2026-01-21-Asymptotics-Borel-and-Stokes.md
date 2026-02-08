---
title: "Asymptotics, Borel Transforms, and Stokes Phenomena"
date: 2026-01-21
motivation: "Asymptotic series are everywhere in physics—perturbation theory, WKB, semiclassical expansions. But they diverge! What does it mean to 'sum' a divergent series, and why do the answers sometimes jump discontinuously?"
background: "Basic complex analysis, comfort with power series. The Stokes phenomenon becomes natural once you see that divergent series encode information about exponentially small terms hiding 'beyond all orders'."
llm: "Claude"
tags: [seed]
math: true
---

# Asymptotics, Borel Transforms, and Stokes Phenomena

## The Problem with Perturbation Theory

Here's a dirty secret of theoretical physics: most of our perturbative expansions are **divergent**.

The QED perturbation series in $\alpha$? Diverges. The WKB expansion in $\hbar$? Diverges. The $1/N$ expansion in large-$N$ gauge theory? Diverges.

And yet these expansions *work*—they give fantastically accurate predictions when truncated at the right order. What's going on?

The answer involves some of the deepest ideas in asymptotic analysis: **Borel summation**, **resurgence**, and the **Stokes phenomenon**. These aren't just mathematical curiosities—they're telling us about non-perturbative physics hiding "beyond all orders" in perturbation theory.

## Asymptotic vs. Convergent Series

A series $\sum_{n=0}^\infty a_n x^n$ is **convergent** if the partial sums approach a limit.

A series is **asymptotic** to a function $f(x)$ as $x \to 0$ if:

$$
f(x) - \sum_{n=0}^{N} a_n x^n = O(x^{N+1}) \quad \text{as } x \to 0
$$

for every $N$. We write $f(x) \sim \sum a_n x^n$.

The crucial difference: an asymptotic series doesn't have to converge! The partial sums might eventually blow up—but for fixed small $x$, the first few terms give a good approximation.

### Example: $e^{-1/x}$ and Its "Taylor Series"

Consider $f(x) = e^{-1/x}$ for $x > 0$. This function is smooth, and all its derivatives at $x = 0$ vanish:

$$
f^{(n)}(0) = 0 \quad \forall n
$$

So its Taylor series is $0 + 0 \cdot x + 0 \cdot x^2 + \cdots = 0$.

But $f(x) \neq 0$ for $x > 0$! The function is "invisible" to Taylor expansion. It's **beyond all orders** in $x$.

This is the prototype for non-perturbative effects: things like $e^{-S/\hbar}$ (instantons) that vanish faster than any power of $\hbar$.

## Divergent Series in Physics

### The Stirling Series

The Stirling approximation for $\ln(\Gamma(z))$ is:

$$
\ln \Gamma(z) \sim \left(z - \frac{1}{2}\right)\ln z - z + \frac{1}{2}\ln(2\pi) + \sum_{n=1}^\infty \frac{B_{2n}}{2n(2n-1)z^{2n-1}}
$$

where $B_{2n}$ are Bernoulli numbers. This series **diverges** for any $z$—the Bernoulli numbers grow like $(2n)!$.

Yet truncating at the right order gives extraordinary accuracy.

### The Anharmonic Oscillator

The ground state energy of the quartic oscillator $H = p^2 + x^2 + \lambda x^4$ has a perturbation series in $\lambda$:

$$
E_0(\lambda) = 1 + a_1 \lambda + a_2 \lambda^2 + \cdots
$$

The coefficients grow like $a_n \sim (-1)^n n! \cdot c^n$. The series has **zero radius of convergence**.

But the energy exists for all $\lambda > 0$. What's the series actually computing?

## Borel Summation: Taming Divergence

The Borel transform is a way to "resum" factorial-divergent series.

Given $f(x) \sim \sum_{n=0}^\infty a_n x^n$ with $a_n \sim n!$, define the **Borel transform**:

$$
\hat{f}(t) = \sum_{n=0}^\infty \frac{a_n}{n!} t^n
$$

Dividing by $n!$ often makes the series converge! If $\hat{f}(t)$ converges for $|t| < R$, we can try to recover $f$ via the **Borel sum**:

$$
f(x) = \int_0^\infty e^{-t/x} \hat{f}(t) \, dt
$$

This integral representation can make sense even when the original series doesn't converge.

### Why It Works

Formally:

$$
\int_0^\infty e^{-t/x} t^n \, dt = n! \, x^{n+1}
$$

So the Borel integral "undoes" the division by $n!$, recovering the original (divergent) series term by term.

But the integral might converge when the series doesn't—we've exchanged a sum for an integral.

## Singularities of the Borel Transform

The Borel transform $\hat{f}(t)$ is a function of a complex variable $t$. Its **singularities** encode non-perturbative physics.

### Example: Instanton Effects

For the anharmonic oscillator, $\hat{E}_0(t)$ has singularities on the negative real axis at $t = -S_k$ where $S_k$ are instanton actions.

Near a singularity at $t = -S$:

$$
\hat{E}_0(t) \sim \frac{A}{t + S} + \text{regular}
$$

This pole contributes to the Borel integral. But if we integrate along the positive real axis, we miss it—unless we **analytically continue**.

The singularities of the Borel transform tell us about:
- **Instantons** (classical solutions with imaginary time)
- **Renormalons** (in QFT)
- **Tunneling amplitudes**
- All the non-perturbative stuff that perturbation theory "can't see"

## Darboux's Principle

**Darboux's theorem** says: the large-order behavior of Taylor coefficients is controlled by the nearest singularity of the function.

If $f(z)$ has a singularity at $z = z_0$, then:

$$
a_n \sim \frac{\text{const}}{z_0^n} \cdot n^{\alpha}
$$

The growth rate is set by $|z_0|^{-n}$; the power of $n$ depends on the type of singularity.

For the Borel transform, this means: **singularities of $\hat{f}(t)$ control the divergence of the original series**.

A singularity at $t = -S$ in the Borel plane produces factorial growth:

$$
a_n \sim n! \cdot S^{-n} \cdot (\text{power corrections})
$$

So by analyzing the large-order behavior of perturbation theory, we can infer the locations and strengths of non-perturbative effects!

## Stokes Phenomenon: When Answers Jump

Here's where it gets weird. Consider a function defined by an integral:

$$
f(z) = \int_C e^{-t/z} g(t) \, dt
$$

As $z$ varies in the complex plane, the optimal contour $C$ might need to change—because exponential $e^{-t/z}$ has different decay directions for different $\arg(z)$.

At certain special directions (**Stokes lines**), the asymptotic expansion **changes discontinuously**: a term that was exponentially small becomes exponentially large, or vice versa.

### Example: The Airy Function

$\text{Ai}(z)$ has the asymptotic expansion:

For $\arg(z) = 0$ (positive real axis):

$$
\text{Ai}(z) \sim \frac{e^{-\frac{2}{3}z^{3/2}}}{2\sqrt{\pi}z^{1/4}} \left(1 - \frac{5}{48}z^{-3/2} + \cdots \right)
$$

For $\arg(z) = \pi$ (negative real axis):

$$
\text{Ai}(z) \sim \frac{1}{\sqrt{\pi}|z|^{1/4}} \sin\left(\frac{2}{3}|z|^{3/2} + \frac{\pi}{4}\right)
$$

These are **completely different**! One is exponentially decaying, one is oscillating.

The Stokes lines are at $\arg(z) = \pm 2\pi/3$. Crossing them, the asymptotic expansion picks up or loses exponentially small contributions.

### Stokes Lines and Sectors

The complex plane divides into **Stokes sectors** separated by Stokes lines. In each sector, the asymptotic expansion takes a different form.

The expansion in one sector **does not analytically continue** to the expansion in another sector. They're related, but the coefficients of exponentially small terms jump.

This isn't a failure—it's a feature. The asymptotic expansion is capturing real structure: subdominant exponentials that become dominant as you cross Stokes lines.

## Terminants and Optimal Truncation

If you truncate an asymptotic series at the optimal order (where the terms start growing), the error is typically exponentially small.

More precisely: for a series asymptotic to $f(x)$, truncate at $N \approx \text{const}/x$. The error is $O(e^{-\text{const}/x})$.

This exponentially small error is the **terminant**—the contribution from the tail of the series, which encodes non-perturbative effects.

The terminant "knows about" the Borel singularities. By studying it, we can bootstrap from perturbation theory to non-perturbative physics.

## Resurgence: Everything Is Connected

**Resurgence** is the idea that perturbative and non-perturbative contributions are not independent—they're secretly related through the structure of the Borel transform.

The perturbative series, the one-instanton correction, the two-instanton correction... they all "know about" each other. The large-order behavior of one encodes information about the others.

This has been explored extensively in:
- Matrix models
- Topological string theory
- Gauge theory (especially Chern-Simons)
- Quantum mechanics of periodic potentials

The hope is that resurgence might eventually allow us to reconstruct non-perturbative physics from perturbative data alone.

## Summary

| Concept | What It Means |
|---------|---------------|
| **Asymptotic series** | Approximates a function; may diverge |
| **Borel transform** | Divide by $n!$ to tame factorial divergence |
| **Borel sum** | Integral representation that may converge |
| **Borel singularities** | Encode non-perturbative effects (instantons, etc.) |
| **Darboux's principle** | Nearest singularity controls large-order growth |
| **Stokes lines** | Where asymptotic expansions change discontinuously |
| **Terminant** | Exponentially small error from optimal truncation |
| **Resurgence** | Perturbative and non-perturbative are linked |

**The philosophy:** Divergent series aren't meaningless—they're encoding information about exponentially small effects in their divergence. The singularities of the Borel transform, the Stokes phenomenon, the factorial growth of coefficients—it's all telling us about physics beyond perturbation theory.

---

*See also: [WKB and Matched Asymptotics], [Functional Equations].*
