---
title: "[Notes] Coalitions, Canonical Kernels, and Gradient Shapley"
date: 2026-05-31
math: true
---

*Research notes, not a polished piece.  Whiteboard session with a friend and collaborator.  I had Claude draft the notes; roughly 80% endorse them.  Read accordingly.*

This picks up directly from [Selection on the GP Map and Feature Learning]({{ site.baseurl }}/Selection-on-the-GP-Map-and-Feature-Learning/).  That post was static: the $G$-matrix is the NTK, eigenvalues are fast and eigenvectors are slow, and post-training only turns the knobs the slow frame already built.  This session was about making it *dynamical* - getting an actual handle on "circuit depth," and pinning down the three matrices I keep conflating (and which space each one lives in).

The throughline, if you read one thing: §3.  Shapley attribution of the gradient across coalitions of parameters gives a baseline-free decomposition, spectral clustering makes it tractable, and the rate at which attribution mass flows up the coalition hierarchy *is* the depth-of-circuit object I have wanted all along.  Everything else is either the substrate it runs on (§1, §2) or a thread hanging off it (§4-§9).

Notation is inherited from the GP-map post: $\theta\in\mathbb R^P$ parameters $\equiv$ genome, $z=f(\theta)\in\mathbb R^O$ output $\equiv$ phenotype, $J=\partial z/\partial\theta$ the Jacobian (developmental map), $\Theta=JJ^\top$ the NTK, $H$ the parameter Hessian, $\mathcal L$ the loss.  Two bookkeeping points that caused most of the live confusion at the board.  First, $G$ is the *kernel* $JMJ^\top$, never the Jacobian; the first-hour boards used $G$ for $J$ and I have silently fixed the notation below.  Second, and more substantively, every kernel here has a *data-space* form $\Theta(x,x')$ and a *parameter-space* form $\Theta_{\mu\nu}$, and most of what tangled us up was just losing track of which one we were standing in.  I keep the indices explicit below to settle it.

---

## §1.  Three canonical matrices, and which one is "centered"

Everything in this program lives on one of three operators in parameter space.

$$H = \nabla_\theta^2 \mathcal L, \qquad \Theta = J^\top J \ (\text{param block}) \ / \ JJ^\top \ (\text{output block}), \qquad C(\theta) = \operatorname{Cov}_{B}(\nabla_\theta \mathcal L).$$

The Hessian $H$, the eNTK $\Theta$, and the **batch-noise covariance** $C$.

- **$H$ vs $\Theta$** is the Gauss-Newton split from the last post: $H = J^\top H_z J + r\cdot\mathcal T$, and the GN piece $J^\top H_z J$ has the same nonzero spectrum as $\Theta$ up to the loss-curvature metric $H_z$.  Near a minimum the residual term dies and $H\approx\Theta$.  Static fact, no dynamics.

- **$C$ vs $\Theta$** is the one I was unsure about in my raw notes, and the board settled it.  Write the per-example gradient as $g_i=J_i^\top r_i$.  The minibatch-gradient second moment is the eNTK-flavoured Gram $\mathbb E_{B}[g g^\top]$, and the *covariance* subtracts the mean:

$$C_{\mu\nu} = \operatorname{Cov}_B(\nabla_\mu,\nabla_\nu) \;=\; \Theta_{\mu\nu} - \mathbb E_\alpha[\partial_\mu Z_\alpha]\,\mathbb E_\alpha[\partial_\nu Z_\alpha].$$

So **batch noise is the eNTK with the mean-gradient outer product removed** - it is the *centered* feature kernel.  Not "centered" in the usual CKA double-centering sense, but the same flavour: the mean direction is the deterministic selection pull, and what is left over after removing it is the structured drift.  My worry that batch noise is "notoriously low-rank" survives but reframes: low rank is fine, even desirable, if the landscape is genuinely flat in the complementary directions, because then the noise basis is exactly the basis of cheap moves.

This $C$ is the ML stand-in for the **mutational covariance** $M$ of quantitative genetics.  Under isotropic mutation $M=I$; in a real network $M\approx C$ is anisotropic and data-shaped, and that anisotropy is plausibly the thing that matters for meta-learning in terms of finding flat basins (Roberts-Yaida says an MLP carries three orders of interaction, but idk how noise comes in since this seems like a different picture).

**Diagnostic this suggests.**  If a memorization circuit and a generalizing circuit both sit at $\varepsilon$ loss, I think they should be indistinguishable to the gradient but *not* to $C$: the memorization circuit should take a much larger hit from gradient covariance (worse SNR per unit of function it computes).  Bad circuits should die in the noise even when they are invisible to the mean gradient.  This is my best guess why grokking kills the memorization circuit?

---

## §2.  The $G$-matrix, properly, and the canonical (whitened) kernel

Lande's breeder's equation is $\Delta\bar z = G\beta$ with

$$G = J\,M\,J^\top,$$

$M$ the mutational covariance, $\beta$ the selection gradient.  In bio, $M$ is the identity matrix, so in ML we think that this may give a nice canonical basis in parameter space that is more like the SNP basis in bio.  At the board we built $M$ as the covariance of parameter updates, $M\approx\operatorname{Cov}[\,\text{Adam}(\nabla_\theta\mathcal L)\,]$ - i.e. $M\approx C$ from §1, possibly preconditioned.  Adaptive optimizers smuggle a Fisher-flavoured metric into $M$, which is the ML version of the genome having a canonical (locus) basis in which $M$ is roughly diagonal.  (The below we need for SGD anyways)

Eigendecompose $M = S S^\top$.  Then the natural **canonical / whitened kernel** is

$$\Theta_{\text{canon}} = \Theta\, S, \qquad \hat J_{\text{canon}} = \hat J\, S,$$

the eNTK expressed in the metric of the noise, not the naive Euclidean one.  This is the right thing to spectrally cluster on, because it asks "which directions matter *relative to how cheaply noise moves them*," which is the SNR question, not the raw-magnitude question.  Two clusterings fall out, and they are different objects:

- on the output/phenotype side ($O\times O$): **task clustering** - which behaviours co-vary;
- on the parameter side ($P\times P$): **circuit clustering** - which parameters act as a unit.

A notation reconciliation that bit me: the output-block eNTK is $\Theta^{ij}=\partial_\mu Z_i\,\partial_\mu Z_j$, whereas the loss-gradient version $G^{ij}=\partial_\mu \mathcal L_i\,\partial_\mu \mathcal L_j$ is the same object chain-ruled through the residual.  They are not interchangeable; the residual weighting is exactly the $H_z$ gate from the last post's §3.

The phenotype is *free*.  Nothing forces $z$ to be the network outputs.  Pick any readout - an eval score, a probe direction, an RL return - and you get *its* gradient kernel, induced from the eNTK by how that readout is computed.  This is what makes the eval $G$-matrix and the RL projection of §5 instances of one construction rather than separate projects.

---

## §3.  Shapley attribution of the gradient → coalitions → circuit depth

This is the section to read.  The goal is a principled, computable notion of "how deep are the circuits that have effectively formed."

**The object.**  Attribute the gradient - the change it produces in the readout, or equivalently the loss decrease - fairly across *coalitions* of parameters.  The fair attribution of a jointly produced effect to the players that produce it is the **Shapley value**.  Let $v(S)$ be the effect produced by the parameters in coalition $S$ acting together (the gradient signal, or loss change, attributable to $S$).  A single parameter has a standalone contribution; a pair $\{\mu_1,\mu_2\}$ contributes something beyond the sum of its parts; and so on up the orders.  The Shapley attribution to parameter $r$ is its fair share,

$$\phi_r = \sum_{S \ni r} (\text{Shapley weight})\,\big[v(S) - v(S\setminus r)\big],$$

and the map from the coalition values $\{v(S)\}$ to the higher-order interaction terms is a **Möbius inversion** on the subset lattice.  Those interaction terms are what I actually want: $v(\{\mu_1,\mu_2\}) - v(\{\mu_1\}) - v(\{\mu_2\})$ is the gain from cooperation between two parameters, and the higher orders are deeper cooperation.

**Where this came from, and what I am dropping.**  The route in was the hierarchical (multilevel) **Price equation**, which splits a change in mean trait into between-group and within-group covariances, recursively over a group structure; that recursion is genuinely the coalition hierarchy, and it is worth keeping in mind as the source.  But the Price framing drags in a *fitness* and a *reproducing population*, and on reflection neither is needed - there is no population, and calling the gradient a fitness was forcing the analogy.  The clean statement is just Shapley attribution of the gradient over parameter coalitions.  Keep the hierarchy, drop the biology.

**The wall, and the trick.**  In general this is hopeless: $2^P$ coalitions, Möbius inversion over the full lattice.  The move is to let a hierarchical spectral clustering of one of the §1 kernels ($\Theta$, $H$, or the whitened $C$ of §2 - which one is genuinely open) *define* the coalition structure.  A clustering with $\log P$ levels has $2^L$ groups at level $L$; the Möbius/Shapley sum then runs along that tree rather than the full lattice, and approximate Shapley becomes tractable.  The between-cluster interaction term at each level is the canonical, baseline-free importance of that coalition.

**The payoff and the hypothesis.**

> Early in training, single-parameter attributions dominate - there are no gains from cooperation yet.  Later, attribution mass flows *up* the hierarchy as higher-order coalitions become load-bearing.  **The rate and height of that upward flow is the effective depth of the circuits being formed.**

That is the object I have wanted.  "Coalitions becoming more important over training" $\equiv$ "circuit depth increasing," made quantitative and baseline-free.

**Caveats and neighbours.**

- Whether the dynamics is *gradient-dominated* or *noise-dominated* changes what the attribution measures: in the noise-dominated regime the coalition values come from $C$, not the mean gradient, and the structure being attributed is the drift structure.
- Michaud et al. (verify ref) do gradient-similarity plus k-means spectral clustering to find circuits.  Ours differs by being hierarchical, which is what buys the depth notion rather than a flat partition.
- There is an "information Shapley" literature; a kernelized version might be the natural object here, since the coalition values are kernel quantities.
- Regularization should reshape the balance of Shapley mass across coalition orders.  There may be an SNR optimum: high-order interactions are complex and slow to equilibrate, so you want to suppress them early but switch them on once everything beneath has settled.  This rhymes with the moment-bias / order-by-order story (see §9).

---

## §4.  Layerwise eNTK and the forward/backward split

Carried over and sharpened from the GP-map post's §7.  The eNTK is additive over layers and each block factorizes through the layer-$\ell$ representation $h^\ell$:

$$\nabla_{\theta^\ell} z = B^\ell F^\ell, \qquad \Theta^\ell = B^\ell\, F^\ell F^{\ell\top}\, B^{\ell\top}, \qquad \Theta(x,x')=\sum_\ell \Theta^\ell(x,x'),$$

with the **forward** kernel $F^\ell = \partial h^\ell/\partial\theta^\ell$ (params to representation, a *representation-similarity* kernel) and the **backward** kernel $B^\ell=\partial z/\partial h^\ell$ (representation to output, a *sensitivity* kernel).  $\mathcal F^\ell(x,x')=F^\ell(x)F^\ell(x')^\top$ is the rep Gram; $\mathcal B^\ell(x,x')=B^\ell(x)B^\ell(x')^\top$ is how parameters steer it.  (Yes, I had $B$ and $F$ swapped in the first-hour boards; this is the consistent assignment.)

What I still need and did not get this session: the *semantics* of these as data-space kernels $\Theta(x,x')$.  The program:

- Treat $\Theta^\ell$, $\mathcal F^\ell$, $\mathcal B^\ell$ as kernels on datapoints and **cluster the data** with them.  This is close to "how the network learns to tell these inputs apart," which is what I actually care about.  MDS or diffusion maps on datapoints, layer by layer.
- Track alignment between the forward and backward kernels, across layers and over training, with CKA/CCA: $\mathrm{CKA}(\mathcal B^\ell,\mathcal B^{\ell'})(t)$, and the cross terms $\mathrm{CKA}(\mathcal B,\mathcal F)$, $\mathrm{CKA}(\mathcal F,\mathcal F)$.  I need to actually understand whether CKA and CCA agree here before leaning on either.
- **Diachronic** layerwise clustering: watch learning happen as samples become mutually dissimilar and the kernel rank climbs.  Rank going up over training is a clean, cheap observable.

---

## §5.  The $G$-matrix for nontrivial phenotypes

Because the phenotype is free (§2), the most interesting $G$-matrices are not on raw outputs but on *high-level traits*: eval scores, capability axes, personality-battery items.  This is the alignment sell.

For a battery of behavioural readouts you get a trait $\times$ trait $G$-matrix whose structure is the same dictionary as before:

- **Modularity** $\to$ $G$ block-diagonal.  Big Five should show up as a few large blocks accounting for most of the variance in a big personality battery, with a large spectral gap above them.  Same expectation for an IQ/mental-health battery: a few coherent factors plus a "spectral" tail.
- **Cross-abilities and cross-susceptibilities** are the off-diagonal blocks: which capabilities co-improve, which vulnerabilities co-fire.  That is the quantity you want for predicting and steering side effects of an intervention.
- Compute the canonical correlations of $G$ - essentially spectral clustering on traits - to read off how modular the trait structure is.

A sharp, falsifiable sub-hypothesis: **the eNTK does not rotate under RL.**  If KL-regularized RL is an eigenvalue operation (last post's §6), then projecting a trait $G$-matrix through pretraining vs through RL should show the eigenvectors holding still while only the eigenvalues retune.  "Context vs no population" and "good / no good" were the live uncertainties at the board about whether this projection is clean.

---

## §6.  Policing circuits

A speculative unit worth naming.  Suppose part of the network exists *only* to counteract noise on another part - a "police" sector.  Its signature:

$$\mathbb E[g_{\text{police}}] \approx 0, \qquad \operatorname{Cov}(g_{\text{police}}, g_{\text{policed}}) \neq 0.$$

It has (near) zero mean gradient, so it contributes nothing to the deterministic update and is invisible to ordinary attribution.  But it co-varies with the sector it protects: when noise would push the policed sector off the flat region, the police sector counter-weights the update back into the null space.  In Hessian terms the two raw gradients should be **antiparallel with respect to $H$**, and the police sector should *track the PCAs of the other sector's noise*.

So a policing circuit is "low mean gradient, high covariant importance" - exactly the kind of structure that $C$ sees and $\Theta$'s mean part misses.  This is why the centered kernel of §1 is not a technicality: it is the only one of the three that can detect a circuit whose entire job is variance management.  Open: what, semantically, is the police sector's raw gradient?  Maybe just mean-zero with no output effect at all.

---

## §7.  An orthogonal thread: RKHS / RG via IO contracts

This was a separate small board (the red one), a different attack on coarse-graining, not obviously coupled to the rest yet.

Take the eNTK feature functions $\phi(x)$ as an RKHS embedding.  A distribution over inputs maps to a **mean embedding**

$$p(x) \;\longmapsto\; \mu_p = \mathbb E_{X\sim p}[\phi(X)],$$

and you can run a renormalization flow on the singular values of the kernel - most of which are noise and get integrated out.  This is, I think, the natural way to do RG on a network: flow on the kernel spectrum rather than on a lattice.

The IO-contract idea: localize an **input/output contract** around a subsystem so that it shields its internal degrees of freedom from the outside.  Build $\varepsilon$/$\upsilon$-machines (presumably kernelized) on the boundary statistics and scale outward.  The boundary needs a kernel for $D_{\mathrm{KL}}(\cdot\,\Vert\,\cdot)$ between the conditional output distributions $P(z_b^i)$, with the mean embeddings $\mu_z=\mathbb E_z[\phi(z)]$ carrying the statistical relationships.  A region's internal complexity is invisible from outside as long as its boundary contract is honoured - that is the shielding, and the unit of coarse-graining.

Loosely related: the "binding" operation (the binding paper) is, I think, just one instantiation of a general bind/unbind primitive - the neuroscience version does it with $\oplus$ and Fourier de/convolution.  There are many ways to implement the same contract, so I would not over-index on the specific mechanism.  Whether the Wiener/Volterra expansion belongs here is unclear; it indexes over *time* rather than interaction order, so it may only matter for the sequence structure of transformers.  Neuroscience uses it; filing it under "maybe."

---

## §8.  Measurement side quest

None of this is worth much if the operators are uncomputable.  The practical questions:

- **Can we find spectral gaps in $\Theta$ (or $H$, or $C$) without materializing the matrix?**  Random sketching / matrix-free methods on the GN-Hessian.  We never form $P\times P$; we only need the top blocks and the gaps.
- **Context-dependent kernels.**  Instead of $\mathbb E_{\text{all data}}[G]$, condition on a cluster: $\mathbb E_{\text{cluster}}[G]$.  This gives "dynamical" / context-sensitive networks - the kernel a model effectively uses *in a given context*.  The brain analogy is the default-mode network and other context-dependent circuits: the same substrate, different effective wiring per regime.
- **Modular addition as the testbed.**  Can we recover the distinct frequency ($\omega$) circuits by block-diagonalizing the layerwise $\Theta^\ell$?  If the clustering machinery cannot separate the Fourier circuits of a grokked modular-addition network, it is not ready for anything harder.

A bookkeeping note so I stop confusing myself: SAEs operate in *activation* space, not weight space.  All three matrices here are weight/parameter-space objects.  The eNTK is the bridge - it is a kernel on inputs built from parameter-space gradients - but the comparison to SAE features has to go through that bridge, not around it.

---

## §9.  Standing open questions and loose ends

The two that organize everything:

1. **When, if ever, are the eNTK eigenvectors equal to the *learned* features?**  Static, this is just SVD of the kernel.  The interesting claim is dynamical: that mid-training the slow eigenvectors carry the actual learned structure.  My gut says this holds in mid-training, around the river-valley phase, when eigenvalue equilibration is effectively instantaneous relative to eigenvector rotation (last post's §3 pushed to its limit).  Unproven.
2. **What, precisely, is the relationship of the eNTK to interpretability?**  This is the core question the whole program is circling.  Everything above is an attempt to make "eigenvector = feature, block = circuit" into something defensible rather than asserted.

Smaller loose ends:

- **Moment bias / order-by-order.**  $n$-th moments are roughly $n$-th order interactions, and moment-matching breaks down at some $n$ because high orders are just $n$-grams.  There is plausibly a regime shift at $n^\ast$ above which data is too sparse and inductive bias dominates; learning pushes $n^\ast$ upward, and improvements below $n^\ast$ somehow translate into better extrapolation above it.  The coalition-order picture of §3 is a clean lens on this: high-order coalitions are exactly the high-order interactions, and their SNR-gated switch-on is the moving bias ceiling.
- A kernelized **information-Shapley** as the right currency for coalition importance (§3).
- The **gradient-vs-noise-dominated** dichotomy needs to be made quantitative; it gates which of §3's stories applies.

---

## References

Inherited from the GP-map post (Lande 1979; Saxe et al. 2014; Atanasov-Bordelon-Pehlevan 2021; Bordelon-Pehlevan 2022; Cohen et al. 2021, 2024; Korbak et al. 2022).  New / to-verify this session:

- Michaud et al. - circuits via gradient similarity + k-means spectral clustering (verify exact paper; possibly the quantization/scaling line of work).
- Price (1972), *Extension of covariance selection mathematics* - the multilevel Price equation (the source analogy for §3, since dropped in favour of plain gradient-Shapley).
- Shapley value / Möbius inversion on the subset lattice - standard; the kernelized "information Shapley" variant is the part I want and do not have a reference for.
- The "binding" paper and its neuroscience analogue ($\oplus$ + Fourier de/convolution) - find the canonical refs.
- Roberts-Yaida (the effective-theory book) for the three-orders-of-interaction claim in MLPs.

Still unsourced, same as last time: a clean reference for noise-robustness driving circuit factorization, and for whether CKA and CCA actually agree on gradient kernels.

---

*Written with Claude.*
