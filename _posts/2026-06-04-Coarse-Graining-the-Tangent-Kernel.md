---
title: "[Notes] Coarse-Graining the Tangent Kernel: PCCA+ and Renormalization for Interp"
date: 2026-06-04
math: true
---

*Notes, not a result - a direction I am sketching out loud so collaborators can see the shape of it and tell me where it breaks.  I had Claude draft these from a conversation; treat the PCCA+ specifics as "verify before you cite," and read the whole thing as thinking-out-loud rather than claims.  Anything experimental here is a toy.*

This builds on my earlier post [Coalitions, Canonical Kernels, and Gradient-Shapley]({{ site.baseurl }}/Coalitions-Canonical-Kernels-and-Gradient-Shapley/).  The "coalitions" there are exactly the macrostates I want to extract here.  The one-line version of this post: I think there is a real, usable correspondence between **metastable-state coarse-graining of Markov chains (PCCA+)** and **renormalization**, and that the right object to point it at for interpretability is the network's **tangent kernel**.

---

## 1.  The motivating analogy

Interpretability is, at bottom, a search for the right **macro-variables** of a trained network.  We have millions of micro-variables (individual weights, individual neuron activations on individual inputs) and we believe there is a much smaller set of collective objects - circuits, features, computational subroutines - that actually carry the explanation.  The hard part is not *describing* a candidate macro-variable, it is *deriving* the right ones in a principled way instead of pattern-matching by eye.

Physics has one mature paradigm for exactly this move: the **renormalization group**.  RG is the systematic procedure for integrating out fine-grained degrees of freedom to get an effective theory at a coarser scale, keeping the *relevant* (slow, long-wavelength, low-energy) modes and discarding the *irrelevant* (fast, short-wavelength) ones.  Its whole power comes from one structural fact: **a separation of scales lets you truncate**.

The claim I want to take seriously is that we already have, sitting in the Markov-state-model literature, a fully worked-out, numerically robust version of this move for a setting that looks a lot like ours.  It is called **PCCA+**, and it coarse-grains a Markov chain by exploiting a *spectral* gap in exactly the way RG exploits a *scale* gap.  If we can pose "find the macro-variables of a network" as "find the metastable sets of a Markov chain built from the network," we inherit that machinery wholesale.

---

## 2.  The tangent kernel as a coupling operator

The object I want to coarse-grain is the **empirical neural tangent kernel (eNTK)**.  For a network $f(x;\theta)$ with Jacobian $J_{ic,p} = \partial f_c(x_i)/\partial\theta_p$, the eNTK comes in two dual blocks:

- **Data-space:** $\Theta = J J^\top$, an $N \times N$ Gram matrix over data points.  $\Theta_{ij} = \langle \nabla_\theta f(x_i),\, \nabla_\theta f(x_j)\rangle$ measures how much two inputs share gradient direction - how strongly training on one moves the other.
- **Parameter-space:** $G = J^\top J$, a $P \times P$ Gram matrix over parameters.  $G_{pq}$ measures how much two parameters co-respond across the dataset.

Both are symmetric PSD **coupling operators**.  That is the key word.  A coupling matrix is the input every coarse-graining method wants: it says who is tied to whom.  In RG the coupling is the interaction term in the Hamiltonian; here it is the gradient inner product.  The reason the eNTK (rather than, say, raw weight correlations) is the natural choice is that it is the canonical kernel from the coalitions/Gradient-Shapley story - it is the bilinear form in which "moving along this direction in parameter space" and "this input responding" are the *same* pairing.  Coarse-graining it is coarse-graining the network's first-order response structure.

(The trace identity $\operatorname{tr}(J^\top J) = \operatorname{tr}(J J^\top)$ is a nice sanity check throughout: the two blocks are different reshapings of the same energy.)

---

## 3.  From a kernel to a Markov chain

PCCA+ wants a **stochastic operator**, not a static Gram matrix, so we need one bridging step.  This is the standard diffusion-maps construction (Coifman-Lafon), and it is worth spelling out because the choices in it are where the modeling assumptions hide.

Start from a symmetric affinity $K \ge 0$ (the kernel, or a magnitude-normalized $|\cos|$ version of it to strip out per-unit scale heterogeneity).  Density-normalize with exponent $\alpha$, then row-normalize:

$$ q_i = \sum_j K_{ij}, \qquad K^{(\alpha)}_{ij} = \frac{K_{ij}}{q_i^{\alpha} q_j^{\alpha}}, \qquad M = D^{-1} K^{(\alpha)}, \quad D = \operatorname{diag}\!\Big(\sum_j K^{(\alpha)}_{ij}\Big). $$

$M$ is row-stochastic - a random walk on the micro-units - and for $\alpha = 1$ it approximates the Laplace-Beltrami diffusion, factoring out the sampling density so the geometry rather than the density drives the dynamics.  $M$ is similar to a symmetric matrix, so it has a real spectrum $1 = \lambda_0 \ge \lambda_1 \ge \dots$, a unique stationary distribution $\pi$, and (by construction) detailed balance.

