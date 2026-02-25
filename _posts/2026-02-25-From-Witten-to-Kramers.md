---
title: "From Witten to Kramers"
date: 2026-02-25
motivation: "The Witten deformation connects two things that look very different: the Morse complex (a topological chain complex counting gradient flow lines) and the Kramers rate matrix (a finite-state Markov chain on potential minima).  Both are projections of the same operator onto its low-energy subspace."
background: "Morse theory at the level of 'Morse Theory', the Witten Laplacian at the level of 'The Witten Deformation'.  We'll use both freely."
llm: "Claude"
tags: [seed]
math: true
---

# From Witten to Kramers

## Where We Are

We have a deformed Laplacian $\Delta_t$ acting on differential forms, with parameter $t$ playing the role of inverse temperature.  At large $t$ (see [The Witten Deformation]):

- Each index-$k$ critical point contributes one near-zero eigenvalue to $\Delta_t^{(k)}$
- All other eigenvalues are $O(t)$

The near-zero eigenforms are exponentially localized at the critical points.  There's a clean spectral gap.  The game now: project everything onto the low-energy subspace and see what structure survives.

## The Instanton Matrix

Let $\Pi_k$ be the spectral projection onto the low-energy subspace of $\Delta_t^{(k)}$ - the span of eigenforms with eigenvalues below the gap.  This subspace has dimension $c_k$ (one basis vector per index-$k$ critical point).

The twisted exterior derivative $d_t$ maps $k$-forms to $(k+1)$-forms.  Its projection to the low-energy subspaces gives a finite-dimensional operator:

$$
\hat{d}_k = \Pi_{k+1}\, d_t\, \Pi_k \;:\; \hat{C}_k \to \hat{C}_{k+1}
$$

where $\hat{C}_k$ is the $c_k$-dimensional low-energy subspace.

The matrix elements of $\hat{d}_k$ connect critical points of adjacent index.  If $p$ has index $k$ and $q$ has index $k+1$, with localized eigenforms $\vert p\rangle$ and $\vert q\rangle$:

$$
\langle q \vert\, d_t \,\vert p \rangle \sim A_{pq}\, e^{-t[f(q) - f(p)]}
$$

The exponential factor $e^{-t\Delta f}$ is set by the difference in critical values.  The prefactor $A_{pq}$ is an $O(1)$ quantity that depends on the geometry: curvatures at the critical points, the determinant of the fluctuation operator around the connecting gradient flow line.

**These matrix elements are instanton contributions.**  The gradient flow line from $q$ (higher) down to $p$ (lower) is the classical solution connecting two critical points.  The matrix element of $d_t$ is computed by a WKB/saddle-point evaluation around this classical path (see [WKB and the Art of Matched Asymptotics]), giving the exponential suppression times a one-loop prefactor.

The time-reversed flow line - from $p$ uphill to $q$ - is the instanton in the Langevin dynamics: the optimal fluctuation path that carries the system from one metastable state over a barrier (see [Instantons in Statistical Physics]).  Same geometry, seen from the analytical side.

When multiple gradient flow lines connect $p$ to $q$, the matrix element sums over all of them.  The signed count (with orientations from the unstable manifolds) determines the leading-order coefficient.

## From Witten to Morse

The projected complex $\hat{d}: \hat{C}_k \to \hat{C}_{k+1}$ is a finite-dimensional chain complex.  It satisfies $\hat{d}^2 = 0$ because $d_t^2 = 0$ and the projection preserves this to the relevant order.

**Claim:** at large $t$, this projected complex is isomorphic to the Morse complex from [Morse Theory].

The generators match: one per critical point of each index.  The boundary operator matches: the matrix elements of $\hat{d}$ between adjacent-index critical points are controlled by gradient flow lines, and after extracting the common exponential factors and normalizing the basis, the signed count of flow lines reproduces the Morse boundary operator $\partial$.

More precisely: the leading term in $\langle q \vert d_t \vert p \rangle$ as $t \to \infty$ is determined by the number and orientations of gradient flow lines from $q$ to $p$.  The exponential factors $e^{-t\Delta f}$ depend only on the critical values (not on which specific pair of critical points), so they can be absorbed into a rescaling of the basis vectors.  What's left is the combinatorial data: $n(q, p)$, the signed flow line count.

This gives an **analytical proof of the Morse Homology Theorem**:

1. The $d_t$-complex has the same cohomology as $d$ for all $t$ (they're conjugate via $e^{tf}$)
2. The $d$-complex computes de Rham cohomology $H^*_{\text{dR}}(M)$
3. At large $t$, the low-energy subspace of the $d_t$-complex is well-approximated by the projected complex $\hat{d}$
4. The projected complex is the Morse complex

Therefore: Morse homology $\cong$ de Rham cohomology.  Please clap.

This is Witten's great contribution (1982): a physical/analytical proof of a topological theorem, via semiclassical localization.  The semiclassical limit ($t \to \infty$) is the low-temperature limit, and the instanton expansion around gradient flow lines is what connects the analytical and combinatorial sides.

## The Spectral Sequence

For the algebraically inclined: the passage from the Witten Laplacian to the Morse complex can be organized as a **spectral sequence**.

The filtration is by eigenvalue scale:
- $E_0$: the full $d_t$-complex (all forms, all eigenvalues)
- $E_1$: the Morse complex (project to the near-zero subspace, take cohomology)
- $E_\infty$: the de Rham cohomology $H^*(M)$

The $E_1$ page is the Morse complex.  The spectral sequence converges to de Rham cohomology.

Physical interpretation: $E_0 \to E_1$ is integrating out the fast modes (eigenvalues $\sim t$).  Each subsequent page incorporates higher-order instanton corrections - multi-instanton processes where a gradient flow line passes through intermediate critical points.

For most applications, $E_1$ already gives the answer (the Morse function is "perfect" or close to it).  When there are nontrivial cancellations in the Morse boundary operator, the higher pages resolve them.

## The Finite-State Markov Chain

Now restrict attention to 0-forms.  This is where we came from: the Fokker-Planck equation.

The low-energy subspace of $\Delta_t^{(0)}$ has dimension $c_0$ = number of local minima of $V$.  Each basis vector $\vert i \rangle$ is a near-zero eigenform exponentially localized at minimum $x_i$.

The FP dynamics projected onto this subspace is a **finite-state continuous-time Markov chain** with generator:

$$
\hat{L}_{ij} \propto \langle i \vert\, \Delta_t^{(0)} \,\vert j \rangle
$$

The Witten Laplacian on 0-forms factors as $\Delta_t^{(0)} = d_t^*\,d_t$, so:

$$
\langle i \vert\, \Delta_t^{(0)} \,\vert j \rangle = \sum_s \langle i \vert d_t^* \vert s \rangle \langle s \vert d_t \vert j \rangle = \sum_s \overline{\langle s \vert d_t \vert i \rangle}\, \langle s \vert d_t \vert j \rangle
$$

where the sum runs over saddles $s$ (the low-energy 1-form states).  The transition rate from minimum $j$ involves the instanton matrix elements at the intervening saddle:

$$
\vert \langle s \vert d_t \vert j \rangle \vert^2 \sim e^{-2t[V(s) - V(x_j)]} = e^{-[V(s) - V(x_j)]/T}
$$

That's **Kramers' formula**: the rate out of minimum $j$ via saddle $s$ goes as $e^{-\Delta V/T}$, where $\Delta V = V(s) - V(x_j)$ is the barrier height.  The prefactor comes from the fluctuation determinant (curvatures at the minimum and the saddle).  Derived, not assumed.

The derivation rests on three things:
1. **Spectral gap** of $\Delta_t^{(0)}$ justifies the projection onto the slow subspace
2. **Instanton calculus** (WKB around gradient flow lines) gives the matrix elements
3. **Factorization** $\Delta_t^{(0)} = d_t^* d_t$ routes the transition through the saddle

**SUSY guarantees detailed balance.**  The projected chain satisfies:

$$
\hat{L}_{ij}\,\pi_j = \hat{L}_{ji}\,\pi_i
$$

where $\pi_i \propto e^{-V(x_i)/T}$ is the projected equilibrium weight.  This follows from the self-adjointness of the conjugated operator (the Witten Laplacian is manifestly self-adjoint), which in turn follows from the SUSY structure $H = QQ^\dagger + Q^\dagger Q$.

The finite-state Markov chain on the minima of a potential isn't just a physicist's convenient approximation.  It's a rigorous slow-manifold reduction, and the proof passes through differential topology.

## The Full Dictionary

| Statistical Physics | Witten Deformation | Morse Theory / Topology |
|---|---|---|
| Potential $V(x)$ | Morse function $f$ | Height function on $M$ |
| Temperature $T$ | $1/(2t)$ | Deformation parameter |
| Boltzmann weight $e^{-V/T}$ | Conjugation $e^{-tf}$ | Twisting |
| FP operator $L_{\text{FP}}$ | $\Delta_t^{(0)}$ | Deformed Hodge Laplacian on 0-forms |
| Metastable states (minima) | Low-energy 0-forms | Index-0 critical points |
| Transition states (saddles) | Low-energy 1-forms | Index-1 critical points |
| Kramers rate $\sim e^{-\Delta V/T}$ | Instanton matrix element $\sim e^{-t\Delta f}$ | Morse boundary $\partial$ |
| Kramers prefactor | Fluctuation determinant | Gradient flow line orientation |
| Finite Markov chain | Projected $\Delta_t^{(0)}$ on slow subspace | $C_0$ of Morse complex |
| Slow relaxation rates | Exponentially small eigenvalues | $b_0$ (connected components) |
| Number of basins $c_0$ | $\dim\hat{C}_0$ | Morse inequality $c_0 \geq b_0$ |
| Arrhenius/Kramers law | WKB/semiclassical expansion | Instanton action |
| Integrate out fast modes | Spectral projection $\Pi_k$ | $E_0 \to E_1$ in spectral sequence |
| Detailed balance | Self-adjointness of $\Delta_t$ | SUSY: $H = QQ^\dagger + Q^\dagger Q$ |
| Equilibrium $\rho_{\text{eq}}$ | Harmonic 0-form | Generator of $H^0(M)$ |
| $\sum(-1)^k c_k = 0$ (typical) | Witten index | Euler characteristic $\chi(M)$ |

## What We Built

Three seeds, one arc.  [Morse Theory] gave us the combinatorial skeleton: critical points, gradient flow lines, and a chain complex that computes homology.  [The Witten Deformation] showed that the Fokker-Planck equation, after a similarity transformation, naturally produces a deformed version of this complex - with the algebraic structure of the exterior derivative (a.k.a. supersymmetry) protecting the topological content and pairing eigenvalues across form degrees.  Here, projecting onto the slow subspace, we recovered both the Morse complex (the topological content) and the Kramers rate matrix (the physical content) as two faces of the same spectral projection.

The finite-state Markov chain on potential minima isn't a cartoon.  It's a theorem.

Open directions: the same framework extends to singular learning theory (where the RLCT plays a role analogous to the Morse index in a degenerate setting), to quantum field theory (where $V$ becomes an action functional on an infinite-dimensional space), and to computational topology (discrete Morse theory provides algorithms for homology).

---

*See also: [Morse Theory], [The Witten Deformation], [Instantons in Statistical Physics], [WKB and the Art of Matched Asymptotics].*

Written with Claude.
