---
title: "[Notes] Selection on the GP Map and Feature Learning"
date: 2026-05-26
math: true
---

*I gave Claude a heap of my notes on this and had it stitch them into prose.  Much less latitude than last time (the immune-system post) — the ideas and the algebra are mine; Claude cleaned them up, made the structure legible, and caught a few places where I'd mislabeled a Jacobian as a kernel.  I roughly 80% endorse the material; treat it as a research note rather than a polished publication.  If you can source the two **[ref?]** items in §8, email me.*

**How to skim:** every section opens with a bolded punchline.  The named under-braced terms in the equations are the objects that actually matter.  Tags: **[fact]** = standard / derivable, **[fix]** = correction to my original notes, **[conjecture]** = speculative, **[depends: …]** = what the claim leans on.

---

## The logical skeleton (read this, then skip around)

The spine is one analogy taken seriously: **the genotype–phenotype map is the network's parameter→output map, and the quantitative-genetics $G$-matrix is the NTK.** Everything hangs off that. The dependency order:

§0 (notation) → §1 (feature learning = non-constant Jacobian) → §2 (Gauss–Newton split) → **§3 (the load-bearing derivation: kernel eigenvalues are fast, eigenvectors are slow)** → §4 (the evo dictionary) → §5 (fine-tuning only moves eigenvalues → emergent misalignment) → §6 (RL = eigenvalue reweighting, scaffold) → §7 (layerwise eNTK = circuits, with one big assumption) → §8 (noise → factored computation → circuit Darwinism, full crackpot) → §9 (the adiabatic frame that ties it together).

If you read one section, read §3. If you read two, add §5.

---

## §0 — Notation, and the Jacobian/kernel fix

**[fix]** One symbol, one job. My original notes used $G$ for two different objects and *that is the entire source of the confusion*, so we're not doing that.

- $\theta \in \mathbb R^{P}$ — the optimized vector. NN params $\equiv$ genome $g$.
- $z = f(\theta) \in \mathbb R^{O}$ — output / phenotype $\equiv \phi$.
- $J = \partial z/\partial\theta \in \mathbb R^{O\times P}$ — the **Jacobian** of the map (the developmental matrix). *This is what I'd been calling $G$, wrongly.*
- $\mathcal L(z)$ loss, $r=\nabla_z\mathcal L$ residual, $H_z=\nabla_z^2\mathcal L$ output-curvature. Bio register flips the sign: fitness $w$, selection gradient $\beta=\nabla_{\bar z}\ln\bar W$.
- $\Theta = JJ^{\top} \in \mathbb R^{O\times O}$ — the **NTK**.

Here's the punchline that untangles it. In quantitative genetics **the $G$-matrix is already the kernel**, not the Jacobian. Lande's multivariate breeder's equation is

$$ \underbrace{\Delta\bar z}_{\text{trait change}} \;=\; \underbrace{G}_{\substack{\text{additive-genetic}\\\text{covariance}}}\;\underbrace{\beta}_{\substack{\text{selection}\\\text{gradient}}}, \qquad \underbrace{G}_{\text{kernel}} \;=\; \underbrace{J}_{\substack{\text{dev.}\\\text{Jacobian}}}\,\underbrace{M}_{\substack{\text{mutational}\\\text{covariance}}}\,J^{\top}. $$

So the additive-genetic covariance $G$ *is* $JMJ^{\top}$, and under isotropic mutation $M=I$ you get $G = JJ^{\top} = \Theta$. **The evolutionary $G$-matrix and the NTK are the same object up to the mutational metric $M$.** What I'd written as "$\mathcal G = GG^\top$" was a kernel built from a Jacobian I'd mislabeled. From here: $J$ = Jacobian, $\Theta$ = NTK, and $G = JMJ^\top$ when we're being biologists.

---

## §1 — Feature learning is just a Jacobian that won't sit still

**[fact]** If the Jacobian is constant, gradient descent is linear regression with frozen features. Feature learning *is* the statement that it isn't constant.

One step $\delta\theta_1$ gives $\delta z_1 = J\,\delta\theta_1$. The next gives

$$ \delta z_2 = J(\theta+\delta\theta_1)\,\delta\theta_2 = \big(\underbrace{J}_{\text{old features}} + \underbrace{(\partial_\theta J)\,\delta\theta_1}_{\text{features moved}}\big)\,\delta\theta_2. $$

