---
title: "The Witten Deformation"
date: 2026-02-25
motivation: "The Fokker-Planck equation for a particle in a multi-well potential has a hidden algebraic structure: it's one piece of a supersymmetric complex.  This structure connects statistical mechanics to topology via Morse theory."
background: "Familiarity with the Fokker-Planck equation, basic spectral theory, Morse theory at the level of 'Morse Theory'.  Differential forms at the level of 'what is a $k$-form' helps but isn't strictly required."
llm: "Claude"
tags: [seed]
math: true
---

# The Witten Deformation

## The Physical Question

Consider a particle in a multi-well potential $V(x)$ on a compact manifold $M$, subject to overdamped Langevin dynamics at temperature $T$:

$$
\dot{x} = -\nabla V(x) + \sqrt{2T}\,\xi(t)
$$

At low temperature, the particle sits near a local minimum for a long time, occasionally hopping to another.  The transition rates are exponentially small: $k \sim e^{-\Delta V/T}$ where $\Delta V$ is the barrier height (this is Kramers' formula - see [Instantons in Statistical Physics]).

Here's a natural question.  Physicists routinely approximate the slow dynamics by a **finite-state Markov chain** whose states are the minima of $V$ and whose rates are given by Kramers' formula.  Can this be made rigorous?  Which degrees of freedom are slow, which are fast, and why does the projection onto slow modes respect the structure of the original dynamics?

The Fokker-Planck equation for the probability density $\rho(x, t)$ is:

$$
\partial_t \rho = \nabla \cdot (T\nabla\rho + \rho\nabla V) \equiv L_{\text{FP}}\,\rho
$$

The equilibrium distribution is Boltzmann: $\rho_{\text{eq}} \propto e^{-V/T}$.  Everything we need is hiding in the spectrum of $L_{\text{FP}}$.

## Ground State Conjugation

The FP operator $L_{\text{FP}}$ is not self-adjoint in the standard $L^2$ inner product.  This makes spectral analysis painful - eigenvalues could be complex, eigenvectors non-orthogonal.  But there's a similarity transformation that fixes this.

Write $\rho = \psi \cdot e^{-V/(2T)}$.  Then $\partial_t \psi = -H_0\,\psi$, where:

$$
H_0 = -T\Delta + \frac{\vert\nabla V\vert^2}{4T} - \frac{\Delta V}{2}
$$

This is a **Schrödinger operator** - self-adjoint and non-negative (the FP eigenvalues are non-positive, and conjugation flips the sign).  The ground state $\psi_0 = \text{const}$ has eigenvalue zero, corresponding to the Boltzmann equilibrium.

The potential $U(x) = \frac{\vert\nabla V\vert^2}{4T} - \frac{\Delta V}{2}$ has a nice structure:

- **At critical points** of $V$ (where $\nabla V = 0$): $U = -\frac{1}{2}\Delta V = -\frac{1}{2}\sum_i \lambda_i$, where $\lambda_i$ are the Hessian eigenvalues.
- **Away from critical points** at low $T$: the term $\vert\nabla V\vert^2/(4T)$ dominates, creating steep potential walls that confine eigenstates near the critical points.

Near a minimum (all $\lambda_i > 0$), the operator looks like a sum of harmonic oscillators:

$$
H_0 \approx \sum_i \left(-T\,\partial_i^2 + \frac{\lambda_i^2}{4T}\,x_i^2\right) - \frac{1}{2}\sum_i \lambda_i
$$

The ground state energy of the $i$-th oscillator is $\frac{1}{2}\vert\lambda_i\vert$, so the total zero-point energy is $\frac{1}{2}\sum_i \vert\lambda_i\vert - \frac{1}{2}\sum_i \lambda_i$.  At a minimum, all $\lambda_i > 0$ and this vanishes: $E = 0$.  That's the Boltzmann equilibrium.

At a saddle with $k$ negative eigenvalues, the same arithmetic gives $E = -\sum_{i:\lambda_i < 0} \lambda_i > 0$.  The modes localized at saddles have positive energy - they decay fast.  The spectral gap between the near-zero modes (at minima) and the bulk is of order $\min_i \vert\lambda_i\vert$, while the splitting of the ground state manifold due to tunneling is exponentially small in $1/T$.

tl;dr: the low-lying spectrum sees the minima.  The saddles sit above a gap.

## The Twisted Exterior Derivative

Here's where it gets interesting.  The operator $H_0$ acts on functions (0-forms).  But there's no a priori reason its eigenstates should encode topology.  Witten's insight (1982): $H_0$ is one component of a **deformed Laplacian** acting on all differential forms, and this larger structure is where the topology lives.

Define the **twisted exterior derivative**, using $f = V$ (the potential as Morse function) and $t = 1/(2T)$:

$$
d_t = e^{-tf}\,d\,e^{tf} = d + t\,df \wedge
$$

The ordinary exterior derivative $d$ gets an extra piece: "wedge with $t$ times the gradient 1-form."

Key properties:
1. **Still a complex**: $d_t^2 = 0$, because $d_t = e^{-tf}de^{tf}$ and $d^2 = 0$.
2. **Same cohomology**: the map $\omega \mapsto e^{tf}\omega$ intertwines $d_t$ and $d$, so the $d_t$-cohomology equals the de Rham cohomology, independent of $t$.

The adjoint (with respect to the Riemannian $L^2$ inner product) is:

$$
d_t^* = d^* + t\,\iota_{\nabla f}
$$

where $\iota_{\nabla f}$ is interior product (contraction) with the gradient vector field.

Now the key calculation.  The **Witten Laplacian**:

$$
\Delta_t = d_t\,d_t^* + d_t^*\,d_t
$$

On 0-forms, $d_t^*$ kills everything (no $(-1)$-forms), so $\Delta_t^{(0)} = d_t^*\,d_t$.  In flat coordinates:

$$
\Delta_t^{(0)} = -\Delta + t^2\vert\nabla f\vert^2 - t\,\Delta f
$$

With $f = V$ and $t = 1/(2T)$, this is $H_0/T$.  **The conjugated FP operator on functions was secretly the 0-form piece of a deformed Hodge Laplacian.**

## The Witten Laplacian and Localization

The Witten Laplacian $\Delta_t^{(k)}$ acts on $k$-forms.  At large $t$ (low temperature), its spectrum is controlled by the critical points of $f$.

### Local structure near critical points

Near a critical point $p$ of index $\lambda$, using Morse Lemma coordinates (see [Morse Theory]):

$$
\Delta_t^{(k)} \approx \sum_{i=1}^n \left(-\partial_i^2 + t^2\lambda_i^2 x_i^2\right) + t\sum_{i=1}^n \lambda_i\,\epsilon_i
$$

The first sum is a harmonic oscillator, one per direction.  The second sum is a **form-degree term**: $\epsilon_i = +1$ if the basis form $dx^i$ is present in the $k$-form, and $\epsilon_i = -1$ if absent.  (More precisely, $\epsilon_i$ is the eigenvalue of the operator $[dx^i\wedge, \iota_{\partial_i}]$ on the form in question.)

The ground state energy at critical point $p$, in the $k$-form sector, is:

$$
E_0^{(k)}(p) = \sum_{i=1}^n t\vert\lambda_i\vert + t\sum_{i=1}^n \lambda_i\,\epsilon_i
$$

This is minimized by choosing the $dx^i$ factors to align with the negative-eigenvalue directions of the Hessian.  For a critical point of index $\lambda$: the optimal $k$-form involves exactly the $\lambda$ directions with $\lambda_i < 0$, which means $k = \lambda$.

**The upshot:** as $t \to \infty$, the low-energy eigenforms of $\Delta_t^{(k)}$ localize at the index-$k$ critical points.  Each index-$k$ critical point contributes one near-zero eigenvalue.  All other eigenvalues grow like $t$.

### Spectral gap and Morse inequalities

At large $t$, the spectrum of $\Delta_t^{(k)}$ splits:
- **Near-zero eigenvalues**: one per index-$k$ critical point, exponentially small in $t$
- **Bulk eigenvalues**: $O(t)$, from the harmonic oscillator gap

The near-zero count is $c_k$ (the number of index-$k$ critical points).  The actual zero eigenvalues give $b_k = \dim H^k(M)$ (the Betti numbers).  Since the $d_t$-cohomology is independent of $t$, the Betti numbers are pinned:

$$
c_k \geq b_k
$$

The **weak Morse inequality**, proved by spectral analysis.  The eigenvalues of $\Delta_t$ can move continuously as $t$ varies, but the $c_k$ near-zero eigenvalues can't all escape through the gap to join the bulk - at least $b_k$ of them must stay at zero.

## Fokker-Planck as Supersymmetry

The Witten Laplacian has an algebraic structure that physicists call supersymmetry.  This isn't imported from particle physics - it's an intrinsic feature of the exterior derivative on any Riemannian manifold.

Define the **supercharge** $Q = d_t$ and its adjoint $Q^\dagger = d_t^*$.  The Witten Laplacian is the anticommutator:

$$
H = \lbrace Q, Q^\dagger \rbrace = QQ^\dagger + Q^\dagger Q = \Delta_t
$$

The supercharge squares to zero: $Q^2 = 0$ and $(Q^\dagger)^2 = 0$.  The Hilbert space is the space of all differential forms, graded by degree.  Even-degree forms ($k = 0, 2, 4, \ldots$) are "bosonic."  Odd-degree forms ($k = 1, 3, \ldots$) are "fermionic."

Three payoffs:

### 1. Spectral pairing

If $\omega$ is a $k$-form eigenvector of $H$ with eigenvalue $E > 0$, then $Q\omega / \lVert Q\omega \rVert$ is a $(k+1)$-form eigenvector with the same eigenvalue.  Non-zero eigenvalues come in boson-fermion pairs.

Why: $\langle \omega, H\omega\rangle = \lVert Q\omega \rVert^2 + \lVert Q^\dagger\omega \rVert^2$.  If $E > 0$, at least one of $Q\omega$ or $Q^\dagger\omega$ is nonzero.  And $HQ\omega = QH\omega = EQ\omega$.

### 2. Witten index

The **Witten index** counts zero modes with signs:

$$
\operatorname{ind}(Q) = \sum_k (-1)^k \dim\ker\Delta_t^{(k)} = \sum_k (-1)^k b_k = \chi(M)
$$

Because non-zero eigenvalues pair between adjacent form degrees, the alternating sum telescopes.  The Witten index equals the Euler characteristic, independent of $t$.

### 3. Protected zero modes

Zero modes can't be lifted to positive eigenvalues by smooth changes in $t$.  Lifting a zero mode would break a boson-fermion pair, changing the Witten index.  But the Witten index is topological - it can't change.  So the zero-mode count in each degree is protected.

This is why the Betti numbers are rigid: they count zero modes of a self-adjoint operator, and the SUSY algebra prevents those zero modes from disappearing.

**The physical picture:** The FP operator on functions is the bosonic ground floor ($k = 0$) of a supersymmetric building.  The "fermionic partners" are FP-type operators on $k$-forms for $k > 0$.  The whole structure comes from the exterior derivative and a Riemannian metric - no quantum field theory needed.  The "fermions" are differential forms.

## Summary

| Fokker-Planck | Witten Deformation | Topology |
|---|---|---|
| Potential $V(x)$ | Morse function $f$ | Height function on $M$ |
| Temperature $T$ | $t^{-1}/2$ | Deformation parameter |
| Boltzmann weight $e^{-V/T}$ | Conjugation $e^{-tf}$ | Twisting |
| FP operator $L_{\text{FP}}$ | $\Delta_t^{(0)}$ (up to $T$) | Deformed Hodge Laplacian |
| Equilibrium $\rho_{\text{eq}}$ | Harmonic 0-form | Generator of $H^0(M)$ |
| Low-energy modes at minima | Near-zero eigenvalues | Betti numbers $b_k$ |
| Spectral gap $\sim \min\vert\lambda_i\vert$ | Bulk gap $\sim t$ | Morse inequalities $c_k \geq b_k$ |
| FP on functions | Bosonic sector ($k = 0$) | 0-forms |
| "Partner" operators | Fermionic sectors ($k > 0$) | $k$-forms |
| Detailed balance | SUSY: $Q^2 = 0$ | $d^2 = 0$ |

The Fokker-Planck equation at low temperature produces a deformed de Rham complex.  The deformation localizes eigenforms at critical points, with $k$-forms concentrating at index-$k$ critical points.  The algebra of the exterior derivative - repackaged as supersymmetry - protects the topological content.

Next: projecting this complex onto its low-energy subspace recovers the Morse complex on one hand and the Kramers rate matrix on the other.  See [From Witten to Kramers].

---

*See also: [Morse Theory], [Instantons in Statistical Physics], [From Witten to Kramers].*

Written with Claude.
