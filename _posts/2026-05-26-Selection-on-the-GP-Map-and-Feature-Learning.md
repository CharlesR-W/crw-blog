---
title: "Selection on the GP Map and Feature Learning"
tags: [notes, ai]
date: 2026-05-26
math: true
---

These notes take one analogy seriously: the genotype-phenotype map is the network's parameter-to-output map, and the quantitative-genetics $G$-matrix is the NTK.  Everything else hangs off the timescale split in §3.

---

## §0.  Notation

One symbol, one job.  My original notes used $G$ for two different objects, which was the entire source of the confusion.

- $\theta \in \mathbb{R}^P$: the optimized vector.  Network parameters $\equiv$ genome $g$.
- $z = f(\theta) \in \mathbb{R}^O$: output / phenotype $\equiv \phi$.
- $J = \partial z / \partial \theta \in \mathbb{R}^{O \times P}$: the Jacobian (the developmental matrix).  This is what I had been calling $G$, wrongly.
- $\mathcal{L}(z)$ loss, $r = \nabla_z \mathcal{L}$ residual, $H_z = \nabla_z^2 \mathcal{L}$ output-curvature.  In bio register the signs flip: fitness $w$, selection gradient $\beta = \nabla_{\bar z} \ln \bar W$.
- $\Theta = J J^\top \in \mathbb{R}^{O \times O}$: the NTK.

The point that untangles the rest: in quantitative genetics the $G$-matrix is already the kernel, not the Jacobian.  Lande's multivariate breeder's equation is

$$\Delta \bar z = G \beta, \qquad G = J M J^\top,$$

with $M$ the mutational covariance.  Under isotropic mutation $M = I$ and $G = J J^\top = \Theta$.  The evolutionary $G$-matrix and the NTK are the same object up to a mutational metric.

---

## §1.  Feature learning = non-constant Jacobian

If $J$ is constant, gradient descent is linear regression on its columns and the features never move.  Feature learning is exactly the statement that $J$ does not sit still.

One step gives $\delta z_1 = J \delta \theta_1$; the next gives

$$\delta z_2 = J(\theta + \delta \theta_1)\, \delta \theta_2 = \bigl(J + (\partial_\theta J)\, \delta \theta_1\bigr)\, \delta \theta_2.$$

Constant $J$: design fixed, $z = J\theta$.  Non-constant $J$: the effective design changes as you move, i.e. you are learning the features (in the learning-theory sense; need not be semantic).  Lazy / NTK is the limit $\partial_\theta J \to 0$; rich / feature-learning is everywhere else.  $\mu$P is the parametrization that keeps the second term alive at infinite width.  The split is about parametrization, not nature.

---

## §2.  The Hessian splits Gauss-Newton-style

$\nabla_\theta \mathcal{L} = J^\top r$, so

$$\nabla_\theta^2 \mathcal{L} = J^\top H_z J + r \cdot \mathcal{T},$$

with map-curvature $\mathcal{T}_{aij} = \partial^2 z_a / \partial \theta_i \partial \theta_j$.  Two corrections to the original notes: the sandwich is $J^\top H_z J$ (param $\times$ param), not $J H_z J^\top$; and the "$\epsilon \nabla^2 z$" term I had written sloppily is exactly $r$ contracted into $\mathcal{T}$.  Near a minimum, $r \to 0$ kills the residual term.

The function-space operator with the same nonzero spectrum is

$$K := J H_z J^\top,$$

since $J^\top H_z J$ and $J H_z J^\top$ share nonzero eigenvalues.  For MSE, $H_z = I$ and $K = \Theta$.  So "in low-loss regions the kernel is approximately the Hessian" is nothing mystical: it is $r \to 0$ killing the residual term.  Call this fact (A).  It is static; don't confuse it with the dynamical claim in §3.

---

## §3.  Eigenvalues are fast; eigenvectors are slow

The kernel's eigenvalues retune fast; its eigenvectors rotate roughly $10^4 \times$ slower.  That ratio is gap-suppressed off-diagonal velocity, and it drives everything downstream.

