---
title: "Comparing Predictors by What They Must Know"
date: 2026-02-12
math: true
---

*These are interim notes on a research direction I'm developing at MATS 9.0 under the mentorship of Richard Ngo. The core framework is established mathematics — control theory, automata theory, kernel methods — that I'm porting to an alignment-relevant context. I'm sharing this for feedback, not to announce results.*

---

Here's the question driving this: what you're trying to predict shapes what you learn about the world. Two agents in the same environment, optimizing different objectives, will develop different internal representations — but we lack good vocabulary for talking about *how* they differ, or by *how much*. The Hankel framework offers one answer: a black-box spectral decomposition of "what matters for predicting $f$," complete with exact importance weights and truncation guarantees, drawn from well-established mathematics in control theory and automata theory. This is theory-stage work — I'm trying to make the conceptual question precise, not build a practical tool.

## Hankel matrices as behavioral fingerprints

Given a function $f$ on sequences — strings, time series, action-observation histories — its **Hankel matrix** $H_f$ has rows indexed by prefixes (pasts) and columns indexed by suffixes (futures), with entry $(u, v) = f(u \cdot v)$. This is a behavioral fingerprint: it records every past-future relationship without reference to how they're computed. A neural net, a lookup table, and a very patient human computing the same function have identical Hankel matrices.

The functions this applies to are computed by **weighted finite automata (WFAs)**: $f(\sigma_1 \cdots \sigma_k) = \alpha^\top A^{\sigma_1} \cdots A^{\sigma_k} \omega$, where $\alpha, \omega$ are initial/final weight vectors and $A^\sigma$ is a transition matrix per symbol. This is surprisingly general — HMMs, linear dynamical systems, and probabilistic automata are all WFAs.

Fliess (1974) showed that $\text{rank}(H_f)$ equals the minimal number of states needed by *any* WFA computing $f$ — a hard lower bound extracted from behavior alone. The SVD $H_f = U \Sigma V^\top$ decomposes predictive structure into ranked modes, each with a singular value $\sigma_i$ measuring its importance. The SVD also gives you **balanced features**: past features $\alpha_f(u) = \Sigma^{1/2} U^\top e_u$ and future features $\omega_f(v) = \Sigma^{1/2} V^\top e_v$, so that $H_f(u,v) = \alpha_f(u)^\top \omega_f(v)$. The past feature $\alpha_f(u)$ *is* the state that the minimal machine assigns to history $u$. Truncating to the top $r$ modes incurs error *exactly* $\sigma_{r+1}$ (Eckart-Young) — an equality, not a bound.

The point of all this: different prediction objectives on the same environment produce different Hankel matrices with different spectra.  The Hankel matrix is a promising black-box way to express how prediction-objective influences how one learns the world - a priority-weighting of which bits are the most important.

To be precise about what this says: the structure extracted is a property of *the prediction objective*, not of a model trained on it.  There are ways to extend this to models, e.g., by predicting activations, but I haven't thought much about this yet.  I also don't know the practical scalability of this sort of spectral approach - right now I'm interested in this as a mathematization of a conceptual question I've had.

## Directional salience: comparing two predictors

Given two prediction objectives $f$ and $g$ on the same environment, you can ask: *how much of $g$'s predictive structure can $f$'s state representation capture?*

The SVD of $H_f$ gives a projector $\Pi_f$ onto $f$'s state space. Apply it to $H_g$, and Pythagoras gives:

$$\|H_g\|^2 = \|\Pi_f H_g\|^2 + \|(I - \Pi_f) H_g\|^2$$

The residual $\|(I - \Pi_f) H_g\|^2$ — **directional Hankel salience** — is predictive structure of $g$ that $f$'s representation cannot see at any rank. This is asymmetric: a rich objective is a wide net; a narrow one misses most of a richer one's structure. The salience tells you exactly how much.

Crucially for interpretation, you can take SVD truncations of this statement, and compare mode-by-mode. Define a **capture function** $\mathcal{C}(r, M) = \|\Pi_f^{(r)} H_g^{(M)}\|^2 / \|H_g^{(M)}\|^2$, which measures: of $g$'s top $M$ predictive modes, what fraction lives in $f$'s top $r$ directions? This gives you an "exchange rate" — how many $f$-modes to capture $M$ $g$-modes. Aligned objectives have $\mathcal{C}(M, M) \approx 1$; structurally incompatible ones have $\mathcal{C}(r, M) \ll 1$ for all $r$.

