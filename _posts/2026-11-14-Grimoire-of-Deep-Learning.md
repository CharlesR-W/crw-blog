---
title: "Grimoire of Deep Learning"
date: 2026-11-14
math: true
tags: [unlisted]
---

*Note: I don't consider this post 100% complete yet - some entries still need fixing and checking.*

**Contents**

- I. Early/Late Training
- II. Universality, Robustness, and Funny Business With The Layers

This is a list of surprising facts about how deep learning appears to work - the ones I think about often.  I'm writing this to serve as a reference I can share with others.  Take this as a personal read on what seems important to me - all of these things seem deep enough to me that a good theory of deep learning should either predict them or explain why they're wrong or irrelevant.  Probably lots _are_ wrong or irrelevant.  That's part of the fun!

Here's the summary:

- There's probably a qualitative difference between **"early" and "late" training**, with early training being more 'formative' than late training.  Tentatively, early training sees 'representation formation', while late training 'sharpens' these representations. *(§I)*
- Lots of things appear to be **architecture independent** in a meaningful way, from example-difficulty or learning order, perhaps including even [the overall structure of the learned representation](https://arxiv.org/abs/2310.02557)†.  I forget who said this, but I've heard it said that "talking to Claude is talking to its training data". *(§II)*
- Models are **robust** to really strange kinds of ablations, and this makes it hard to imagine a layer as secretly implementing one step of a boolean circuit.  There's probably an implicit tradeoff between 'learning new computations' and 'denoising or becoming more confident in old ones'. *(§II)*
- **Gradient flow (with no noise etc.) at least kinda works**, so whatever our explanation is, it should at least kinda work if we assume that training can _never_ cross a loss barrier. *(§II)*

## I. Early/Late Training

First, there is a family of effects that suggest a difference between the 'early' and 'later' phases of training, with meaningfully different processes happening in either case.  These are all things which point in this direction - to be clear, I do not contend they are the same thing, and some don't clearly apply to LLMs.  I merely wish to gesture at a pile of weak-moderate evidence that training is not 'homogeneous' - that it behaves differently at different times.  Thus a mental model which cannot accommodate this cannot be correct.

Loosely, I think of the early phase as being like 'learning representations' and the latter phase as 'sharpening' them.  A related idea I like is that of drift-diffusion transition from Tishby's ['Information Bottleneck'](https://arxiv.org/abs/1703.00810) ([Stanford seminar on YouTube](https://www.youtube.com/watch?v=XL07WEc2TRI))[^ib-measurements], which imagines the forward and backward passes as sending a signal subject to some noise, with the transition occurring when the signal-to-noise ratio crosses one.  In the early phase, gradient signal is high and optimization occurs normally.  The latter phase begins when the gradient signal reaches the noise floor - then the network moves stochastically, occasionally lowering the noise floor by chance, and then optimizing until the newly resolvable signal is eaten.

**Basin Commitment**: The [point in training at which SGD noise ceases to matter](https://arxiv.org/abs/1912.05671) to the solution - in particular, the time $$t_{commit}$$ such that networks cloned at time $$t' > t_{commit}$$ with different batch noise will result in trained networks joined by a simple low-loss path.  The region of parameter space occupied by these solutions is the final 'basin' of the model (see also [Git Re-Basin](https://arxiv.org/abs/2209.04836)).

![instability (linear-interpolation error barrier) vs rewind step k, five networks](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/frankle-lmc.png)
*Frankle et al. 2020, Fig. 3: instability (linear-interpolation error barrier) vs rewind step k, five networks.*

**(Linear, Layerwise) Mode Connectivity**: Often, one can linearly interpolate (perhaps [on a per-layer basis](https://arxiv.org/abs/2307.06966)) between models cloned after $$t_{commit}$$ without crossing a significant loss barrier.  [Kuditipudi, ..., Arora, Ge](https://arxiv.org/abs/1906.06247) shows this is a direct consequence of learned noise robustness. (I forget if they are equivalent or if the implication is unidirectional).

**NTK Fit vs. Rotation**: The NTK is a kernel you calculate from your network - the dot-product of its gradient on two samples - 'how similarly' the network would update on two samples.  This literature confuses me more than it's worth, but the main thing is that people like to talk about the eigenvectors of the kernel rotating vs fitting.  It seems to be that the kernel rotates in early training but not in later training - later training is 'more linear' (see [Fort et al. 2020](https://arxiv.org/abs/2010.15110)† and the ['silent alignment'](https://arxiv.org/abs/2111.00034)† paper).

![linearized training started at epoch t̃ (green) vs full nonlinear training (red); the gap closes after the first few epochs](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/fort-linearized.png)
*[Fort et al. 2020](https://arxiv.org/abs/2010.15110), Fig. 8: linearized training started at epoch t̃ (green) vs full nonlinear training (red); the gap closes after the first few epochs.*

**Breakeven Point**: There is a [single point in training](https://arxiv.org/abs/2002.09572) at which models trained at different learning rates (LRs) qualitatively diverge - larger LR models end up with lower spectral norm and better generalization etc.  If I understand correctly this is synonymous with the activation of the [**edge of stability**](https://arxiv.org/abs/2103.00065) phenomenon (when the largest Hessian eigenvalue becomes greater than 2/LR, the stability threshold for discretized gradient descent); [**Central flows**](https://arxiv.org/abs/2410.24206) uses secular perturbation theory to show how this qualitatively changes the trajectory and results in flatter solutions.[^catapult]

![UMAP of early trajectories for two LRs, coloured by gradient-covariance spectral norm and train accuracy](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/jastrzebski-breakeven.png)
*Jastrzębski et al. 2020, Fig. 1: UMAP of early trajectories for two LRs, coloured by gradient-covariance spectral norm and train accuracy.*

![train loss and sharpness; sharpness rises to 2/η and hovers there](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/cohen-eos.png)
*Cohen et al. 2021, Fig. 1: train loss and sharpness; sharpness rises to 2/η and hovers there.*

![the catapult trajectory and test accuracy vs learning rate](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/catapult.png)
*Lewkowycz et al. 2020, Fig. 1: the catapult trajectory and test accuracy vs learning rate.*

**Model Averaging**: for a training trajectory $$\theta(t)$$, there exists a time $$t_{av}$$ such that averaging together checkpoints taken after $$t_{av}$$ produces a functional model (occasionally with _better_ loss - this is related to the more classical Polyak averaging, see [Goodfellow, Bengio & Courville §8.7.3](https://www.deeplearningbook.org/contents/optimization.html)).  I believe at least some production LLMs have done this or a complicated version of it.  The intuition is that if there's a sharp pit in the loss-landscape, the trajectory probably bounces around this rather than going 'in', so the average should be closer.  In our language, the 'late' loss-landscape is flat and so steps are noisier - note this isn't batch noise so much as the landscape just being low-frequency, low-amplitude; we imagine that averaging the checkpoints helps (retroactively) 'triangulate' the direction the model should have moved.  There's a cute interpretation: for $$\bar \theta := \frac{1}{M}\sum_{n=1}^{M} \theta_{t_0 + n \Delta t}$$, you imagine each step to have a slowly changing drift component, and a stochastic diffusion component, and you want to choose $$t_{\text{diffusion}} \lesssim \Delta t \lesssim t_{\text{drift}}$$.

![latest-weight-averaging vs SGD on ResNet50/ImageNet and RoBERTa/WikiText103](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/lawa.png)
*[Kaddour 2022 (LAWA)](https://arxiv.org/abs/2209.14981), Fig. 1: latest-weight-averaging vs SGD on ResNet50/ImageNet and RoBERTa/WikiText103.*

**Emergence of Activation Plateaus and Cell Structure**.  This is something I and a collaborator have been thinking about a lot, and I hope to have a post on soon.  Tl;dr, if you take three activation vectors and draw the plane that passes through them, then [look at the image of that plane](https://www.lesswrong.com/posts/LajDyGyiyX8DNNsuF/interim-research-report-activation-plateaus-and-sensitive-1), you tend to see the outputs change only across a thin boundary, rather than interpolate smoothly - the activations seem to be arranged in Voronoi-like cells - an emergent digital code (see also [Janiak et al. 2024](https://arxiv.org/abs/2409.17113), [Shinkle & Heimersheim 2025](https://www.lesswrong.com/posts/WMfSbt7AAcJdHzysB/activation-plateaus-where-and-how-they-emerge), ['Deep Networks Always Grok'](https://arxiv.org/abs/2402.15555)).  Tentatively, with details forthcoming, these cells seem to form quite early in training and sharpen over time - some significant portion of training is spent on this sharpening, corresponding to more confident predictions ([implicit bias of GD](https://arxiv.org/abs/1710.10345)).  They seem to be more prominent in larger models.

![KL divergence of the output over the plane through three activations; flat plateaus with sharp walls](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/activation-plateaus.png)
*Heimersheim & Mendel 2024: KL divergence of the output over the plane through three activations; flat plateaus with sharp walls.*

**Hessian Spectra**: At initialization, the Hessian eigenvalues are random, but they [very rapidly change](https://arxiv.org/abs/1901.10159) to have a [characteristic structure](https://arxiv.org/abs/1611.07476) (see also [Papyan 2018](https://arxiv.org/abs/1811.07062)): a few large-positive-curvature directions, many near-neutral directions, and a few lightly negative-curvature directions.  I've talked before ([here](https://charlesr-w.github.io/crw-blog/Selection-for-Selectability/#5b--hessian-eigenvalues-mirror-mutation-effects)) about the parallel to the fitness-effect-of-mutation distribution in biology.  Part of this [may be idiosyncratic to the classification objective](https://arxiv.org/abs/2008.11865), but the qualitative picture [extends to LLMs](https://arxiv.org/abs/2402.16788)[^vocab-classification].  I don't know enough about this yet, but it also seems to be true that the Hessian is nearly block-diagonal per-layer[^hessian-blocks] - which implies that layers are nearly independent of one another.  Probably this is only directionally true, but it seems noteworthy.  See below on the 'painters' view as well.

![Hessian and its eigenvalue histograms, a bulk at zero plus a few outliers (panels composited)](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/sagun-hessian.png)
*Sagun et al. 2016, Fig. 1: Hessian and its eigenvalue histograms, a bulk at zero plus a few outliers (panels composited).*

![Hessian spectral density at step 0 vs step 400; the negative eigenvalues vanish](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/ghorbani-hessian.png)
*Ghorbani et al. 2019, Fig. 2: Hessian spectral density at step 0 vs step 400; the negative eigenvalues vanish.*

**Critical Periods**: Vision networks shown distorted training data for part of training [recover much better if the distortion is later rather than earlier](https://arxiv.org/abs/1711.08856); the deficit is worse as the distortion is maintained for longer.  There's a qualitative similarity to critical periods in optic development and amblyopia in animals.  Iirc this can be a bit finicky depending on LR and optimizer, so it's maybe not that universal.  The metric they measure, the Fisher trace, is closely related to the Hessian, and so this can be predicted from that.  Qualitatively (with $$f$$ the network outputs, $$J = \partial f / \partial \theta$$, and $$\ell$$ the per-example loss),

$$H \;=\; \underbrace{\mathbb{E}\!\left[J^\top \big(\nabla_f^2 \ell\big) J\right]}_{\text{Gauss-Newton}\;\approx\;\text{Fisher}} \;+\; \underbrace{\mathbb{E}\!\left[\sum_k \frac{\partial \ell}{\partial f_k}\, \nabla_\theta^2 f_k\right]}_{\text{residual}\,\times\,\text{curvature of } f}$$

later in training, the residuals $$\partial \ell / \partial f_k$$ are small, so the Hessian is roughly the Fisher.

![final accuracy vs the epoch at which the blur deficit is removed, beside the kitten data](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/achille-critical.png)
*Achille, Rovere & Soatto 2019, Fig. 1: final accuracy vs the epoch at which the blur deficit is removed, beside the kitten data.*

## II. Universality, Robustness, and Funny Business With The Layers

In this section, I'll point to a few phenomena that suggest there is a meaningful universality to what models learn, often independent of training objective, architecture, etc.  I'll add a few miscellaneous puzzling comments about the layerwise structure of learning in transformers.  These should all be taken with quite the grain of salt (most of them are controversial, but I think they're pointing at something real, even if their particular claims are refuted), but the fact that human brains reliably implement the same functionality should set our priors to thinking this is at least limitedly true.

**Platonic Representation Hypothesis**: by far the most enticing and controversial claim on this list is [the idea that models, even across modalities, learn the same structures and organize them similarly](https://arxiv.org/abs/2405.07987).  The evidence for this is something of the form 'the k-nearest-neighbors of this point in modality A are the same as the k-nearest neighbors of the corresponding point in modality B', plus some other stuff about downstream finetuning.  [Margot's 'An Ontology of Representations: Limits of Universality'](https://www.lesswrong.com/posts/ezdWqXviKmovkvcta/an-ontology-of-representations-limits-of-universality) is a good discussion on how seriously to take this claim's implications, supposing it is strongly-true.  This is methodologically related to [CKA](https://arxiv.org/abs/1905.00414) and [(SV)CCA](https://arxiv.org/abs/1706.05806) analyses, which analyze how these representations change between layers.

![representational alignment rises with competence (VTAB tasks solved); panels composited](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/prh.png)
*Huh et al. 2024, Fig. 2: representational alignment rises with competence (VTAB tasks solved); panels composited.*

**Model Stitching**: If you cut two models in half and [form a chimera](https://arxiv.org/abs/2106.07682) (fitting a linear adapter from one residual stream to another), the result seems to work reasonably well.  This applies mainly for the middle layers of transformers, and doesn't seem to work for the later or earlier layers.  This suggests that the partially-completed computations are interchangeable between models.  Think how strange this would be for circuit-boards or python programs!

![stitching penalty vs fraction of layers](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/bansal-stitching.png)
*Bansal, Nakkiran & Barak 2021, Fig. 2: stitching penalty vs fraction of layers.*

**Critical Layers**: We observe that if we [reset a given layer to its value at initialization](https://arxiv.org/abs/1902.01996) (or just early in training), some layers disproportionately affect the loss while others seem not to matter.  Looking at the numbers, it's possible this is just normalization layers or something architectural rather than a true phenomenon - it survives in my mind in light of the latter.

![per-layer re-randomization / re-initialization robustness, MNIST FCN (panels composited)](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/zhang-critical-layers.png)
*Zhang, Bengio & Singer 2019, Fig. 1: per-layer re-randomization / re-initialization robustness, MNIST FCN (panels composited).*

**Painters**: [Sun et al.](https://arxiv.org/abs/2407.09298) claim that if you take a transformer's middle layers one can generally repeat a layer, reverse them etc. with minimal reduction in loss (though not always).  The "painters" idea is that 'each layer is a painter which adds its own brushstroke to the canvas' lol.  I expect this to be related to how [looping transformers](https://arxiv.org/abs/2502.17416) work (see also [Geiping et al. 2025](https://arxiv.org/abs/2502.05171)), as well as to the earlier-discussed cell structure.  My best understanding of this is that these layers are at least sorta doing 'error correction', or some sort of cleanup.  Iirc there's a claim that this sort of fuckiness differentially harms hard math/coding benchmarks - if so it'd suggest that reasoning ability may be bottlenecked by this sort of error-correction.  Intriguing but I'm a bit dubious that there's a straightforward relationship.

![accuracy when a single middle layer is skipped, Llama2-7B (top) and BERT-Large (bottom)](https://charlesr-w.github.io/crw-blog/assets/images/lw/Grimoire-of-Deep-Learning/painters.png)
*Sun et al. 2024, Fig. 4: accuracy when a single middle layer is skipped, Llama2-7B (top) and BERT-Large (bottom).*

(this one didn't fit in either of the two sections well, so I'll just add it here)

**Full-Batch Training**: Training with no batch noise at least kiiiinda works.  [Geiping et al.](https://arxiv.org/abs/2109.14119) do CIFAR and get comparable to SGD with full-batch.  A friend ran [full-batch on GPT-2](https://www.lesswrong.com/posts/9gqjdRyJxSM6kS7zi/i-trained-gpt-2-with-full-batch-gradient-descent-so-you-don).  There's also a paper where they really-really-definitely-for-real do gradient flow because they directly numerically solve the whole ODE ([Cohen et al. 2021, Appendix J](https://arxiv.org/abs/2103.00065)†).  This is surprising to me because noise is really essential for evolution to 'work well', as it gives some 'selective slack'.  I especially am surprised by this because I had thought that it was very important that batch-noise was "data-shaped" such that it fulfilled some role normal noise couldn't.

IMAGE

Two ideas that I read about, but not enough to have a coherent picture, are LoRA and distillation.  The paper I really liked about LoRAs was ['an illusion of equivalence'](https://arxiv.org/abs/2410.21228), where they show that LoRAs typically end up adding new top singular vectors to their weight matrices ('intruder dimensions'), rather than being 'smoothly integrated in' as happens with full fine-tuning.  This has some relationship with plasticity/downstream-tunability.

---
*LLM Usage Statement: I wrote all the text, then asked Claude to format etc. and check for mistakes.  It corrected a handful of errors and suggested some places where it wanted to add papers - roughly 1/3 are Claude recommendations, most of which I recognise but haven't read (those added in the final pass are marked with a '†').  Claude did all the screenshots of the figures as well.*

[^ib-measurements]: I believe their measurements are poor evidence for this, and their particular information-theoretic version needn't be right, but I think this is a good framing of the right overall idea

[^catapult]: Interestingly, the [**catapult effect**](https://arxiv.org/abs/2003.02218) is essentially this phenomenon transiently activating at initialization, and the usefulness of LR warmup is in part due to the fact that catapult is useful for sharpness reduction, but only works when the sharpness is between 2/LR and 4/LR, above which it really does diverge - you start low enough to not diverge altogether, then increase it in order to achieve sharpness-reducing benefits.  Probably that's not the whole story, but it's neat!

[^vocab-classification]: I know technically autoregressive transformers are doing classification over next token, but the large d_vocab means we should expect qualitatively different structure, so to the extent this still kinda holds, it suggests the qualitative picture is right

[^hessian-blocks]: per-head?  The blocks vary a lot in size ([Adam-mini](https://arxiv.org/abs/2406.16793), building on [Zhang et al.](https://arxiv.org/abs/2402.16788)) so I'm not sure if the raw Hessian is fair to look at to claim that layers are 'independent'.  In theory there is a 'Fisher-corrected' Hessian which is the more geometrically-natural thing to use, but I work with what I've got.

