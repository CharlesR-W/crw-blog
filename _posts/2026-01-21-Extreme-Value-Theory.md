---
title: "Extreme Value Theory: Why Maxima Have Universal Statistics"
date: 2026-01-21
tags: [seed, math, physics]
motivation: "CLT tells me about sums converging to Gaussians—is there an analogous story for maxima? Surely 'take the max of N things' is as natural an operation as 'sum N things'."
background: "Basic probability, familiarity with CLT. The question becomes natural when you realize sums and maxima are both aggregation operations that might have universal limits."
llm: "Claude"
---

# Extreme Value Theory: Why Maxima Have Universal Statistics

## The Punchline

The Central Limit Theorem says: sums of random variables converge to Gaussians (under mild conditions).

Extreme Value Theory says: **maxima of random variables converge to one of three distributions** (under mild conditions).

Just three. That's it. No matter what distribution you start with, the maximum of $N$ samples, properly rescaled, converges to either:
- **Gumbel** (Type I): light tails (Gaussian, exponential)
- **Fréchet** (Type II): heavy tails (power law, Pareto)
- **Weibull** (Type III): bounded support (uniform, beta)

This is the **Fisher-Tippett-Gnedenko theorem**, and it's as fundamental as the CLT.

## Setup: What We're Computing

Let $X_1, \ldots, X_N$ be iid from some distribution $F(x) = P(X \leq x)$.

Define $M_N = \max(X_1, \ldots, X_N)$.

We have:

$$
P(M_N \leq x) = P(X_1 \leq x, \ldots, X_N \leq x) = F(x)^N
$$

As $N \to \infty$, this converges to 0 or 1 for any fixed $x$ (unless $x$ is exactly the upper endpoint of the support). We need to **rescale**.

Look for sequences $a_N > 0$, $b_N$ such that:

$$
P\left(\frac{M_N - b_N}{a_N} \leq x\right) \to G(x)
$$

for some non-degenerate $G$.

## The Three Universal Distributions

### Gumbel (Type I)

$$
G_1(x) = \exp(-e^{-x}), \quad x \in \mathbb{R}
$$

PDF: $g_1(x) = e^{-x} \exp(-e^{-x})$

**Domain of attraction:** Distributions with tails decaying faster than any power law but slower than bounded.

Examples: Gaussian, exponential, gamma, lognormal.

**Characteristic:** The tail $\bar{F}(x) = 1 - F(x)$ satisfies

$$
\lim_{x \to x^*} \frac{\bar{F}(x + t \cdot a(x))}{\bar{F}(x)} = e^{-t}
$$

for some auxiliary function $a(x)$.

### Fréchet (Type II)

$$
G_2(x; \alpha) = \begin{cases} 0 & x \leq 0 \\ \exp(-x^{-\alpha}) & x > 0 \end{cases}
$$

**Domain of attraction:** Power-law tails, $\bar{F}(x) \sim x^{-\alpha}$.

Examples: Pareto, Cauchy, Student-t.

**Characteristic:** Regularly varying tails:

$$
\lim_{t \to \infty} \frac{\bar{F}(tx)}{\bar{F}(t)} = x^{-\alpha}
$$

### Weibull (Type III)

$$
G_3(x; \alpha) = \begin{cases} \exp(-(-x)^\alpha) & x \leq 0 \\ 1 & x > 0 \end{cases}
$$

**Domain of attraction:** Distributions with finite upper endpoint $x^*$.

Examples: Uniform, beta, any bounded distribution.

**Characteristic:** Near the endpoint, $\bar{F}(x^* - \epsilon) \sim \epsilon^\alpha$.

## The Generalized Extreme Value Distribution

All three can be unified into a single family with shape parameter $\xi$:

$$
\boxed{G_\xi(x) = \exp\left(-(1 + \xi x)^{-1/\xi}\right)}
$$

where $1 + \xi x > 0$.

- $\xi > 0$: Fréchet (heavy tail)
- $\xi = 0$: Gumbel (limit as $\xi \to 0$)
- $\xi < 0$: Weibull (bounded)

The parameter $\xi$ is the **tail index**. It controls how extreme the extremes get.

## Why Only Three? The RG Perspective

Here's the physics intuition: **extreme value distributions are RG fixed points**.

Consider the "renormalization" operation: take $N$ samples, compute the max. Then take $N$ of *those* maxima, compute the max again. This is equivalent to taking the max of $N^2$ original samples.

For the distribution of maxima to be stable under this operation, we need:

$$
G(x)^N = G(a_N x + b_N)
$$

This is a **functional equation** for $G$, and it turns out to have exactly three solutions (up to location-scale).

### The Stability Argument

Let $G$ be an extreme value distribution. Then:

$$
G^n(a_n x + b_n) = G(x)
$$

for appropriate normalizing sequences.

Taking logs:

$$
n \log G(a_n x + b_n) = \log G(x)
$$

For this to hold for all $n$, the function $\log(-\log G(x))$ must transform linearly under rescaling. This means:

$$
-\log G(x) = c \cdot h(x)
$$

where $h$ satisfies the functional equation:

$$
h(a_n x + b_n) = \frac{1}{n} h(x)
$$

The solutions are:
- $h(x) = e^{-x}$ (Gumbel)
- $h(x) = x^{-\alpha}$ for $x > 0$ (Fréchet)
- $h(x) = (-x)^\alpha$ for $x < 0$ (Weibull)

### Von Mises Conditions

