---
title: "Manifolds for the Anti-Mathematician"
date: 2026-01-21
tags: [seed, math, physics]
motivation: "I keep hitting differential geometry prerequisites and bouncing off. Topology-first presentations lose me. What's the minimum I need to actually compute things?"
background: "Calculus, linear algebra, physics intuition. Frustrated by formal definitions when you just want to know: what IS a tangent vector, and why do Christoffel symbols exist?"
llm: "Claude"
---

# Manifolds for the Anti-Mathematician

## The Problem

Differential geometry is by nature scary. Physicists who are dedicated to understanding what they're learning get stuck in a widening pile of formal mathematics—they feel they need to grip what it means to say a manifold is a "second-countable Hausdorff space locally homeomorphic to $\mathbb{R}^n$" (with further definitions for differentiable manifolds, atlases, transition maps...).

It's important that someone knows and works with that stuff. But it ain't me, and if you want it to be not you (at least to start with), this post is for you.

## The Punchline

A manifold is a calculus-thing.

That's it. That easy. Drop the topology, draw the upside-down triangle next to your function, and turn your frown upside-down.

What I mean when I say "manifold" is: **a thing where I can use a slightly jacked-up version of calculus**. You get "calculus in whacky coordinate systems" for free. Ever wanted to compute a parabolic derivative? You should probably learn numerics or do something else instead, but manifolds will let you do that if you insist.

Even better: integration is actually much more robust to define than differentiation. You can slap an integral on basically any space you want. We only *need* manifolds for derivative-y stuff.

## The Game

Here's how we play:

1. I'll say a thing from calculus in Cartesian coordinates on $\mathbb{R}^n$
2. We'll make a big deal about how to write this in different coordinates
3. We'll pretend we're fancy mathematicians and write it "coordinate-free"
4. Then the actual manifold-y stuff is just icing

---

## Part 1: Vectors Live at Points

### The Lie About Vectors

You learned: "A vector is a list of numbers." Or maybe: "A vector is an arrow."

Both are half-truths. Here's what's actually going on.

**The adult version:** Vectors live at points, and **you cannot move them**.

Seriously. You. Cannot. Move. Them.

In flat $\mathbb{R}^n$ with Cartesian coordinates, you can *pretend* to move vectors around because the space looks the same everywhere. But on a curved surface? A vector at the North Pole and a vector at the equator don't live in the same vector space. They can't be added. They can't be compared directly.

### Tangent Spaces

At each point $p$ on your manifold, there's a vector space $T_p M$ called the **tangent space**. Think of it as all the possible "directions you could go" starting from $p$.

For $\mathbb{R}^n$: $T_p \mathbb{R}^n \cong \mathbb{R}^n$ (a copy of $\mathbb{R}^n$ attached at $p$).

For a sphere: $T_p S^2$ is the plane tangent to the sphere at $p$.

**Morally:** A vector at $p$ says "this direction!" with a magnitude attached. Vectors point *in* directions, they don't point *to* distant points.

### Basis Vectors and Coordinates

At each point, pick a basis for $T_p M$. Now vectors become lists of numbers again—their components in that basis.

**Choosing coordinates = choosing bases at every point (in a smooth way).**

In Cartesian coordinates on $\mathbb{R}^2$: basis vectors are $\hat{e}_x$, $\hat{e}_y$ everywhere.

In polar coordinates: basis vectors are $\hat{e}_r$, $\hat{e}_\theta$—and these **depend on where you are**.

At $(r, \theta) = (1, 0)$: $\hat{e}_r$ points in the $+x$ direction, $\hat{e}_\theta$ points in the $+y$ direction.

At $(r, \theta) = (1, \pi/2)$: $\hat{e}_r$ points in the $+y$ direction, $\hat{e}_\theta$ points in the $-x$ direction.

Different points, different bases. LIST OF NUMBERS IS BACK THANK GOD—but the list means different things at different points.

### Example: Velocity in Polar Coordinates

A particle spirals outward: $r(t) = t$, $\theta(t) = t$.