Constant $J$ ⇒ the features are the columns of $J$ and they never move; you're doing linear regression on a fixed design, $z=J\theta$. Non-constant $J$ ⇒ the effective design $J_{\text{eff}}$ changes under you, i.e. you're learning the features — equivalently, learning a good inductive bias. The features need not be semantic; this is the learning-theory sense of the term. Lazy/NTK $\Leftrightarrow \partial_\theta J\to 0$ (frozen columns); rich/feature-learning $\Leftrightarrow \partial_\theta J$ matters. $\mu$P is just the parametrization that keeps the second term alive at infinite width. The regime split is a fact about parametrization, not about nature.

---

## §2 — The Hessian pullback is a Gauss–Newton split

**[fix]** $\nabla_\theta\mathcal L = J^\top r$, and differentiating once more,

$$ \nabla_\theta^2\mathcal L \;=\; \underbrace{J^{\top} H_z J}_{\substack{\text{Gauss–Newton}\\\text{(loss curvature seen through the map)}}} \;+\; \underbrace{(r\cdot\mathcal T)}_{\substack{\text{residual} \times \text{map-curvature}\\ \mathcal T_{aij}=\partial^2 z_a/\partial\theta_i\partial\theta_j,\;\to 0\text{ near a min}}}. $$

Two corrections to the notes: the sandwich is $J^\top H_z J$ (param × param), not $JH_zJ^\top$; and the term I'd sloppily called "$\epsilon\nabla^2 z$" is *exactly* the residual $r$ contracted into the map curvature $\mathcal T$. The function-space operator with the same nonzero spectrum is

$$ K := \underbrace{J H_z J^{\top}}_{\text{GN image in output space}}, $$

since $J^\top H_z J$ and $JH_zJ^\top$ share nonzero eigenvalues. For MSE, $H_z=I$ and $K=\Theta$. So **"in low-loss regions the kernel ≈ the Hessian"** is nothing mystical: it's just $r\to 0$ killing the residual term. Call this **fact (A)** — purely static, no dynamics in it. Hold that thought; §3 needs to *not* confuse it with the dynamical thing.

---

## §3 — Eigenvalues sprint, eigenvectors crawl (the one to read)

**The kernel's eigenvalues retune fast; its eigenvectors rotate ~$10^4\times$ slower. That ratio is gap-suppressed off-diagonal velocity, and it's the whole engine of everything downstream.**

Gradient flow $\dot\theta = -J^\top r$. Push forward to function space, then to the residual:

$$ \dot z = J\dot\theta = -\Theta r, \qquad \dot r = H_z\dot z = -H_z\Theta\,r \;\Rightarrow\; \underbrace{r(t)\approx e^{-H_z\Theta\,t}r_0}_{\text{convergence governed by }H_z\Theta}. $$

Now the kernel's own velocity. With $\dot J_{ai}=\sum_j\mathcal T_{aij}\dot\theta_j=-\sum_{j,b}\mathcal T_{aij}J_{bj}r_b$, define the map-curvature double-contracted by Jacobians,

$$ \Xi_{abc}=\sum_{ij}\mathcal T_{aij}J_{bj}J_{ci}\quad(\text{symmetric in }b,c), $$

and you get

$$ \boxed{\;\dot\Theta_{ac} \;=\; -\!\sum_b r_b\big(\Xi_{abc}+\Xi_{cab}\big) \;=\; -\,\underbrace{(\Xi\cdot r)}_{\substack{\text{3rd-order map curvature}\\\text{contracted with the residual}}}\;} $$

**The kernel moves at a rate set by the third-order curvature of the map, driven by the residual.** Lazy limit $\mathcal T\to 0\Rightarrow\dot\Theta=0$: frozen kernel. Feature learning lives entirely in $\mathcal T\neq 0$. This $\dot\Theta\sim\Xi\cdot r$ tower is the neural tangent hierarchy, which closes at large width.

**The $10^4$, demystified.** Write $\Theta=\sum_\mu\lambda_\mu u_\mu u_\mu^\top$, treat $\dot\Theta = V$ as a perturbation, and first-order perturbation theory hands you the split:

$$ \dot\lambda_\mu = \underbrace{u_\mu^\top V u_\mu}_{\text{diagonal of }V}, \qquad \dot u_\mu = \sum_{\nu\neq\mu}\frac{\overbrace{u_\nu^\top V u_\mu}^{\text{off-diagonal}}}{\underbrace{\lambda_\mu-\lambda_\nu}_{\text{spectral gap}}}\,u_\nu. $$

