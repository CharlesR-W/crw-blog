---
title: "Slouching Towards Interpretability: Thinking About Computation in LLMs"
date: 2026-11-14
math: true
tags: [unlisted]
---

I started writing this essay to share some thoughts on how to reconcile the idea of circuits with gradient descent.  In doing this, I've come to change my perspective pretty substantially.  The first half of this essay engages a Darwinian picture of circuits, but I think the central point - that we need a clearer ontology of computation in neural networks - holds without reference thereto.

Before, I was thinking about circuits as 'units of selection' - the kinds of things which engage in some gradient-hacking shenanigans to save themselves from gradient descent.  I don't think this picture is unimportant or unhelpful, but I've come to think that it sidesteps the hard part of the problem - that the things the circuit Darwinism picture takes for granted are the confused parts, and I think therefore the more insightful to examine.  I have gone from thinking "circuit Darwinism, but we need to formalize how to delineate the circuits" to "things that under circuit Darwinism seem like implementation details are actually the deep source of confusion, and we should treat these as _the_ problem".  I'll aim to convince you that this change in perspective is the right direction to head in.

I wrote this essay in three parts, plus what became a companion post.

- The companion post is the ['Grimoire of Deep Learning'](https://charlesr-w.github.io/crw-blog/Grimoire-of-Deep-Learning/) - things I think a mental model of wtf is happening in deep learning has to explain.  While it informs later discussion, it is mostly separate from the present piece.
- The first part offers two pictures of where circuits come from - "prune" and "precipitate" - and three conceptual problems I think a good theory of circuits has to solve.
- The second part discusses some problems in specifying circuit Darwinism adequately - the model predicts very differently depending on what _precisely_ we think circuits are, what the environment is, etc. and the naive guesses don't seem consistent.
- In the third part, I'll outline an incomplete synthesis of how we get to 'defining circuits' - it takes the 'circuits live together, die together' intuition and works backwards: 'where do we look and how to find things that are selected together?'.  This proto-synthesis has a lot of exciting connections to, i.a., neuroscience and dynamical-systems inference; for our purposes, the precise details are less the point than the fact that the richness of the problem should reveal how much confusion was hiding in 'implementation details'.
- In the epilogue I envision a 'fundamental theory of interpretability' sufficient to argue for itself.

For highest value-to-engagement-demanded ratio, I recommend reading: part I (all parts), part II.e (the summary), the intro of part III, its summary III.d, and the Epilogue.

Part III has the most direct bearing on mechinterp and should be readable on its own, if that is your preference.

---

**Contents**

- **I. "Prune" or "Precipitate": Conceptual Problems in Specifying the Circuit Analogy**
  - I.a. "Prune"
  - I.b. "Precipitate"
  - I.c. Conceptual Challenges
  - I.d. Grimoire of Deep Learning: an Invitation to Confusion
- **II. Problems with the Initial Circuit Ensemble**
  - II.a. Infinite-Data Loss Implies a Decaying Circuit Population
  - II.b. Full-Batch GD (Mostly) Discredits Batch-Variance Selection
  - II.c. LLM Training Is Too Fast to Be Mostly Darwinian
  - II.d. Circuit Darwinism Fails to Predict the Importance of Fresh Data
  - II.e. Summary
- **III. From the Neuron Up: Reservoir Computing, Coherent Sets, and Spectral Clustering**
  - III.a. Reservoir Computing, Expansion Coding
  - III.b. Neurons Read Coherent Sets?
  - III.c. A Whiff of Unity: Activation Cells, Coherent Sets, and Spectral Clustering
  - III.d. Summary
- **Epilogue: Kritik of Fundamental Interpretability**

---

# I. "Prune" or "Precipitate": Conceptual Problems in Specifying the Circuit Analogy

In this first section, I'll frame the distinction by offering two visions of 'where circuits come from', and showing how this ostensible implementation detail ends up suggesting fundamentally different models.  The first mental model I offer I call **"Prune"** - a naive circuit Darwinism that presupposes an **'initial circuit ensemble'** amongst which competition occurs.  The second I call **"Precipitate"**, where circuits are 'grown' from the bottom up (roughly), as a crystal might be precipitated from solution.

I'll argue that the "Prune" picture requires a much greater specification of the analogy than we can yet give.  "Precipitate" is an alternative I tried out to explain some empirical facts about deep learning and to connect to reservoir-computing models in neuroscience.  It is less confused only insofar as it is less committal to the basic abstractions under study.  Both are bottlenecked by our ability to deconfuse what _exactly_ we mean by 'circuit'.  I'll argue that the ability to characterise persistent structures is _the_ central conceptual problem.

![Whiteboard sketch: the 'prune' picture](https://charlesr-w.github.io/crw-blog/assets/images/lw/Gradients-and-Circuits/prune.jpg)
*"Prune": the initial circuit ensemble*

## I.a. "Prune"

**"Prune"**: This picture envisions the randomly initialized model as a tangled mass of circuits with arbitrary connections.  It understands training as a process of pruning and re-allocating circuits and the connections between them.  The reason it is useful to think this way is that it lets one straightforwardly apply the ideas of neural Darwinism - one imagines circuits competing for gradient, building gradient-barriers around themselves, etc.  One can also then use the language of multi-level selection to talk about composition of circuits.  I have [written lovingly](https://charlesr-w.github.io/crw-blog/Coalitional-Darwinism/) about how evolutionary-transitions theory could be used to think of composed circuits as coming to form a higher-level unit of selection.

When I think this way, I'm much more likely to think about looking for 'functional units' and their identification - it's more weight-space than activation-space in spirit.  The most important posit of this theory is the **'initial circuit ensemble'** - it tells us how 'dog ear' circuit wins over 'airplane nose' circuit, but not how either came about, nor how to identify or localise these circuits.

## I.b. "Precipitate"

![Whiteboard sketch: the 'precipitate' picture](https://charlesr-w.github.io/crw-blog/assets/images/lw/Gradients-and-Circuits/precipitate.jpg)
*"Precipitate"*

**"Precipitate"**: This picture imagines the untrained network as a formless _prima materia_; development occurs mostly layerwise/stagewise, with many small (and nearly independent?) functional units.  Circuits are _grown_, so the functional units are defined by their co-selection as much as anything.  One reason to think this way is that it has connections to the biological theory of reservoir computing (for which v.i.), which describes how we can use random functions to do computation - the random functions are substrate not structure.

Because there are many libraries of random functions which we expect to be trainable to perform the same computation, this suggests we look instead at the dual - whatever the weights, similar programs should process data similarly: we ask what _processing steps_ are done to the data, and trust that we can sort out _who_ processed it later.  This is the natural way to factor out the problem of irrelevant microstructure I mentioned in my [previous essay](https://charlesr-w.github.io/crw-blog/What-if-not-Circuits/).  The spirit is to throw locality and modularity overboard, and [find them a few weeks later where we least expect](https://en.wikipedia.org/wiki/Polycrates#Polycrates'_ring).

This picture has been useful to me less because it answers questions or better specifies the abstractions in question, and more because 'what if it's all slightly modified random functions' forces me to think much differently about looking for structure in the weights.

## I.c. Conceptual Challenges

These models offered, I'll next outline three places where I think we need *technical progress to achieve conceptual clarity* - the right microscopes.  These are things I think a good theory of circuits should incorporate, but for which we don't yet have good language.  Of course, these are only the ones I currently have the wherewithal to see, as I am not yet a very incisive conceptual thinker when unguided by math - "who knows the words sees double" and all.

The first is **scale-sensitive entity delineation** ("at coarseness level 2.3, this weight is 90% part of circuitA and 1% part of circuitB and circuitC", "at coarseness level 2.3, circuitA and circuitB are 12% overlapping").  We need this because neural networks are messy, so obviously we should be asking 'scalar' questions instead of binary 'yes/no', and because circuits should compose, we need a scale parameter to set what 'size' of circuit we're looking for.

The second is a notion of **similarity between implementations of a computation** - ideally general enough that we could compare Mamba, LSTM and GPT implementations of 'the same circuit' ("the Mamba and the LSTM both learned grade-school multiplication, but the GPT learned Karatsuba multiplication" h/t [Erez Abrams](https://www.lesswrong.com/posts/mMERyrvEJ4xbiozie/what-if-not-circuits?commentId=K5eFB2imWZibS8hoy)).  This is necessary to solve the "irrelevant microstructure" problem mentioned earlier - we want to 'factor out' the spurious implementation details.

Third and finally is a notion of **expressivity as a resource**.  The idea here is that ReLU (or whatever) is a very simple function.  It is presumably the case that if we had far more expressive neural layers (e.g. [ones which solve convex optimization problems](https://web.stanford.edu/~boyd/papers/pdf/diff_cvxpy.pdf)), we should expect computation to be organized very differently.  One idea I have considered recently is what it would look like for neural networks to be bottlenecked by *computational expressivity* rather than a *concept/neuron ratio* à la superposition.  In reservoir computing (v.i.), neuron count is the number of pulls you get at the random-function slot machine - more neurons means _larger repertoire of computations_ rather than more storage.  Of the three problems outlined here, this is the one which I've thought least about.

To paraleptically mention the mathematics I've been using to _identify_ (as opposed to solve, lol) these problems: I think of entity-delineation through the lens of spectral clustering and coherent structures.  Computation-similarity I have been thinking about with realization theory and Hankel methods.  Expressivity-as-resource I have been thinking about through Galerkin projections of the Koopman operator.

(no, Claude didn't write that; I really am just this way...:') ).

## I.d. Grimoire of Deep Learning: an Invitation to Confusion

In early drafts of this post I had a big list of surprising findings about how deep learning works (which I expect to be probably directionally correct) which I think any theory has to reckon with.  I've instead broken this out to [a separate post](https://charlesr-w.github.io/crw-blog/Grimoire-of-Deep-Learning/).  The main ideas are summarized here:

- There's probably a qualitative difference between **"early" and "late" training**, with early training being more 'formative' than late training.  Tentatively, early training sees 'representation formation', while late training 'sharpens' these representations.
- Lots of things appear to be **architecture independent** in a meaningful way, perhaps including even the overall structure of the learned representation.  I forget who said this, but I've heard it said that "talking to Claude is talking to its training data".
- Models are **robust** to really strange kinds of ablations, and this makes it hard to imagine a layer as secretly implementing one step of a boolean circuit.  There's probably an implicit tradeoff between 'learning new computations' and 'denoising or becoming more confident in old ones'.
- **Gradient flow (with no noise etc.) at least kinda works**, so whatever our explanation is, it should at least kinda work if we assume that training can _never_ cross a loss barrier.

---

# II. Problems with the Initial Circuit Ensemble

In this section, I'll talk about some problems with a strong form of circuit Darwinism which I've dubbed the 'initial circuit ensemble'.  These 'problems' will all end with the conclusion "that's fine - in fact we can fix it by making one of three plausible simple assumptions about the _precise_ analogy we're making to neural networks".  My thesis here is that we can't yet make the Darwinian analogy precise enough to think clearly with it; figuring out 'what circuits are' is the core conceptual and technical problem.

We will take the 'initial circuit ensemble model' to have two important propositions:

- the network is conceived of as being made entirely of circuits
- these circuits are present from initialisation, or we can otherwise take for granted their existence

Problems with the initial circuit ensemble:

- the infinite-data, finite-parameter loss limits the total amount of selection; squaring this with adaptation is hard
- full-batch training works far better than would be expected by selection-for-selectability arguments
- LLM training takes place in _extremely_ few steps compared to what we'd expect from evolution, especially if we think of grokking as a baseline
- the theory cannot explain the importance of fresh vs. stale data, and in fact selection-for-selectability arguments suggest the opposite effect.

Put another way, we're confused about what the 'population' is, how circuits adapt, die, or replenish, what 'the environment' is, and what the right unit of time is - the naive identifications mostly don't work.

I'll also add that there are many effects which I think are important discussed in the [companion post](https://charlesr-w.github.io/crw-blog/Grimoire-of-Deep-Learning/) which our underspecified circuit Darwinism just can't engage with usefully, especially the early-/late-training distinction.[^cut-mechanisms]

## II.a. Infinite-Data Loss Implies a Decaying Circuit Population

Here I'll argue that we can only explain the infinite-data loss by positing a decaying effective-population of circuits - otherwise circuit Darwinism predicts continued improvement from **endogenous competition**.[^relative-fitness]

Consider the [Chinchilla](https://arxiv.org/abs/2203.15556) scaling law

$$L = L_{irred} + A N^{-\alpha} + B D^{-\beta}$$

with $$L$$ the loss, $$N$$ the parameter count, and $$D$$ the amount of data.

We see that for infinite data, there remains a contribution from the number of parameters.  By default, for fixed circuit size, the number of parameters is something like the *number of parallel selection events*, and so should set the _rate_ of competition, but have no definite effect on its outcome.

I think the simplest explanation for this (though it has other problems matching the scaling law!) would be to imagine that the circuit population *decreases over time* (perhaps as circuits aggregate into bigger units, or are simply selected away) - eventually, there are $$O(1)$$ circuits left and no further selection can occur.  This lets us predict an $$N$$-dependent saturation.  It also predicts that the _rate of selective progress_ should decrease as $$N$$ does, but I'm not comfortable equating that to loss-reduction and don't have a better guess.

This isn't the end of the world, but we now enter the territory of having to think about circuits dying vs being absorbed, and how the size of circuits should change over time, and whether they eat the parameters that would otherwise give rise to new circuits - these are things that could happen, and it would be useful to think of them in Darwinian terms - the problem is that we're expanding the number of alternative things our model can predict while we have no way of measuring or identifying which of those things actually win out.

That is to say: not a dunk on circuit Darwinism - but a point for needing more microscopic understanding of variation so we can get the rules of the game straight.

## II.b. Full-Batch GD (Mostly) Discredits Batch-Variance Selection

Circuit Darwinism imagines that circuits compete with one another - and in particular we should hope that there is some mechanism by which 'more general' circuits outcompete 'less general' ones, so that we can explain generalization.

One of the ways I liked to explain this was by positing that, imagining we have several circuits competing to fulfill the same function, we should expect the general one to have a low per-sample gradient, while the more memorize-y one might depend on a precarious balancing of positive and negative pulls from samples in a given batch.  This **batch-variance selection** corresponds schematically to the [Bergstrom–Lachmann](https://arxiv.org/abs/q-bio/0510007) effective penalty for having a fitness which varies.

This seems to be discredited by the fact that full-batch GD [works at least somewhat meaningfully](https://arxiv.org/abs/2109.14119) (see [companion post](https://charlesr-w.github.io/crw-blog/Grimoire-of-Deep-Learning/#ic-pathology)) in image and language models.  Of note is that the Nanda grokking paper also uses full-batch - as best I can tell, grokking relies on the regularization to work, not batch noise.

To be clear, other types of things like [EoS](https://arxiv.org/abs/2103.00065) could select to prefer less noisy circuits, but the hope of _batch_-variance selection was that we could imagine this as leading to generalization by being like 'test the organism in many environments'.  We certainly have 'make this organism robust to mutation' effects still, but just in a generic not-related-to-environment way.  It becomes harder to imagine selection-for-selectability occurring, which I've hitherto understood as synonymous with 'generalization' in Darwinism.

There are of course other ways we could imagine selection for generalizable circuits occurring, perhaps because more generalizable circuits produce outputs which are 'useful to more downstream tasks' or something like this, but the fact that batch noise seems to be merely important rather than the *sine qua non* of generalizability makes it hard to think of batch-noise as environment variation as generalization-pressure.

This shouldn't be overstated: [gradient flow](https://arxiv.org/abs/2107.06608) only works if you try _really hard_ to make it - full-batch GD is pathological but still works within reason.  This means we need a theory that at least kinda works without selection-for-selectability, at least in the sense I had imagined it.

## II.c. LLM Training Is Too Fast to Be Mostly Darwinian

Next I'll argue that the number of optimization steps in frontier LLM training runs makes it implausible that Darwinian competition is the best description of what is occurring.  The numbers here are all _extremely_ sus - I tried to save you the thirty footnotes that would add caveats - but I'm confident in the overall "deep learning very fast, evolution very slow - needs explanation".

First note that the grokking experiments in the [Nanda paper](https://arxiv.org/abs/2301.05217) show grokking time on the order of 5k epochs (iiuc getting grokking requires a bit of fiddlin' with the parameters, so *cum grano salis*).  If you squint, [TMoS takes about the same](https://transformer-circuits.pub/2022/toy_model/index.html#learning)[^tmos-time], plus-or-minus an OOM.

More substantively: a quick google says training [GPT-3](https://arxiv.org/abs/2005.14165) took about 100k steps.  Presumably this varies by several OOMs for frontier models - this is just an existence proof.  If we imagine grokking as the prototypical "competition between circuits selects for the more general one" event at 5k steps, GPT-3 gets twenty 'rounds' of selection.

Compare this to [Haldane's limit](https://en.wikipedia.org/wiki/Haldane%27s_dilemma), which suggests that a population can manage only about one adaptive substitution per 300 generations.[^haldane-different-quantity]  Though it does violence to our analogy between LLMs and population genetics, ~2M params per step (175B params / ~94k steps) vs. 100 steps per param is enough OOMs to make the qualitative point - _evolution is slow_.

Let's do another egregiously simple comparison to ensure that anyone that knows anything hates me: suppose the human brain has 100T params (100B neurons and 1k synapses per), with a tick time of 100ms - fixing 2M params per step means $$5 \times 10^6$$ seconds - 2 months, give or take some OOMs, lol.  So in terms of train time "brain is closer to LLMs than evolution".

Again, this is easily patched by, say, talking about the number of _parallel_ queries, or taking the 2M parameters fixed to mean like '1 parameter per circuit', etc.

But then we again enter the frustrating realm of needing to specify very precise details that we don't have the ability to check - 'is competition between all the circuits at once?  or in small groups doing similar functions?'.

## II.d. Circuit Darwinism Fails to Predict the Importance of Fresh Data

Finally, I think the thing that's hardest to explain under circuit Darwinism is the importance of fresh data.

Evolution doesn't really have a role for something like the amount of data $$D$$ - we only get to smuggle it in by assuming compute-optimality and treating it as 'time'.  If we try to think of $$D$$ as the 'amount of unique environments' our little tamagotchi circuits are selected under, one can recover a prediction that the final loss should depend on $$D$$, but there's no way to reconcile this with the fact that the loss reduction [falls to nearly zero](https://arxiv.org/abs/2305.16264) after ~16 epochs.

My favorite mechanism for how you could get generalization from circuit Darwinism is '[selection for selectability](https://charlesr-w.github.io/crw-blog/Selection-for-Selectability/)' (S4S) - it is precisely this repeated oscillation of the environment that drives selection-for-selectability (related to generalization), and this effect is parametrically small compared to instantaneous selection, so we would predict that many _epochs_ of training would be needed to saturate the usefulness of data.  We could have said that ackshually the environment fluctuation is batch-noise, but as I argued above this seems wrong too.

So we're confused about how exactly to think about 'environment variation' over time.  A blind spot I haven't talked about at all is that we can't usefully address the comparative importance of endogenous competition vs environment change for adaptation.

## II.e. Summary

I've argued that thinking usefully of circuit Darwinism requires us to be much more specific about the detailed ontology of the theory than we are ready to be.

Scaling laws imply a finite reservoir of variation on which selection can occur, so we have to provide an account for how we can get enough 'interesting' variation that Darwinism is useful while also predicting its limitedness.

We can't understand batch-noise or epochs of training as directly representing environmental variation in the way that lets us get selection-for-selectability effects, so it would have to come from some other unit of time.

Finally, training an LLM takes extremely few steps.  Selection-for-selectability (which my mental model hitherto identified with generalization) is parametrically slow - e.g. if 'environments' were different kinds of documents for an LLM, it would scale with the number of documents rather than tokens.  We need to drop S4S or posit that the correct 'unit of time' isn't the optimizer step.

In sum, to think usefully about any kind of circuits competing or doing interesting Darwinian stuff, we need to get much more precise about the analogy, and we simply don't have precise enough definitions to make the predictions that would test between these different versions of the model.

This section is in essence an argument that 'wtf is a circuit' is _the_ core confusion, conceptually and technically, rather than an implementation detail.

Onwards!

---

# III. From the Neuron Up: Reservoir Computing, Coherent Sets, and Spectral Clustering

In this section I'll talk about two threads that have fed into my thinking about how we can talk about functional units arising in LLMs.

First I'll discuss two related ideas from neuroscience, '[reservoir](http://www.scholarpedia.org/article/Echo_state_network) [computing](https://doi.org/10.1162/089976602760407955)' and '[expansion coding](https://doi.org/10.1016/j.neuron.2014.07.035)'.  Then I'll relate this to kernel learning on random functions - we'll see that 'real learning' lives in the changing of these random functions, which corresponds to a network updating its inductive biases.

Next I'll change tack and present a toy model of a neuron that learns to predict its next input, and relate this to a more general technique called spectral clustering.  This motivates looking at activations and asking how we can think about the network 'treating some group of data points the same' - as a warmup for finding functional groupings like circuits.

I'll then draw on an empirical observation about LLM activations to motivate a relaxed version of spectral clustering in activation-space.  The idea is to imagine coherent sets of activations as coarse-grained 'computational states'.  A work in progress.

Two things to note: first, there's a bit of a jump after part a - I don't know how to connect the ideas in this part yet, but they have been very influential to my mental models.  Second, in III.c I'll write about how I've been thinking about this theory in activation-space.  [This post](https://www.alignmentforum.org/posts/gYfpPbww3wQRaxAFD/activation-space-interpretability-may-be-doomed) outlines conceptual problems to activation-space interpretability (though I think these mostly do not apply for my purposes).  Please do not feel deceived - I too want a theory of circuits, and hope to develop the theory to get us back to weight-space++ soon.

## III.a. Reservoir Computing, Expansion Coding

**Reservoir computing** is a model in neuroscience that attempts to explain how a big ol' soup of randomly connected neurons can usefully store and retrieve patterns.  [This YouTube video](https://www.youtube.com/watch?v=cDxtFtoQVNc) describes it well.  The short of it is that each neuron is essentially a random function (the soup's weights are assumed fixed, and they're all recurrent-y, not layerwise); then each pattern you want to learn is a linear readout of the neurons.  It seems [part of the hippocampus](https://doi.org/10.1016/j.neuron.2019.01.044) and [fly olfactory bulbs](https://doi.org/10.1016/j.neuron.2017.01.030) do something like this![^dasgupta-fly-hash]

This turns out to be more-or-less equivalent to kernel learning with random features in ML!  Both learn $$y_{out}(w) = \sum_i w_i \phi_i$$, with $$\phi_i$$ your random functions (in ML these are probably vectors, but in reservoir computing they're functions of time).  This is cool!  Random-feature kernel learning feels pretty primitive to us in the deep learning age - the first main point here is that we can show that learning is really possible if you just take a linear readout on sufficient amounts of random bullshit - i.e., there _is no circuit-like structure_ anywhere, and we can still do something useful.

The second point is more macro-level.  We know that [random-feature learning has scaling laws](https://arxiv.org/abs/2210.16859)[^bahri-scaling] _AND_ we know that for a technical definition of 'learn', these kernel learners do _not_ 'learn'.  In particular, we can understand kernel methods as never updating their 'inductive biases', while other methods do. See [_The Principles of Deep Learning Theory_](https://arxiv.org/abs/2106.10165) (ch. 10–11) for this formulation of inductive bias.  It is possible to get scaling laws while definitely not learning, and neuron soup just about does this.

A close-by idea I've found useful is **'expansion coding'**.  This is a coding scheme where computation is done primarily by computing a bunch of random functions of your inputs, and hoping _one_ of them is useful.  I.e., it's basically the same thing as above just with less contextual baggage.  On this picture, you compute $$\mathrm{XOR}(a,b)$$ by computing enough random functions $$\phi_i(a,b)$$ that hopefully _one_ of them is at least _sorta_ doing XOR, then just picking that one.

Insofar as representational superposition / sparse-sensing are what you should do when you have many more concepts than neurons, expansion coding is kiiiinda opposite - it's what you should do if *computational expressivity* is super limited but you have neurons out the wazoo.

In the [companion post](https://charlesr-w.github.io/crw-blog/Grimoire-of-Deep-Learning/#ia-earlylate-training), we talked about **NTK fitting-vs-rotation** as being one way of thinking about 'early' and 'late' training being very different.  Here we can note that reservoir-computing is approximately the same as the NTK regime.  What we want is a story that interpolates from "fitting random functions" to "[memorizing n-grams](https://arxiv.org/abs/2402.04362)" to "simulating the universe".

I'll also gesture noncommittally to the (contested) [lottery-ticket hypothesis](https://arxiv.org/abs/1803.03635) - the idea of which is that you can usually find a tiny sub-network inside your network such that if you [_rewind_ training](https://arxiv.org/abs/1912.05671) and prune everything else, only training that network suffices to get you most of the loss-reduction.  This suggests that there's some grounds to imagine starting with a big bag of random functions and modifying them.

I'm not confident in this, but I think we have not thought enough about what it would look like for networks to be bottlenecked by computational expressivity rather than representation capacity.

The two models above have been influential in my thinking.  In the next sections I'll try to get much more specific and explain how we might think of neurons as 'detectors of coherent sets' - I apologize that I can't yet draw a more direct connection between these two halves of the picture, but hopefully each is informative :)

## III.b. Neurons Read Coherent Sets?

Back in the [good](https://research.google/blog/inceptionism-going-deeper-into-neural-networks/) old [days](https://distill.pub/2017/feature-visualization/), we thought a lot about 'receptive fields' of neurons - what kinds of things activate them?  Here's one trivial idea: "the input weights of a neuron divide input-space into regions, and the neuron's activation is a scalar membership score for that region; then in proportion to that membership, the input-activation gets nudged in a direction fixed by the neuron's output-weights".

Now without going too much into detail about [my special interest](https://youtu.be/831Ell3QNck)[^hankel-greentext], there is a way to see this trivial observation from a very different angle.  In [this paper](https://arxiv.org/abs/2510.26955), they analyse a neuron which reads a single scalar input signal $$I(t_n)$$ and predicts $$I(t_{n+1}) \approx \mathrm{nonlinearity}(\sum_i w_i I(t_{n-i}))$$.  Roughly, the $$w_i$$ should come from the singular vectors of the time-evolution matrix and go 'ping' when it sees a similar pattern - morally, the neuron gets a vector of inputs $$I(t_{1:n})$$ and goes ping when that vector is in a coherent set.

In case the math lost you, the one-liner: **the receptive field of a neuron is a [_coherent set_](https://en.wikipedia.org/wiki/Lagrangian_coherent_structure) of its input-space**.

While I am trying very hard to write no additional math about my favorite thing in the world, I had already drawn Niels the neuron teaching coherent set detection when I decided to cut down the math. Niels, presumably in collaboration with your LLM, explains:

![Whiteboard sketch: Niels the Neuron and the Hankel matrix](https://charlesr-w.github.io/crw-blog/assets/images/lw/Gradients-and-Circuits/niels-hankel.jpg)
*Niels the Neuron explains how the SVD of the delay-embedding Hankel matrix is spectral clustering on input-patterns; after [Pughe-Sanford et al. 2025](https://arxiv.org/abs/2510.26955)*

These coherent sets are important to us neuron-enjoyers because they are the sets which are in some sense the most predictive of future state - they're an **approximation to the optimal coarse-graining**, forgetting as much microscopic detail as possible (where in the set the point was) while remaining maximally useful for predicting the future macroscopic state (i.e., the particle is still in the set and the set hasn't much changed shape).

![Whiteboard sketch: spectral clustering and receptive fields](https://charlesr-w.github.io/crw-blog/assets/images/lw/Gradients-and-Circuits/spectral-receptive-fields.jpg)
*Spectral clustering triptych: similarity-graph → eigenproblem → partition the thing into different regions*

Btw, as in the picture, 'spectral clustering' is when you take some graph, find eigenfunctions on it, and then use those eigenfunctions to 'segment' it into clusters - I mention this later, but I consider this admissible as an interpretability technique because it's essentially an SVD.  It is 'the most complicated thing that still counts', because SVDs are great, so the argument reduces to arguing that you're SVD-ing the _right thing_.

## III.c. A Whiff of Unity: Activation Cells, Coherent Sets, and Spectral Clustering

[The dream of interpretability](https://www.lesswrong.com/posts/3eo4SSZLfpHHCqoEQ/dmitry-s-koan) is to be given a knob, call it $$\beta$$, such that making it very small lets you resolve very coarse structure very cheaply, and that, tuning it up, you can resolve finer structure at increasing computational cost.  Ideally, you can focus your efforts on a particular behaviour rather than the whole model, and spend your limited computational power analysing particularly important computations (presumably of the alignment flavour).

My collaborator and I have spent the last few months, i.a., looking at the [activation cells](https://www.lesswrong.com/posts/LajDyGyiyX8DNNsuF/interim-research-report-activation-plateaus-and-sensitive-1) in LLMs.  These are Voronoi-like cells in activation-space such that points in the same cell are treated in essentially the same way by the network.  Our aim has been to figure out if we can understand these as _discrete states of some computation_ - if so, we could reduce the model to a table of transition rules (presumably not perfectly!), which would then be the natural thing to analyse.

![Figure 1 from Janiak et al.: Voronoi-cell-like structure in the residual stream](https://charlesr-w.github.io/crw-blog/assets/images/lw/Gradients-and-Circuits/image-2.png)
*Figure 1 from [Janiak et al.](https://arxiv.org/abs/2409.17113): Voronoi-cell-like structure in the residual stream of LLMs*

In part because of tractability issues, in part because of theoretical connections between computation identification and Hankel methods, and in part pursuing the intuition that we should be looking at 'points the network treats the same', we're working on developing a technique which analyses clusters of data-points building on this perspective.

![Label propagation on a similarity graph of MNIST digits](https://charlesr-w.github.io/crw-blog/assets/images/lw/Gradients-and-Circuits/zgl-harmonic-graph.png)
*Label propagation on a similarity graph of MNIST digits; from [this paper](https://mlg.eng.cam.ac.uk/zoubin/papers/zgl.pdf).*

Activation cells are groups of points the network 'treats similarly'; old ML has a family of methods called **label propagation** where it'll propagate the labels of known data-points to unknown ones through a similarity graph - you can sorta-kinda-don't-think-too-hard-about-it understand the activation cells as perfectly-isolated groups of points - label prop from training points to any test points that happen to be nearby.  The core idea is to zoom out and look at a much more macroscopic similarity-graph on activations.

I've outlined the idea in this image.

![Whiteboard sketch: towards spectral clustering for interp](https://charlesr-w.github.io/crw-blog/assets/images/lw/Gradients-and-Circuits/towards-spectral-interp.jpg)
*Coherent sets of activations are those the network 'treats the same' between some specified layers L' → L*

While I'm trying to practice writing without math, I'm well aware that "I drew it on the whiteboard" strains credibility if you don't know me well enough to know that I have cut >2000 words on Hankel matrices from drafts of this post.  As bona fides, here's a teaser of the method applied to ResNet18+CIFAR10.  Preliminary, working on the writeup, but proof of concept.

![ResNet18 on CIFAR-10: UMAPs of activations across layers and training times, coloured by four coherent sets fit at t=2500 (left); class composition and representative images of each set (right)](https://charlesr-w.github.io/crw-blog/assets/images/lw/Gradients-and-Circuits/image-1.png)

Here we fit data-points into 4 coherent sets based on how they move through the first ~half of the network at t=2500 steps; we color the corresponding points for all other times and layers.  The left is just UMAPs of the activations.  The right is class composition and representative images of the four coherent sets.

Eyeballing, it seems to be ~separating things by background colour.  Once I earn it, the desired interpretation is something like "at time t=2500, at the resolution scale of 4 coherent sets, the first half of the network seems to treat points similarly according to their background colour".  Again, work in progress.

## III.d. Summary

Okay so in this section I've covered two big ideas: first, what reservoir computing has to tell us about how random neural networks can work (and how this is like NTK learning) and what it might look like for a network to be bottlenecked by computation rather than by representation; second, how we can think of the natural operation of neurons as spectral clustering, and how spectral clustering and coherent structures are a natural language for characterising how a neural network treats data en masse.

I think expansion coding and reservoir computing are important as, in spirit, an alternative perspective to the superposition hypothesis.  Schematically, superposition imagines networks are bottlenecked in the number of neurons they have or concepts they can represent while taking for granted that computations can be done on these concepts.[^comp-in-sup]  Expansion-coding is, i.a., a story of how neural networks can work if neurons are cheap but computation difficult or inexpressive.  I like it mainly because this is very contiguous with what we know to be the case for NTK-regime-learning.  I'm not sure how to make it more substantive or bridge to the coherent structures bit yet.

The coherent structures / spectral clustering thing is much more substantial as a framework for thinking about what neurons are doing and how they encode information.  In particular, my most curmudgeonly fundamental-interp-research opinion is that the only thing that is truly interpretable is an SVD, so we need to find the right SVD, and we'll call this spectral clustering.[^why-svd]  This family of ideas makes me excited by the amount of things it's connected to - predictive state representations, realization theory, approximation of automata...  Claude dared me to add [quantum channel metrology](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.2.010343) lol.

![Meme: guy who has only seen eigenvalue decomposition](https://charlesr-w.github.io/crw-blog/assets/images/lw/Gradients-and-Circuits/boss-baby-eigen.png)
*[edited by GPT]*

The end goal has always been to find the mathematical object which tells us what the network's ontology is.  I'm excited to think about this more!

---

# Epilogue: Kritik of Fundamental Interpretability

I will close by reflecting on my aims and vision for a 'fundamental theory of interpretability'.  Briefly, and then with elaboration:

> A fundamental theory of interpretability must be complete enough to justify its ontology and argue for its own completeness.

John Wentworth has an [excellent post](https://www.lesswrong.com/posts/GhFoAxG49RXFzze5Y/what-s-so-bad-about-ad-hoc-mathematical-definitions) about Shannon's contribution to cryptography: before we knew what mutual information was, people did hacky things like making sure encrypted text had zero _correlation_ with the plaintext, but would pikachu surprise face when you could hack their cypher by using information stored in higher order correlations.  The correct answer is of course to zero out the mutual information, which captures all such effects.

Shannon did not postulate some quantity and prove that it fortuitously solves the problem of encryption - Shannon invented the language by which we _know what it means_ for an encryption to be perfect.  The argument that mutual information is the correct quantity to evaluate encryption is _inextricable_ from the argument for inventing mutual information at all - perfection by design!

This is what I want from a theory of interpretability - the theory must be able to justify its ontology *independently* of the theory's practical results, and must be sufficiently complete to argue for its completeness.

Practically, this is why the river of random math and spectral clustering and Hankel matrices and... - not a flailing for things to throw at the wall, but because I am groping after the _combination_ of ontology and mathematical tools sufficient to argue for itself.

To be useful for superalignment - modulo dropping all your chips on Big Orange 6 and spinning the wheel - we must have an interpretability which we _have the right to expect works_.  This is the thing I want from a 'fundamental theory of interpretability'.

It is a grand and humbling thing to stand confused in the shadow of this last Deep Mystery.  For this, and for those who stand with me, I am grateful beyond words.

---

"All processes that are stable we shall predict. All processes that are unstable we shall control."  — John von Neumann (attributed by Freeman Dyson)

---

[^cut-mechanisms]: an earlier version of this post intended to spend a lot of time on example calculations and mechanisms I developed to describe how circuit selection might occur - this was lengthy, technical, and minimally-enlightening.  It also didn't address the core problems of being able to _identify_ circuits.  In the end, 'prune' posits an answer to this hard problem - which can be a way to make progress of course - but I now think that this avoidance focused my attention on the wrong places.

[^relative-fitness]: more accurately, Darwinism more readily talks of relative proportions of a phenotype rather than its absolute numbers, so it doesn't often say anything about a trend in 'overall' fitness, which is a bit more the domain of population ecology.

[^haldane-different-quantity]: tbc, this is admittedly a totally different kind of quantity - a population-level substitution rate rather than a competition-timescale - my only point is that evolution is _slow_ - gradient descent is obviously qualitatively faster.

[^dasgupta-fly-hash]: see also [Dasgupta, Stevens, Navlakha 2017](https://doi.org/10.1126/science.aam9868)

[^bahri-scaling]: see also [Bahri et al. 2021](https://arxiv.org/abs/2102.06701)

[^hankel-greentext]: \>\> scrolls down \>\> sees 10 paragraphs about Hankel matrices \>\> he went into too much detail

[^comp-in-sup]: Of course, both [TMoS](https://transformer-circuits.pub/2022/toy_model/index.html) and later [comp-in-sup](https://arxiv.org/abs/2408.05451) work talk about how computation _can_ be done in superposition.  Some comp-in-sup stuff like [this thing](https://arxiv.org/abs/2607.04800) is simple enough to be plausible.  Pro tempore let's take my posited contrast as a spiritual one between representation-first and computation-first views.

[^why-svd]: I'm going to try to write about the non-shitpost version of this, but essentially it's because SVD is _the_ way to talk about one thing approximating another thing in an importance-sensitive way with bounds and guarantees.

[^tmos-time]: I had codex do some sanity checks on this and it seems to take O(10k) steps, though if you use Adam instead of SGD it takes ~100 steps.  This remained roughly true at the sparsity ratio implicit in GemmaScope (71 active of 16k = 0.4% = 7x compression).  Surprisingly, the time-to-learn is ~constant at fixed compression-ratio (num_inputs per hidden-layer neuron) - suggesting learning rate is the relevant bottleneck to superposition rather than capacity.  While we know SGD doesn't work on transformers, lest we take this as evidence of the necessity of superposition, the [Adam-mini](https://arxiv.org/abs/2406.16793) paper (building on [Zhang et al.](https://arxiv.org/abs/2402.16788)) shows this is due to component heterogeneity, and fixing a component-wise learning rate suffices to train.