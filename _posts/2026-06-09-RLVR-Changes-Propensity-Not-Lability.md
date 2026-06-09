---
title: "RLVR Changes Propensity, Not Lability"
date: 2026-06-09
math: true
---

This post was produced as part of MATS 9.1 under the mentorship of Richard Ngo.  It is not part of my main research project, but the ideas have been an important conceptual anchor to me.  Epistemically, treat this as watercooler talk.  Please feel free to share additional or contradictory work in the comments.

Low-fidelity 5-word summary:

**RLVR changes propensity, not lability**

Tl;dr is that RL acts on the weights of LLMs in a qualitatively different way from pre-training / SFT.[^1]  I give a mental model of how and why, and draw a speculative connection to 'emergent misalignment' and 'subliminal learning'.

Most of the papers below I heard of via these two youtube videos by Bycloud:

['The LLM's RL Revelation We Didn't See Coming'](https://www.youtube.com/watch?v=z3awgfU4yno&t=6s)

['The RL Irony in LLMs (and its insane new meta)'](https://www.youtube.com/watch?v=IdV5TEIsJhs)

## 1. Weight-level

**1.a** [The Path Not Taken: RLVR Provably Learns Off the Principals](https://arxiv.org/abs/2511.08567) (**This is the most important one in this section**)

- RLVR's updates are qualitatively different from those of SFT; specifically, they rotate the 'principal subspaces' less (iiuc, a tractable proxy for Hessian/eNTK eigenvectors) -- 5-ish degrees versus 50-ish degrees.  They say other interesting, valuable stuff but this is the most important thing, imo.[^2]

![](https://i.imgur.com/ZWj7jUb.png)

(Figure 1c)

![](https://i.imgur.com/ITUXCGk.png)

**1.b** [Reinforcement Learning Finetunes Small Subnetworks in Large Language Models](https://arxiv.org/abs/2505.11711)

- RLVR updates consistently have ~80% sparsity, compared to SFT's ~20%.[^3]

![](https://i.imgur.com/UUPL4MW.png)

(Figure 1)

**1.c** RLVR updates are sparse / lower-rank than SFT

- [LoRA Without Regret](https://thinkingmachines.ai/blog/lora/)
  - rank ~1 LoRA is essentially equivalent to full policy-gradient RL (presumably for fixed rank this only holds for a fixed variety of tasks, but morally seems consistent with the rest of the story)
- [On Predictability of Reinforcement Learning Dynamics for Large Language Models](https://arxiv.org/abs/2510.00553)
  - RLVR updates occur in a rank-1 subspace and this subspace is consistent enough over training that you can basically just extrapolate to guess the final model after just a few checkpoints.

## 2. Behavioural-level

**2.a** [Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?](https://arxiv.org/abs/2504.13837) (**This is the most important one in this section**)

- RLVR seems to move LLMs along a bias-variance tradeoff - given K~1000 tries at a problem, RLVR-ed models are correct a larger percentage of times than the base model, but the base model gets a larger percentage of problems correct _at least once_.  This is the most compelling evidence I am aware of that RLVR mostly elicits rather than creates capabilities.  Distillation from a better parent model seems to genuinely improve performance.

![](https://i.imgur.com/4t8Lzyd.png)

(Figure 1)

![](https://i.imgur.com/6cPQAU3.png)

(Figure 2)

![](https://i.imgur.com/K6Uhw6x.png)

(Figure 7)

**2.b** [The Invisible Leash: Why RLVR May or May Not Escape Its Origin](https://arxiv.org/abs/2507.14843)

- RLVR mostly does not discover 'new policies', just reweights probability mass.  This is because of RL's in-distribution bias.

**2.c** [RL's Razor: Why Online Reinforcement Learning Forgets Less](https://arxiv.org/abs/2509.04259)

- Using RL vs SFT for the same task, RL causes less degradation of performance on other tasks than SFT.  They show this is due to RL minimizing KL distance travelled.[^4]

![](https://i.imgur.com/HUIgoyl.png)

**2.d** [Spurious Rewards: Rethinking Training Signals in RLVR](https://arxiv.org/abs/2506.10947)

- RLVR lifts Qwen math performance even if the reward signal is completely random.  This doesn't generalize to other models but I have to include it - it's so funny.  They claim it's just to do with suppressing low-probability behaviours; idk why it's specific to Qwen.

![](https://i.imgur.com/uhtRvSa.png)

(Figure 1)

### Further reading (unread)

Some more papers which ChatGPT suggests are important and which I have not yet read nor internalized:

- [ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models](https://arxiv.org/abs/2505.24864)
  - GPT suggests this one is the most likely to be a strong counterargument to the above
- [Beyond the 80/20 Rule: High-Entropy Minority Tokens Drive Effective Reinforcement Learning for LLM Reasoning](https://arxiv.org/abs/2506.01939)
- [Reinforcement Learning vs. Distillation: Understanding Accuracy and Capability in LLM Reasoning](https://arxiv.org/abs/2505.14216)
- [Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs](https://arxiv.org/abs/2506.14245)
- [Reinforcement Learning via Self-Distillation](https://arxiv.org/abs/2601.20802)

## 3. My mental model

**RL changes propensity, not lability**
(and I think that **propensity** changes correspond to changing singular **values** of the eNTK and **lability** corresponds to rotating eNTK eigen**vectors**)

### 3.a Brush-up on Hessian / eNTK eigenvectors

**TLDR:** Hessian, Gauss-Newton, and eNTK eigenvectors are all morally the same thing, and I quote the eNTK because it's loss-independent.

The Hessian of the loss decomposes (Gauss-Newton) as

$$ H = \underbrace{J^\top A\, J}_{\text{Gauss-Newton } G} \;+\; \underbrace{\textstyle\sum_k (\partial_{z_k}\ell)\, \nabla_\theta^2 f_k}_{\text{residual } R} $$

where $J = \nabla_\theta f$ is the output Jacobian and $A = \nabla_z^2 \ell$ is the loss curvature in output space.  Near an interpolating minimum the residuals $\partial_{z_k}\ell$ vanish, so $R \to 0$ and $H \approx G$.  The eNTK $\Theta = J J^\top$ shares its nonzero spectrum with $G$, with eigenvectors related by $J$, so **Hessian $\approx$ Gauss-Newton $\approx$ eNTK eigenvectors**.

I quote the eNTK because $G = J^\top A J$ carries the loss-dependent factor $A$, whereas $\Theta = J J^\top$ depends only on the model's input-output Jacobian -- so "RL doesn't rotate the eigenvectors" is a statement about the _model_, not a particular loss $\mathcal L$.  The 'principal subspaces' of _Off the Principals_ are a cheap proxy for the top of this spectrum.

Everything comes down to kernel eigenvector rotations -- RL doesn't rotate them, SFT does.  RL re-fits the magnitudes assigned to ~fixed eigenvectors, while SFT rotates them.

I think this is likely true over short periods of training, but I'm not sure if this is true over longer periods of training; I am fairly sure that this does not come from merely having fewer rollouts / samples - it seems true on a per-batch basis.  Whether or not this proves true in weight-space, I expect a looser version of this story holds in 'trait-space' - replace the network-output Jacobian $\nabla_\theta f_i(x)$ with a suite of $n$ behavioural/eval-losses $\nabla_\theta \mathcal L_n(f(x))$ - for example $\mathcal L$ = ("alignment", "SWE-talent", "similarity to Winston Churchill") etc.  This intuition comes from observations in biology that a similar object called the $G$-matrix tends to follow roughly this story.

### 3.b Speculative Implications

This model might retrodict emergent misalignment and subliminal learning.  I'll give specific stories below; low confidence in these narratives, but I expect the general propensity/lability division to be important regardless.

Note that both stories below are about SFT, not RL -- they really just illustrate what _lability_ (eigenvector rotation) buys you, since the dramatic generalization comes from rotating eigenvectors rather than rescaling them.

**Subliminal learning.**  Decompose the teacher's output, and hence the student's gradient, into a task-nominal part and a subliminal part:

$$(\text{teacher output}) = (\text{nominal output}) + (\text{subliminal output})$$

$$(\text{student gradient}) = (\text{nominal gradient}) + (\text{subliminal gradient})$$

IIUC subliminal learning only works between models of the same class (for some value of 'the same').  The nominal gradient is shared across models -- a number sequence is a number sequence -- so it transfers however normal training does.  The subliminal gradient is model-specific: against a _different_ model's eigenbasis it is incoherent, with ~zero projection, so there is nothing to train on; against the _same_ model's eigenbasis it is exactly aligned, and a small-but-consistent push along an existing eigendirection accumulates over many SFT steps.

This makes subliminal learning a case where SFT behaves _propensity-like_: because the data is self-generated by that same model, the update is _already_ aligned with the eigenbasis, so it rescales magnitudes along fixed directions rather than rotating them.  Like an antenna which achieves high gain by being extremely directional.

**Emergent misalignment.**  Here the story does lean on lability.  Suppose 'alignment' is carried by a low-dimensional -- plausibly near one-dimensional -- shared subspace.  Then narrow misaligned SFT data, whatever its surface topic, has large overlap with that _whole_ subspace, so a single push shifts the global alignment representation and the misalignment generalizes broadly.  How far it generalizes would track the size of that subspace.  (At least consistent with the empirical EM finding that a single direction can mediate and steer the effect.)

*Paper-linking, formatting, and the Hessian / eNTK brush-up were done with Claude.*

[^1]: Most of the research here compares RLVR vs SFT; I'm not sure if there are important differences between SFT vs. pre-training.  Likewise for RLVR vs RLHF, respectively.

[^2]: They attribute this behaviour largely to the KL penalty, but other papers disagree.  I don't have a strong estimation of which is right.

[^3]: The authors explicitly claim that RL updates are also full-rank, but afaict, they use the naive calculation for sparsity and rank - meaning I don't trust the rank number, and the sparsity number is all the more surprising.  'Off the Principals' talks about this; I think rank should use entropy-rank or effective-rank for robustness reasons.

[^4]: For alignment: consider the differential effect of RLHF versus e.g. SFT persona fine-tuning.