**Eigenvalues feel the diagonal of the kernel velocity; eigenvectors feel the off-diagonal, divided by the gaps.** So eigenvectors freeze relative to eigenvalues exactly when (i) $V$ is near-diagonal in $\Theta$'s eigenbasis and (ii) the gaps are big. Your empirical $10^4$ is just $|V_{\text{off}}|/(|V_{\text{diag}}|\cdot\text{gap})\sim 10^{-4}$ — not a theorem, an observation that the off-diagonal drive is small. And it's *why* "selection wants $G$ diagonal in the genome's preferred basis": diagonal $V$ = pure eigenvalue tuning = maximal phenotype-signal → genome transfer with zero wasted rotation.

**Now untangle the alignment claim**, because "$\Theta$ aligns to $JH_zJ^\top$" was hiding two different facts:

- **(A) Convergence coincidence — static.** As $r\to 0$, $\Theta=JJ^\top$ and the GN image $K=JH_zJ^\top$ share eigenvectors (trivially for MSE, up to the $H_z$ metric otherwise). This is just §2's "kernel ≈ Hessian." No dynamics.
- **(B) Silent alignment — dynamical.** The kernel *rotates toward the task* during training, and the target is **not** $K$ itself — it's the residual structure, $H_z$-weighted. Integrate the boxed equation with $r(t)=e^{-H_z\Theta t}r_0$:

$$ \delta\Theta(t)=-\,\Xi\cdot\Big[\underbrace{(H_z\Theta)^{-1}}_{\substack{\text{loss-curvature}\\\text{gate}}}\big(I-e^{-H_z\Theta t}\big)\,r_0\Big]. $$

The residual is filtered by $(H_z\Theta)^{-1}$: **the loss curvature $H_z$ gates which output directions are allowed to drive the kernel.** So $\delta\Theta$ grows preferentially along steep-loss, large-residual directions. Combine with gap-suppressed eigenvector dynamics and the stationary kernel is the one whose *top eigenvectors are the high-$H_z$, high-residual task directions* — i.e. $\Theta$ co-diagonalizes with $K$ on the task-relevant subspace. So the claim is correct **as a fixed-point statement**, provided you read "what $\Theta$ aligns to" as "the loss-curvature-weighted task directions," which at convergence *are* $K$'s top eigenvectors. The clean rigorous cases are deep-linear nets (exact alignment to the target's singular modes, Saxe et al.) and small-init rich training (the silent alignment effect, Atanasov–Bordelon–Pehlevan).

**[depends: quasi-static $H_z$]** The (B) fixed-point argument assumes $H_z$ barely moves over the rotation timescale. For MSE, fine ($H_z=I$). For **cross-entropy this is false late in training** — $H_z=\operatorname{diag}(p)-pp^\top$ collapses as the predictions saturate, which *un-gates* exactly the slow directions right when rotation would otherwise matter. So the silent-alignment story is cleanest in the early/rich phase; in the saturated regime the gate closes and you're back to pure eigenvalue motion (which, conveniently, is the regime §5 cares about). Honest version: what's robust here is the *structure* — residual-driven velocity, $H_z$-gating, gap-suppressed rotation — not the closed-form fixed point outside linear/small-init.

Your four bullet observations, now earned rather than asserted: **silent alignment** = (B); **eigenvectors ≪ eigenvalues in rate** = gap suppression; **fine-tuning ≈ hold $J$'s eigenvectors fixed, refit eigenvalues** = because rotation is $\sim 10^4\times$ slower; **low-loss kernel ≈ Hessian** = (A).

---

## §4 — What $J$ and $G$ mean to a biologist