Velocity: $\vec{v} = \dot{r} \hat{e}_r + r\dot{\theta} \hat{e}_\theta = 1 \cdot \hat{e}_r + t \cdot \hat{e}_\theta$

At $t = 1$: the velocity is $\hat{e}_r + \hat{e}_\theta$.

In Cartesian, you'd write:

$$
\vec{v} = \dot{x}\hat{e}_x + \dot{y}\hat{e}_y
$$

with $x = r\cos\theta = t\cos t$, $y = r\sin t$, so $\dot{x} = \cos t - t\sin t$, etc.

The vector is the same object. The *components* depend on your basis choice.

---

## Part 2: Derivatives Get Weird

### The 1D Case

Derivative: $f'(x) = \lim_{\epsilon \to 0} \frac{f(x+\epsilon) - f(x)}{\epsilon}$

No problems here. (Well, actually there are, but never mind.)

### Higher Dimensions

In $\mathbb{R}^n$: "same but for any direction."

Directional derivative in direction $\vec{v}$:

$$
D_{\vec{v}} f = \lim_{\epsilon \to 0} \frac{f(p + \epsilon \vec{v}) - f(p)}{\epsilon}
$$

The gradient $\nabla f$ is the object such that $D_{\vec{v}} f = \nabla f \cdot \vec{v}$.

**But wait.** We said vectors live at points. What does "$p + \epsilon \vec{v}$" mean?

In flat $\mathbb{R}^n$, it's fine—there's a canonical way to turn "direction from $p$" into "nearby point." On a curved manifold, there isn't. You need more structure.

### The Connection Problem

Suppose I want to take the derivative of a *vector field* $\vec{V}(x)$—a vector at every point.

$$
\frac{d\vec{V}}{dx} = \lim_{\epsilon \to 0} \frac{\vec{V}(x + \epsilon) - \vec{V}(x)}{\epsilon}
$$

**Uh oh.** $\vec{V}(x + \epsilon)$ lives in $T_{x+\epsilon}M$. $\vec{V}(x)$ lives in $T_x M$. These are different vector spaces. You can't subtract vectors from different spaces!

In Cartesian coordinates on flat $\mathbb{R}^n$: the basis vectors $\hat{e}_i$ are the same everywhere, so you can pretend this isn't a problem. Just differentiate component-by-component.

In curvilinear coordinates: the basis vectors $\hat{e}_i(x)$ depend on $x$. When you differentiate $\vec{V} = V^i \hat{e}_i$, you get:

$$
\frac{d\vec{V}}{dx^j} = \frac{\partial V^i}{\partial x^j} \hat{e}_i + V^i \frac{\partial \hat{e}_i}{\partial x^j}
$$

That second term is the problem. How do basis vectors at one point relate to basis vectors at another?

### Enter the Connection

A **connection** tells you how to "parallel transport" vectors from one tangent space to another.

Write: $\frac{\partial \hat{e}_i}{\partial x^j} = \Gamma^k_{ij} \hat{e}_k$

These $\Gamma^k_{ij}$ are the **Christoffel symbols**. They encode "how the coordinate basis twists as you move."

The **covariant derivative** is:

$$
\nabla_j V^i = \frac{\partial V^i}{\partial x^j} + \Gamma^i_{jk} V^k
$$

This is the "correct" derivative—it transforms properly under coordinate changes.

### The Invariance Principle

**If I change coordinates, my answers shouldn't change.**

The partial derivative $\partial_j V^i$ transforms badly (picks up extra terms from chain rule on the basis).

The Christoffel symbols also transform badly.

But $\nabla_j V^i$? Transforms like a tensor. The bad transformations cancel.

This is the point of covariant derivatives: they're coordinate-independent notions dressed up in coordinate-dependent clothing.

---

## Part 3: What a Manifold Actually Is

Now we can say what a manifold is without the topology jargon:

**A manifold is a space where:**
1. At each point, there's a tangent space (directions you can go)
2. You can choose coordinates (smoothly varying bases)
3. You can do calculus (derivatives, integrals) in any coordinates and get consistent answers

