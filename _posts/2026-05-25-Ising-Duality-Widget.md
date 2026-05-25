---
title: "The 2D Ising Model and Its Self-Dual Critical Point — a Widget"
date: 2026-05-25
motivation: "The 2D Ising model is everyone's first phase transition.  Most expositions show you a picture of magnetisation jumping at Tc and call that the phase diagram.  But the deeper story is that you can locate the critical point without ever running a simulation: Kramers-Wannier duality maps low-temperature physics to high-temperature physics, and the only fixed point of that map is the critical temperature.  This widget puts the two sides of the duality next to each other so you can watch them collide."
background: "Two-dimensional nearest-neighbour ferromagnetic Ising model.  Wolff cluster updates.  Two-point correlation function.  Onsager's exponent η = 1/4."
llm: "Claude"
tags: [widget, statistical-mechanics]
math: true
---

# The 2D Ising Model and Its Self-Dual Critical Point

Slide the temperature.  Watch the left lattice melt and the right lattice freeze at the same rate.  At a single temperature in the middle they become indistinguishable — that is the critical point, and you have just located it by symmetry alone.

<iframe src="{{ '/assets/widgets/ising-duality.html' | relative_url }}"
        style="width:100%; height:820px; border:0; border-radius:12px; background:#000;"
        loading="lazy"
        title="Ising duality widget"></iframe>

## What you're looking at

Two copies of the 2D Ising model on a $96 \times 96$ periodic lattice, run in parallel by Wolff cluster updates.  The left panel is at temperature $T$; the right is at the **dual temperature** $T^\ast$ defined by

$$\sinh(2\beta) \, \sinh(2\beta^\ast) = 1, \quad \beta = 1/T.$$

Move the slider and both temperatures update at once.

The lower panels are diagnostics:

- The **two-point function** $C(r) = \langle s_0 s_r \rangle$ on log-log axes, with a dashed reference line of slope $-1/4$.  Off-critical, the curves bend: below $T_c$ they level out at a plateau equal to $m^2$ (long-range order); above $T_c$ they fall off the bottom of the chart (exponential decay to zero).  At the critical temperature both curves hug the dashed line: a true power law.  An exponential moving average smooths the per-frame Wolff noise.
- The accumulating **$\xi(T)$ trace**.  Sweep the slider back and forth and you fill in the curve $\xi(T) \sim |T - T_c|^{-\nu}$ with $\nu = 1$.  The two colours come from the two panels; they are mirror images about $T_c$.
- The **phase strip** below the slider shows the ordered phase (cyan tint) and the disordered phase (amber tint), with a red tick at $T_c$.  A filled dot tracks $T$; an open dot tracks $T^\ast$.  They swap sides as you cross $T_c$.

The view toggle changes what is drawn on each lattice:

- **spins** — each pixel is one spin, light for $+1$, dark for $-1$.
- **walls** — the dual lattice picture: a red segment is drawn on every edge of the dual lattice whose two adjacent spins disagree.  These are *domain walls*, and they are the elementary excitations of the low-temperature phase.
- **both** — spins faded, walls overlaid.

## Why $T_c$ is self-dual

The cleanest derivation of $T_c$ in the 2D Ising model uses no simulation at all.  It works as follows.

The partition function $Z(\beta) = \sum_{\{s\}} e^{\beta \sum_{\langle ij \rangle} s_i s_j}$ can be expanded in two equivalent ways:

- A **low-temperature expansion** around the all-aligned ground state: the leading correction is a single flipped spin, then a flipped pair, then a flipped domain.  Every excitation is a closed loop of domain walls drawn on the *dual* lattice, weighted by $e^{-2\beta \cdot (\text{length})}$.

- A **high-temperature expansion** around $\beta = 0$: write $e^{\beta s_i s_j} = \cosh\beta + s_i s_j \sinh\beta$, expand the product, and observe that the spin sum kills every term except those whose chosen bonds form closed loops on the *original* lattice, weighted by $(\tanh\beta)^{\text{length}}$.

Both series count the same thing — closed loops — on lattices that are equivalent (the square lattice is self-dual).  Matching their per-edge weights gives the Kramers-Wannier relation