Gradient flow $\dot \theta = -J^\top r$.  Push forward to function space, then to the residual:

$$\dot z = -\Theta r, \qquad \dot r = -H_z \Theta r \;\;\Rightarrow\;\; r(t) \approx e^{-H_z \Theta t}\, r_0.$$

The kernel's own velocity comes from differentiating $\Theta = J J^\top$.  With $\dot J_{ai} = \sum_j \mathcal{T}_{aij} \dot \theta_j = -\sum_{j,b} \mathcal{T}_{aij} J_{bj} r_b$, define the map-curvature double-contracted by Jacobians,

$$\Xi_{abc} = \sum_{ij} \mathcal{T}_{aij}\, J_{bj}\, J_{ci} \qquad (\text{symmetric in } b, c),$$

so that

$$\dot \Theta_{ac} = -\sum_b r_b \bigl(\Xi_{abc} + \Xi_{cab}\bigr).$$

The kernel moves at a rate set by the third-order curvature of the map, driven by the residual.  Lazy limit $\mathcal{T} \to 0$ gives $\dot \Theta = 0$; feature learning lives in $\mathcal{T} \neq 0$.  This is the first step of the neural tangent hierarchy, which closes at large width.

**Where the $10^4$ comes from.**  Treat $V := \dot \Theta$ as a perturbation to $\Theta = \sum_\mu \lambda_\mu u_\mu u_\mu^\top$ and first-order perturbation theory gives

$$\dot \lambda_\mu = u_\mu^\top V u_\mu, \qquad \dot u_\mu = \sum_{\nu \neq \mu} \frac{u_\nu^\top V u_\mu}{\lambda_\mu - \lambda_\nu}\, u_\nu.$$

Eigenvalues feel the diagonal of $V$; eigenvectors feel the off-diagonal divided by spectral gaps.  Eigenvectors freeze relative to eigenvalues exactly when (i) $V$ is near-diagonal in $\Theta$'s eigenbasis and (ii) the gaps are large.  The empirical $10^4$ is just $\lvert V_\text{off} \rvert / (\lvert V_\text{diag} \rvert \cdot \text{gap}) \sim 10^{-4}$: not a theorem, an observation that the off-diagonal drive is small.  It is also why "selection wants $G$ diagonal in the genome's preferred basis": diagonal $V$ is pure eigenvalue tuning, no rotation wasted.

**Two alignment claims, kept apart.**  "$\Theta$ aligns to $JH_zJ^\top$" was hiding two different statements:

- **(A) Static / convergence coincidence.**  As $r \to 0$, $\Theta = J J^\top$ and $K = J H_z J^\top$ share eigenvectors (trivially for MSE, up to the $H_z$ metric otherwise).  Just §2's "kernel $\approx$ Hessian."  No dynamics.
- **(B) Dynamical / silent alignment.**  The kernel rotates toward the task during training, and the target is not $K$ itself but the residual structure, $H_z$-weighted.  Integrating with $r(t) = e^{-H_z \Theta t} r_0$,

$$\delta \Theta(t) = -\Xi \cdot \bigl[(H_z \Theta)^{-1} \bigl(I - e^{-H_z \Theta t}\bigr)\, r_0\bigr].$$

The residual is filtered by $(H_z \Theta)^{-1}$: the loss curvature gates which output directions are allowed to drive the kernel.  $\delta \Theta$ grows preferentially along steep-loss, large-residual directions.  Combined with gap-suppressed eigenvector rotation, the stationary kernel has its top eigenvectors along the high-$H_z$, high-residual task directions.  So "$\Theta$ aligns to $K$" is correct as a fixed-point statement provided you read it as "$\Theta$ aligns to the loss-curvature-weighted task directions", which at convergence are $K$'s top eigenvectors.  Clean rigorous cases: deep linear nets (Saxe et al.); rich training from small initialization (silent alignment, Atanasov-Bordelon-Pehlevan).