The interpretation: **a random walker that prefers to step between strongly-coupled units**.  Tightly-coupled groups become traps the walker rarely leaves.  Those traps are the macrostates.  This is the move that turns "coupling structure" into "timescale structure," which is what makes the spectral gap meaningful.

---

## 4.  PCCA+ in detail

This is the part I actually want to communicate, because the geometry is more constrained than "spectral clustering, but soft" suggests.

### 4.1  Metastability and the Perron cluster

Suppose the walk has $m$ *metastable* sets: groups of micro-units between which transitions are rare and within which equilibration is fast.  In the idealized limit where the sets are perfectly decoupled, $M$ is block-diagonal with $m$ blocks, each block an irreducible stochastic matrix.  Each block contributes an eigenvalue exactly equal to $1$, so $\lambda = 1$ has multiplicity $m$.

Turn the coupling between blocks back on as a small perturbation.  Perron-Frobenius theory tells you what happens to that degenerate cluster: it splits into **one** eigenvalue pinned exactly at $1$ (the global stationary mode) and $m-1$ eigenvalues sitting *just below* $1$, separated by a **gap** from the rest of the spectrum.  This tight group near $1$ is the **Perron cluster**, and

$$ \#\{\text{eigenvalues before the gap}\} \;=\; \#\{\text{metastable sets}\}. $$

So the *number* of macrostates is read off the spectrum, not chosen by hand.  The implied timescales $t_k = -1/\ln \lambda_k$ make this concrete: eigenvalues near $1$ are slow processes (rare inter-set transitions), eigenvalues past the gap are fast intra-set relaxation that we are about to integrate out.

### 4.2  The eigenvectors are nearly piecewise-constant

Here is the fact the whole method rests on.  In the decoupled limit, the $m$ dominant right eigenvectors are **piecewise constant** - constant on each metastable set.  (For a block-diagonal stochastic $M$ the $\lambda=1$ right eigenspace is spanned by the block indicator vectors - all-ones on a block, zero off it - so any basis of that space is constant within blocks.)  Under weak coupling they stay *approximately* piecewise constant.

Now do the thing that makes it geometric.  Stack the first $m$ eigenvectors as columns, $X = [\xi_0, \xi_1, \dots, \xi_{m-1}] \in \mathbb{R}^{n \times m}$ with $\xi_0 = \mathbf{1}$ the constant mode.  Read $X$ **by rows**: each micro-unit $i$ becomes a point $X_{i,:} \in \mathbb{R}^m$.  Because the eigenvectors are piecewise constant, all micro-units in the same metastable set map to (nearly) the *same* point.  In the ideal limit there are exactly $m$ distinct points, and - this is the rigid part - they sit at the **vertices of a simplex**.  Weak coupling smears each vertex into a small cloud, but the overall point set still fills out an $m$-vertex simplex $\sigma$, with the "purest" representatives of each macrostate sitting at the corners and the ambiguous, between-states units sitting in the interior.

### 4.3  Membership functions as convex coordinates

Original PCCA used the *sign structure* of the eigenvectors to assign units to states.  That is brittle: near the simplex faces the signs flip on noise.  **PCCA+** (Deuflhard & Weber) replaces it with the natural thing the simplex picture is begging for.  Find the $m$ vertices, then write every micro-unit as a **convex combination** of them.  Concretely, solve for a linear map $A \in \mathbb{R}^{m \times m}$ such that

$$ \chi = X A, \qquad \chi_i(k) \ge 0, \qquad \sum_{k=1}^{m} \chi_i(k) = 1. $$

The $\chi_i(k)$ are the convex coordinates of unit $i$ inside the simplex, and they are exactly the **membership functions**: $\chi_i(k)$ is the (soft) degree to which unit $i$ belongs to macrostate $k$.  Partition-of-unity is automatic because $\xi_0 = \mathbf{1}$ is one of the columns, so the row sums of $XA$ can be pinned to $1$.  The corners get membership $\approx 1$ in one state; interior units get fractional, honestly-fuzzy memberships.  In the decoupled limit the $\chi$ become exact indicator functions of the metastable sets - the soft assignment hardens into a true partition precisely when the scale separation becomes clean.

The vertices are found by an *inner simplex* algorithm: pick the micro-unit farthest from the origin as the first vertex, then iteratively pick the unit maximizing the volume of the simplex spanned so far.  Optionally one then optimizes $A$ to sharpen the memberships (maximize "crispness" / metastability) subject to the feasibility constraints.  The upshot is a method with very little to tune: you get $m$ from the gap and $\chi$ from a near-deterministic geometric construction.

### 4.4  The effective coarse operator

Memberships in hand, the coarse $m \times m$ dynamics is a Galerkin projection of $M$ onto the membership basis, in the $\pi$-weighted inner product $D_\pi = \operatorname{diag}(\pi)$:

$$ M_c = \big(\chi^\top D_\pi\, \chi\big)^{-1} \chi^\top D_\pi\, M\, \chi. $$

