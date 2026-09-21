---
title: "What if not Circuits"
date: 2026-09-21
math: true
---


*This post was written as part of the [Iliad Fellowship](https://www.iliad.ac/).  My thanks for their continued support.*

**Preface:** I'm confused about how neural networks do and learn computations.  In response to a friend's challenge, I'm writing up some interim thoughts.  This essay has four parts: the first tries to track what I call the 'default ontology' of the mechinterp community over the years.  The second part is about 'representational drift' as an important obstacle to weights-based approaches to circuits.  The third part reflects on how 'universality' should shape our explanations of LLM function.  The fourth part is a sketch of a 'co-selectionist' view of circuits I have been thinking about.  These parts share a common theme but should be readable separately.

---

I want to understand how neural networks, LLMs in particular, work.  In my research I've spent a lot of time trying to think through what _kinds of explanatory accounts_ are best suited to this.  In thinking about comparisons between evolution, neuroscience, and deep learning, I've ended up with an intuition like the following:

> Large-scale learning processes like deep learning or the brain are different in kind from computers or assemblies of circuits.  'Circuits' and 'computation' are not the natural ontology for understanding what is happening inside LLMs.[^crisp][^static]

This post is an attempt to communicate what I mean (part I), why I have this intuition (parts II and III).  Part IV is a sketch of a perspective on circuits as emergent 'units of selection'.

[^crisp]: There still likely _are_ crisp traditional circuits, but they are likely in the minority.  More importantly, I have a hard time visualizing evidence that would settle the question 'how much of Claude is circuits' satisfactorily.

[^static]: A tentative reason for this: humans design circuits to be modular and predictable - see ['static discipline'](https://en.wikipedia.org/wiki/Static_discipline) for digital circuit design.  Evolution typically learns to operate in spite of noise, or even use it as in e.g. [kinetic proofreading](https://en.wikipedia.org/wiki/Kinetic_proofreading).

**Contents**

- [I. What Might We Mean By "Circuits"?](#i-what-might-we-mean-by-circuits)
  - [I.A. Definitions](#ia-definitions)
  - [I.B. Circuits, Features, and MechInterp](#ib-circuits-features-and-mechinterp)
- [II. The Central Problems of Noise and Representational Drift](#ii-the-central-problems-of-noise-and-representational-drift)
  - [II.A. Representational Drift in the Brain](#iia-representational-drift-in-the-brain)
  - [II.B. Representational Drift in Neural Networks](#iib-representational-drift-in-neural-networks)
- [III. Developmental Motifs Circumscribe Notions of 'Circuits'](#iii-developmental-motifs-circumscribe-notions-of-circuits)
  - [III.A. Neurotrophins and Microstructure](#iiia-neurotrophins-and-microstructure)
  - [III.B. Back to Neural Networks](#iiib-back-to-neural-networks)
- [IV. A Co-Selectionist View: Circuits Move Together?](#iv-a-co-selectionist-view-circuits-move-together)

---

## I. What Might We Mean By "Circuits"?

### I.A. Definitions

Definitions are important - here I'll lay out what I think are the core components of the circuit ontology.  The central thesis is something like:

> Trained LLMs are well thought of as programs - they consist of a collection of algorithms and heuristics, implemented in a way that is functionally modular and likely sparse in an appropriate sense.  These functional modules are circuits; they turn a semantically meaningful input into a semantically meaningful output by an in-principle-understandable algorithm.  Given enough effort, we could decompile an LLM into readable Python code.

There are a lot of live variants.  The most important axes of variation that come to mind are:

- **Sparsity**: Is sparsity (in any sense) a property we expect the model to 'have', or a pragmatic interpretive lens?
- **Semantic Bootstrap**: How do we bootstrap 'semantic meaning' from the inputs or outputs?  Or is there some better, _mainly functional_ criterion for identifying circuits?
- **Regime Dependence**: Should our explanations be allowed to depend on the training data distribution?  That is, must the explanation hold on arbitrary inputs?
- **Metric of Faithfulness**: If causal intervention is the gold standard for 'explaining' a circuit, against what should we measure shortfalls of such an explanation?  E.g. loss, downstream behaviour.
- **Localizability**: Should the 'circuit' be spatially localizable within the model - to, e.g., a handful of attention heads?  If so, must those units' behaviour be completely described by their action within that circuit?
- **Modularity / Isolability**: How do we distinguish between 'two circuits composed' and 'one big circuit'?

First, note that the question of circuits is in principle distinct from theories of representation - the latter being 'feature directions', the '[linear representation hypothesis](https://arxiv.org/abs/2311.03658)', etc.

Second, note that these questions are definitional as much as they are pragmatic - we're jointly unsure of what a 'circuit' should be _and_ how to look for them.

### I.B. Circuits, Features, and MechInterp

Here I'll give a rough account of how I see the interp community's 'default ontology' as having changed over time.  I think this is useful because it relates what _kinds_ of structure we thought neural networks have to _how_ we went looking for them.

I think of things as proceeding in roughly three phases, which I'll call the '**exploratory**', the '**mechanistic**', and the '**prosaic**'.  Alternatively, we might call these 'worldviews'.  The sketch below is more intellectual autobiography than history, has no pretension to completeness etc., so _cum grano salis_.

By '**exploratory**', I essentially mean 'look at the neural network, and poke it and see if you can make sense of what it's doing'.  This work had rather little conceptual baggage attached to it - it was less about 'how can we understand the model-qua-gestalt' but instead 'can we find anything understandable at all'.  It seems important that during this era, 'neural networks are just inherently uninterpretable messes' felt like a live hypothesis.  I think the best examples are things like Chris Olah's pre-transformer-circuits work (see his blog [here](https://colah.github.io/)) and also the [Distill circuits thread](https://distill.pub/2020/circuits/).[^images]

I would also tentatively put the earliest mechinterp work in this category.  E.g., the early [induction heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) work essentially avoided the 'semantic bootstrap' problem I mentioned above - that of needing to jointly assign semantic meaning to circuits' _operations_ and their _inputs/outputs_.  Their induction head metric is essentially operational - an eigenvalue statistic[^eigenvalues] - and their analysis would have worked as well on transformers which predict sheet music instead of text.

[^eigenvalues]: Claude tells me that different induction head works have used different operationalizations, some less principled than the OV eigenvalue definition.  I'm unsure if this matters for my point here.

[^images]: Having not read all of them, I understand that most(?) of this earlier work is focused on image processing instead of text.  Unsure if this is significant, but perhaps natural visualization and not having to handle the complexity of sequence models lends itself to more methodological flexibility?  Speculative.

With the advent of the LLM era, we moved towards what I'll call the '**mechanistic**' era - we finally got models that _fucking have to_ be 'thinking' for some definition of that word, and we wanted to figure out how.  I don't think anyone seriously thought they had _the_ theory of understanding neural networks, but I think the spirit of this era was that we were looking for it.  This was the era of sparsity, mechinterp, and SAEs.

The most important organizing principle people posited was 'sparsity' - the idea that for most datasets, the most natural way to compress them was to learn a big conceptual dictionary, such that a sparse subset of these would be active at any given time.  The best articulation of this idea I'm aware of is [this note in the transformer circuits thread](https://transformer-circuits.pub/2023/superposition-composition/index.html), which does a very good job tying together the intuitions from neuroscience and sparse sensing.  This line of thinking leads to SAEs and descendants.  The SAE vision focused less on circuits or computation, than on 'feature directions' in the residual stream.

Essentially all[^anth] of the later transformer-circuits thread research built on the conceptual foundation of linear representation, superposition, sparsity, etc.  The apotheosis of the SAE vision is '[scaling monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)'.  Following this, Anthropic's interp team tried harder to focus on computation and what gets 'done' with features, resulting in the [transcoders](https://transformer-circuits.pub/2025/attribution-graphs/methods.html) and '[biology](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)' work.  These are extremely cool, but also, in my opinion, go quite a bit further than SAEs in 'imposing' an ontology on a model - they train, layer-by-layer, a sparse replacement for the base model, replacing each MLP layer by a much larger layer of sparse neurons with more permissive (cross-layer) connectivity.

[^anth]: I'll note that I am probably overindexing on Anthropic's work here, even within the LW-adjacent research community.  I am unsure if this reflects their impact on the community or is just my own sample bias.

Separate from the SAE-driven cluster of things, there is also an ongoing tradition of very gears-level mechinterp.  Good examples of what I have in mind are things like '[logit lens](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens)', [automated circuit discovery](https://arxiv.org/abs/2304.14997), etc.  This 'gears-level' mechinterp is certainly 'mechanistic', but I would feel disingenuous slotting it into one of my three arbitrary worldviews/eras here - I think _looking_ for circuits assumes less about what's going on inside than do SAEs.  Redwood's [causal scrubbing](https://www.lesswrong.com/posts/JvZhhzycHu2Yd57RN/causal-scrubbing-a-method-for-rigorously-testing) was an early negative result on this approach.[^casc]

[^casc]: Causal scrubbing predates the SAE life-cycle - 'Scaling Monosemanticity' came out mid-2024, while causal scrubbing was end of 2022.  Just be aware this is a bit garbled as a timeline.

This 'mechanistic' era gave way to the '**prosaic**' around the time that the GDM mechinterp team published '[negative results for SAEs](https://www.lesswrong.com/posts/4uXCAJNuPKtKBsi28/negative-results-for-saes-on-downstream-tasks)'.  Anthropic's interp work since 'biology' has largely focused on pragmatic interpretability for really _large_ language models - training various interpretable surrogates, interpreters, or empirical studies of LLM behaviour.  I think it's fair to say that the field (at least at the frontier) drifted away from work on a "fundamental" science of interpretability - from neuroscience to biology and psychology.[^vibes]

[^vibes]: This is my read of overall field vibes; I expect this is distorted by overweighting the transformer-circuits thread, but I expect a similar effect to hold for the overall community.

'Prosaic' interpretability is based on the idea that LLMs are fucking complicated, possibly unstructured in important ways, and 'fundamental' interpretability either can't or won't get us to useful tools before we need them for alignment.  I think of this era as crystallizing with Neel and co.'s '[pragmatic vision](https://www.alignmentforum.org/posts/StENzDcD3kpfGJssR/a-pragmatic-vision-for-interpretability)', which gave us the 'pragmatic/ambitious interp' dichotomy.  Things like [natural language autoencoders](https://transformer-circuits.pub/2026/nla/index.html) (NLAs) are especially characteristic of this era - I recall them being described as 'bitter-lesson-pilled interp'.  The spirit of the era is training big interpretable ML models on top of big ML models.

To the extent this era has a 'default ontology', it's that interpretability is essentially machine-learning complete, or perhaps that there aren't (or we can't find) faithful useful accounts of model internals at scale - at least not fast enough to be useful for alignment.  On a slightly different reading, the default ontology could also be that 'interpretability' is essentially orthogonal to functionality - that LLMs are a big ol' mess in the way we once feared was true of AlexNet, and that interpretability is thus not a problem to be solved, but an additional desideratum.

So in summary, there are a handful of different ways of thinking about what structures neural networks learn.  There are exploratory methods which are reasonably structure-agnostic, circuit-discovery methods, feature-interaction methods, looping back around to structure-agnostic surrogate-model methods.  These all come from different ideas of 'where the structure is' in neural networks.  Next I'll talk about representational drift and why I think this suggests the need to 'look somewhere else' for the fundamental units of computation/structure.

---

## II. The Central Problems of Noise and Representational Drift

![Representational drift as a stochastic process, with and without statistical learning; maintaining representational structure is like herding cats]({{ site.baseurl }}/assets/images/lw/what-if-not-circuits/representational-drift-eppler2025.png)

_Figure: representational drift, and also cats.  Sure.  From '[Statistical learning and representational drift: a dynamic substrate for memories](https://www.sciencedirect.com/science/article/pii/S0959438825001382)'._

### II.A. Representational Drift in the Brain

The main idea from neuroscience that updates me against thinking of 'circuits' as residing in a fixed set of weights is that of 'representational drift'.  Disclaimer: I'm acting as a synthesist here, not a neuroscientist; I still have much to learn here.

There is in neuroscience a notion of something called an '[engram](https://en.wikipedia.org/wiki/Engram_(neuropsychology))' - roughly, a localizable 'trace' of having learned some particular thing; the mouse learns the maze, and you circle some neurons where the knowledge of the maze is stored.  This is intuitive and I'd be surprised if it was uniformly wrong, but there's more to it.

Instead there is something called '[representational drift](https://www.sciencedirect.com/science/article/abs/pii/S0959438819300303)' - you run the mouse through the maze, and you circle the neurons where that maze knowledge is etc. - but then you find that that localization is not _stable over time_.  The population of neurons which encode that knowledge seems to migrate around over the timescale of days to weeks.  Iiuc this is fairly random motion, rather than 'memories migrate predictably as they age', though that probably happens somewhere too.

This feels fucky because if stuff just moves around at random, how does the brain track it to know how to access it?  But I claim this is actually rather natural once you think about the design problem the brain faces - in particular, the problem of plasticity.

Plasticity management is one of the deep problems the brain has to solve - you have to manage activity on many different space- and time-scales in order to preserve _both_ **representational capacity** _and_ the ability to **continually learn**.  Too much overall activity in a region means you lose information in the noise, and too much rigidity means you can't learn things anymore, nor can you readily adapt your firing rules to the population.

Imagine you wanted to inscribe some fact in the synapse weights of a group of neurons - you have two problems.  One: since there needs to be at least short-timescale regulation of each neuron (if the community's average firing rate isn't regulated, you lose signal, and also maybe have a seizure), your encoding can't depend on very precise values of the weights - it'll have to be encoded diffusely, and since there's always noise, probably redundantly.  Two: even once you've done that encoding, you do still need to leave those synapses open for long-term plasticity in case new, more important information comes in, or some of the neurons in your circuit are part of another circuit with interfering updates, so you need to jiggle some stuff around.  So by engineering fiat, the brain mostly can't be acting like a von Neumann computer with variables stored at some address with particular access wires.  The _dynamics_ of operating a functional brain means the system needs to let 'addresses' of 'facts' move, and once they're allowed to 'move', it's natural to let them move by default.[^plasticity]  Your learning algorithm will just adapt.

[^plasticity]: Global changes in plasticity I think are moderate evidence against this argument, but long-term plasticity is structurally different than short-term - idk more thinking needed.

### II.B. Representational Drift in Neural Networks

I expect this picture to apply to neural networks at both the micro and macro levels.  Here I'll give some concrete ways we _know_ it holds at the micro level.  I'll note one could assent to these microscopic phenomena and still expect macroscopically fixed functional units.

Fixing some low level of loss, there remain a drift and a diffusion component causing nonzero motion in the parameters.

When you add noise, you get an effective loss like (see [this paper](https://arxiv.org/abs/2009.11162) for GD and [this one](https://arxiv.org/abs/2101.12176) for SGD)

$$
L_{\mathrm{eff}} = L + \frac{\eta}{4}\,\mathbb{E}_B\Vert \nabla L_B\Vert ^2
$$

where $$L_B$$ is the loss on a minibatch $$B$$.  You can imagine doing descent until $$L$$ is minimized, at which point you'll start doing descent on the noise term alone - i.e. even if you've minimized the loss already, you'll keep moving in a deterministic way in order to reduce noise.  That to say even once you've learned to implement a particular function, your parameters still have reason to be moving about - not just in a random way, but _also_ in a concerted overall way.  If you get to zero on that _effective loss too_, still there will be merely random motion in the weights.

Even at equilibrium, you can use the '[fluctuation-dissipation relations for SGD](https://arxiv.org/abs/1810.00004)' to show

$$
\langle \theta \cdot \nabla f \rangle = \frac{\eta}{2}\, \langle \mathrm{Tr}\, \tilde C \rangle
$$

and

$$
\langle \Vert \nabla f\Vert ^2 \rangle = \frac{\eta}{2}\, \langle \mathrm{Tr}(H \tilde C) \rangle + O(\eta^2)
$$

(here $$\langle\cdot\rangle$$ is the stationary average, $$\tilde C = \langle \nabla f_B \nabla f_B^\top \rangle_B$$ is the second moment of the minibatch gradient, and $$H$$ is the Hessian), i.e., that at equilibrium, you'll still have nontrivial motion due to batch noise etc.  This is an imprecise argument, but the point is that by default, you do not get zero motion in parameter space.

So neural networks have _some_ analogue of this representational drift problem, at least by default.  You can hypothesise that the various effective penalties will cause the network to _enter_ the regime where it _can_ just encode stuff at the weights level without needing to worry about it moving around - it definitely does get progressively flatter!  But this adds an extra hypothesis which I've found it hard to justify - that 'more noise robust' should for some fundamental reason correspond to circuits in any functional sense.

So to summarize, the brain can't plop information down at known addresses and re-access it like a von Neumann computer, because noisiness favors diffuse encoding and plasticity favors gradually-migratable encodings.  There are similar-ish phenomena in neural networks that come from effective loss terms caused by noise, so we can be relatively sure that parameters will always be moving, at least a bit - which means that probably neural networks should want to distribute functionality and representation as broadly as possible.  If you're thinking about _features_, this leads you to think about superposition, which I think everyone is on board with.

It's less clear what this looks like if _computation_ is itself 'diffuse'.  There is '[computation in superposition](https://arxiv.org/abs/2408.05451)', which is what it says on the tin.  But by 'diffuse computation', I really mean a paradigm of computation where the computation is designed under comparable constraints.  The difference is like 'writing precise algorithms to operate on noisy data' vs 'noisily writing algorithms to noisily operate on noisy data'.  That there should be some kind of spiritually different 'theory of diffuse computation' is I think my central intuition.  I expect this 'diffuse computation' to converge to 'normal computation' in some regimes some of the time - I don't doubt that GPT learns some fairly precise algorithms some of the time.

Regardless, I think one promising direction is to think a lot about denoising operations; [Dmitry Vaintrob's recent work](https://www.lesswrong.com/posts/SNAKJuN8FdoEaWeFC/in-search-of-natural-features) on this is cool.[^diffusion]  An example of something that would be borderline between either of these two views would be something like voting among a bag of heuristics.

[^diffusion]: See [this video](https://www.youtube.com/watch?v=T_GhB7lK2YE), which talks about a method of training transformers inspired by thinking of them as doing denoising diffusion.

---

## III. Developmental Motifs Circumscribe Notions of 'Circuits'

### III.A. Neurotrophins and Microstructure

I think it's useful to look now at the problem the brain has to solve in order to reliably get useful neural circuitry.

There's some level of large-scale connectivity in the brain which is genetically hardcoded - [see this article for a good exposition](https://www.neuroai.science/p/cell-types-encoding-the-brains-bios).  For the sake of argument, we'll pretend that there are $$N$$ brain regions and that your brain roughly hardcodes connections between those $$N$$ regions, and that it encodes what it wants each of those regions to _do_ by specifying a distribution of neurotrophins[^ntf] for each of those $$N$$ regions.  So there's a **global connectivity rule** and a **local development rule**.

[^ntf]: Strictly, the linked article is about cell types and transcription factors rather than neurotrophins.  The distinction isn't the point for now - read 'neurotrophins' as 'whatever local chemical signal sets a region's developmental program'.

![Whiteboard sketch: global connectivity between brain areas, each area specified by a local rule and implemented as any of many microstructures]({{ site.baseurl }}/assets/images/lw/what-if-not-circuits/whiteboard-global-local.png)

_Figure: the global connectivity rule says which areas talk to which; the local rule says what each area should become, and is implemented as any one of many microstructures.  The local rule is sufficient but not interpretable, and the microstructure is irrelevant by design - so we need to understand both separately._

For example, let's imagine that the neurons are smart enough that the population will always evolve to be one of 8 circuits, and the neurotrophin distribution just sets which of the 8 it becomes.  We'll assume we don't know this in advance.  To _understand_ that that's what's happening, you need to know how the development rules work _and_ how the neurotrophins select between those behaviours.

The problem roughly factors - we can pretty reasonably map out the connections between these $$N$$ regions, and we can plausibly map out these neurotrophin distributions as well.

But if we want to do _interp_ we have something of a problem - we have no idea _why_ this works reliably - no idea how the $$N$$th area's connectivity + neurotrophin distribution _reliably produces_ the right functional behaviour.  We do know for sure that there's some process by which specifying these things, along with the normal rules for neural development, results in reliably having some particular function.

But by the same token we know that the _particular_ configuration of weights and neurons _cannot_ be the right way to explain what area $$N$$ is doing, because that configuration is only one of a bajillion completely different configurations those neurons could have taken under that local development environment and still produced equivalent functionality.

On this picture there's no need to ask about weights, just as there is no need to ask about the locations of atoms in a gas.

I'm sure there _are_ functional units which implement different computations, but I'm _not_ sure that these are in weight-space - that's why I think it's important to think about how these top-down explanations circumscribe the kinds of bottom-up explanations we will need.

### III.B. Back to Neural Networks

This of course isn't directly analogous to neural networks, because we do much less hardcoding - but there still are meaningful structural motifs - layers specialize differently, there are characteristic eNTK spectra,[^entk] etc.

[^entk]: The empirical neural tangent kernel: the Gram matrix $$K(x, x') = \nabla_\theta f(x) \cdot \nabla_\theta f(x')$$ of per-example gradients at the current parameters.  Its spectrum tells you which directions in function space the network can currently move in easily, and it has a characteristic shape (a few large outliers plus a power-law-ish bulk) across architectures.

Here I mean to argue that, _conditioning on_ your neural network + training procedure _predictably working at all_, most of a good account of this is a combination of generic neural network developmental motifs _plus_ some theory of how this comes to reflect different properties of data.

Put another way, suppose arguendo an LSTM and a transformer learn essentially the same function on some given data, and that this is essentially true for a wide range of tasks we're considering.  Then our explanation of what they have learned should be _symmetric_ between them.  If we want to know something deep about why training these networks on given data produces a particular outcome, we needn't explain things in terms of QK circuits if we know that the phenomenon occurs in architectures without attention heads.  Instead we explain why _both_ architectures have neuro-magic-property-X, then explain why that joint neuro-magic-property-X results in that behaviour.

I don't expect that strat to work irl - instead I argue only that we should focus a lot of effort on these local development rules, and maybe this will help us understand what kinds of structures to look for and where - I don't expect that those rules _alone_ will be useful.  But consider 'superposition' - knowing about superposition, any interp methods that _don't_ assume superposition appear confused.  Once you understand superposition, you realize you shouldn't be looking at the neurons - you should be looking at feature directions.  Once you know about feature directions, you realize you were looking in the 'wrong place'.

I think superposition is one of a few such ontology-changes, some of which we still need to figure out.  Personally I expect 'circuits' will become some theory of 'denoising computation', and this will tell us to look for 'interpretable computations' in a different place.

---

## IV. A Co-Selectionist View: Circuits Move Together?

Here I'll talk about one particular operationalization of circuits which I have found useful to think about, based on the idea that circuits should receive correlated gradients - 'live together, die together' - '[neural Darwinism](https://en.wikipedia.org/wiki/Neural_Darwinism)'.  tl;dr is that I think there's a principled mathematical description of circuits as 'emergent units of selection', but there's still ambiguity in what the 'type signature' of a circuit is.[^persistence]

[^persistence]: Note here I mean persistence selection rather than real Darwinism - circuits don't have offspring.

The guiding intuition is that circuits, as functional units, should receive correlated gradients - that they are 'emergent units of selection'.  Another way to put this is that we should be able to say 'these $$N$$ weights are in the circuit' and the individual gradients should mostly be predicted by how well the _whole_ circuit is reinforced.  This is also the natural response to representational drift: if the weights are always moving, then the thing to look for is not a fixed set of weights but whatever moves _together_ under that motion.

It turns out that there's a distantly analogous problem in fluid mechanics - looking for so-called '[coherent structures](https://en.wikipedia.org/wiki/Lagrangian_coherent_structure)' in a flow.  There's also the related problem of '[community detection](https://en.wikipedia.org/wiki/Community_structure)' on graphs, where you try to find regions with lots of internal connections and minimal external connections.  Turns out you can write these in a very general way so that they become special cases of the same problem.

![Three schematic panels: a teal fluid blob stays together over time, a dense teal graph community has few links to grey outside nodes, and teal weights have long parallel gradient arrows amid short grey arrows pointing in varied directions]({{ site.baseurl }}/assets/images/lw/what-if-not-circuits/coselection-figure.png)

_Figure: codex tried hard to illustrate the analogy._

A 'coherent structure' in fluid mechanics is some bounded volume of fluid such that the boundary doesn't move wildly and that there isn't too much mass flow across it over time.  Morally, you look for

$$
\mathrm{Incoherence}(S) = \frac{1}{T} \int_0^T dt\, \big(\text{mass flow across } \partial S(t)\big) + \big(\text{stretching penalty}\big)
$$

![Lagrangian coherent structures in a periodically forced flow]({{ site.baseurl }}/assets/images/lw/what-if-not-circuits/lagrangian-coherent-structures-wikipedia.png)

_Figure: Lagrangian coherent structures in a periodically forced flow, from [Wikipedia](https://en.wikipedia.org/wiki/Lagrangian_coherent_structure).  The coherent structures are those little eyes - they mostly 'move together' and mostly stay looking like eyes.  Reminder that we're talking about _persistence selection_, so we want to find the right notion of 'persistent' structures in a neural network._

The reason you need this functional is because presumably nothing is ever perfectly coherent, so you look for structures which are as coherent as possible.

The generalization of this is to understand these as coming from some manifold and use the Laplacian on that manifold to write an energy function.  Basically, once you tell me what you think the 'type signature' of a circuit is, there's a corresponding coherence functional.

For circuits, this is cool because it lets us swap in different incoherence functions corresponding to different accounts of 'what a circuit is'.  For example, circuits as directions in parameter space (in $$T\Theta$$), as collections of weights (in $$2^\Theta$$), as $$k$$-dimensional _subspaces_ of parameter space ($$Gr(k,\vert \Theta\vert )$$), etc.  You do this by choosing either a Laplacian, a Dirichlet energy, or a manifold to work with - once you specify the 'type signature' of the circuit, this is determined for you.

I'm consciously stopping myself from writing a lot of math.  I'm doing some experiments with this with a friend so the math'll be in the writeup.  If you want a preview, you can look at [my claudeslop notes](https://charlesr-w.github.io/crw-blog/Dynamic-Spectral-Geometry-for-Identifying-Computations/).

This formulation is really nice because it ports right into dynamical systems, so you get useful tools like Lyapunov exponents for analyzing stability etc.

The point is that you _can_ write down a pretty principled selectionist view of circuits, and this has very nice natural connections to dynamical systems, community detection, etc.  It gives us lots of nice ways to say how stable a circuit is over time, how 'not-quite-circuit-y' it is.

But!  Look at the degrees of freedom we still have!  We still need to tell the theory what the type signature of the circuit is!  I'm still working on exploring this, so I'll just note that this type-signature freedom makes things a bit difficult.

Overall I'm optimistic about 'circuits as co-selected units', but I don't think those units will be in weight-space.  I'm less sure about activation space.  Lord knows there has to be structure _somewhere_ in there...

---

> "Wir müssen wissen.  Wir werden wissen."  - Hilbert

---

*LLM Usage Statement: I wrote everything - yes sadly the emdashes really are all mine and I really am that insufferable.  I had Claude make minor changes, link references, fix figures, and accepted some small corrections.  Codex made one of the figures.*
