---
title: "Power Laws for Mechinterp"
date: 2026-06-28
math: true
kind: research note
---

*This post was produced as part of the Iliad Fellowship under the mentorship of Dmitry Vaintrob.*

**Tl;dr:** Power-law ("heavy-tailed") distributions have universality theorems similar to those which make Gaussians common.  We observe many things in ML are power-law distributed, most robustly and interestingly, the spectra of weight matrices.  I explain how we can think of power-laws as being a natural generalization of the idea of 'sparsity', interpolating between true sparsity and Gaussianity according to the 'tail-index' $\alpha$ of the distribution.  I share some hypotheses about how this might relate to the 'sparse'/'discrete'/'factored' representations that neural networks seem to learn.

I promise this is not a Santa-Fe-Institute encomium for power laws or "black swans"; different genre.

## Contents

- [1. The generalized central limit theorem proves power-law distributions are universality classes](#1-the-generalized-central-limit-theorem-proves-power-law-distributions-are-universality-classes)
- [2. Power laws observed in NNs might help us understand representation learning](#2-power-laws-observed-in-nns-might-help-us-understand-representation-learning)
  - [2.A. HTSR: phase changes in weight-matrix spectra and data-free prediction of generalization](#2a-htsr-phase-changes-in-weight-matrix-spectra-and-data-free-prediction-of-generalization)
  - [2.B. BBP transition as a quantum of learning](#2b-bbp-transition-as-a-quantum-of-learning)
  - [2.C. HTSR as an extended BBP transition](#2c-htsr-as-an-extended-bbp-transition)
  - [2.D. Training evidence for heavy tails is mixed, and I'm not sure if they're important](#2d-training-evidence-for-heavy-tails-is-mixed-and-im-not-sure-if-theyre-important)
- [3. The tail exponent α is a smooth proxy for sparsity and compressibility](#3-the-tail-exponent-α-is-a-smooth-proxy-for-sparsity-and-compressibility)
  - [3.A. α captures compressibility across heavy tails](#3a-α-captures-compressibility-across-heavy-tails)
  - [3.B. α-stable noise can make discrete codebooks optimal](#3b-α-stable-noise-can-make-discrete-codebooks-optimal)
  - [3.C. Heavy-tailed noise can convert analog inputs into discrete codebooks](#3c-heavy-tailed-noise-can-convert-analog-inputs-into-discrete-codebooks)
- [4. Summary](#4-summary)
- [5. References and useful citations](#5-references-and-useful-citations)

---

## 1. The generalized central limit theorem proves power-law distributions are universality classes

Gaussian distributions are important because of the 'central limit theorem': morally, any phenomenon which is the sum of a bunch of tiny additive effects will give you a bell-curve.  Lots of genes contribute a bit to height, so height is roughly normally distributed in the population, as each person is an approximately independent random draw of each of those height alleles.

Except the central limit theorem is a psyop.

The 'central limit theorem' which makes everything converge to Gaussian only holds, in its usual form, for random variables with finite variance.  If you don't have finite variance, the 'generalized' central limit theorem applies, and you get what are called Lévy $\alpha$-stable distributions.  If some underlying phenomenon is $\alpha$-stable, adding together many of them will also be an $\alpha$-stable distribution after the right rescaling.  The Gaussian is the special case $\alpha = 2$, but otherwise $\alpha$ can be between 0 and 2.

The CLT needs **finite variance**: for i.i.d. $X_i$ with mean $\mu$ and variance $\sigma^2 < \infty$,
$$\frac{1}{\sqrt{n}}\sum_{i=1}^{n}(X_i-\mu)\ \xrightarrow{d}\ \mathcal{N}(0,\sigma^2).$$

But there's a more general version of this for random variables which don't have finite variance (or, optionally, even no finite mean).  These more general distributions are called **stable distributions**, and the non-Gaussian cases have power-law tails with exponent $\alpha$: roughly, $p(x) \sim x^{-\alpha-1} \textrm{ as } x\to \infty$ for the density tail.

**Closure + GCLT, in brief.**  *Stable* means sums of independent copies stay in the family, $aX_1 + bX_2 \stackrel{d}{=} cX + d$, with $c^{\alpha} = |a|^{\alpha} + |b|^{\alpha}$ in the symmetric unit-scale case.  Gaussian is $\alpha = 2$, so to sum 0-mean Gaussians, sum their variances.

The Generalized CLT: sums of power-law-tailed variables ($P(|X| > x) \sim x^{-\alpha}$, $0 < \alpha < 2$), centered when the mean exists and normalized by $n^{1/\alpha}$ rather than $\sqrt n$, converge to the stable law $S_\alpha$.  The tail exponent *becomes* the stability index.  Familiar cases: $\alpha = 2$ Gaussian, $\alpha = 1$ Cauchy, $\alpha = \tfrac12$ "the" Lévy (since $\alpha$-stable distributions as a whole are often, incl. by me, called Lévy).  NB that the actual law of $S_\alpha$ usually isn't easy to write down, so everything in power-law world is done in terms of characteristic functions.  In the symmetric, centered case, $\psi_\alpha(t) = \log \mathbb E_{S_\alpha}[e^{itS_\alpha}] = - |\frac{t}{t_0}|^{\alpha}$.

Pareto distributions aren't quite the same thing as alpha-stable distributions, but they are the cleanest toy model for the same tail exponent.  The [Pareto principle](https://en.wikipedia.org/wiki/Pareto_principle), "80% of the outcomes can be explained by 20% of the causes", is actually a precise statement about $\alpha$ for a Pareto tail: the 80:20 split appears near $\alpha \approx 1.16$.  The exponent $\alpha$ controls how much of the mean is carried by rare events, and in the $\alpha \to 0$ limit almost all mass is carried by a finite number of extreme draws.  (See [stable distributions](https://en.wikipedia.org/wiki/Stable_distribution).)[^1]

![Schematic density comparison between a finite-variance distribution and a heavy-tailed distribution.](https://i.imgur.com/HIMAqdV.png)

*Figure: The center of a heavy-tailed distribution can look quite ordinary, but rare events remain much heavier than in the finite-variance case.  This is the intuitive picture behind the generalized CLT: summing many variables does not necessarily wash the tail away.*

![Lévy walk and Brownian-motion walk comparison.](https://i.imgur.com/5mhiB9K.png)

*Figure: A simulated Brownian walk and a simulated heavy-tailed Lévy walk, shown on the same spatial scale.  The Brownian path is made from many comparable steps; the Lévy path is dominated by rare jumps.  Image credit to [Wikipedia](https://en.wikipedia.org/wiki/L%C3%A9vy_flight)*

---

## 2. Power laws observed in NNs might help us understand representation learning

![Comparison of light-tailed and heavy-tailed matrix entries and their Gram spectra.](https://i.imgur.com/yzFOKs5.png)
*Figure: Toy matrices with Gaussian versus heavy-tailed entries.  The spectrum of $W^\top W$ is the diagnostic object: it records the strength and spread of directions in weight space.*

### 2.A. HTSR: phase changes in weight-matrix spectra and data-free prediction of generalization

The main ML motivation here is [Heavy-Tailed Self-Regularization](https://arxiv.org/abs/1810.01075) and the associated [WeightWatcher](https://weightwatcher.ai/) analysis.  Mahoney has a cool-looking presentation [here](https://www.stat.berkeley.edu/~mmahoney/talks/mahoney_bari_apr23_talk_abr.pdf) that may be a bit more pedagogical.  Their thesis is that weight matrices in neural networks often pass through spectrum-level training phases:

1. initial spectra are close to the [Marčenko-Pastur](https://en.wikipedia.org/wiki/Marchenko%E2%80%93Pastur_distribution) bulk expected for random Gaussian matrices;
2. the first learned signal appears as a BBP-style spike detaching from that bulk;
3. eventually enough signal directions accumulate that the spectrum looks less like "bulk plus a few spikes" and more like a heavy-tailed spectrum.

![Spectrum phases during training.](https://i.imgur.com/qjb8PBr.png)

*Figure: A simplified version of the HTSR story: an initially random-looking spectrum develops separated signal directions, then a broad heavy-tailed spectrum.*

Martin, Peng & Mahoney show that spectrum-only tail exponents can predict trends in generalization without access to training or test data.[^2]  This is the observation that got me here.  It's worth emphasising that this is more 'perihelion of mercury'-style theorizing - their measurements do not definitively show this transition occurring cleanly and consistently everywhere in neural networks.  I think their measurements are suggestive, and I'm guided here more by theoretical intuition.

To make the mechanism more legible, I'll quickly summarize the idea of a BBP transition, as I think this is a useful thing to know anyways, and their theory builds on it.

![Fitted alpha as a data-free generalization signal.](https://i.imgur.com/bPs6OHx.png)

*Figure: Schematic of the HTSR claim that a fitted spectral tail exponent can carry data-free information about generalization.  The point is not the exact curve; it is that the spectrum supplies a layer-level summary richer than a single norm.*

### 2.B. BBP transition as a quantum of learning

The **BBP transition** is a phase transition that occurs when you're looking for a low-rank signal inside an otherwise random covariance matrix.  You can do this with different models, but for here we'll be thinking about weight matrices of neural networks, and looking at their Gram matrix, $W^T W$.  Above a threshold, the signal pops out as a separated spike eigenvalue.  Schematically,

$$W^\top W = W_0^\top W_0 + \gamma \boldsymbol u \boldsymbol u^\top$$

where $W_0$ is a matrix with iid random Gaussian entries, and $\gamma \boldsymbol u \boldsymbol u^\top$ is a rank-one signal with strength $\gamma$.  Morally, you can "see" the signal iff its strength is above a threshold value $\gamma_{BBP}$.

I think this is worth knowing about on its own as a diagnostic of learning.[^3]  BBP is something like the "classical" or "linear" regime of learning: it is easy to say whether the model learned thing X, and where the knowledge of thing X "is" (in the corresponding eigenvector).  You can even think of a linear-regression regularizer as the dividing line between spikes/signal and noise.  This is great if there is a well-defined gap.

But if you try to learn too many things, and you get too many "spikes" ($N_{\mathrm{spikes}} \ll \operatorname{dim}(W)$ is the comfortable BBP regime), this stops being a well-defined phase transition.

### 2.C. HTSR as an extended BBP transition

HTSR talks about what happens when they're all spikes.  Empirically, they fit a power law with exponent $\alpha$ to the tail of each layer's spectrum and show that an aggregated $\alpha$ predicts generalization without access to held-out data.[^2]

Why might this work?  What does it mean that it does?

There are two useful ways of thinking about why this might work.  One view is that it is just some metric of signal propagation: the spectral norm is already a decent generalization predictor, so the power-law fit may just give a better fit because it has a fittable parameter.[^4]

The second view though is theoretical: we know BBP spikes are ontically robust and "have meaning", and it sure looks like power-law spectra are like "the limit where everything is BBP spikes".  We are in a regime where BBP no longer cleanly applies, but we are also definitely not in Kansas.

Further, information-theoretically, power-law distributions are a natural generalization of **sparsity** to noisier settings: lighter tails correspond to gentler sparsity, and in the infinitely heavy-tail limit we recover the traditional sparsity notion of counting nonzero entries.  If you buy this, then things start to make a bit more sense - we love sparsity!  This is something like 'simplicity'.  **Thus it may be the case that power-law spectra are mechanistic signatures of neural networks implementing Occam's razor**.  This may give a way to measure how "memorize-y" vs generalize-y a neural network is, and might point toward a new ontology for "knowledge" in neural networks.

Mechinterp researchers may also enjoy: this [anti-grokking paper](https://openreview.net/forum?id=xEzQCFSfPG) also suggests that fitted $\alpha$ can act as a diagnostic: anti-grokking corresponds to the average HTSR layer-quality metric $\alpha$ deviating from $2.0$, with $\alpha < 2.0$ treated as a warning sign in their experiments.

![Anti-grokking diagnostic.](https://i.imgur.com/5RAAXOD.png)

*Figure: Schematic of the anti-grokking diagnostic: as training continues, held-out performance can collapse while spectrum-derived quantities continue to flag memorization or overfitting.*

### 2.D. Training evidence for heavy tails is mixed, and I'm not sure if they're important

Many heavy-tail claims about activations, gradient magnitudes, or batch noise appear secondary.  The [Outlier Features paper](https://arxiv.org/abs/2306.12929) shows some of those phenomena can be mitigated with architectural tweaks, and [Attention Sinks](https://arxiv.org/abs/2309.17453) suggests some apparent heavy-tail behavior is a relatively simple signal artifact.

I remain confident that the weight SVD spectrum is structurally significant.  The data-Gram spectrum story has support from Ruderman's natural-image statistics and from the solvable neural-scaling model of Maloney, Roberts & Sully, but these are just 'power-law in power-law out' - true but don't have the structural connection I want.  Different origins of the power-law spectrum could lead to different mental models of NNs.

The LessWrong post [Basic facts about language models during training](https://www.lesswrong.com/posts/2JJtxitp6nqu6ffak/basic-facts-about-language-models-during-training-1) is a useful empirical companion.

![Artifact-sensitive attention or activation tails.](https://i.imgur.com/r0eJr9r.png)

The Wesley Erickson talk '[Heavy-tailed Noise & Stochastic Gradient Descent](https://www.youtube.com/watch?v=mQNktY6aJmY&list=PL0oAgcyKrxGuNd7MrN-KU7h9skBsz86ZG&index=8)' is also quite good and is part of what turned me on to this line of thinking.  Also has a good discussion of the debate over heavy-tailed noise.  Two screenshots for flavour (oddly cropped to not include the speaker's face).

![Heavy-tailed SGD noise survival probabilities.](https://i.imgur.com/DWYZJTz.png)

![Heavy-tailed SGD noise comparison from the PIBBSS talk.](https://i.imgur.com/1xuqWT0.png)

---

## 3. The tail exponent α is a smooth proxy for sparsity and compressibility
(Sections 3.A and 3.B, but not 3.C, are primarily LLM-generated.)

### 3.A. α captures compressibility across heavy tails

Nature doesn't believe in zeroes (or more precisely, in floating point equality) - all our metrics must be smooth.  What is the "smooth" version of "sparsity" which doesn't rely on something being exactly zero?  Obviously, small deviations should matter less than big things.  Probably this should be relative: a '2.35' in a matrix whose entries are $O(1,000,000)$ is different than the same '2.35' in a matrix whose entries are $O(0.003)$.

Let's imagine you have a list of magnitudes $x_i \in \mathbb R_+$ of length $N$.  For now, no tricky encoding: the operative definition of sparsity is "how much error reduction can I buy by representing one more mode?"  If the magnitudes sorted from largest to smallest obey a power law,

$$
|x|_{(i)} \sim i^{-1/\alpha},
\qquad
\epsilon_p(k) = \sum_{i > k} |x|_{(i)}^p \sim \sum_{i > k} i^{-p/\alpha} \sim k^{1-p/\alpha}
\quad(\alpha < p),
$$

where $\epsilon_p(k)$ is the $p$-error left after keeping the top $k$ modes.  That is the headline result: below the threshold $\alpha < p$, best-$k$ error decays as a power law in $k$.

For squared error, $p=2$, so $\alpha = 2$ is the Gaussian/compressibility threshold.  This is the same threshold as the finite-variance boundary from the GCLT section.  If $\alpha < 2$, a small fixed number of top modes captures a non-vanishing share of the squared mass, and any fixed fraction of top modes captures an increasing share as $N$ grows.  If $\alpha \geq 2$, the distribution is dense or marginal in the $\ell_2$ sense.[^5]

As you get heavier tails, $\alpha \rightarrow 0$, the error after keeping only a few modes becomes essentially nil.  In that limit, you recover the traditional definition of sparsity: only $O(1)$ entries matter.  So data distributed according to $\alpha$ between 0 and 2 interpolates between truly sparse and minimally compressible.[^6]

### 3.B. α-stable noise can make discrete codebooks optimal

The mechanism: the Gaussian channel ($Y = X + N$, power constraint $\mathbb E[X^2] \le P$) has a *continuous* Gaussian-optimal input ($C = \tfrac12\log(1 + P/\sigma^2)$).  Under $\alpha$-stable noise ($\alpha < 2$) the variance is infinite, so ordinary power is no longer the natural signal-strength measure.  Fahs & Abou-Faycal study alpha-stable additive-noise channels under fractional-moment input constraints such as $\mathbb E|X|^r \le c$, and their broader support/discreteness results say that suitable super-logarithmic cost constraints can force bounded, discrete capacity-achieving inputs.  Chain: heavy-tailed channel noise $\Rightarrow$ changed input-cost geometry $\Rightarrow$ discrete alphabets can become optimal.

### 3.C. Heavy-tailed noise can convert analog inputs into discrete codebooks

(Note: I think this is still an interesting and plausible idea, but I would only bet at 30% that it's usefully true.  I'm actively thinking about this.)

To send information in a channel which has Gaussian noise under a total-power constraint, one should send analog data.  Under heavy-tailed noise with the right input-cost constraint, however, the optimal solution can become a discrete codebook.  Consider that, if Lévy-like noise is fairly common in ML, then... well... your residual stream is a noisy channel with Lévy-like noise, and communication along it may prefer a discrete codebook.  This is a mechanism by which we _predict_ SAE features - and moreover, we might be able to use this model to predict when it fails.

![Capacity-achieving input schematic: continuous Gaussian-channel input versus discrete mass points for an α-stable channel.](https://i.imgur.com/krs6Yj8.png)
*Figure: In the Gaussian channel, the capacity-achieving input is continuous.  In the alpha-stable noise channel under an appropriate input-cost constraint, the capacity-achieving input can become a finite discrete codebook.*

Unironically big if true: a generic mechanism for an inductive bias towards discrete representations.  General enough that a similar idea could possibly apply to the brain.

Why?  Two perspectives.  First, mechanically: on this account, Lévy-like noise is the mechanism which makes discrete codebooks optimal in some regimes.  It is part of the mechanism by which we can expect discrete representations to occur.  What's more, if we can work out this mechanism in more detail, this may give us the ability to directly extract those representations based on their noise signatures (c.f. how one could try to learn what parity-check code someone is using by flipping the bits of the encoding and seeing what happens to the decoding).

Second, universality: people differ in priors on how similarly they expect human brains and LLMs to learn, etc.  Lévy-like noise provides the basis for an account which _starts_ with a common mechanism: **a prior on discrete representations can be encoded by learning algorithms which internally optimize communication under heavy-tailed noise**.  To zeroth order, a learning algorithm can promote discrete codebooks just by being in a universality class which prominently features heavy-tailed noise.  That's not hard!  There is at least suggestive neuroscience-adjacent work on heavy-tailed synaptic weight distributions and edge-of-chaos dynamics, but every time I ask about this Claude lists like 10 back-and-forth volleys in the intellectual flame-war over how to interpret these data.

Anyways, this would be pleasing from a Kantian perspective: the apparent immanent "sparse" structure of reality revealed to be an artifact of the nature of intelligence.  We needn't posit discreteness or sparsity as a miraculous property of the ding-an-sich universe to which we have no access save by our perceptions.  Instead, we can attribute this structure to the fact that 'discrete' learners are more efficient in a sufficiently wide regime than Gaussian learners.  No unanswerable appeal to Solomonoff priors, no 'simplicity bias' (Why should the universe be simple?  What does 'simple' mean, really?  isn't it easier to believe that any fundamental simplicity is to be attributed to the perceivers?)

Two related ideas do not quite fit the main argument, but seem worth keeping on the table:
1. SAE features on the residual stream correspond to lattice codes (see [these MITOCW notes](https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/18e413df88c6303554cc45a6b3b876b6_MIT6_441S16_chapter_18.pdf)).
2. Random matrices with entrywise heavy-tailed distributions are isomorphic to sparse random graphs, and sparse graphs are also used in coding theory.  This is another connection between heavy tails and sparsity, separate from that from Levy noise.

---

## 4. Summary

Power-law ("heavy-tailed") distributions have universality theorems similar to those which make Gaussians common.  We observe many things in ML are power-law distributed, most robustly and interestingly, the spectra of weight matrices.  I have argued that power laws are a natural generalization of sparsity: by varying the tail-index $\alpha$, they interpolate between true sparsity and Gaussian-like density.  This gives one possible bridge between spectral structure, compressibility, and the factored or discrete representations neural networks seem to learn.

In writing this, I thought a lot about BBP transitions / learning quanta and random matrices with iid Lévy entries.  Heavy-tailed random matrices have a lot of properties that could be the jumping-off point for mechanically principled definitions of things like "features" (localized eigenvectors, mobility edges, connections to sparse graph codes).  But heavy-tailed random matrices are critically inconsistent with the light-tailed weight matrix _entries_ found by Beren and others.  I tried to rescue the Lévy-entry story: since Lévy noise is not isotropic and the eigenbasis is trivially sparse, one has to propose a new privileged basis other than the neuron basis.  I poked at ICA, but at the end of the day the neuron basis is definitely the privileged basis, so trying to do anything else feels like cheating.

Light-tailed entries plus a power-law spectrum, morally, implies loads of small correlations.  Some experiments on retinal ganglion cells show that maxent / Ising models based on one- and two-body statistics can recover much of the collective structure, and related work argues the fitted model can sit near criticality.  This suggests that we might do better to think in terms of many low-order interactions rather than organized higher-order correlations.  More on this in a later piece: the spirit of the thing is to move from the "sparse sensing" regime that inspired SAEs to a "weak sensing" regime characterized by many noisy overlapping measurements.  I'm very excited to think more about this, as it feels much more brain-like.

## 5. References and useful citations

- Wikipedia: [Stable distribution](https://en.wikipedia.org/wiki/Stable_distribution) · [Pareto principle](https://en.wikipedia.org/wiki/Pareto_principle) · [Lévy flight](https://en.wikipedia.org/wiki/L%C3%A9vy_flight) · [Lévy flight foraging hypothesis](https://en.wikipedia.org/wiki/L%C3%A9vy_flight_foraging_hypothesis)
- Ari Brill, *Neural Scaling Laws Rooted in the Data Distribution* - [arXiv 2412.07942](https://arxiv.org/abs/2412.07942) · [LessWrong](https://www.lesswrong.com/posts/sgR3BxRvowmecwJNT/neural-scaling-laws-rooted-in-the-data-distribution) · [code](https://github.com/aribrill/scaling-laws-paper)
- Beren Millidge, *The Scaling Laws Are In Our Stars, Not Ourselves* - [beren.io](https://www.beren.io/2025-03-01-The-Scaling-Laws-Are-In-Our-Stars-Not-Ourselves/)
- Martin & Mahoney, *Implicit Self-Regularization in DNNs: Evidence from RMT* - [arXiv 1810.01075](https://arxiv.org/abs/1810.01075) · [JMLR](https://jmlr.org/papers/v22/20-410.html)
- Martin, Peng & Mahoney, *Predicting trends … without access to training or testing data* - [arXiv 2002.06716](https://arxiv.org/abs/2002.06716) · [Nature Communications](https://www.nature.com/articles/s41467-021-24025-8)
- *Heavy-Tailed Universality Predicts Trends in Test Accuracies …* - [arXiv 1901.08278](https://arxiv.org/abs/1901.08278)
- WeightWatcher - [github](https://github.com/CalculatedContent/WeightWatcher) · [weightwatcher.ai](https://weightwatcher.ai/) · popularization: [KDnuggets pt.1](https://www.kdnuggets.com/2018/09/power-laws-deep-learning.html) / [pt.2](https://www.kdnuggets.com/2018/09/power-laws-deep-learning-2-universality.html)
- Baik, Ben Arous & Péché, *Phase transition of the largest eigenvalue for non-null complex sample covariance matrices* - [arXiv math/0403022](https://arxiv.org/abs/math/0403022)
- Fahs & Abou-Faycal, *On the capacity of additive white α-stable noise channels* - [IEEE Xplore (ISIT 2012)](https://ieeexplore.ieee.org/document/6284067)
- Fahs & Abou-Faycal, *On Properties of the Support of Capacity-Achieving Distributions for Additive Noise Channel Models with Input Cost Constraints* - [arXiv 1602.00878](https://arxiv.org/abs/1602.00878)
- Elhage et al., *Toy Models of Superposition* - [transformer-circuits.pub](https://transformer-circuits.pub/2022/toy_model/index.html)
- Compressed sensing / weak-$\ell_p$ compressibility: Candès, Donoho (canonical)
- Bondarenko et al., *Quantizable Transformers: Removing Outliers by Helping Attention Heads Do Nothing* - [arXiv 2306.12929](https://arxiv.org/abs/2306.12929)
- Xiao et al., *Efficient Streaming Language Models with Attention Sinks* - [arXiv 2309.17453](https://arxiv.org/abs/2309.17453)
- Maloney, Roberts & Sully, *A Solvable Model of Neural Scaling Laws* - [arXiv 2210.16859](https://arxiv.org/abs/2210.16859)
- Ruderman, *The statistics of natural images*, Network: Computation in Neural Systems 5 (1994) 517–548 - [DOI 10.1088/0954-898X_5_4_006](https://www.tandfonline.com/doi/abs/10.1088/0954-898X_5_4_006)
- *Late-Stage Generalization Collapse in Grokking: Detecting anti-grokking with WeightWatcher* - [arXiv 2602.02859](https://arxiv.org/abs/2602.02859)
- Yoon et al., *Edge of chaos and avalanches in neural networks with heavy-tailed synaptic weight distribution* - [arXiv 1910.05780](https://arxiv.org/abs/1910.05780)
- Schneidman et al., *Weak pairwise correlations imply strongly correlated network states in a neural population* / *Ising models for networks of real neurons* - [arXiv q-bio/0611072](https://arxiv.org/abs/q-bio/0611072)
- Tkačik et al., *Searching for collective behavior in a network of real neurons* - [arXiv 1306.3061](https://arxiv.org/abs/1306.3061)

---

[^1]: Technically, expected values are often undefined for $\alpha$-stable distributions, but y'know what I mean.

[^2]: Martin, Peng & Mahoney report these spectrum-only generalization predictions in *Predicting trends in the quality of state-of-the-art neural networks without access to training or testing data*.

[^3]: Though please note, BBP is about statistical signal-detection more than "learning" per se.

[^4]: This surprise is somewhat mitigated if you look at the predictors to which they compare, especially the weight-matrix spectral norm; that such a simple quantity does nearly as well surprises me and is moderate counterevidence against the claim that power-law scaling is the mechanical bridge between sparsity and generalization.  On the other hand they have a 140pg theory PDF justifying it - jury will remain out until that rainiest of days.

[^5]: This is extremely interesting if you don't believe in float equality - we shouldn't be allowed to have qualitatively different behaviour at $\alpha = 2$!  This is a 'singular limit', and addressing it means using intermediate asymptotics - one of my favourite things in math, but paraphrasing the pokemon professor, this is neither the time nor the place.

[^6]: Note here I'm using a metric/error-based notion of compressibility - information-theoretic measures are only sensible over real-variables if you have noise - see the section below on channel coding!

---

*LLM Usage Statement:* I had Claude write out some of the standard math exposition in sections 3.A. and 3.B. based on a bullet list.  It also handled MD formatting and other emendatory work.  Plots and images not taken from papers were generated by GPT (by code and gpt-image, resp.).