$$e^{-2\beta} \;=\; \tanh(\beta^\ast), \quad \text{equivalently} \quad \sinh(2\beta) \sinh(2\beta^\ast) = 1.$$

This relates $Z(\beta)$ and $Z(\beta^\ast)$ up to a non-singular factor.  If $Z$ has a singularity at some $\beta_c$, it must also have one at $\beta_c^\ast$ — and assuming there is exactly one phase transition, the *only* possibility is that $\beta_c$ is its own dual:

$$\sinh(2\beta_c)^2 = 1 \;\;\Rightarrow\;\; \beta_c = \tfrac{1}{2}\ln(1 + \sqrt{2}), \quad T_c \approx 2.269.$$

Please clap.  Duality has located the critical point without any computation of the free energy.

In the widget, this is the statement that pushing the slider to the unique value where the two panels look statistically identical lands you on $T_c$.

## The power law

At $T_c$ the connected correlator is no longer exponential.  Onsager's solution gives

$$C(r) - \langle s \rangle^2 \sim r^{-\eta}, \quad \eta = \tfrac{1}{4}.$$

The dashed line on the $C(r)$ plot is exactly $r^{-1/4}$.  Watch both curves drop onto it as you slide toward $T_c$ and bend off it as you slide away.  Conformal field theory (the $c = 1/2$ free fermion) recovers this exponent and many more; reading $\eta = 1/4$ off the plot is the experimental side of that mathematics.

## The correlation length and its divergence

Away from $T_c$ the connected correlator decays exponentially, $C(r) - \langle s \rangle^2 \sim e^{-r/\xi(T)}$, and the widget estimates $\xi$ by subtracting the long-$r$ plateau and fitting the log of the residual.  As $T \to T_c$,

$$\xi(T) \sim |T - T_c|^{-\nu}, \quad \nu = 1.$$

Sweep the slider slowly back and forth; the scatter you build up is $\xi(T)$.  Two things to notice:

1. The cyan branch ($T$) and the amber branch ($T^\ast$) are mirror images about $T_c$.  That is duality at the level of observables.
2. The peak saturates at $\xi \approx L/2 = 48$, because no correlation length larger than the box can be resolved on a finite lattice.  In an infinite system the peak would actually diverge.

This finite-size cutoff is also why $C(r)$ on the log-log plot never quite extends to large $r$ at $T_c$: the lattice runs out.

## What is going on under the hood

- Both lattices run **Wolff cluster updates** by default (one cluster flip per sweep).  Single-spin Metropolis dynamics is available as a toggle — try it at $T = T_c$ and watch how much slower equilibration is.  This is *critical slowing down*: the relaxation time itself diverges, and any local-update Monte Carlo scheme gets choked by it.  Wolff updates non-locally to dodge the issue.
- The displayed correlator is the unconnected $\langle s_0 s_r \rangle$, not the connected one.  A single-snapshot connected estimator would have to subtract the *instantaneous* $\langle s \rangle$, which fluctuates wildly under Wolff dynamics on a finite lattice and corrupts the curve.  Showing the unconnected version makes the plateau at $\langle s \rangle^2$ visible as the actual signature of long-range order, instead of hiding it.
- Lattice size $L = 96$ is a compromise.  Smaller lattices let finite-size effects swamp criticality; larger ones grind in pure JS.  At $L = 96$ you can clearly see the $\eta = 1/4$ regime persist over about a decade in $r$.

## Keyboard

- `space` — pause/resume.
- `r` — reset (re-randomise both lattices, clear the $\xi$ trace).
- `[` and `]` — nudge $T$ down/up by $0.05$.

## Where to push next

Try $T$ slightly below $T_c$.  Click "walls".  Each red loop is a domain wall enclosing a flipped region; in the low-temperature expansion these are the elementary excitations.  Now look at the right panel (high-$T$): the *same* picture of "loops on a lattice" appears, but now it is the bonds-of-the-high-$T$-expansion picture, not the domain-wall picture.  Same combinatorics, dual lattice.

Try $T$ exactly at $T_c$.  The cluster sizes you can see by eye span every scale from a single pixel to the whole box.  That is what scale invariance looks like in a snapshot.

Push the slider to its limits.  Notice that the dual lattice becomes either trivially ordered or trivially disordered.

---

*Built with Claude.*