As an example of the kind of thing I'm thinking about: a toy operationalization of the "platonic representation hypothesis"/"natural latents" might claim that broad classes of macroscopic functions have common spectral 'bands', where a handful of features are enormously important to prediction, with a sharp decline in marginal prediction gains after these features are exhausted.  Then these modes would correspond to the Platonic forms / natural latents. (that's obviously a super-philosophically-fraught statement but I had an opportunity to say bullshit like "the Platonic forms are just eigenmodes of this here matrix" and so of course I couldn't help myself... :) )

## Connection to information theory

One thing that makes me think this framework is tracking something real: the observable $f$ induces a kernel on the state space — $k_f(x, x') = f(x) f(x')$ for scalar $f$ — and $\|H_f\|_F^2$ turns out to equal $\text{HSIC}(\text{past}, \text{future}; k_f)$, the Hilbert-Schmidt Independence Criterion measuring past-future dependence in that kernel. HSIC in turn equals $\text{MMD}^2(P_{\text{joint}},\, P_{\text{past}} \otimes P_{\text{future}})$ — the kernel analogue of KL divergence between joint and product of marginals. And MMD² has the structure of a Rényi-2 divergence. So $\|H_f\|_F^2$ is a **Rényi-2 mutual information** between past and future, as seen through $f$. The directional salience $\|(I - \Pi_f) H_g\|^2$ is the conditional version: MI in $g$ that survives after conditioning on $f$'s state representation.

This isn't an analogy — it's a chain of exact identities (Fukumizu-Bach-Jordan, Gretton et al.). The spectral decomposition really is decomposing *how much the past tells you about the future*, mode by mode, in the metric that $f$ defines on states.

## Direction: what policies know

This is a more speculative connection to reinforcement learning and real problems in alignment.

If an agent acts in a POMDP environment, you can build a Hankel-like object $H_\pi$ from its action-observation sequences and compare it to the environment's full predictive structure $H_{\text{env}}$ (formalized via predictive state representations). The projector decomposition should then give you:

- $\|\Pi_\pi H_{\text{env}}\|^2$ = environment structure the policy's implicit model *can* represent
- $\|(I - \Pi_\pi) H_{\text{env}}\|^2$ = environment structure the policy *doesn't* represent

The extension I find most interesting: **reward-differential salience**. Different reward functions $R, R'$ select different predictive modes. Given a proxy reward $R$ and true reward $R'$, I think there are ways to spectrally characterize 'how much $H_\pi$ knows about $R$ vs $R'$'.  This could mean a possible **spectral diagnostic of reward hacking**. The math should be a straightforward application of the framework above, but I haven't verified whether the RL-specific parts (action-conditioning, closed-loop identification) play nicely with the spectral machinery.

## Gaps and limitations

- **No experiments yet** on neural networks. HMM proof-of-concept only. Whether Hankel spectra can be efficiently estimated from black-box queries to large models is open.  This is theory for now.  People have done experiments where they apply this to real RL, and spectral methods are common in control theory, so I'm fairly sure there's at least _some_ numerical tractability
- **Purely behavioral.** This characterizes what a prediction task requires, not how a system computes it. Complementary to interpretability more than a tool for interpretability.

I also plan to connect this to work on belief geometry (cf. the Simplex paper), as well as to the SLT 'modes' paper (their SVD modes are very closely related), but that's downstream.

The obvious next step is experiments — estimating Hankel spectra from black-box models, testing whether directional salience detects known representation differences, seeing if any of this survives contact with neural networks.  If you're interested in the empirical side of this, I'd love to talk.

## References

- Fliess, M. (1974). Matrices de Hankel. *J. Math. Pures et Appliquées*, 53, 197–222.
- Eckart, C. & Young, G. (1936). [The approximation of one matrix by another of lower rank](https://link.springer.com/article/10.1007/BF02288367). *Psychometrika*, 1(3), 211–218.
- Gretton, A., Bousquet, O., Smola, A., & Schölkopf, B. (2005). [Measuring statistical dependence with Hilbert-Schmidt norms](http://www.gatsby.ucl.ac.uk/~gretton/papers/GreBouSmoSch05.pdf). *ALT 2005*, 63–77.
- Fukumizu, K., Bach, F.R., & Jordan, M.I. (2004). [Dimensionality reduction for supervised learning with reproducing kernel Hilbert spaces](https://www.jmlr.org/papers/volume5/fukumizu04a/fukumizu04a.pdf). *JMLR*, 5, 73–99.

---

*Written with Claude.*