**[fact]** $G$ tells you the *path of least genetic resistance* — not how *wise* a direction is (that's $\beta$), how *easy* it is.

$\Delta\bar z = G\beta$ turns selection gradients into trait change. Because $G=JMJ^\top$ is heritable and itself under selection — the within-lifetime analog is the $\mathcal T$-driven kernel dynamics of §3; across generations it's selection for evolvability — its structure recapitulates most of the evolutionary story. The pretty part: selection on $G$ tends to make the *easy* directions coincide with the *recurrent* environmental ones.

The dictionary, in prose because it reads better than a table:

**Modularity** is $G\approx$ block-diagonal. **Pleiotropy** is $J$ dense (one gene, many traits → dense columns). **Polygenicity** is $J^{\dagger}$ dense (one trait, many genes → dense rows of the pseudoinverse). **Neutrality** is $\dim\ker J$ — the parameter directions that leave the phenotype untouched.

**[fix]** That last one matters and I'd gotten it backwards. I wrote "number of zero eigenvalues of $G$." Those are the *dual* notion: phenotype directions with *no genetic variance*, i.e. constraints. The SLT-relevant neutrality — the degeneracy the RLCT actually counts — is $\ker J$ on the *genome* side, not the null space of the kernel. SLT enjoyers, take the corrected note.

On the basis: the genome has a canonical basis (loci) in which $M$ is roughly diagonal; ML mostly doesn't, except adaptive optimizers smuggle in a Fisher-flavored preconditioner — but, Fisher information be damned, weight space's canonical basis is *the weights, damnit*. It comes out in the wash; the noise just enters somewhere else.

The $10^4$ rotation/retune ratio is the same near-diagonal-$V$ condition from §3 — empirical, regime-dependent, true when perturbations are nearly diagonal. And **flat minima**: environmental variation jostles the landscape, and a lineage wins by carrying variants that suit the *next* landscape *cheaply* — low fitness cost to hold = flat directions. So evolution navigates to flat minima, same as noisy SGD. The bio name for this is canalization / mutational robustness.

---

## §5 — Fine-tuning only moves eigenvalues. Hence emergent misalignment.

**You can ablate a man's eigenvalues but you will never rotate his eigenvectors.**

Bio has environmental variation (ML's nearest analog is curriculum learning, which we mostly don't run). What ML *does* have is noise: minibatch noise, higher-order Taylor terms in the gradient, dropout and explicit regularizers, and the secular oscillations of edge-of-stability. Central flows (Cohen–Damian–Lee–Kolter 2024) make the time-averaged trajectory explicit and show adaptive optimizers implicitly steer toward low curvature — *acceleration via regularization*, which is the optimizer doing §4's flat-minimum hunt on purpose. Dropout, meanwhile, is a geometric-mean ensemble via the weight-scaling inference rule (Goodfellow–Bengio–Courville §7.12) — note the geometric-mean / log-fitness rhyme with the bio side.

**The hypothesis.** If ~99% of learning is the slow rotation of $J$'s (equivalently $\Theta$'s) eigenvectors, then fine-tuning — running at orders of magnitude less compute than pretraining — *can only move eigenvalues*, by the §3 timescale split. This retrodicts emergent misalignment and the general difficulty of unlearning.

**The EM picture** (Betley et al. 2025). Treat post-training as a sudden environment shift. Pretraining left you in a flat minimum stuffed with useful features; post-training says *crank the "helpful-harmless" eigenvalue*, so you fast-remap eigenvalues — no rotation — and you now perch at a pseudo-maximum of alignment **reached along low-resistance directions**. Then fine-tune on literally anything: a generic update has nonzero dot product with those low-resistance directions, and — here's the kicker — the low-resistance (high signal-to-noise) directions are plausibly *exactly* the ones the model represents linearly in its residual stream. The "toxic persona" direction (Chen et al. 2025) is a found instance. So a benign nudge tips you off the pseudo-max along the cheapest available axis. *Ruh roh, Raggy.* Presto: misalignment vector.

**The prescription.** Robust alignment ≈ align-train **and then entrench**: deliberately jack up the curvature around the aligned configuration so generic fine-tunes can't cheaply move it. That reframes robust alignment as a *modified unlearning / entrenchment problem*; anything short of it is tiptoeing along a cliff face. Preventative steering ("vaccination," Chen et al. 2025) and tracing persona vectors through pretraining (Moskvoretskii et al. 2026) are adjacent. **[depends: eNTK dynamics over pretraining]** The open empirical question is *when* the alignment-relevant eigenvectors set during pretraining, and whether you can make them stiff. If they set early and stiffen, entrenchment is cheap; if they're still rotating at the end, you've got a problem.

---

## §6 — RL, KL, singular directions

