---
title: "Coarse-Graining the Tangent Kernel: PCCA+, Renormalization, and Scale-Aware Macrostates"
tags: [notes, ai]
date: 2026-06-04
math: true
---

The setup, in one line:

> I have a set of **natural kernels** sitting on a trained network, and I want **scale-sensitive interpretability** of the kind the [scale-aware interpretability agenda](https://arxiv.org/abs/2602.05184) (Principles of Intelligence) asks for. **Diffusion maps + PCCA+** turn those kernels into a soft, scale-selected set of **macrostates**, with the scale of the cut chosen by a *gap in the operator* rather than by hand.

This builds on [Coalitions, Canonical Kernels, and Gradient-Shapley](https://charlesr-w.github.io/crw-blog/Coalitions-Canonical-Kernels-and-Gradient-Shapley/) - the "coalitions" there are the macrostates extracted here - which in turn builds on [Selection on the GP Map and Feature Learning](https://charlesr-w.github.io/crw-blog/Selection-on-the-GP-Map-and-Feature-Learning/). Notation is inherited: $\theta\in\mathbb R^P$ parameters, $z=f(\theta)\in\mathbb R^O$ output, $J=\partial z/\partial\theta$ the Jacobian, $\Theta$ the eNTK.

The fork worth flagging is in §6: there are **two orthogonal axes** of coarse-graining - by *similarity* (the diffusion-map route) and by *computation* (a kernelized causal-state / $\upsilon$-machine route) - and PCCA+ is the same engine for both.

---


## §1. The target: macro-variables whose scale is *derived*, not eyeballed

Interpretability is, at bottom, a search for the right **macro-variables** of a trained network. We have millions of micro-variables - individual weights, individual activations on individual inputs - and we believe a much smaller set of collective objects (circuits, features, subroutines) carries the explanation. The hard part is not *describing* a candidate macro-variable; it is *deriving* the right ones, at the right scale, in a principled way instead of pattern-matching by eye.

This is precisely the gap the **scale-aware interpretability** agenda names. That agenda asks interpretability methods to (i) find the *natural scales* at which a network organizes information, (ii) extract a *scale-dependent* notion of which degrees of freedom are relevant, and (iii) come with a *separation-of-scales* diagnostic telling you when fine-grained fluctuations can be safely ignored. It points at renormalization as the framework and - relevant here - explicitly lists eigenmodes of the activation/NTK correlation structure as a *candidate scale object*.

This post is a concrete proposal for that slot. The pipeline is: take a natural kernel on the network → turn it into a random walk → coarse-grain the walk with PCCA+. The payoff I want is exactly the agenda's three desiderata, made operational:

- **natural scale** = the timescale set by the dominant eigenvalues of the walk;
- **relevance** = membership in the slow (Perron-cluster) subspace;
- **separation of scales** = the spectral gap itself. When the gap is clean, the coarse description is trustworthy; when it is not, the method tells you so by *not* having a gap.

The physics paradigm for this move is the **renormalization group** (RG): systematically integrate out fast, short-wavelength, irrelevant modes to get an effective theory in the slow, relevant ones. RG's whole power is one structural fact - *a separation of scales lets you truncate.* My claim is that the Markov-state-model literature already contains a numerically robust, off-the-shelf version of this move, and it is called **PCCA+**. If we can pose "find the macro-variables of a network" as "find the metastable sets of a Markov chain built from the network," we inherit that machinery wholesale.

---


## §2. The natural kernels

The object I want to coarse-grain is the **empirical neural tangent kernel** (eNTK). For $f(x;\theta)$ with Jacobian $J_{ic,p}=\partial f_c(x_i)/\partial\theta_p$ (datapoint $i$, output channel $c$, parameter $p$), the eNTK comes in two dual blocks:

- **Data-space:** $\Theta = JJ^\top$, an $N\times N$ Gram matrix over data points (channels summed). $\Theta_{ij}=\langle\nabla_\theta f(x_i),\nabla_\theta f(x_j)\rangle$ measures how strongly training on $x_i$ moves the network's output on $x_j$.
- **Parameter-space:** $G = J^\top J$, a $P\times P$ Gram matrix over parameters. $G_{pq}$ measures how strongly two parameters co-respond across the dataset.

Both are symmetric PSD **coupling operators** - and "coupling operator" is the key phrase. A coupling matrix is the input every coarse-graining method wants: it states who is tied to whom. In RG the coupling is the interaction term in the Hamiltonian; here it is the gradient inner product. The reason the eNTK rather than, say, raw weight correlations is the natural choice is that it is the *canonical* kernel from the coalitions / Gradient-Shapley story - the bilinear form in which "move along this parameter direction" and "this input responds" are the same pairing. Coarse-graining it is coarse-graining the network's first-order response structure.

Two bookkeeping facts I will lean on later.

**Shared nonzero spectrum.** $JJ^\top$ and $J^\top J$ have *identical nonzero eigenvalues* (and $\operatorname{tr}(JJ^\top)=\operatorname{tr}(J^\top J)$ is the trace sanity check). So *before any normalization*, the data-space and parameter-space blocks have the **same gap structure** - the same candidate count $m$ of macrostates. What differs between the two spaces is the *eigenvectors*, and therefore the geometry the clustering actually sees. This sharpens the data-vs-parameter question in §9: it is not "which space has the gap" (same gap), it is "which space has cleaner *eigenvectors*."

**Singular-value duality gives a free dual readout.** Write $J=\sum_k s_k\,u_k v_k^\top$. The $u_k$ are output/data modes; the $v_k$ are parameter modes. A macrostate built from a set of singular directions automatically has *both* a data-face (a span of $u_k$'s - "the inputs this state is about") and a parameter-face (a span of $v_k$'s - "the weights this state is made of"). That is the dual readout I keep wanting and cannot get from thresholded-attention by eye, and it falls out of the SVD for free - provided we coarse-grain in a way that respects the singular structure.

**Layerwise forward/backward split.** The eNTK is additive over layers and each block factorizes through the layer-$\ell$ representation $h^\ell$ (carried over from the GP-map post §7):
$$
\nabla_{\theta^\ell}z = B^\ell F^\ell,\qquad
\Theta^\ell = B^\ell\,\mathcal F^\ell\,B^{\ell\top},\qquad
\Theta = \sum_\ell \Theta^\ell,
$$
with the **forward** kernel $F^\ell=\partial h^\ell/\partial\theta^\ell$ (parameters $\to$ representation) and the **backward** kernel $B^\ell=\partial z/\partial h^\ell$ (representation $\to$ output). The induced datapoint kernels are $\mathcal F^\ell(x,x')=F^\ell(x)F^\ell(x')^\top$ (a *representation-similarity* Gram) and $\mathcal B^\ell(x,x')=B^\ell(x)B^\ell(x')^\top$ (a *sensitivity* kernel). So "the kernel" is not one object: I can coarse-grain the full $\Theta$, the per-layer $\Theta^\ell$, the forward $\mathcal F^\ell$, or the backward $\mathcal B^\ell$, and they mean different things (§8).

---


## §3. From a kernel to a Markov chain

PCCA+ wants a **stochastic operator**, not a static Gram matrix, so we need one bridging step: the standard diffusion-maps construction (Coifman and Lafon). It is worth spelling out because the choices in it are where the modeling assumptions hide.

Start from a symmetric affinity $K\ge 0$ - the kernel itself, or a magnitude-normalized $|\cos|$ version $K_{ij}/\sqrt{K_{ii}K_{jj}}$ that strips out per-unit scale heterogeneity so that "alignment" rather than "magnitude" drives the walk. Density-normalize with exponent $\alpha$, then row-normalize:
$$
q_i = \sum_j K_{ij},\qquad
K^{(\alpha)}_{ij} = \frac{K_{ij}}{q_i^{\alpha}\,q_j^{\alpha}},\qquad
M = D^{-1}K^{(\alpha)},\quad
D = \operatorname{diag}\!\Big(\textstyle\sum_j K^{(\alpha)}_{ij}\Big).
$$
$M$ is row-stochastic - a random walk on the micro-units. For $\alpha=1$ it approximates the Laplace-Beltrami diffusion, factoring out the sampling density so that the *geometry*, not the density, drives the dynamics. Because $M=D^{-1}K^{(\alpha)}$ is similar to the symmetric $D^{-1/2}K^{(\alpha)}D^{-1/2}$, it has a real spectrum $1=\lambda_0\ge\lambda_1\ge\cdots$, a unique stationary distribution $\pi$, and detailed balance by construction.

The interpretation is what makes the next step meaningful: **a walker that prefers to step between strongly-coupled units.** Tightly-coupled groups become traps the walker rarely leaves; those traps are the macrostates. This is the move that converts *coupling structure* into *timescale structure*, via $t_k=-1/\ln\lambda_k$: eigenvalues near $1$ are slow processes (rare inter-trap transitions), and a gap in the spectrum is a gap in timescales. That is what turns "the eNTK has block structure" into "the network has a separation of scales."

One honest caveat for §9: the density/row normalization is *not* the same operation in data-space and parameter-space, so the exact shared-nonzero-spectrum fact of §2 holds for the raw Gram blocks but is *perturbed* once we pass to the stochastic $M$. The leading gap is largely inherited; the fine structure is not.

---


## §4. PCCA+ in detail

The geometry here is more constrained than "soft spectral clustering" suggests, so it is worth doing in the physicist's way rather than asserting the result.

### 4.1 Metastability and the Perron cluster

Suppose the walk has $m$ *metastable* sets: groups between which transitions are rare and within which equilibration is fast. In the idealized decoupled limit, $M$ is block-diagonal with $m$ irreducible stochastic blocks. Each block, being stochastic and irreducible, has Perron eigenvalue exactly $1$ with a one-dimensional eigenspace; so the full $M$ has $\lambda=1$ with multiplicity exactly $m$.

Now turn the inter-block coupling back on as a small perturbation $\varepsilon$. Perron-Frobenius theory says what happens to that degenerate cluster: it splits into **one** eigenvalue pinned at $1$ (the global stationary mode) and $m-1$ eigenvalues pushed *just below* $1$, separated by a **gap** from the rest of the spectrum. This tight group near $1$ is the **Perron cluster**, and
$$
\#\{\text{eigenvalues before the gap}\}\;=\;\#\{\text{metastable sets}\}=m.
$$
So the *number* of macrostates is read off the spectrum, not chosen by hand. Eigenvalues past the gap are fast intra-set relaxation - the modes we are about to integrate out.

### 4.2 The dominant eigenvectors are nearly piecewise-constant

Here is the fact the method rests on. For block-diagonal stochastic $M$, the $\lambda=1$ right-eigenspace is spanned by the **block indicator vectors** (all-ones on a block, zero off it). Any basis of that eigenspace is therefore *constant within blocks*, i.e. piecewise constant. Under weak coupling the $m$ dominant eigenvectors stay *approximately* piecewise constant.

Now make it geometric. Stack the first $m$ right eigenvectors as columns, $X=[\xi_0,\xi_1,\dots,\xi_{m-1}]\in\mathbb R^{n\times m}$ with $\xi_0=\mathbf 1$ the constant mode, and read $X$ **by rows**: each micro-unit $i$ becomes a point $X_{i,:}\in\mathbb R^m$. Because the eigenvectors are piecewise constant, all units in the same metastable set map to (nearly) the *same* point. In the ideal limit there are exactly $m$ distinct points, and - the rigid part - they sit at the **vertices of a simplex** $\sigma$. Weak coupling smears each vertex into a small cloud; the "purest" representatives of each macrostate sit near the corners, the ambiguous between-states units in the interior.

### 4.3 Membership functions as convex coordinates

The original PCCA used the *sign structure* of eigenvectors to assign states - brittle, because near the simplex faces signs flip on noise. **PCCA+** (Deuflhard and Weber) replaces this with the natural thing the simplex picture begs for: find the $m$ vertices, then write every micro-unit as a **convex combination** of them. Solve for a linear map $A\in\mathbb R^{m\times m}$ with
$$
\chi = XA,\qquad \chi_i(k)\ge 0,\qquad \sum_{k=1}^m \chi_i(k)=1.
$$
The $\chi_i(k)$ are the convex coordinates of unit $i$ inside the simplex - exactly the **membership functions**: the soft degree to which unit $i$ belongs to macrostate $k$. Partition-of-unity is automatic because $\xi_0=\mathbf 1$ is a column, so the row sums of $XA$ can be pinned to $1$. Corners get membership $\approx 1$ in one state; interior units get honestly fractional memberships. In the decoupled limit the $\chi$ harden into exact indicator functions - the soft assignment becomes a true partition *precisely when* the scale separation becomes clean.

Vertices are found by an *inner-simplex* construction: take the unit farthest from the origin as the first vertex, then iteratively pick the unit maximizing the volume of the simplex spanned so far. Optionally one then optimizes $A$ to sharpen crispness/metastability subject to feasibility. The upshot is a method with very little to tune: $m$ comes from the gap and $\chi$ from a near-deterministic geometric construction.

### 4.4 The effective coarse operator

With memberships in hand, the coarse $m\times m$ dynamics is a Galerkin projection of $M$ onto the membership basis, in the $\pi$-weighted inner product $D_\pi=\operatorname{diag}(\pi)$:
$$
M_c=\big(\chi^\top D_\pi\,\chi\big)^{-1}\,\chi^\top D_\pi\,M\,\chi.
$$
This is the **renormalized operator**: the effective Markov chain on macrostates, the dynamical analogue of an effective Hamiltonian. And nothing stops you iterating - coarse-grain, get $M_c$, coarse-grain *that* - which is where the renormalization reading stops being an analogy and becomes a procedure.

---


## §5. The renormalization dictionary

Lining the two up, because the correspondence is tighter than "both coarse-grain":

| Renormalization group                   | PCCA+ / transfer-operator coarse-graining                 |
| ---------------------------------------- | --------------------------------------------------------- |
| Separation of scales (energy / length)   | Spectral gap (timescale separation)                       |
| Relevant, slow, long-wavelength modes     | Dominant eigenvectors near $\lambda=1$ (Perron cluster)   |
| Irrelevant fast modes, integrated out     | Sub-gap eigenvectors, discarded                           |
| Block-spin / decimation map               | Membership projection $\chi$ (lump micro $\to$ macro)     |
| Effective Hamiltonian $H'$                | Coarse generator $M_c$ (Galerkin projection)              |
| Iterating the RG step                     | Recursive coarse-graining / hierarchy of macrostates      |
| Fixed point, universality                 | *(open - no clean analogue yet, see §9)*                  |

The cleanest *precise* instance is the **transfer-matrix RG** of 1D statistical mechanics, and its DMRG descendant (White): the transfer matrix's leading eigenvalues set the correlation length, and the RG step keeps the dominant invariant subspace. An MSM transfer operator is the dynamical sibling of that transfer matrix, and PCCA+ is "keep the dominant invariant subspace, but with a *fuzzy, convex* block-spin assignment instead of a hard one." That fuzziness is not a hack: it is what lets coarse states overlap at their boundaries, which is exactly where real interpretability boundaries are soft (a parameter that participates in two circuits).

There is a separate, well-known RG/deep-learning correspondence (Mehta and Schwab's variational-RG-RBM mapping) - worth flagging so we do not reinvent it, but it flows over *depth/layers*, which is a different direction from the one here (§7).

---


## §6. Two axes of coarse-graining: similarity vs computation

This is a genuine fork, and the literature already has both prongs.

Everything in §3-§5 coarse-grains by **similarity**: the eNTK says which units are *coupled*, the diffusion map turns coupling into a reversible walk, and PCCA+ lumps units that the walker treats as one trap. The equivalence being quotiented is "you and I are gradient-aligned." Call this **Axis A**.

But there is a second, orthogonal thing one could mean by "coarse-grain the network," and it is the one I keep circling in the IO-contract / shielding notes: coarse-grain by **computation** - group micro-states that are *predictively equivalent*, i.e. that induce the same distribution over the network's future behavior, regardless of whether they look similar. Call this **Axis B**. This is the move that computational mechanics formalizes.

**Computational mechanics, briefly.** For a process with past $x^{\leftarrow}$ and future $x^{\rightarrow}$, define the **causal equivalence** $x^{\leftarrow}_a\sim x^{\leftarrow}_b \iff P(x^{\rightarrow}\mid x^{\leftarrow}_a)=P(x^{\rightarrow}\mid x^{\leftarrow}_b)$. The equivalence classes are the **causal states** $\sigma$; the Markov chain on them is the **$\varepsilon$-machine**, the *minimal* sufficient statistic for prediction (Shalizi and Crutchfield). The thing to notice is that causal-state construction is *itself a lumping of a Markov chain* - it merges histories that are predictively indistinguishable. That is structurally the same operation PCCA+ performs, with "metastable" replaced by "predictively coherent."

**The kernelized version - the "$\upsilon$-machine" I want.** ("$\upsilon$-machine" is my shorthand for the continuous-state, kernelized causal-state machine; flag it as my coinage, see references.) The conditional future $P(x^{\rightarrow}\mid x^{\leftarrow})$ becomes a **mean embedding** $\mu(x^{\leftarrow})=\mathbb E[\phi(x^{\rightarrow})\mid x^{\leftarrow}]$ in the RKHS of a kernel $\phi$, and causal states become clusters of histories with equal (within the gap, *near*-equal) mean embeddings. This is not hypothetical: Brodu, and Crutchfield's RKHS $\varepsilon$-machines, already build causal states by RKHS embedding of conditional distributions. The natural choice of $\phi$ for our setting is the eNTK feature map - which is what makes this the *same* family of kernels as Axis A, pointed at a different equivalence.

**The bridge.** Build a *directional, predictive* transfer operator in eNTK feature space - the past-to-future map - and run PCCA+ on it. Its metastable lumping should approximate the causal-state lumping, but **soft and scale-selected by a gap** rather than exact and hand-thresholded. In other words: *PCCA+ on the right operator is spectral, fuzzy causal-state discovery.* And Brodu's **decisional states** - a coarser partition of the causal states induced by a higher-level criterion - are literally the PCCA+ move applied one level up, which is the recursive coarse-graining of §4.4 but now over the *computation*.

**Where the wall is.** A *predictive* operator is past$\to$future; it is generically **non-reversible**. So the moment we move from Axis A to Axis B, the detailed balance that the diffusion construction handed us for free is gone, and vanilla PCCA+ (which assumes a reversible chain) no longer applies. The fix is the **GenPCCA / G-PCCA** generalization (Reuter, Weber, Fackeldey, Röblitz), which replaces the real eigen-decomposition with a real **Schur** decomposition and so coarse-grains non-reversible and even cyclic operators. The reversibility wall flagged as a worry in the old notes is *exactly* the boundary between the similarity axis and the computational axis. Crossing it is the point of Axis B, and GenPCCA is the tool that crosses it.

The two axes are orthogonal to the "which direction do we flow" question of §7. You can do similarity-coarsening along the scale flow (the first toy below), or computational-coarsening along the depth flow (a kernelized $\upsilon$-machine, layer by layer), or any combination.

---


## §7. Three flows: which direction do we coarse-grain?

"Renormalization for a network" is ambiguous because there are at least **three** candidate directions to flow along, and they are not the same.

1. **Scale flow** - coarse-grain the coupling operator itself, $M\to M_c\to M_{cc}$, building a hierarchy of macrostates at a fixed checkpoint.
2. **Depth flow** - coarse-grain layer by layer, treating depth as RG "time" (the Mehta-Schwab direction).
3. **Training flow** - watch the macrostructure evolve over SGD steps; ask whether the coarse operator flows toward something stable as training converges. An "RG flow in training time" would be the most striking version if it exists.

The **scale flow with Axis A** is the one I would build a toy explorer around first: take one checkpoint, build the eNTK, diffusion-map it, PCCA+ it, look at the macrostates. A recursive Fiedler bipartition (a hard 2-way normalized cut at each level) is the crude hierarchical cousin; moving to PCCA+ proper is the natural step because it (a) chooses $m$ from the gap rather than forcing balanced binary splits, and (b) gives *soft* memberships, which I expect to matter at the boundaries. The **depth flow with Axis B** is the $\upsilon$-machine direction and the more ambitious one.

The payoff to aim for is the **dual readout** of §2: every macrostate viewable both on the architecture (which weights it is made of, via the $v_k$ face) and over the data (a membership-weighted mean input - "the average thing this state is about", via the $u_k$ face).

---


## §8. Context-conditional circuits: cluster the data, re-read the parameters there

Everything so far coarse-grains *one* parameter-space block. But that block is itself an average over data, and that turns out to matter. Writing the per-datapoint Jacobian $J(x_i)\in\mathbb R^{O\times P}$,
$$
G = J^\top J = \sum_i J(x_i)^\top J(x_i) = \sum_i G_i,\qquad
G_i := \sum_c \nabla_\theta f_c(x_i)\,\nabla_\theta f_c(x_i)^\top,
$$
so $G$ is a sum - an unnormalized $\mathbb E_x[G_x]$ - of per-datapoint parameter-coupling matrices. The circuits PCCA+ pulls out of $G$ are therefore *context-averaged*: marginalized over the entire input distribution.

I suspect that marginalization is exactly why the parameter block looks like a hairball (§2, §9). If a parameter sits in circuit A when the input is a 3 and in circuit B when the input is an 8, then in the pooled $G$ it is coupled to *both*, and those cross-links are the off-diagonal bridges that wash out the blocks. The marginal coupling is a *superposition* of several cleaner conditional couplings, and superposing them muddies the structure. The fix is to condition.

**The procedure.**

1. Cluster the data points with the data-space block $\Theta=JJ^\top$ - the face we already expect to cluster cleanly. Call the clusters $C_1,\dots,C_K$ and read them as *contexts*, or operating regimes of the network.
2. For each context, re-evaluate the parameter-space eNTK *restricted to that cluster*:
$$
G_{C_k}=\sum_{i\in C_k}G_i\quad\Big(\text{or }\tfrac1{|C_k|}\sum_{i\in C_k}G_i\Big),\qquad \sum_k G_{C_k}=G.
$$
This is the parameter coupling *as the subpopulation $C_k$ sees it* - a law-of-total-coupling decomposition of the global $G$.
3. Diffusion-map and PCCA+ each $G_{C_k}$ on its own, yielding *context-conditional* parameter macrostates.
4. Compare across contexts. Coalitions present in *every* $C_k$ are context-invariant machinery - something the network always runs; coalitions that appear under only one context are *context-dependent* circuits - computation the network deploys only in that regime.

**Why I think it is worth doing.**

- It is a *falsifiable* test of the hairball hypothesis: if $G$ is a context-mixture, each $G_{C_k}$ should be *more* modular than the pooled $G$ - cleaner gap, tighter simplex, crisper memberships. If conditioning sharpens nothing, the hairball is intrinsic and not an averaging artifact. Either answer is informative.
- It is a concrete handle on *context-dependent computation* / polysemanticity. A parameter that is monosemantic *within* a context but wears different hats *across* contexts shows up as a unit whose membership vector $\chi$ rotates from $C_k$ to $C_{k'}$. The thing that is illegible globally - because it is mixed - becomes legible once indexed by context.
- It uses both faces in the way §2 wanted: the *clean* data-space geometry supplies the index (the "where"), and the parameter block is read out conditionally on that index (the "what"). Neither face alone gives you context-dependent circuits; the product does.

**Caveats.**

- The contexts inherit a *scale choice* from the data clustering (the number $K$). So this nests a renormalization inside a renormalization: a data-space coarse-graining feeding a family of parameter-space ones. The honest version sweeps $K$ and watches conditional circuits split and merge as contexts refine - a joint (data-scale, parameter-scale) diagram rather than a single partition.
- $G_{C_k}$ is a conditional second moment, close kin to a *Fisher / Gauss-Newton matrix restricted to a data region*; that reading argues for the whitened metric of §9 *inside* each context rather than the raw Euclidean one.
- It is correlational. Shared $\chi$ across contexts says the *coupling* is shared, not that the *same computation* runs; pinning that down wants an intervention (ablate the macrostate, check that it only bites within its context).

This is still **Axis A** (§6) - similarity coarse-graining - with the similarity made *conditional*. The Axis B version conditions the *predictive* operator on the context instead, i.e. asks for context-dependent causal states: the same conditioning idea, on a harder operator.

---


## §9. Open questions

**Is the eNTK the right operator?** It is a *static* coupling, so turning it into a Markov chain by diffusion is a modeling choice, not an intrinsic dynamics. Axis B is the principled alternative: use an operator that *already* has dynamics (the layer-to-layer forward map, the SGD transition kernel, the predictive past$\to$future map). The eNTK is the most *canonical* static choice, but canonical is not the same as correct-for-this-purpose.

**Data-space vs parameter-space.** Recall §2: the two raw blocks share their nonzero spectrum, so they propose the *same* $m$ - the question is which space has cleaner *eigenvectors*, hence a tighter simplex and crisper memberships. My guess is that the modular structure is cleaner in function/data space ($JJ^\top$) than in the parameter hairball ($J^\top J$), which may need whitening by a Fisher/Hessian metric before it will coarse-grain - i.e. the *canonical/whitened* kernel $\Theta S$ from the Coalitions post §2 rather than the naive Euclidean one. The SVD duality says I may be posing a false dichotomy: a singular-subspace coarse-graining carries *both* faces, and the real choice is only which face's geometry to run the simplex-finding in. Cheap to check directly - and §8 turns it into a sharper experiment: condition $G$ on data clusters first, since the parameter hairball may be a context-mixture rather than a genuine lack of structure.

**Which kernel - plain eNTK, forward, or backward?** Coarse-graining $\mathcal F^\ell$ clusters by *representational similarity* ("which inputs the layer represents alike"); coarse-graining $\mathcal B^\ell$ clusters by *output sensitivity* ("which directions the output is steered by"); coarse-graining the full $\Theta^\ell$ mixes both and tracks *sequential computation* layer by layer. These are different macrostate notions and I do not yet know which is the right substrate - plausibly $\mathcal F$ for "features" and $\Theta^\ell$ for "circuits."

**The reversibility wall (now understood).** §6 reframes this from a worry into a signpost: Axis A is reversible (diffusion symmetry), Axis B is not (prediction is directional). GenPCCA / Schur is the crossing. Worth knowing exactly where the wall is before hitting it - and it is exactly at the boundary between similarity and computation.

**What is the fixed point?** The RG analogy is still missing its punchline. RG's payoff is universality at fixed points. Is there an analogue - a coarse operator invariant under further coarse-graining, or a macrostructure shared across architectures trained on the same task (a Platonic-representation flavor)? Without something like this it is "coarse-graining inspired by RG," not RG.

**Does the structure flow over training?** Flow (3). If the data-space macrostates sharpen monotonically from init to convergence - the gap opening as training proceeds - that is a clean story about the network *acquiring* its coarse structure, and it would connect directly to the "circuit depth increasing over training" object from the Coalitions post §3.

If even the weak version of this works - principled, spectral, multiscale macrostates with soft memberships and a dual data/parameter readout - I think it is a more honest "circuit discovery" than thresholded-attention pattern-matching, because *the scale at which you cut is selected by a gap in the operator, not by us.*

---


## References

**Confident / linked.**

- Scale-aware interpretability agenda - *Towards Worst-Case Guarantees with Scale-Aware Interpretability* (Principles of Intelligence; Teixeira, Vaintrob, Rosas, Stapleton, et al., 2026), [arXiv:2602.05184](https://arxiv.org/abs/2602.05184). Names the NTK spectrum as a candidate scale; this post is a concrete proposal for that slot.
- PCCA+ - Deuflhard and Weber, *Robust Perron Cluster Analysis in Conformation Dynamics*, Linear Algebra Appl. 398 (2005) 161-184. Background/explainer: [markovmodel docs, PCCA](http://docs.markovmodel.org/lecture_pcca.html). Original (sign-based) PCCA: Deuflhard, Huisinga, Fischer, Schütte, Linear Algebra Appl. 315 (2000) 39-59.
- GenPCCA / G-PCCA (non-reversible, Schur) - Reuter, Weber, Fackeldey, Röblitz, Garcia; software [pyGPCCA](https://github.com/msmdev/pyGPCCA). Complex-eigenvalue PCCA+ (equivalent to GPCCA): [arXiv:2206.14537](https://arxiv.org/abs/2206.14537).
- Computational mechanics / $\varepsilon$-machines - Shalizi and Crutchfield, *Computational Mechanics: Pattern and Prediction, Structure and Simplicity*, J. Stat. Phys. 104 (2001) 817-879. [Abstract/page](https://csc.ucdavis.edu/~cmg/compmech/pubs/cmppss.htm).
- Kernelized / RKHS causal states (the "$\upsilon$-machine" target) and **decisional states** - Brodu, *Reconstruction of Epsilon-Machines in Predictive Frameworks and Decisional States*, [arXiv:0902.0600](https://arxiv.org/abs/0902.0600). See also Crutchfield et al., *Discovering Causal Structure with Reproducing-Kernel Hilbert Space $\varepsilon$-Machines*.

**Verify before citing.**

- Diffusion maps - Coifman and Lafon, *Diffusion maps*, Appl. Comput. Harmon. Anal. 21 (2006) 5-30 (verify DOI/link).
- RG-deep-learning mapping - Mehta and Schwab, *An exact mapping between the Variational Renormalization Group and Deep Learning* (~arXiv:1410.3831; verify id).
- DMRG / transfer-matrix RG - White (1992), Phys. Rev. Lett. 69, 2863 (verify).
- "$\upsilon$-machine" as a *named* object distinct from the $\varepsilon$-machine - this is my shorthand for the kernelized/continuous-state causal-state machine; I do not have a reference establishing it as standard terminology. Treat as my coinage until verified.

Inherited from the lineage posts: Lande 1979; Saxe et al. 2014; Atanasov, Bordelon, Pehlevan 2021; Bordelon and Pehlevan 2022; Cohen et al. 2021, 2024.

---


*Written with Claude.*