This is the **renormalized operator**: the effective Markov chain on macrostates.  It is the dynamical analogue of an effective Hamiltonian.  And nothing stops you from iterating - coarse-grain, get $M_c$, coarse-grain *that* - which is where the renormalization reading stops being an analogy and starts being a procedure.

---

## 5.  The renormalization dictionary

Lining the two up explicitly, because the correspondence is tighter than "both are coarse-graining":

| Renormalization group | PCCA+ / transfer-operator coarse-graining |
|---|---|
| Separation of scales (energy / length) | Spectral gap (timescale separation) |
| Relevant, slow, long-wavelength modes | Dominant eigenvectors near $\lambda = 1$ (Perron cluster) |
| Irrelevant fast modes, integrated out | Sub-gap eigenvectors, discarded |
| Block-spin / decimation map | Membership projection $\chi$ (lump micro $\to$ macro) |
| Effective Hamiltonian $H'$ | Coarse generator $M_c$ (Galerkin projection) |
| Iterating the RG step | Recursive coarse-graining / hierarchy of macrostates |
| Fixed point, universality | *(open - no clean analogue yet, see below)* |

The cleanest precise instance of the correspondence is the **transfer-matrix RG** of 1D statistical mechanics (and its DMRG descendant): there the transfer matrix's leading eigenvalues set the correlation length, and the RG step keeps the dominant invariant subspace.  An MSM transfer operator is the dynamical sibling of that transfer matrix, and PCCA+ is "keep the dominant invariant subspace, but with a *fuzzy, convex* block-spin assignment instead of a hard one."  That fuzziness is not a hack; it is what lets the coarse states overlap at their boundaries, which is exactly where real interpretability boundaries are soft (a parameter that participates in two circuits).

There is also a known, separate RG-deep-learning correspondence (Mehta & Schwab's mapping between variational RG and RBMs) - worth flagging so we do not reinvent it, but it renormalizes over *depth/layers*, which is a different flow than the one here.

---

## 6.  Three flows

A subtlety worth being explicit about: "renormalization for a network" is ambiguous because there are at least **three** candidate directions to flow along, and they are not the same.

1. **Scale flow** - coarse-grain the coupling operator itself, $M \to M_c \to M_{cc}$, building a hierarchy of macrostates at a fixed checkpoint.
2. **Depth flow** - coarse-grain layer by layer, treating depth as RG "time" (the Mehta-Schwab direction).
3. **Training flow** - watch the macrostructure evolve over SGD steps.  Does the coarse operator flow toward something stable as training converges?  An "RG flow in training time" would be the most striking version if it exists.

The first is the one I would build a toy explorer around first: take one checkpoint, build the eNTK, coarse-grain it, look at the macrostates.  A recursive Fiedler bipartition (a hard, 2-way normalized cut at each level) is the crude hierarchical cousin of PCCA+; moving to PCCA+ proper is the natural step because it (a) chooses $m$ from the gap rather than forcing balanced binary splits, and (b) gives *soft* memberships, which I expect to matter at the boundaries.

The payoff you would want out of this is a **dual readout**: every macrostate viewable both on the architecture (which weights it is made of) and over the data (a membership-weighted mean input - "the average thing this state is about").  That is the picture I keep wanting and cannot get from thresholded-attention by eye.

---

## 7.  Open questions I would want your read on

- **Is the eNTK the right operator?**  It is a *static* coupling, so turning it into a Markov chain via diffusion is a modeling choice, not a given dynamics.  Should the operator instead be something with intrinsic dynamics (the SGD transition kernel, the layer-to-layer forward map)?  The eNTK is the most *canonical* static choice, but canonical is not the same as correct-for-this-purpose.
- **Where does the modular structure live?**  My guess is that the natural coalitions live more in function/data space than in raw weight space - that the data-space block $JJ^\top$ has cleaner scale separation than the parameter-space $J^\top J$, which may be too much of a hairball to coarse-grain without first whitening (Fisher / Hessian normalization).  Worth checking directly, and cheap to.
- **What is the fixed point?**  The RG analogy is missing its punchline.  RG's payoff is universality at fixed points.  Is there any analogue here - a coarse operator that is invariant under further coarse-graining, or a macrostructure shared across architectures trained on the same task?  Without something like this it is "coarse-graining inspired by RG," not RG.
- **Does the structure flow over training?**  Flow (3) above.  If the data-space macrostates sharpen monotonically from init to convergence, that is a clean story about the network *acquiring* its coarse structure.
- **Reversibility.**  PCCA+ assumes a reversible chain (detailed balance), which the diffusion construction gives us by symmetry.  But the moment we reach for a genuinely directional operator (SGD, forward passes) reversibility breaks, and we would need the Schur / GenPCCA generalizations.  Worth knowing where that wall is before we hit it.

If even the weak version of this works - principled, spectral, multiscale macrostates with a soft membership structure and a dual data/parameter readout - I think it is a more honest "circuit discovery" than thresholded-attention pattern-matching, because the scale at which you cut is *selected by a gap in the operator*, not by us.  That is the part I find worth chasing.