**[conjecture — this section is a skeleton, I haven't done the work]** **KL-regularized RL is an eigenvalue operation, not an eigenvector one.**

KL-penalized RL has the Bayesian characterization (Korbak et al. 2022): the optimum is a tilted posterior

$$ \pi^{*}(\cdot)\;\propto\;\underbrace{\pi_{\text{ref}}(\cdot)}_{\text{base}}\;\underbrace{e^{r/\beta}}_{\text{reward tilt}}, $$

so RLHF *tilts* the reference along the reward — it doesn't rebuild it. In eNTK language that's reweighting existing kernel directions toward the reward inside the trust region the KL enforces; it doesn't pay to *rotate*. This is the formal bones of the "RL just elicits" / pass@$k$ debate: RL moves you to high-reward regions of the span already present at the end of pretraining (coverage), and reaches genuinely new eigenvectors only if the KL budget plus sampling actually populate them (exploration). The directions RL moves cheaply are the top singular directions of $J$ at the SFT init — large $\lambda_\mu$, cheap to reweight; behaviors needing *new features* require eigenvector rotation, which a KL leash and a short horizon won't fund.

**[conjecture — the gap I keep wanting to close]** An RHM-style hierarchical-compositionality analysis of *which* kernel directions post-training can and can't touch. I don't have it. If you do, tell me.

---

## §7 — The layerwise eNTK respects computational structure

**[fact, then one big conjecture]** The NTK is additive over parameter blocks, $\Theta=\sum_\ell\Theta^\ell$, and each block factorizes into a representation piece and a sensitivity piece.

Chain rule through the layer-$\ell$ representation $h^\ell$:

$$ \nabla_{\theta^\ell}z=\underbrace{(\partial z/\partial h^\ell)}_{B^\ell\;\text{(backward)}}\,\underbrace{(\partial h^\ell/\partial\theta^\ell)}_{F^\ell\;\text{(forward)}}, \qquad \Theta^\ell=\underbrace{B^\ell}_{\text{sensitivity}}\underbrace{F^\ell F^{\ell\top}}_{\text{representation Gram}}B^{\ell\top}. $$

**[fix]** My intermediate line had $B$ and $F$ swapped relative to the final $BFFB$. Consistent assignment: $F^\ell$ is the **forward** map params → representation, $B^\ell$ the **backward** map representation → output. Then the two natural kernels are

$$ \underbrace{\mathcal F^\ell(x_1,x_2)=F^\ell(x_1)F^\ell(x_2)^\top}_{\text{representation-similarity kernel (the activation Gram — closest thing to grounding the rep)}}, \qquad \underbrace{\mathcal B^\ell(x_1,x_2)=B^\ell(x_1)B^\ell(x_2)^\top}_{\text{gradient / sensitivity kernel}}. $$

The chain of objects, for the record: the **Hessian** relates loss ↔ params; $\Theta$ is a kernel on **inputs**; the dual $\tilde\Theta$ is a kernel on **gradients**; the GN split sends Hessian → NTK-like ($J^\top H_z J$) + residual. $\Theta^\ell$ is the natural object for tracking *sequential* computation layer-by-layer, $\mathcal F$ for representations, $\mathcal B$ for how params steer them. Data × param duality is baked in.

**The circuits caveat, stated honestly.** These are *local, linear* objects — necessarily, because that's what makes them kernels. **[conjecture]** The speculative bridge: **if** learned eNTK eigenvectors *are* features — which requires assuming eigenvalue alignment is effectively instantaneous, so the eigenvectors carry the learned structure (this is the §3 timescale split pushed to its limit) — **then** the layerwise $\Theta^\ell$ blocks are candidate circuit localizers. The "eigenvectors = features" step is the load-bearing assumption. I think it's roughly right; it is not proven; flag it as such.

---

## §8 — Noise → factored computation → circuit Darwinism

**[conjecture, escalating to full crackpot — labeled throughout]** Noise-robustness does more work in producing *structured computation* than the loss-landscape story lets on.

The standard line is: noise ≈ a flatness regularizer. Fine. My stronger claim: the jump from "flat minimum ⇒ good generalization" to "the network learned a *structured computation*" is too big to swallow on landscape grounds alone. I think noise-robustness drives computation to **factor** into circuits, each developing its own noise isolation, which approaches semantic isolation and maybe anomaly detection.

**[ref?]** the result that MLPs become robust to Gaussian noise injection *without* any explicit regularization — it's built in, not imposed. I couldn't re-source the exact paper; if you know it, send it.
**[ref?]** the mode-connectivity ↔ noise-robustness equivalence. (Garipov et al. 2018 is the canonical mode-connectivity paper, but the noise-robustness link I can't pin down.)

**The "one level up" bet.** If a model has many circuits with semantic content, the same noise-universality that makes *weight-level* robustness emerge for free should recur at the *semantic* level — call it "thought noise" — factorizing not circuits but high-level behavioral routines. A generic anomaly-detect/suppress circuit is wildly profitable as long as coarse anomaly detection is cheap: the suppressor gets reinforced to the exact extent its targets get weakened. *Bam* — a teensy-weensy cognitive immune system / executive function, and with it **circuit Darwinism**: competition → coalitions → emergent higher-level units of selection → hierarchical organization. The brain *loves* opponent-process motifs and encodes meso-scale structure by synaptic competition and pruning — selection plus opponent-process, which is especially good for parallel / multiplexed computation — so hierarchical Darwinism starts to look like a plausible *default* for building a mind.

*Parrhesiacally:* introspection in LLMs may arise from Darwinian competition among circuits; competition yields coalitions and thence emergent units of selection. **If you believe in circuits, Claude may be an ecosystem.** (Whether introspective ability rises monotonically with capability is unclear — evolution is finicky; cf. the paradox of the plankton and the resource curse.) Crackpot, maybe. It's also the most fun thing in here, so it stays.

---

## §9 — The adiabatic frame that ties it together

**[fact + framing]** The eigenvalue/eigenvector timescale split from §3 *is* an adiabatic separation, and once you see it that way the whole stack collapses into one statement.

Eigenvectors of $\Theta$ are the **slow** variables — the "$G$ background"; eigenvalues are **fast**. So model the network as **adiabatically learning the eNTK under optimization/environmental noise**: hold the slow eigenvector frame approximately fixed, let the eigenvalues equilibrate to the current task. That's the adiabatic theorem's slow-frame / fast-occupation picture, transplanted. The eNTK's layer structure and data/param duality let you track computation layer-by-layer and sample-by-sample. The units of hierarchical selection are the (approximately) block-diagonal pieces of the eNTK; **leakage between levels is off-block eNTK weight**.

The **eNTK hypothesis** — *learnability ≈ having-learned*, i.e. a direction is learnable iff it already has support in the kernel — is the same sentence as "post-training can only reweight existing eigenvectors," which loops §5 and §6 straight back to here. The slow frame is the thing pretraining builds; everything after just turns its knobs.

---

## References

**Confident:**

- Lande (1979), *Quantitative genetic analysis of multivariate evolution* — the $G$-matrix, $\Delta\bar z = G\beta$.
- Saxe, McClelland, Ganguli (2014), arXiv:1312.6120 — exact deep-linear dynamics; alignment to target singular modes.
- Atanasov, Bordelon, Pehlevan (2021), arXiv:2111.00034 — the silent alignment effect.
- Bordelon, Pehlevan (2022), arXiv:2205.09653 — DMFT of kernel evolution in wide nets.
- Cohen, Kaur, Li, Talwalkar, Kolter (2021), arXiv:2103.00065 — edge of stability.
- Cohen, Damian, Lee, Kolter (2024), arXiv:2410.24206 — central flows.
- Goodfellow, Bengio, Courville (2016), *Deep Learning* §7.12 — dropout as geometric-mean ensemble.
- Betley, Tan, Warncke, et al. (2025), arXiv:2502.17424 (ICML 2025) — emergent misalignment.
- Chen et al. (2025), arXiv:2507.21509 — persona vectors; preventative steering.
- Moskvoretskii et al. (2026), arXiv:2605.13329 — tracing persona vectors through pretraining.

**Verify the exact id before you cite:**

- Huang & Yau (2020), *Dynamics of Deep Neural Networks and the Neural Tangent Hierarchy* (~arXiv:1909.08156 — verify).
- Korbak et al. (2022), *RL with KL penalties is better viewed as Bayesian inference* (~arXiv:2205.11275 — verify).
- Garipov et al. (2018), arXiv:1802.10026 — loss surfaces / mode connectivity (the noise-robustness link still needs its own source).

**Couldn't source — help wanted:**

- **[ref?]** Gaussian-noise-injection robustness in MLPs without regularization.
- **[ref?]** mode-connectivity ↔ noise-robustness equivalence.

---

*Written with Claude.*
