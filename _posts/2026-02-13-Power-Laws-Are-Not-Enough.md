---
title: "Power Laws Are Not Enough"
date: 2026-02-13
math: true
---

# Power Laws Are Not Enough

*This post was written during [MATS](https://www.matsprogram.org/) 9.0 under the mentorship of Richard Ngo.*

**The argument in brief:**  Neural scaling laws — the power-law improvement of loss with model size, data, and compute — can be derived essentially from the second-order statistics (covariance) of the data distribution.  Any data with the right spectral decay produces the same scaling behavior, regardless of whether it has any deeper structure.  The low-dimensional manifold structure of natural data explains *why* we get power-law scaling, but not why we get 'capabilities'.  Power laws are real, but they are not, by themselves, deep.  There is depth, and power laws are a signature thereof, but they do not suffice to explain the 'miracle of deep learning'.

This argument is well-enough known in particular corners, but I want to present my own synthesis of how the puzzle-pieces fit together.  At least ime many ML/alignment folks are not aware of this part of the scaling deep lore.

---

The standard scaling laws picture: train a bigger model on more data, and loss improves as a power law in model size, dataset size, and compute (Kaplan et al. 2020):

$$L(N, D) = \left(\frac{N_c}{N}\right)^{\alpha_N} + \left(\frac{D_c}{D}\right)^{\alpha_D} + L_\infty$$

This is well-measured and has been enormously productive as an engineering tool.  My claim is that it's also, in a specific technical sense, shallow — and that seeing why points toward what we should actually be trying to understand about data.

## The power spectrum story

Power-law structure in data has a longer history than the scaling laws literature sometimes suggests.  Ruderman (1994) showed that natural images have 1/f² power spectra — the Fourier transform of pixel intensities falls off as the inverse square of spatial frequency, regardless of what you photograph.  This is a nearly universal property of natural images (though the exponent can vary from 2, iirc).

Maloney, Roberts, and Sully (2022) connected this to neural scaling by building a solvable model: a random feature model trained on data whose covariance matrix has power-law eigenvalues.  They derived the scaling laws analytically.  If the eigenvalues decay as

$$\lambda_i \sim i^{-\beta}$$

then test loss follows a power law whose exponent depends on β.  Their model is a toy one, but I regard it as telling essentially the correct story: power laws come from throwing more features at data which always 'has more to learn', but this doesn't directly imply anything about those representations being "useful" in the sense we think of for NNs - their model works for random features!

Sharma and Kaplan (2020) reached a related result from geometry: if data lives on a manifold of intrinsic dimension *d*, the scaling exponent goes as α ≈ 4/d.  Lower intrinsic dimension, steeper scaling.

These are two angles on the same story.  The covariance has a power-law spectrum *because* the data sits on a low-dimensional manifold.  Pope et al. (2021) confirmed empirically that common datasets have strikingly low intrinsic dimension — this is an important observation.  Low dimensionality is a big part of what makes natural data learnable, rather than cursed by exponential sample costs.

The key observation: everything here is second-order statistics.  The covariance matrix.  Two-point correlations.  The power spectrum is the Fourier transform of the two-point correlation function (Wiener-Khinchin theorem), and as Batterman emphasizes, everything about the scaling exponent — including the manifold dimension that determines it — is encoded in the lowest-order statistical description of the data.

## The insufficiency

Take any distribution, give it a power-law covariance spectrum matching natural language, and train a large model on it.  You'll get the scaling curve.  Loss comes down as a power law, Chinchilla-optimal tradeoffs hold, your model becomes an excellent next-token predictor for that distribution.  It won't do anything you'd recognize as 'intelligent'.

The Maloney et al. derivation doesn't require feature learning — random features suffice.  Any data with the right spectral decay produces the right scaling behavior.  The covariance structure alone is enough for loss to improve on schedule.  Capabilities don't follow from the covariance spectrum alone; something else is doing the work.

Intuitively, we recognize that NNs generalize and are useful because they learn "good representations".  Power laws do not indicate that we are learning good representations.  There is presumably some structural property about these representations (hierarchy/compositionality is part of the story), but those properties are _not_ encoded in the second order correlators which give rise to scaling.

## Three interesting observations

I haven't yet sat deeply with any of these papers but they seem important in light of the above.

**Emergent capabilities.**  Wei et al. (2022) found that certain capabilities appear sharply as models scale — performance jumps from near-chance to competent over a narrow range of sizes, while loss curves remain smooth.  There's debate about how much of this is metric artifact (Schaeffer et al. 2023), but either way: smooth loss improvement doesn't straightforwardly predict when or whether specific capabilities appear.  Loss and capabilities are measuring different things.

**Distributional simplicity bias.**  Belrose et al. (2024) found that networks learn statistics of increasing complexity during training, starting with low-order moments.  If I understand correctly, early training is well-approximated by matching the data's covariance — the higher-order structure that makes a language model more than an autocorrelation machine comes later.

**Data pruning.**  Sorscher et al. (2022) showed that keeping only the most informative training examples can beat power-law scaling entirely — exponential improvement as a function of pruned dataset size.  Their story would seem to go like: power-law scaling is what you get when you treat data as interchangeable, exploiting only spectral structure; selecting *which* data points matter means leveraging something the power law doesn't see.  I don't really understand yet what this means, but would be surprised if it meant nothing.

## The question

If scaling laws reflect the covariance and the covariance alone, then understanding what produces intelligence requires understanding what natural data has beyond its covariance.  It obviously involves higher-order statistical structure, but that's nearly tautological.  You can try and get a few more orders of moments by polyspectra, and there are some interesting results, but I don't think it will give satisfying answers - long-range correlations are too hard to resolve this way.

I'm confident there still is some essential structure to be understood - there is some kind of universality to how brains and LLMs work that we haven't articulated to my satisfaction.  I'll write later about 'what makes data learnable', but even this doesn't say enough to get us from 'learnable' to 'learning this data should result in structured compositional-ish representations by default'.

---

### References

- Ruderman, D.L. (1994).  "The Statistics of Natural Images."  *Network: Computation in Neural Systems* 5(4).
- Kaplan, J. et al. (2020).  "Scaling Laws for Neural Language Models."  [arXiv:2001.08361](https://arxiv.org/abs/2001.08361)
- Maloney, A., Roberts, D.A., and Sully, J. (2022).  "A Solvable Model of Neural Scaling Laws."  [arXiv:2210.16859](https://arxiv.org/abs/2210.16859)
- Sharma, U. and Kaplan, J. (2020).  "A Neural Scaling Law from the Dimension of the Data Manifold."  [arXiv:2004.10802](https://arxiv.org/abs/2004.10802)
- Pope, P. et al. (2021).  "The Intrinsic Dimension of Images and Its Impact on Learning."  ICLR 2021.
- Batterman, R.W. (2024-25).  "Deep Learning, Correlations, and the Statistics of Natural Images."  Talk series (unpublished).
- Belrose, N. et al. (2024).  "Neural Networks Learn Statistics of Increasing Complexity."  [arXiv:2402.04362](https://arxiv.org/abs/2402.04362)
- Wei, J. et al. (2022).  "Emergent Abilities of Large Language Models."  [arXiv:2206.07682](https://arxiv.org/abs/2206.07682)
- Schaeffer, R., Miranda, B., and Koyejo, S. (2023).  "Are Emergent Abilities of Large Language Models a Mirage?"  [arXiv:2304.15004](https://arxiv.org/abs/2304.15004)
- Sorscher, B. et al. (2022).  "Beyond Neural Scaling Laws: Beating Power Law Scaling via Data Pruning."  [arXiv:2206.14486](https://arxiv.org/abs/2206.14486)

---

Written with Claude