**Caveat.**  The (B) fixed-point argument needs $H_z$ approximately static over the rotation timescale.  Fine for MSE.  For cross-entropy this fails late in training: $H_z = \operatorname{diag}(p) - p p^\top$ collapses as predictions saturate, ungating the slow directions exactly when rotation would matter.  The silent-alignment story is cleanest in the early / rich phase; in the saturated regime the gate closes and you are back to pure eigenvalue motion (conveniently, the regime §5 cares about).  What is robust is the structure: residual-driven velocity, $H_z$-gating, gap-suppressed rotation.  The closed-form fixed point is not robust outside linear / small-init settings.

In summary, four observations: silent alignment is (B); eigenvectors $\ll$ eigenvalues in rate is gap suppression; fine-tuning $\approx$ refit eigenvalues at fixed eigenvectors because rotation is $\sim 10^4 \times$ slower; low-loss kernel $\approx$ Hessian is (A).

---

## §4.  Bio dictionary

$\Delta \bar z = G \beta$ converts selection gradients into trait change.  Because $G = J M J^\top$ is itself heritable and itself under selection, its structure recapitulates much of the evolutionary story.  Within a lifetime, this is the $\mathcal{T}$-driven kernel dynamics of §3; across generations, it is selection for evolvability.  Selection on $G$ tends to make the easy directions coincide with the recurrent environmental ones.

The dictionary:

- **Modularity**: $G$ approximately block-diagonal.
- **Pleiotropy**: $J$ dense (one gene, many traits).
- **Polygenicity**: $J^\dagger$ dense (one trait, many genes).
- **Neutrality**: $\dim \ker J$.

The last one matters and I had it backwards in my original notes.  I had written "number of zero eigenvalues of $G$."  Those are the dual notion: phenotype directions with no genetic variance, i.e. constraints.  The SLT-relevant neutrality, the degeneracy the RLCT actually counts, is genome-side $\ker J$.

On basis-dependence: the genome has a canonical basis (loci) in which $M$ is roughly diagonal; ML mostly does not, though adaptive optimizers smuggle in a Fisher-flavored preconditioner.  In weight space the canonical basis is the weights; the noise enters somewhere else.

Flat minima are the bio notion of canalization or mutational robustness.  A lineage wins by carrying variants that suit the next landscape cheaply: low fitness cost to hold means flat directions.  Evolution navigates to flat minima for the same reason noisy SGD does.

---

## §5.  Fine-tuning only moves eigenvalues, hence emergent misalignment

ML has noise rather than environmental variation: minibatch noise, higher-order Taylor terms in the gradient, dropout and explicit regularizers, and the secular oscillations of edge-of-stability.  Central flows (Cohen, Damian, Lee, Kolter 2024) make the time-averaged trajectory explicit and show adaptive optimizers implicitly steer toward low curvature: the optimizer doing §4's flat-minimum hunt deliberately.  Dropout is a geometric-mean ensemble via the weight-scaling inference rule (Goodfellow, Bengio, Courville §7.12), which rhymes with the bio side's log-fitness.

Hypothesis: if most learning is the slow rotation of $J$'s eigenvectors, then fine-tuning, run at orders of magnitude less compute than pretraining, can only move eigenvalues by the §3 timescale split.  This predicts emergent misalignment and the general difficulty of unlearning.

Concretely (Betley et al. 2025): post-training is a sudden environment shift.  Pretraining left you in a flat minimum full of useful features; post-training cranks the "helpful-harmless" eigenvalue, fast-remapping eigenvalues without rotation, and perches you at a pseudo-maximum of alignment reached along low-resistance directions.  Fine-tune on essentially anything: a generic update has nonzero overlap with those low-resistance directions, and the low-resistance / high signal-to-noise directions are plausibly the ones the model represents linearly in the residual stream.  The "toxic persona" direction (Chen et al. 2025) is a found instance.  A benign nudge tips you off the pseudo-max along the cheapest available axis.