The formal definition (charts, atlases, Hausdorff, second-countable) is just making this precise. It ensures:
- Coordinates exist and are well-behaved
- Different coordinate systems are compatible
- The space doesn't have pathological points

For physics: if you can parametrize your thing smoothly and take derivatives, it's a manifold. Don't overthink it.

### Metrics: Measuring Stuff

A **metric** $g_{ij}$ tells you how to measure lengths and angles.

$$
ds^2 = g_{ij} dx^i dx^j
$$

In Cartesian $\mathbb{R}^n$: $g_{ij} = \delta_{ij}$ (the identity matrix).

In polar coordinates: $g_{rr} = 1$, $g_{\theta\theta} = r^2$, off-diagonals zero. So $ds^2 = dr^2 + r^2 d\theta^2$.

The metric is what turns your manifold from a floppy topological thing into a rigid geometric thing.

**Bonus:** The Christoffel symbols for the "Levi-Civita connection" (the natural one) can be computed from the metric:

$$
\Gamma^k_{ij} = \frac{1}{2} g^{k\ell}(\partial_i g_{j\ell} + \partial_j g_{i\ell} - \partial_\ell g_{ij})
$$

Memorize this if you want, or derive it every time from "parallel transport preserves lengths and is torsion-free."

---

## Part 4: The Payoff

### Example: Calculus on Probability Space

Here's a wicked example that'll make all this seem not useless.

The space of probability distributions on $\mathbb{R}^n$ is infinite-dimensional, but it's a manifold! The **Wasserstein geometry** (from optimal transport) gives it a metric.

- **Points:** probability distributions $\rho(x)$
- **Tangent vectors:** velocity fields $v(x)$ that describe how $\rho$ could flow
- **Metric:** $\|v\|^2 = \int |v(x)|^2 \rho(x) dx$

The "gradient" of a functional $F[\rho]$ in this geometry is:

$$
\nabla_W F = -\nabla \cdot \left( \rho \nabla \frac{\delta F}{\delta \rho} \right)
$$

This is the **Otto calculus**. Gradient flow in Wasserstein space gives you the Fokker-Planck equation, heat equation, etc.

All the manifold machinery—tangent spaces, metrics, covariant derivatives—applies to this infinite-dimensional space. That's the power of the abstraction.

### Example: Configuration Space

A robot arm with $n$ joints lives on a manifold: the configuration space.

Each joint angle $\theta_i$ is an element of $S^1$ (a circle). The full configuration space is $(S^1)^n$, a torus.

The metric comes from the kinetic energy:

$$
T = \frac{1}{2} g_{ij}(\theta) \dot{\theta}^i \dot{\theta}^j
$$

where $g_{ij}$ depends on the mass distribution.

Equations of motion? Geodesics on this manifold (plus whatever forces you apply).

---

## Summary

| Concept | Plain English |
|---------|---------------|
| Manifold | Space where you can do calculus |
| Tangent space | Directions at a point |
| Coordinates | A choice of basis at each point |
| Connection | How to compare vectors at different points |
| Christoffel symbols | The "twisting" of coordinate bases |
| Covariant derivative | The coordinate-independent derivative |
| Metric | How to measure length |

**The philosophy:** Work in coordinates when computing, but understand that the answer doesn't depend on your choice. The formal machinery exists to make "doesn't depend on choice" precise.

---

## What We Didn't Cover

- **Curvature tensors** (Riemann, Ricci, scalar curvature)
- **Differential forms** and exterior calculus
- **Fiber bundles** (gauge theory, principal bundles)
- **Riemannian vs. pseudo-Riemannian** (GR uses the latter)
- **Symplectic manifolds** (Hamiltonian mechanics)

For these, read a real book. But now you know what you're getting into.

---

*"The reader who has followed me to this point will find no difficulty in understanding the matter."* — Every differential geometry textbook, lying

*See also: [Lie Groups and Haar Measure].*
