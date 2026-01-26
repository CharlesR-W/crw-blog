---
title: "WKB and the Art of Matched Asymptotics"
date: 2026-01-21
tags: [seed, math, physics]
motivation: "Matched asymptotic expansions are one of the most beautiful techniques in applied mathematics—a symphony of approximations that fit together with stunning precision. WKB is the canonical example."
background: "Quantum mechanics at the Griffiths level, basic complex analysis. The goal isn't to derive Bohr-Sommerfeld (that's a consequence)—it's to see asymptotic matching as a way of thinking."
llm: "Claude"
---

# WKB and the Art of Matched Asymptotics

## What This Is Really About

The WKB approximation isn't just a trick for solving the Schrödinger equation. It's an instance of **matched asymptotic expansions**—one of the most powerful and beautiful techniques in applied mathematics.

The idea: your problem has different regimes where different approximations work. In each regime, you can solve the problem approximately. The magic is in the **matching**: demanding that these different approximations agree in their regions of overlap. This overdetermines the system in exactly the right way to pin down the answer.

When done well, matched asymptotics feels like a symphony. Different instruments playing different parts, but fitting together into something coherent. The WKB treatment of turning points is a canonical example.

## The Setup

We want to solve the time-independent Schrödinger equation:

$$
-\frac{\hbar^2}{2m}\psi'' + V(x)\psi = E\psi
$$

In the WKB regime (small $\hbar$), away from turning points, solutions look like:

$$
\psi(x) \sim \frac{C}{\sqrt{p(x)}} \exp\left( \pm \frac{i}{\hbar} \int^x p(x')\, dx' \right)
$$

where $p(x) = \sqrt{2m(E - V(x))}$ is the classical momentum.

But there's a catch: this formula blows up when $p(x) = 0$, i.e., at the **turning points** where $E = V(x)$. Classically, these are where a particle would turn around. Quantum mechanically, the wavefunction has to smoothly transition from oscillatory (in the classically allowed region) to exponentially decaying (in the forbidden region).

The WKB approximation breaks down precisely where we need it most.

## The Three Regions

Consider a potential with two turning points at $x = a$ and $x = b$ (with $a < b$). For energy $E$:

- **Region I** ($x < a$): Classically forbidden. $V(x) > E$, so $p(x)$ is imaginary. Wavefunction decays as $x \to -\infty$.

- **Region II** ($a < x < b$): Classically allowed. $V(x) < E$, so $p(x)$ is real. Wavefunction oscillates.

- **Region III** ($x > b$): Classically forbidden. $V(x) > E$, so $p(x)$ is imaginary. Wavefunction decays as $x \to +\infty$.

WKB works beautifully in each region—but we need to connect them across the turning points.

## The Turning Point Problem

Near a turning point, say $x = a$, WKB fails because:

1. The prefactor $1/\sqrt{p(x)}$ diverges.
2. The "rapidly varying" phase $\int p\, dx / \hbar$ isn't actually rapidly varying (since $p \approx 0$).

The WKB approximation assumes the phase changes much faster than the amplitude. At turning points, this assumption breaks down completely.

### The Inner Region: Airy Functions

Near the turning point, the potential is approximately linear:

$$
V(x) \approx V(a) + V'(a)(x - a) = E + V'(a)(x - a)
$$

Rescaling with $z = \alpha (x - a)$ where $\alpha = \left( \frac{2m V'(a)}{\hbar^2} \right)^{1/3}$, the Schrödinger equation becomes:

$$
\frac{d^2 \psi}{dz^2} = z \psi
$$

This is the **Airy equation**, with solutions $\text{Ai}(z)$ and $\text{Bi}(z)$.

The Airy functions are exact solutions valid near the turning point—the "inner solution."

### Airy Function Asymptotics

For $z \to +\infty$ (deep in the forbidden region):

$$
\text{Ai}(z) \sim \frac{1}{2\sqrt{\pi} z^{1/4}} \exp\left( -\frac{2}{3} z^{3/2} \right) \quad \text{(decays)}
$$

$$
\text{Bi}(z) \sim \frac{1}{\sqrt{\pi} z^{1/4}} \exp\left( +\frac{2}{3} z^{3/2} \right) \quad \text{(blows up)}
$$

For $z \to -\infty$ (deep in the allowed region):

$$
\text{Ai}(z) \sim \frac{1}{\sqrt{\pi} |z|^{1/4}} \sin\left( \frac{2}{3} |z|^{3/2} + \frac{\pi}{4} \right)
$$

$$
\text{Bi}(z) \sim \frac{1}{\sqrt{\pi} |z|^{1/4}} \cos\left( \frac{2}{3} |z|^{3/2} + \frac{\pi}{4} \right)
$$

The key: $\text{Ai}$ decays into the forbidden region, while $\text{Bi}$ blows up.

## The Matching

Here's where the symphony plays.

**Outer solution** (WKB): Valid far from turning points. In Region I:

$$
\psi_I(x) = \frac{B}{\sqrt{\kappa(x)}} \exp\left( -\frac{1}{\hbar} \int_x^a \kappa\, dx' \right)
$$

where $\kappa = \sqrt{2m(V-E)}$ and we've imposed decay as $x \to -\infty$.

**Inner solution** (Airy): Valid near $x = a$. Must use $\text{Ai}$ (not $\text{Bi}$) to match the decay.

**The overlap region**: Where both solutions are valid. Here $|x - a|$ is large enough for WKB but small enough for the linear approximation to the potential.

In the overlap, the Airy asymptotics must match the WKB form. Near $x = a$, the WKB integrals become:

$$
\int_x^a \kappa\, dx' \approx \frac{2\hbar}{3} z^{3/2}
$$

which matches the Airy exponent exactly!

### The Connection Formula

Matching through the Airy function gives the **connection formula**:

$$
\frac{1}{\sqrt{\kappa}} e^{-\frac{1}{\hbar}\int_x^a \kappa\, dx'} \quad \longleftrightarrow \quad \frac{2}{\sqrt{p}} \sin\left( \frac{1}{\hbar}\int_a^x p\, dx' + \frac{\pi}{4} \right)
$$

The decaying exponential on the forbidden side connects to an oscillating function on the allowed side—with a specific phase shift of $\pi/4$.

This phase shift is the **Maslov index** contribution. It's not arbitrary—it comes from the asymptotics of the Airy function, which in turn comes from the structure of the equation near the turning point.

## Quantization as a Consistency Condition

Now we have connection formulas at both turning points. Matching at $x = a$ gives one expression for $\psi$ in Region II. Matching at $x = b$ gives another. For these to be the same function, we need:

$$
\int_a^b p(x)\, dx = \pi\hbar \left( n + \frac{1}{2} \right), \qquad n = 0, 1, 2, \ldots
$$

This is the **Bohr-Sommerfeld quantization condition**.

The $+\frac{1}{2}$ comes from the two $\frac{\pi}{4}$ phase shifts at the two turning points. It's not put in by hand—it emerges from the matching.

### Physical Interpretation

The quantization condition says: the total phase accumulated by a wave going from $a$ to $b$ and back must be a multiple of $2\pi$ (for constructive interference), **plus an extra $\pi$** from the two turning point reflections.

In action-angle variables:

$$
\oint p\, dx = 2\pi\hbar \left( n + \frac{1}{2} \right) = h\left( n + \frac{1}{2} \right)
$$

The classical action is quantized in units of $h$, with a half-integer offset from zero-point energy.

## Why Matched Asymptotics Is Beautiful

The WKB analysis illustrates the general structure:

1. **Identify the regimes**: Where does your naive approximation work? Where does it fail?

2. **Solve in each regime**: Use whatever approximation is valid locally.

3. **Match in the overlap**: The approximations must agree where both are valid. This pins down unknown constants and phase shifts.

4. **Global consistency**: Matching around the whole domain gives quantization conditions, selection rules, or other global constraints.

The beauty is that each piece is "wrong" by itself—WKB fails at turning points, Airy is only valid near turning points—but together they construct something correct.

This is a general principle. Whenever your problem has **boundary layers** (regions where the behavior changes rapidly), matched asymptotics is likely the right tool.

## Examples Beyond Quantum Mechanics

- **Fluid mechanics**: Viscous boundary layers near surfaces. The outer solution is inviscid, the inner solution includes viscosity, and matching gives the boundary layer thickness.

- **Singular perturbation**: Any problem where setting a small parameter to zero changes the character of the equation.

- **WKB in optics**: Geometrical optics breaks down at caustics. The inner region involves Airy functions (or more generally, catastrophe theory).

- **Tunneling**: The forbidden region requires exponential WKB solutions; matching determines tunneling amplitudes.

## Summary

- **WKB** gives oscillatory/exponential solutions far from turning points
- **Airy functions** solve the problem exactly near turning points
- **Matching** in the overlap region determines phase shifts
- **Global consistency** gives quantization: $\oint p\, dx = h(n + 1/2)$

The $1/2$ isn't magic—it's the Maslov correction from turning-point phase shifts.

And the technique generalizes: identify regimes, solve locally, match globally. This is how you think about problems with multiple scales.

---

*See also: [Asymptotics, Borel, and Stokes], [Principal Symbols and Singularity Propagation].*