The prescription this suggests is align-train and then entrench: deliberately raise the curvature around the aligned configuration so that generic fine-tunes cannot cheaply move it.  Robust alignment becomes a modified unlearning / entrenchment problem; anything short of that is tiptoeing along a cliff face.  Preventative steering ("vaccination", Chen et al. 2025) and tracing persona vectors through pretraining (Moskvoretskii et al. 2026) are adjacent.

The open empirical question is when the alignment-relevant eigenvectors set during pretraining, and whether they can be made stiff.  If early and stiff, entrenchment is cheap.  If they are still rotating at the end, you have a problem.

---

## §6.  RL, KL, singular directions

This section is a skeleton.  Conjecture: KL-regularized RL is an eigenvalue operation, not an eigenvector one.

KL-penalized RL has the Bayesian characterization (Korbak et al. 2022): the optimum is a tilted posterior, $\pi^*(\cdot) \propto \pi_\text{ref}(\cdot)\, e^{r/\beta}$.  RLHF tilts the reference along the reward; it does not rebuild it.  In eNTK language: reweight existing kernel directions toward the reward inside the trust region the KL enforces, with no incentive to rotate.  This is the formal bones of the "RL just elicits" / pass@$k$ debate.  RL moves you to high-reward regions of the span already present at the end of pretraining (coverage); new eigenvectors only if the KL budget plus sampling actually populate them (exploration).  The cheaply movable directions are the top singular directions of $J$ at SFT init: large $\lambda_\mu$, cheap to reweight.  Behaviors needing new features require eigenvector rotation, which a KL leash and a short horizon will not fund.

The gap I keep wanting to close is an RHM-style hierarchical-compositionality analysis of which kernel directions post-training can and cannot touch.  I do not have it yet.

---

## §7.  Layerwise eNTK respects computational structure

The NTK is additive over parameter blocks, $\Theta = \sum_\ell \Theta^\ell$, and each block factorizes.  Chain rule through the layer-$\ell$ representation $h^\ell$:

$$\nabla_{\theta^\ell} z = B^\ell F^\ell, \qquad \Theta^\ell = B^\ell F^\ell F^{\ell\top} B^{\ell\top},$$

with $F^\ell = \partial h^\ell / \partial \theta^\ell$ (forward, params to representation) and $B^\ell = \partial z / \partial h^\ell$ (backward, representation to output).  (Original notes had $B$ and $F$ swapped; this is the consistent assignment.)  The two natural kernels:

$$\mathcal{F}^\ell(x_1, x_2) = F^\ell(x_1) F^\ell(x_2)^\top \quad (\text{representation Gram}),$$

$$\mathcal{B}^\ell(x_1, x_2) = B^\ell(x_1) B^\ell(x_2)^\top \quad (\text{sensitivity}).$$

$\Theta^\ell$ is the natural object for tracking sequential computation layer-by-layer; $\mathcal{F}$ for representations, $\mathcal{B}$ for how params steer them.  The chain of objects: the Hessian relates loss to params; $\Theta$ is a kernel on inputs; the dual $\tilde \Theta$ is a kernel on gradients; the GN split sends Hessian to NTK-like ($J^\top H_z J$) plus residual.  Data / param duality is baked in.