More explicitly, the **von Mises conditions** characterize each domain of attraction in terms of the hazard rate $r(x) = f(x)/\bar{F}(x)$:

**Gumbel:** $\lim_{x \to x^*} \frac{d}{dx}\left(\frac{1}{r(x)}\right) = 0$

**Fréchet:** $\lim_{x \to \infty} x \cdot r(x) = \alpha$

**Weibull:** $\lim_{x \to x^*} (x^* - x) \cdot r(x) = \alpha$

The hazard rate is doing the work of the beta function in RG—it controls how fast you run out of probability mass in the tail.

## Connection to the CLT

The CLT is actually a *special case* of extreme value theory!

Here's why: the sum $S_N = X_1 + \cdots + X_N$ can be written as:

$$
S_N = \max \text{ over all subsets } \{i_1, \ldots, i_k\} \text{ of } X_{i_1} + \cdots + X_{i_k}
$$

...okay, that's cheating. But here's the real connection:

**Poisson representation:** An exponential random variable $E$ satisfies $E = -\log U$ where $U \sim \text{Uniform}(0,1)$.

The sum of $N$ exponentials is (roughly) $\log N + \text{Gumbel}$.

The max of $N$ uniforms is $1 - e^{-\text{Gumbel}/N} \approx 1 - 1/N$.

There's a deep duality: **sums of exponentials ↔ maxima of uniforms**.

More precisely: if $E_1, \ldots, E_N$ are iid exponentials, then:

$$
\frac{E_1 + \cdots + E_N}{E_1 + \cdots + E_{N+1}}, \ldots, \frac{E_1}{E_1 + \cdots + E_{N+1}}
$$

are the **order statistics** of $N$ uniforms on $(0,1)$.

This "exponential-uniform" duality underlies both CLT and EVT.

## Peaks Over Threshold: The Generalized Pareto

Instead of block maxima, you can study **exceedances over a high threshold** $u$.

**Theorem (Pickands-Balkema-de Haan):** For $F$ in the domain of attraction of $G_\xi$, the conditional distribution of $X - u$ given $X > u$ converges to the **Generalized Pareto Distribution**:

$$
H_\xi(x) = 1 - \left(1 + \frac{\xi x}{\sigma}\right)^{-1/\xi}
$$

for $x > 0$ (and $1 + \xi x/\sigma > 0$).

- $\xi > 0$: Pareto (heavy tail)
- $\xi = 0$: Exponential (limit)
- $\xi < 0$: Bounded above

The GPD is to EVT what the exponential is to the CLT (the "infinitely divisible" version).

## Application: Return Periods

In engineering and finance, we ask: "How big is the 100-year flood?" or "What's the 99.9th percentile loss?"

If $G$ is the extreme value distribution of annual maxima, the **$T$-year return level** $x_T$ satisfies:

$$
G(x_T) = 1 - \frac{1}{T}
$$

For the GEV:

$$
x_T = \mu + \frac{\sigma}{\xi}\left[\left(-\log(1-1/T)\right)^{-\xi} - 1\right]
$$

The tail index $\xi$ controls how fast return levels grow with $T$:
- $\xi > 0$: $x_T \sim T^\xi$ (polynomial growth—heavy tails are scary)
- $\xi = 0$: $x_T \sim \log T$ (logarithmic)
- $\xi < 0$: $x_T \to \mu - \sigma/\xi$ (bounded)

## The Extremal Process

Let $\{X_i\}$ be iid. The **extremal process** tracks the running maximum:

$$
M(t) = \max_{i \leq [Nt]} X_i
$$

after proper rescaling. As $N \to \infty$, this converges to a **Poisson point process** transformed by the extreme value distribution.

More precisely: the exceedances over high thresholds form a Poisson process with intensity $\nu(dx) = (1 + \xi x)^{-1/\xi - 1} dx$ (on the appropriate scale).

This is the "continuous-time" version of EVT, just like Brownian motion is continuous-time CLT.

## Tracy-Widom and Beyond

For *dependent* random variables with specific correlation structures, you get different universality classes.

**Tracy-Widom:** The largest eigenvalue of a random matrix (GUE) has fluctuations described by the Tracy-Widom distribution—NOT Gumbel, despite eigenvalues being "maxima" in some sense. The eigenvalue repulsion changes the universality class.

**KPZ universality:** Growth processes, directed polymers, etc. have a different extreme value distribution tied to the Tracy-Widom class.

The EVT fixed points (Gumbel/Fréchet/Weibull) assume independence. Correlations can push you to entirely different universality classes.

## Summary Table

| Property | Gumbel | Fréchet | Weibull |
|----------|--------|---------|---------|
| Tail type | Light | Heavy (power) | Bounded |
| Support | $\mathbb{R}$ | $(0, \infty)$ | $(-\infty, 0)$ |
| $\xi$ | $0$ | $> 0$ | $< 0$ |
| Examples | Gaussian, exp | Pareto, Cauchy | Uniform, beta |
| $T$-year growth | $\log T$ | $T^\xi$ | bounded |

## What We Didn't Cover

- **Multivariate extreme value theory** (copulas, dependence structures)
- **Point process methods** (detailed connection to Poisson processes)
- **Statistical inference** (how to estimate $\xi$ from data)
- **Extremes of Gaussian processes** (Borell-TIS inequality, etc.)
- **Records and their statistics**

---

*See also: [Random Matrix Theory Tour], [Free Probability].*
