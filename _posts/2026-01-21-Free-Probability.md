---
title: "Free Probability: The Non-Commutative Central Limit Theorem"
date: 2026-01-21
motivation: "The semicircle law keeps appearing in random matrix theory. And I know from the RMT diagrammatics that planar diagrams dominate at large N. What's the algebraic structure that emerges when you take N → ∞ seriously?"
background: "Some exposure to RMT, especially the diagrammatic/$1/N$ expansion where planar diagrams dominate. The connection to 'freeness' becomes natural once you see that 'independent random matrices become free at large N' is the algebraic expression of 'only planar diagrams survive'."
llm: "Claude"
tags: [seed]
math: true
---

# Free Probability: The Non-Commutative Central Limit Theorem

## What Free Probability Is

Classical probability theory studies commutative random variables. You can always think of them as functions on some probability space, and $XY = YX$.

Free probability is what happens when you take non-commutative random variables seriously—operators on a Hilbert space, matrices, elements of a C*-algebra—and ask: what's the analog of independence?

The answer is **freeness**, discovered by Voiculescu in the 1980s while studying operator algebras. The miracle is that freeness is exactly what emerges in the large-$N$ limit of random matrix theory. Two independent random matrices become "free" as $N \to \infty$.

**The diagrammatic perspective:** If you've seen the $1/N$ expansion in RMT, you know that planar diagrams dominate at large $N$. Free probability is the algebraic structure that captures "only planar diagrams contribute." The non-crossing partition combinatorics of freeness is exactly the combinatorics of planar graphs.

## The Basic Setup

A **non-commutative probability space** is a pair $(\mathcal{A}, \varphi)$ where:
- $\mathcal{A}$ is a unital algebra (think: matrices, operators)
- $\varphi: \mathcal{A} \to \mathbb{C}$ is a linear functional with $\varphi(1) = 1$ (think: $\varphi(X) = \frac{1}{N}\text{Tr}(X)$)

The **moments** of $X \in \mathcal{A}$ are $\varphi(X^n)$, which determine the "distribution" of $X$.

For self-adjoint $X$, there's a measure $\mu_X$ on $\mathbb{R}$ such that:

$$
\varphi(X^n) = \int \lambda^n \, d\mu_X(\lambda)
$$

This $\mu_X$ is the **spectral distribution**—for matrices, it's the empirical eigenvalue distribution.

## Freeness: The Non-Commutative Independence

Two subalgebras $\mathcal{A}_1, \mathcal{A}_2 \subset \mathcal{A}$ are **free** if:

$$
\varphi(a_1 a_2 \cdots a_n) = 0
$$

whenever:
- Each $a_i$ belongs to $\mathcal{A}_1$ or $\mathcal{A}_2$
- Adjacent elements come from different subalgebras
- Each $\varphi(a_i) = 0$ (centered)

This is strange! It says mixed moments of centered elements vanish—but the elements don't commute, so the order matters.

**Example:** If $X, Y$ are free and centered, then:
- $\varphi(XY) = 0$
- $\varphi(XYXY) = 0$
- But $\varphi(XXYY) = \varphi(X^2)\varphi(Y^2)$ (not zero in general!)

Compare to classical independence where $\mathbb{E}[XY] = \mathbb{E}[X]\mathbb{E}[Y]$ regardless of order.

## The Free Central Limit Theorem

Classical CLT: if $X_1, X_2, \ldots$ are iid with mean 0, variance 1, then $\frac{1}{\sqrt{N}}\sum_{i=1}^N X_i \to \mathcal{N}(0,1)$.

**Free CLT:** If $X_1, X_2, \ldots$ are free, identically distributed, with $\varphi(X_i) = 0$, $\varphi(X_i^2) = 1$, then:

$$
\frac{1}{\sqrt{N}}\sum_{i=1}^N X_i \xrightarrow{d} \text{Semicircle}
$$

The semicircle distribution $\rho(\lambda) = \frac{1}{2\pi}\sqrt{4 - \lambda^2}$ is the free analog of the Gaussian!

This is why the Wigner semicircle appears in random matrix theory: a GUE matrix is (roughly) a sum of many free rank-1 projections.

## Transforms: The Computational Toolkit

### The Cauchy Transform

For a measure $\mu$, define:

$$
G_\mu(z) = \int \frac{d\mu(\lambda)}{z - \lambda} = \sum_{n=0}^\infty \frac{m_n}{z^{n+1}}
$$

where $m_n = \int \lambda^n d\mu$ are the moments.

The measure is recovered by:

$$
d\mu(\lambda) = -\frac{1}{\pi} \text{Im} \, G_\mu(\lambda + i0^+) \, d\lambda
$$

### The R-Transform (for Addition)

Define the **functional inverse** $K_\mu$ such that $G_\mu(K_\mu(z)) = z$.

The **R-transform** is:

$$
R_\mu(z) = K_\mu(z) - \frac{1}{z}
$$

**Theorem (Voiculescu):** If $X$ and $Y$ are free, then:

$$
\boxed{R_{X+Y}(z) = R_X(z) + R_Y(z)}
$$

The R-transform linearizes free additive convolution, just like the log of the characteristic function linearizes classical convolution.

### Computing the R-Transform

For the semicircle: $G(z) = \frac{z - \sqrt{z^2 - 4}}{2}$.

Inverting: if $G(K) = z$, then $K - \sqrt{K^2 - 4} = 2z$, giving $K = z + \frac{1}{z}$.

So $R(z) = K(z) - \frac{1}{z} = z$. The semicircle has $R(z) = z$!

This means: **semicircle + semicircle = stretched semicircle**. If $X, Y$ are free semicircles with variance 1, then $X + Y$ has R-transform $2z$, corresponding to semicircle with variance 2.

### The S-Transform (for Multiplication)

For multiplication of free positive random variables, we use the **S-transform**.

Define the **moment generating function**:

$$
\psi_\mu(z) = \int \frac{z\lambda}{1 - z\lambda} d\mu(\lambda) = \sum_{n=1}^\infty m_n z^n
$$

Let $\chi_\mu$ be its functional inverse.

The **S-transform** is:

$$
S_\mu(z) = \frac{1 + z}{z} \chi_\mu(z)
$$

**Theorem:** If $X$ and $Y$ are free, then:

$$
\boxed{S_{XY}(z) = S_X(z) \cdot S_Y(z)}
$$

## Paradigm Example: Marcenko-Pastur

Let $X$ be an $N \times M$ matrix with iid entries of variance $1/N$. Consider $W = XX^T$ (or $X^T X$), an $N \times N$ (or $M \times M$) matrix.

As $N, M \to \infty$ with $M/N \to \gamma$, the eigenvalue distribution of $W$ converges to the **Marcenko-Pastur distribution**:

$$
\rho_{MP}(\lambda) = \frac{\sqrt{(\lambda_+ - \lambda)(\lambda - \lambda_-)}}{2\pi \gamma \lambda} \cdot \mathbf{1}_{[\lambda_-, \lambda_+]}
$$

where $\lambda_\pm = (1 \pm \sqrt{\gamma})^2$.

For $\gamma < 1$, there's also a point mass $(1 - \gamma)\delta_0$ at zero (more columns than rows means null space).

### Free Probability Derivation

Think of $XX^T$ as a product of free things. In the free probability setup:

- $X$ is a "rectangular free random variable"
- $XX^T$ is its "free square"

The S-transform of Marcenko-Pastur is:

$$
S_{MP}(z) = \frac{1}{1 + \gamma z}
$$

This simple form reflects the factorization property of free multiplication.

## Free Poisson (Marcenko-Pastur as $\gamma \to 0$)

When $\gamma \to 0$ with $\gamma N$ fixed, Marcenko-Pastur becomes the **free Poisson** (or Marchenko-Pastur with rate parameter).

The free Poisson is to free probability what the Poisson distribution is to classical probability—the limit of sums of many small free Bernoulli-like variables.

## Other Key Distributions

| Classical | Free Analog | R-transform |
|-----------|-------------|-------------|
| Gaussian | Semicircle | $R(z) = z$ |
| Poisson | Free Poisson | $R(z) = \frac{1}{1-z}$ |
| Bernoulli | Free Bernoulli | $R(z) = pz$ |
| Cauchy | Free Cauchy | $R(z) = i$ (constant!) |

## Freeness from Random Matrices

**Theorem (Voiculescu):** Let $A_N$ and $B_N$ be $N \times N$ random matrices such that:
- $A_N$ is diagonal with empirical eigenvalue distribution converging to $\mu_A$
- $B_N = U_N D_N U_N^*$ where $U_N$ is Haar-distributed unitary, independent of $A_N$, and $D_N$ diagonal with empirical distribution converging to $\mu_B$

Then $(A_N, B_N)$ converge in distribution to free random variables with distributions $(\mu_A, \mu_B)$.

In other words: **conjugating by a random unitary makes things free**.

This is why freeness appears in random matrix theory: independent random matrices, when multiplied or added, behave as if free in the large-$N$ limit.

## Connection to Classical Probability

There's a beautiful parallel:

| Classical | Free |
|-----------|------|
| Independence | Freeness |
| Gaussian | Semicircle |
| Fourier/char function | Cauchy/R-transform |
| Convolution | Free convolution |
| CLT | Free CLT |
| Poisson limit | Free Poisson limit |

The theories are not isomorphic—freeness is genuinely different from independence—but they share the same structural skeleton.

## What We Didn't Cover

- **Free entropy** and connections to von Neumann algebras
- **Operator-valued free probability** (matrix-valued distributions)
- **Free stochastic calculus** and free Brownian motion
- **Boolean and monotone independence** (other notions of non-commutative independence)
- **Combinatorics of non-crossing partitions** (the enumerative backbone)

---

*See also: [Random Matrix Theory Tour], [Extreme Value Theory].*