These objects are local and linear by construction (that is what makes them kernels).  Speculative bridge: if learned eNTK eigenvectors are features, the layerwise $\Theta^\ell$ blocks are candidate circuit localizers.  The "eigenvectors = features" step needs eigenvalue alignment to be effectively instantaneous so that the eigenvectors carry the learned structure (§3's timescale split pushed to its limit).  I think this is roughly right, though I have not proved it.

---

## §8.  Noise, factored computation, "circuit Darwinism"

This is speculative and gets more so as it goes.

The standard story is that noise is approximately a flatness regularizer.  My stronger claim: the jump from "flat minimum implies good generalization" to "the network learned a structured computation" is too big to make on landscape grounds alone.  Noise-robustness seems to drive computation to factor into circuits, each developing its own noise isolation, which approaches semantic isolation and possibly local anomaly detection.

Two results I want to cite but couldn't re-source:

- MLPs becoming robust to Gaussian noise injection without any explicit regularization (built in, not imposed).
- A mode-connectivity / noise-robustness equivalence (Garipov et al. 2018 is the canonical mode-connectivity paper, but the noise-robustness link is what I cannot pin down).

The "one level up" bet: if a model has many circuits with semantic content, the same noise universality that gives weight-level robustness for free should recur at the semantic level (call it thought-noise), factorizing high-level behavioral routines rather than individual circuits.  A generic anomaly-detect-and-suppress circuit is profitable as long as coarse anomaly detection is cheap: the suppressor gets reinforced exactly to the extent its targets get weakened.  That gives a small cognitive immune system or executive-function module, and with it circuit Darwinism: competition, coalitions, emergent higher-level units of selection, hierarchical organization.  Brains use opponent-process motifs and structure meso-scale content via synaptic competition and pruning; hierarchical Darwinism is a plausible default for building a mind.

The crackpot end of this: introspection in LLMs may arise from Darwinian competition among circuits, with competition producing coalitions and then emergent units of selection.  Whether introspective ability scales monotonically with capability is unclear (evolution is finicky; cf. the paradox of the plankton and the resource curse).  If you take circuits seriously, a model can be an ecosystem.

---

## §9.  Adiabatic frame

The eigenvalue / eigenvector timescale split from §3 is an adiabatic separation, and once you see it that way the stack collapses to a single statement.

Eigenvectors of $\Theta$ are slow (the "$G$ background"); eigenvalues are fast.  Model the network as adiabatically learning the eNTK under optimization / environmental noise: hold the slow eigenvector frame approximately fixed, let the eigenvalues equilibrate to the current task.  This is the standard slow-frame / fast-occupation picture from the adiabatic theorem, transplanted.  The eNTK's layer structure and data / param duality let you track computation layer-by-layer and sample-by-sample.  The units of hierarchical selection are the approximately block-diagonal pieces of the eNTK; leakage between levels is the off-block eNTK weight.

The eNTK hypothesis ("learnability $\approx$ having-learned": a direction is learnable iff it already has support in the kernel) is the same sentence as "post-training can only reweight existing eigenvectors", which loops §5 and §6 back here.  The slow frame is what pretraining builds; everything after just turns its knobs.

---

## References

Confident:

- Lande (1979), *Quantitative genetic analysis of multivariate evolution* (the $G$-matrix, $\Delta \bar z = G \beta$).
- Saxe, McClelland, Ganguli (2014), arXiv:1312.6120 (exact deep-linear dynamics; alignment to target singular modes).
- Atanasov, Bordelon, Pehlevan (2021), arXiv:2111.00034 (silent alignment).
- Bordelon, Pehlevan (2022), arXiv:2205.09653 (DMFT of kernel evolution in wide nets).
- Cohen, Kaur, Li, Talwalkar, Kolter (2021), arXiv:2103.00065 (edge of stability).
- Cohen, Damian, Lee, Kolter (2024), arXiv:2410.24206 (central flows).
- Goodfellow, Bengio, Courville (2016), *Deep Learning* §7.12 (dropout as geometric-mean ensemble).
- Betley, Tan, Warncke et al. (2025), arXiv:2502.17424 (ICML 2025; emergent misalignment).
- Chen et al. (2025), arXiv:2507.21509 (persona vectors; preventative steering).
- Moskvoretskii et al. (2026), arXiv:2605.13329 (tracing persona vectors through pretraining).

Verify the exact arXiv id before citing:

- Huang & Yau (2020), *Dynamics of Deep Neural Networks and the Neural Tangent Hierarchy* (~arXiv:1909.08156).
- Korbak et al. (2022), *RL with KL penalties is better viewed as Bayesian inference* (~arXiv:2205.11275).
- Garipov et al. (2018), arXiv:1802.10026 (loss surfaces / mode connectivity; the noise-robustness link still needs its own source).

Couldn't source:

- Gaussian-noise-injection robustness in MLPs without explicit regularization.
- A mode-connectivity / noise-robustness equivalence.

---

*Written with Claude.*
