---
title: "Selection for Selectability: Inductive Biases in Evolution and in Neural Networks"
date: 2026-08-21
math: true
---

*This post was written as part of MATS 9.1 under the mentorship of Richard Ngo, and was written during Iliad Fellowship, to all of whom my thanks.*

*LLM Usage: prose drafted by Claude from my outline, talk materials, and notes.  I edited thereafter.  There is some residual Claude cringe in the more functional prose, but hopefully most of it is my own and the more entertaining for it.*

## 0.A. **Precis**

Evolution selects not only for having 'good genotype' but for having good genome architecture.  Over long timescales, selection reshapes genome architecture so that random mutations produce phenotypes which vary along directions of repeated environmental variation.  This *genome–environment alignment* is mathematically analogous to kernel alignment in neural networks.  The comparison rests not on the fatuous observation that both processes can be written as equations resembling gradient descent, but on shared structural motifs - many of the interesting things we've observed about, e.g. loss-landscape geometry, are adumbrated in biology.  This post draws the mathematical analogy and introduces the parallels I find most fun - genome–environment alignment ~ feature learning, the $G$-matrix as, i.a., biology's very own measurement of low-rankness of finetuning, and neutral networks as the coolest example structure.

## 0.B. **Preface:**

In [Coalitional Darwinism](https://www.lesswrong.com/posts/Tm2dCH6dHE2ber53Y/coalitional-darwinism-and-the-instrumental-utility-of) I argued that selection had a limited resolution and that therefore lineages should evolve to spend it well.  I have been working on a sequence of followups relating concepts from evolution to deep learning and modern LLM phenomena, but, my native disposition being an unwillingness to release anything less than the Magisterial Compendium of All Truths, I've had to force myself into writing small bits at a time.  Hoc vide.  This post will cover the minimum analogy.  If this analogy feels fatuous, please accept my assurances that it will cash out in the forthcoming 'applications' pieces.

**Tl;dr on the sequence as a whole:**

- Evolution is like SGD not just in mathematical form, but in the induced structural motifs.  It prefers flat minima, sorta-factored-solutions, redundant solutions, and lots of loose parameters for optimization.
- Catalogue of structural motifs shared in ML and evolution: e.g., local-linearity / flatness, facilitated variation, error-correction, degeneracy and redundancy circuitry
- Speculative applications of ideas derived from biology to machine learning, including the hydra effect and subliminal-learning/emergent-misalignment

## **0.C. Contents**

- [**1.  A Population Is a Density Distribution in Genome Space**](#1--a-population-is-a-density-distribution-in-genome-space)
- [**2.  Evolution Learns by Aligning Mutations to Environmental Variation**](#2--evolution-learns-by-aligning-mutations-to-environmental-variation)
- [**3.  Feature Learning Is Genome–Environment Alignment**](#3--feature-learning-is-genomeenvironment-alignment)
  - [**3.A.  The eNTK Tells us a Network's Directions of Preferred Variation**](#3a--the-entk-is-a-networks-reservoir-of-variation)
  - [**3.B.  Kernel Learning Fits; Feature Learning Rotates**](#3b--kernel-learning-fits-feature-learning-rotates)
  - [**3.C.  Selection and SGD Obey the Same Evolution Equations in the Kernel Regime**](#3c--selection-and-sgd-obey-the-same-evolution-equations-in-the-kernel-regime)
- [**4.  The G-Matrix Measures Accessible Variations, for Finches as for Claude**](#4--the-g-matrix-measures-accessible-variations-for-finches-as-for-claude)
  - [**4.A.  LLM Cross-Labilities Can be Likewise Measured by a G-Matrix**](#4a--llm-cross-labilities-can-be-likewise-measured-by-a-g-matrix)
  - [**4.B.  The eeNTK Is the Trait-Level G-Matrix**](#4b--the-eentk-is-the-trait-level-g-matrix)
- [**5.  Neutral Networks Are the Flagship Parallel**](#5--neutral-networks-are-the-flagship-parallel)
  - [**5.A.  Populations Bank Cryptic Variation in Neutral Networks**](#5a--populations-bank-cryptic-variation-in-neutral-networks)
  - [**5.B.  Hessian Eigenvalues Mirror Mutation Effects**](#5b--hessian-eigenvalues-mirror-mutation-effects)
  - [**5.C.  Flatness Counteracts Noise**](#5c--flatness-counteracts-noise)
- [**6.  Next Time:**](#6--next-time)

## **1. A Population Is a Density Distribution in Genome Space** {#1--a-population-is-a-density-distribution-in-genome-space}

A genetics-deep-learning concordance: An organism has a genome $g$ → development turns the genome into a phenotype → the environment scores the phenotype.  An NN has parameters $\theta$ → architecture turns parameters into behavior/outputs → loss scores the behavior.

![Whiteboard: selection reweights a population distribution](https://i.imgur.com/LQqDwGW.jpeg)

*One round of selection: the fitness landscape (left) reweights the current population distribution (right) into a new one (bottom) - probability mass flows toward fitter genotypes.*

Selection reweights a population toward fitter phenotypes, just as SGD pushes weights towards lower-loss regions.

Population genetics is a bit of a hybrid between SGD and Bayesian learning - a population is best thought of as a distribution $p(g)$.  *Locally* $p(g)$ evolves as if you were doing Bayesian learning to optimize the fitness - it behaves like a fluid flowing down the loss valley.  Globally it behaves more like SGD, as it is highly localized in genotype space.  But bio navigates a super interesting tradeoff that we'll soon port to ML: $p(g)$ can only *move* in proportion to its *spread*, so there's a strong incentive to make sure organisms don't all Goodhart to the current environment and converge on a single locally optimal genotype.  This fluid ends up having a 'temperature' corresponding to mutations and other types of noise.  If you have some valley, the genome distribution will line up along the iso-loss curve, with some width set by this temperature.

Modulo the fact that SGD noise comes from qualitatively different sources and some of the associated phenomena are quite different, noise is noise and to zeroth order these are the same sort of thing.  If you know enough to be skeptical of this comparison, you know enough to figure what things should carry over or not.

## **2. Evolution Learns by Aligning Mutations to Environmental Variation** {#2--evolution-learns-by-aligning-mutations-to-environmental-variation}

That DNA works well when hit by random mutations is something that we have mostly forgotten to be surprised by.  It does a little bit of the CS Hamming-code-style error-correction but it's much more defense in depth.  It should naively be all the more surprising that it's possible to find beneficial mutations at all.  There is a deep force at work ensuring that mutations are always *usefully exploring* phenotype space.

We'll abstract away from the molecular specifics and instead imagine an abstract **genotype–phenotype map**: the developmental process that turns genetic changes into phenotypic ones - $\text{phenotype} = \phi(\text{genotype})$.  What's important is that the map $\phi$ is itself encoded by the genome, and so selection acts on it.

![Whiteboard: genome–environment alignment](https://i.imgur.com/CKhuPcp.jpeg)

*Top: if the environment changes once, adaptation is just setting genes to the right values.  Bottom: if it oscillates between demanding "tall-happy" and "short-sad," a genome that flips between those combinations in one mutation out-adapts one that needs to grope haplessly after the right code.  The genome's structure - not just its current phenotype - is under selection.*

Suppose the environment oscillates between demanding one combination of traits and another - on the whiteboard above, "tall and happy" versus "short and sad" (a stipulated toy).  If the environment changed once and settled, there'd be nothing interesting to say: set the genes to the right values and be done.  But under oscillation, a lineage whose genome happens to be organized so that a single common mutation flips it between the two demanded combinations re-adapts faster after each swing.  A lineage that needs three independent rare mutations, in the right order will, eventually, get yeehawed into the dustbin of history.  Zoom out enough that you don't see the oscillations, and just see the average - the more selectable lineage will, ceteris paribus, be fitter.

How big is the advantage?  Let the environment oscillate over a timescale $\tau_{env}$, and let lineage 1 adapt faster than lineage 2, so that it is well-adapted for a time $\delta \tau$ longer than lineage 2 each cycle.  With fitness depression $\delta w$ during adaptation (*between* the lineages - we only track *relative* fitness), the more adaptable lineage gets an average relative-fitness increment $\delta s = \delta w \frac{\delta \tau}{\tau_{env}}$.  The small parameter here is $\epsilon := \frac{\delta \tau}{\tau_{env}}$, so this analysis makes most sense where oscillations are reasonably rare but the fitness-at-stake relatively large.[^1]

This is what I mean by **selection for selectability**: the architecture of variation is shaped by which variation selection was able to see and use.  Foreshadowing, we will call this **genome–environment alignment** - the genome structures itself so that common mutations align with common environmental variations.

## **3. Feature Learning Is Genome–Environment Alignment** {#3--feature-learning-is-genomeenvironment-alignment}

At any moment in training, an NN has a well-defined 'reservoir of variation' on which it can draw for the next gradient step.  Consider some circuit which can be implemented either as robust $C_R$ or as fragile $C_F$.  Perturbations to $C_F$ break it - on the one hand it is well-protected from competition, but on the other, it is well-protected from competition.  $C_R$ performs the same function but is stable under many perturbations - a network with $C_R$ will be much more adaptable than one with $C_F$ - it has more effective parameters (at least assuming the two circuits *require* the same number of parameters).

### **3.A. The eNTK Tells us a Network's Directions of Preferred Variation** {#3a--the-entk-is-a-networks-reservoir-of-variation}

Let's introduce the **empirical neural tangent kernel** (eNTK).  Write the network's behavior as $y = f(x; \theta)$; a small parameter change translates to behavior via the Jacobian,

$$\delta y = \nabla_\theta f \cdot \delta\theta,$$

just as a mutation effects the phenotype through the genotype–phenotype map, $\delta z = \nabla_g \varphi \cdot \delta g$.  The eNTK comes in two flavours.  The data-space version measures how similar two inputs look to the network's gradients,

$$\Theta(x, x') = \nabla_\theta f(x) \cdot \nabla_\theta f(x'),$$

so that under a gradient step, whatever the network learns about $x$ spills over onto $x'$ in proportion to $\Theta(x, x')$.  The parameter-space (dual) version instead scores how similar two proposed parameter changes $\delta\theta_1, \delta\theta_2$ are as seen by behavior.  I typically don't distinguish between them unless it's necessary; note that the parameter-space version is, for a model which outputs logits, the Fisher Information matrix.  Importantly, it depends only on the network, not on the loss.  Don't let me hear you saying circuits are eigen-anything of the loss-Hessian...  No defeatism!  Wir müssen wissen!

The parameter-space eNTK is essentially the network's 'first order inductive bias' - the directions in weight-space it is most prepared to move.  The genome's architecture (which here for concreteness we pretend is identical to the Jacobian) is likewise a lineage's inductive bias in the same sense.

### **3.B. Kernel Learning Fits; Feature Learning Rotates** {#3b--kernel-learning-fits-feature-learning-rotates}

![Whiteboard: the kernel/antenna picture](https://i.imgur.com/ClUd5F9.jpeg)

*Top: Correspondence between NNs and genetics.  The local linearization is the kernel in either case.  Bottom: The antenna analogy: kernel learning fits eigenvalues to a fixed set of eigenvectors; feature learning rotates the eigenvectors 'towards the data'.*

The eNTK and the GP map both have a bunch of eigenvalues and a bunch of eigenvectors.  Think of these as a set of antennae, listening for 'signal' from function space.

There are then two very different modes of learning.  In the **"lazy" or kernel regime**, the antennae stay fixed and training only adjusts how much of each direction gets used - which is just selection acting on *standing variation*, reweighting options the system already offers.  Kernel learning is well thought of as advanced linear regression.  In a meaningful sense which I will make precise in a later post on 'inductive bias', kernel learning really doesn't 'learn' anything - it never updates its inductive biases, never builds a world model etc.[^2]

'Real' learning is when the kernel *moves* during training - somewhat-annoyingly-to-me this is called **feature learning** in the learning theory literature.  Think of the antennae rotating 'towards the data' - it fits the functions its fitting (and they're fit to yet more fit functions dontcha know).

Irl the antenna metaphor is about eigenstuff - eigenvectors of $\Theta$ are the antennae, the eigenvalues their sensitivities.  Lazy/kernel learning holds the vectors fixed, while in feature learning, the Jacobian, and thus the eigenvectors move.  Genome–environment alignment is the same statement about $G$: recurrent selection rotates its leading eigendirections toward the combinations of traits the environment repeatedly demands.

But here's where it comes together!  This is 'the same' as evolution reshaping the genotype–phenotype map.  Kernel learning ≈ fast selection on standing variation; feature learning ≈ aligning your variation-generator with the structure of the environment.  (Though note that whether this fast-slow decomposition holds depends, iiuc, on the training regime?)

### **3.C. Selection and SGD Obey the Same Evolution Equations in the Kernel Regime** {#3c--selection-and-sgd-obey-the-same-evolution-equations-in-the-kernel-regime}

The response equations make this exact.  Quantitative genetics summarizes selection response as Lande's equation:

$$\Delta \bar z = G\beta,$$

the change in mean traits being the selection gradient $\beta$ pushed through $G$, the covariance of heritable variation.  Of this G-matrix we shall say much.  Kernel-regime training obeys

$$\dot f = -\Theta\, r,$$

the change in behavior being the output-space loss gradient $r$ filtered through the kernel $\Theta$.  The two objects occupy the same slot in the same first-order equation: each filters an external pressure through the variation the system can currently express, and - this matters - neither knows anything about the loss or fitness function.  Structure-to-function is firewalled from function-to-utility on both sides.

By saying these are 'the same' I mean "weak evidence because they can be written as schematically similar equations" + "moderate evidence coming from shared surprising phenomena" (of which I will summarize one cool one in this post, but a ton in a later one, so please withhold judgement).  Note though that the comparison that works is between the *effects of perturbations* - what a mutation does to the phenotype, what a parameter delta does to behavior.  Shared form is not shared dynamics; the rest of the sequence is about which further parallels are real.

## **4. The G-Matrix Measures Accessible Variations, for Finches as for Claude** {#4--the-g-matrix-measures-accessible-variations-for-finches-as-for-claude}

Biologists don't have access to the GP map; instead they focus on a few high-level phenotypic traits (like height, pelt thickness, beak width, etc) and measure how they covary.  The relevant quantity is the **$G$-matrix**, the covariance matrix of heritable variation in the chosen traits.  Diagonal entries say how much each trait can respond to selection; off-diagonals say which traits respond will get pulled along for the ride.

The $G$-matrix is the biological half of the response-equation pair from §3.C: selection pushes with a gradient $\beta$, and $\Delta \bar z = G\beta$ says $G$ decides what actually moves.  Perhaps unsurprisingly given our definitions, populations tend to evolve along ["genetic lines of least resistance"](https://doi.org/10.1111/j.1558-5646.1996.tb03563.x).  And measured $G$-matrices are typically [low-rank](https://doi.org/10.1534/genetics.105.052407): most of the available variation lives in a small number of effective directions.  Note the similarity to the low intrinsic dimensionality of fine-tuning, LoRA, and friends...

![Intrinsic dimension of fine-tuning falls with model size](https://i.imgur.com/enKx9zR.png)

*Reproduced from Figure 3 of [Aghajanyan, Zettlemoyer & Gupta (2020)](https://arxiv.org/abs/2012.13255): the intrinsic dimension of fine-tuning ($d_{90}$, the number of free parameters needed in a random subspace to reach 90% of full fine-tuning performance on MRPC) falls as pre-trained models grow.  This is the ML version of "low-rank $G$ matrix" - relevant macrobehaviours tend to be pretty accessible and rather correlated overall.*

### **4.A. LLM Cross-Labilities Can be Likewise Measured by a G-Matrix** {#4a--llm-cross-labilities-can-be-likewise-measured-by-a-g-matrix}

(Presumably someone has done this for various LLM traits, but idk)

Consider traits of an LLM that you can score with some behavioural losses $\mathcal L_i$, e.g., alignment evals, coding evals, talk-like-a-pirate-evals.  Each score has a gradient with respect to parameters; then we can ask how much each behaviour wants to talk to the same parameters.  The overlaps form a trait-level $G$-matrix for the model, and the off-diagonals are **cross-labilities**: when training yanks trait A, how much trait B gets dragged along.  For concreteness, this might look like:

$$\rho \;=\; \begin{pmatrix} 1 & 0.4 & 0.05 \\ 0.4 & 1 & 0.1 \\ 0.05 & 0.1 & 1 \end{pmatrix} \begin{matrix} \text{alignment} \\ \text{coding} \\ \text{pirate} \end{matrix}$$

(This would be a funny world to live in wouldn't it... imagine the ICLR paper titles...)

### **4.B. The eeNTK Is the Trait-Level G-Matrix** {#4b--the-eentk-is-the-trait-level-g-matrix}

If each trait $i$ is scored by a loss $L_i$ on the model's outputs, the "G-matrix" analogue for NNs is

$$G_{ij} = \nabla_{\text{out}} L_i \cdot \Theta \cdot \nabla_{\text{out}} L_j,$$

the network's kernel $\Theta$ sandwiched between the traits' output-gradients.  I call this the **extended eNTK (eeNTK)**.

I'll save it for the followup speculation post, but I expect this sort of trait correlation to be half of an explanation of [emergent misalignment](https://arxiv.org/abs/2502.17424).

## **5. Neutral Networks Are the Flagship Parallel** {#5--neutral-networks-are-the-flagship-parallel}

### **5.A. Populations Bank Cryptic Variation in Neutral Networks** {#5a--populations-bank-cryptic-variation-in-neutral-networks}

(Note the T! neu_T_ral.  Not my fault, sorry.)

Most mutations do approximately nothing.  The genotype–phenotype map is very very many-to-one: the set of genotypes producing a given phenotype - its **neutral network** - is generically enormous, and typically very space-filling.  Locally, these are the directions $\delta g$ with $\nabla_g \varphi \cdot \delta g = 0$.  A cool example: in RNA structure, they can roughly [compute this](https://royalsocietypublishing.org/doi/10.1098/rspb.1994.0040).  Claude also points to '[direct experimental support](https://www.nature.com/articles/s41467-022-32538-z)' for this from high-throughput ribozyme screens.

![Whiteboard: neutral networks facilitate adaptation](https://i.imgur.com/g5LGvBS.jpeg)

*Top: a population that can't climb a fitness barrier can, with more dimensions to move in, go around it.  Bottom: in "peacetime" the population spreads around the valley like water; when the environment changes, part of the spread population is already near the new optimum.*

For population distributions, the population's density in genome-space doesn't concentrate at a single point, but spreads out along the iso-loss set - in particular it [concentrates in the densest, most robust regions](https://www.pnas.org/doi/10.1073/pnas.96.17.9716) of the network.  The spread carries **cryptic variation** - genetic differences with no visible effect today, which nonetheless change what tomorrow's mutations do.  A population pre-spread along a neutral set has already made surface area with tons of directions a new environment might demand, and likewise can find route-around barriers it could never climb *over*.  Another Claude-suggested reference: "[in-vitro RNA-enzyme experiments](https://doi.org/10.1038/nature10083), populations that had quietly accumulated cryptic diversity under purifying selection adapted several-fold faster when handed a new substrate."

### **5.B. Hessian Eigenvalues Mirror Mutation Effects** {#5b--hessian-eigenvalues-mirror-mutation-effects}

The ML analogue of this is the Hessian spectrum - the curvature of the loss-landscape.  Measured Hessian spectra of trained networks have the same characteristic form - a [bulk](https://arxiv.org/abs/1706.04454) of small eigenvalues, plus a [few large outliers](https://arxiv.org/abs/1811.07062).  Relatedly, independently trained minima are typically joined by [low-loss paths](https://arxiv.org/abs/1802.10026) - *mode connectivity*...  Nice, yeah?

### **5.C. Flatness Counteracts Noise** {#5c--flatness-counteracts-noise}

Why should optimization *produce* this geometry?  Ecce the *noise floor* from [Coalitional Darwinism](https://www.lesswrong.com/posts/Tm2dCH6dHE2ber53Y/coalitional-darwinism-and-the-instrumental-utility-of): selection cannot see fitness differences below roughly $1/N_e$; SGD cannot see loss differences below its own noise scale.  A direction whose curvature sits below the floor is effectively neutral: nothing constrains it, so its eigenvalue is not being optimized - its motion is random.  The system therefore drifts through these invisible directions until it happens into a region of sufficient flatness.  Flat regions are where drift comes to rest.  This is a super well-known thing in ML but I think there are a lot of insightful angles on it and I'll reserve this discussion for a later post.

## **6. Next Time:** {#6--next-time}

The idea behind this sequence of posts is that evolution and SGD have common structural motifs.  I don't care - and probably you shouldn't either - that we can make enough assumptions to have them obey the same equation.  The point is instead that they both exhibit shared phenomena - not as modelling artefacts, but as apparently convergent properties of solutions to massive optimization problems.  I think it's important to understand these, first because these convergent structures possibly make a form of sparsity/interpretability a convergent property of the solutions to either.  Second though, is the converse - that if we observe something interesting in SGD *and* evolution, then it cannot tell us anything about the idiosyncratic properties of SGD, neural networks, data structure, or cognition.

Later posts will talk in *much* greater depth about analogies between bio and ML.  After that, I'll take you to the speculators' corner for some speculating on whether common ML phenomena are usefully understood as paralleling phenomena from evolution.

A few fun ones:

- **Additivity and averaging.**  Genomes are selected to keep mutations useful across genetic backgrounds - recombination demands it.  The fact that checkpoint averaging and model soups work at all looks like the response to a similar demand.  This is, I think, a lot deeper than it sounds, and relates to plasticity, noise robustness, steering vectors etc.
- **The Hydra effect.**  Ablate an attention head and downstream circuitry compensates.  Biology's degeneracy and regulatory buffering suggest how this kind of self-repair arises from optimization under noise, rather than being engineered.
- **Selective sweeps.**  Subliminal learning and emergent misalignment look like a sweep dragging linked variation along with it - hitchhiking in trait space.
- **Facilitated variation.**  Conserved core machinery plus cheap regulatory knobs, and whether late training increasingly adjusts routing over reusable circuits rather than the circuits themselves.  This suggests LLMs might be 'a few core circuits plus a ton of circumstantial regulators and error-correctors' - I'm thinkin' on just what this should look like still.

[^1]: Mathematically, you can understand this from the perspective of secular perturbation theory.  This is at least sometimes a useful mathematical tool in ML, but I haven't fully thought through a general theory.  For a good, if non-biological, example, see ['central flows'](https://centralflows.github.io/).  I'd be curious if one could somehow think of batch noise this way, but seems dubious to me.

[^2]: Tldr, you can write a nonlinear kernel evolution problem as a hierarchy of linear kernel problems - feature-functions are fit to meta-features, meta-features to meta-meta-features, etc.  Skipping details, on a new observation, you update your inductive bias on how to update your inductive bias on...  Roberts and Yaida's PDLT book does this perturbatively for MLPs.
