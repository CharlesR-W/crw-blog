---
title: "Coalitional Darwinism"
date: 2026-05-26
math: true
---

This post was written as part of MATS 9.1 under the mentorship of Richard Ngo.

This post is the first of several I will be writing on using natural selection to understand artificial intelligence and agency.  This post will show how noisy selection on genome structure can make evolution effectively non-myopic.  From this, we give a Darwinian account of the emergence of 'individuals' constituted by coalitions of lower-level replicators.

Later posts will develop the connection between genome-structure selection and neural-network feature-learning, with applications to interpretability and alignment.

Note: I will use 'Darwinism', 'evolution' and '(natural) selection' interchangeably — more technical discussions of selection often distinguish between them.

---

## **0.  Outline**
1.  Natural selection is limited by noise in its ability to resolve small differences in fitness.  Because selection is a limited resource, and because selection makes lineages more fit on average, organisms will tend to evolve to make more efficient use of what selective power they have.

2.  The noise floor can make evolution effectively hyperopic (the opposite of 'myopic') by buffering the effects of mutations which may be beneficial in the short-term but harmful in the long-term.  The evolution of 'bet-hedging' is given as an example.  Hyperopia permits the evolution of pre-commitments detrimental to some individuals.

3.  The 'bowtie' network motif is an example where selectability is an essential property of the architecture.  The network develops low-rank structure, limiting its expressivity, in order to be selectable.  This may be understood as a 'coalition of the invisible' — network links which otherwise have too little effect to be tunable by selection instead commit themselves to this low rank structure, trading optimality for selectability.  The coalition is then entrenched as selection optimizes it.

4.  In prisoners' dilemmae, groups of organisms can evolve obligate co-operation (an inability to 'defect').  In some circumstances, obligate co-operators may evolve policing structures and joint heritability, resulting in the emergence of a new effective unit of selection.  The suborganisms constitute the effective genome of the superorganism.

5.  The noise floor limits how effectively subagents can be aligned to the superagent; this imperfect alignment provides the reservoir of variability which permits selection to act on the superagent.  Thus subagent misalignment (which is typically only minimally deleterious) is _synonymous_ with 'exploration' in the superagent's genome space.  Incoherence (i.e., subagent conflict to the superagent's detriment) is the fitness subsidy paid by the individual to its lineage in the form of typically-slightly-harmful exploration.

---

## **1.  Noise Limits the Precision of Selection**
*Summary*: _Due to randomness, natural selection can only reliably fix or purge mutations with large enough effects on fitness.  This resolution is proportional to the (effective) population on which selection acts._

For clarity, we'll consider here species that reproduce in fixed generations, with constant fitnesses; the qualitative picture remains similar regardless.  Spherical cow stuff.

Consider $N_{types}$ types of organism; at each generational turnover, they replicate according to a fitness $w_i := \frac{N_i^{t+1}}{N_i^t}$, with $N_i^t$ the population of type $i$ at time $t$.  The fraction of the total population represented by type $i$, $p_i^t$ obeys the replicator equation:

$$p_i^{t+1} = p_i^t \cdot \frac{w_i}{\bar w^t}$$

Where $\bar w^t$ is the average fitness of the population at time $t$, $\bar w^t = \sum_i p_i w_i$, which changes as the proportions change, even as we have assumed the fitnesses $w_i$ constant.  This says that the proportion of the population made up by type $i$ grows in proportion to how much its fitness exceeds the population mean fitness.

### **1.A.  Smaller Populations Have More Sampling Noise**

![Genetic Drift Sampling](https://i.imgur.com/OdN4lVu.png)
[Image and Caption from Wikipedia](https://en.wikipedia.org/wiki/Genetic_drift#/media/File:Random_sampling_genetic_drift.svg)

In fact this is not exactly what happens — a type $i$ organism might perchance have slightly more or less than their allotted average number of descendants $w_i$.  One way to model this effect is to imagine the $p_i^{t+1}$ to be idealized probabilities, and, for a population assumed to have size $N_e$[^1], we independently draw $N_e$ samples according to the categorical distribution on $p_i^{t+1}$.  I'll spare you some math (see, e.g., [these notes](https://personal.math.ubc.ca/~db5d/SummerSchool09/lectures-dd/lectures6-7.pdf)).

[^1]: the 'e' subscript stands for 'its more complicated than that'

In effect, this introduces noise with variance $Var(p^{t+1}_i) \sim p^t_i(1-p^t_i)/N_e$.  Functionally, if two types have comparable populations and a fitness difference much smaller than the noise scale, the noise makes it impossible to resolve.  Concretely, if all types have fitness $1$, except for one type with fitness $1+s$, selection will only 'see' this difference if

$$|s|N_e \geq 1$$

That is, selection has a resolution power proportional to the population size — larger populations mean the noise is averaged out.  This is referred to as the *drift-diffusion threshold* — 'drift' means 'mostly governed by fitness differences', 'diffusion' means 'mostly governed by noise'.[^2]

[^2]: Yes, this _is_ the exact opposite of what physicists mean when they say 'drift', and yes it _is_ completely standard convention in biology.

And of course, all of the above is a toy model — $N_e$ isn't exactly the real population, which should change over time anyways, etc. — the point is that noise is important and governs the resolution at which selection can operate.

### **1.B.  Evolution is Usually Nearly Neutral**

Evolution is solving a high-dimensional optimization problem, just like neural network training via backprop.  In both cases, and I think this is probably a fairly general property of useful high-dimensional optimization algorithms, most directions in genome/parameter space are 'neutral' — they have effectively zero loss.  

Two important upshots of this for now: first, if we look at an organism and see lots of complexity, it's not necessarily true that this complexity solves a problem as opposed to being a kludge.  Second, this 'non-adaptive complexity' _can_ still serve as the substrate for later _adaptive_ mutations.

For example, in a regime where having long genomes is very cheap, it's mostly fine to have 4 or 5 copies of gene A.  If, down the line, one has need of a variant of protein A, it's quite handy to be able to have those extra copies around so you can finetune the variant without messing up the function of the old protein.[^3]

[^3]: This particular pattern is called ['subfunctionalization'](https://en.wikipedia.org/wiki/Subfunctionalization).

Neutrality is _extremely important_ for studying the behaviour of evolution — it is the basis for a lot of the surprising phenomena we talk about below.  Having lots of neutral directions is, by definition, inconsequential to the organism _locally_ — it matters because it changes the nature and difficulty of the search problem in genome space.

See also:

['Constructive Neutral Evolution'](https://en.wikipedia.org/wiki/Constructive_neutral_evolution)

['Neutral Theory of Molecular Evolution'](https://en.wikipedia.org/wiki/Neutral_theory_of_molecular_evolution)

---

## **2.  The Noise Floor Can Make Evolution Effectively Hyperopic**
*Summary*: _Outcome noise acts to buffer the effects of selection; noise's restraining effect on selection can permit low-variance 'steady' strategies to outcompete myopic strategies (e.g. those with high growth but large extinction risk).  On long timescales, selection incentivises strategies like 'bet-hedging' which reduce systematic lineage-risk at the expense of individuals' fitness.  In the long-run, selection is hyperopic, dispreferring naively profitable short-termist strategies._

Evolution is commonly thought of as 'myopic' — a local, greedy optimizer, with no ability to 'plan ahead' or make local sacrifices in fitness for future gains — every step must justify itself _per ipsum_.  In this section, I will show that the noisiness of selection (the resolution limit from [§1](#1--noise-limits-the-precision-of-selection)) can make selection effectively non-myopic — what I call 'hyperopic'.

Roughly, short-term greedy strategies can outperform long-term strategies for a short period of time — if selection is noisy enough, the long-term strategy can preserve enough of its population to 'wait out' the short-term strategy, rather than being outcompeted right away.[^4]  Thus, the noise floor can 'subsidize' low-variance, long-term-optimal strategies, even if their advantage is only apparent on the scale of a handful of generations.  Conversely, this will look, from the outside, like evolution learning _not_ to go down the 'blind alley' of the greedy strategy — it appears to look ahead!

[^4]: The noise floor for selection provides a kind of 'slack' (c.f. [this post](https://www.lesswrong.com/posts/yLLkWMDbC9ZNKbjDG/slack)).

### **2.A.  The Evolution of 'Bet-Hedging' is an Example of Hyperopia**

'Bet-hedging' is the cleanest example of hyperopia.  Bet-hedging is, roughly, a behaviour whereby organisms take an action according to the probability they think it is optimal, rather than taking the action they think is most likely optimal.

The classic example of this in humans is coin-tossing; participants are informed that the coin may be weighted unfairly, and then repeatedly asked to predict the outcome of the next coin flip.  Seeing a sequence like "THHHHTHTHH" (70% heads and 30% tails), about 70% of the time, participants call the next flip as 'heads', and about 30% as tails — the optimal answer is of course to predict 'heads' 100% of the time.[^5]

[^5]: See the post ["The Correct Response to Uncertainty is *Not* Half-Speed"](https://www.lesswrong.com/posts/FMkQtPvzsriQAow5q/the-correct-response-to-uncertainty-is-not-half-speed) for a related idea.

We can see why this is: in the long-run, for selection on a fixed set of phenotypes, the population sizes are determined by the average LOG growth rate

$$\frac{N^{t+1}}{N^t} = w_t \quad\rightarrow \quad \log N^T - \log N^0 = \sum^T_t \log w_t$$

So the winning strategy is not to maximize $w$, but to maximize $\log w$.[^6]  This logarithm, its concavity, is the original sin from which flows all conflict between a lineage and its constituents.  Whence risk-aversion.

[^6]: Garrabrant's [Geometric Rationality](https://www.lesswrong.com/s/4hmf7rdfuXDJkxhfg) has a lot of cool adjacent ideas, including the especially salient idea of the 'arithmetic-geometric boundary'.  The nexus is that population-sizes under natural selection are the bankrolls of Kelly bettors.  Kelly betting definitionally maximizes the geometric growth rate, i.e., $\log w$.

See also:

[A good lecture on the topic of bet-hedging](https://www.youtube.com/watch?v=UYZJIRMC55k)

#### **2.A.i.  Toy Model of the Evolution of Bet-Hedging**

Imagine the same setup as the coin-toss game:  A tribe must choose where to live: the Usually-Edenic Gardens, which give them 10 fitness with probability 99% and 0 fitness with probability 1%, and the Plague-Blasted Heath, which gives them 1.1 fitness with probability 100%.  The group maximizes expected fitness by choosing to live in the Gardens.  The log growth rate is maximized by choosing the Heath with probability 1.  A tribe which chooses the Gardens with _any_ probability will eventually run out of luck and be extinguished in one fell swoop. (For simplicity this assumes the group chooses as a whole, etc etc.)

How sluggishly alight the wings of retribution on those who durst profane the garden?  The gardens have an extinction event every ~100 generations, and so on shorter timescales, populations preferring the garden will predominate — selection will only favour the Heath-dwellers on timescales $\tau >> 100$.  The interesting consequence is this: if a mutation should cause a Heath-dweller to become a Garden-enjoyer, this mutation is, in the long-run, as good as an instant fatality (assuming the reverse mutation doesn't occur).  In the long run, the Heath-dwellers will evolve to _prevent_ such mutations _as if_ they were instantly fatal — evolution should be willing to pay a cost to prevent this mutation.

![Bet-Hedging Model](https://i.imgur.com/wOsgmc1.png)

Cool contrived model.  Why care?  Roughly, evolution is, in _some_ parameter regime, effectively non-myopic.  More spectacular cases of hyperopia in direct conflict with individual interests seem uncommon in biology outside of cases with artificially high mutation rates (like in [these](https://www.nature.com/articles/35085569) [contrived](https://pubmed.ncbi.nlm.nih.gov/18054366/) [models](https://link.springer.com/article/10.1186/1471-2148-11-2)).  Bet-hedging is the cleanest, [definitely-real](https://en.wikipedia.org/wiki/Bet_hedging_(biology)#In_organisms), common example.  I'm working on a separate post about analogies and disanalogies between evolution and gradient descent, where I'll try to articulate precisely the regimes in which this is relevant based on scale-separation.[^7]

[^7]: One may be reminded of work on [optimization daemons](https://www.lesswrong.com/posts/KnPN7ett8RszE79PH/demons-in-imperfect-search) and [gradient hacking](https://www.lesswrong.com/posts/w2TAEvME2yAG9MHeq/gradient-hacking-is-extremely-difficult?ref=conjecture.ghost.io) (see also [here](https://www.lesswrong.com/posts/bdayaswyewjxxrQmB/understanding-gradient-hacking) and [here](https://www.lesswrong.com/posts/ioZxrP7BhS5ArK59w/did-claude-3-opus-align-itself-via-gradient-hacking)); my take is that hyperopia is a property of the optimizer, so this analysis doesn't relate directly to mesa-optimizers.  If you're interested in the care and feeding of benign mesa-optimizers, do consider studying the immune system (see my quick-take [here](https://www.lesswrong.com/posts/QbSpNkPzb4W4Judh2/charlesrw-s-shortform?commentId=vDwqKPXo7kzuL9gSd)).

_"In the long run, we are all \[Kelly bettors or\] dead."_
J.M. Keynes

### **2.B.  A Toy Model of When Selection is Effectively Hyperopic**

Here I'll be more explicit about the nebulous 'weird parameter regime' in which selection can be effectively 'hyperopic'; we'll build a toy model that will grow into the real multi-scale expansion that I intend to use to apply these ideas to analyze neural networks.

Consider an environment which varies somewhat slower than the timescale of selection — a species which is slow to adapt will suffer a fitness penalty $\delta w$.  Evolution should be willing to 'pay' to decrease it — the question is if it _can_.  Supposing a mutation appears at cost to an individual, $s$, then this mutation can survive if $s N_e \leq 1$ (the resolution condition from [§1.A](#1a--smaller-populations-have-more-sampling-noise)).  The mutation is favoured if $\delta w \geq s$ and $\delta w N_e \geq 1$:

$$\frac{1}{\delta w} \leq N_e \leq \frac{1}{s}$$

Thus, such amortizations are only possible when the population is small enough as to be unable to resolve them, but large enough to be able to resolve the group effect.  Note that this argument applies in reverse to entrenchment effects.

Please note that this is a very heuristic derivation meant to give an idea — I expect that in reality, most such changes are essentially neutral on the short timescale, and are only resolved on the long timescale by second-order effects from changing noise statistics.  For changes which aren't neutral, it's likewise a question of comparing timescales and fluctuations.  The dynamic version is a good bit more complicated mathematically, and I'll save it for the more technical neural networks post.

## **3.  The 'Bowtie' Motif is a Coalition Formed to Maximize Selectability**
*Summary*: _Many biological networks are 'bowtie' shaped — a highly optimized 'core' knot, with many feed-in and feed-out signals, forming a 'regulatory periphery'.  The low-rank bottleneck of the 'knot' amplifies the selective signal passed to the peripheral pathways; thus the bowtie can be understood as a 'coalition of the invisible' — many sub-noise-threshold pathways sacrifice tunability by binding themselves to the knot.  Selection entrenches the coalition by optimizing the newly legible periphery._

Consider a highly optimized metabolic cycle like the Krebs cycle — the core cycle is essentially [optimal](https://link.springer.com/article/10.1007/BF02338838)), thus highly conserved over evolution.  Evolution has to figure out a way to manage its golden boy without walking off a fitness cliff — the solution we often see is the *regulatory periphery* — the cell's various chemical networks route through the central knot, and all the regulatory knobs get attached to these various input/output channels.

[This article](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004055) shows that bowties tend to evolve when a network processes a low-rank signal under a cost-of-regulation, which seems reasonable — low-rank things (e.g. "how much metabolism should I be doing") are much easier to control and understand — but here I want to propose that one origin of this kind of regulation-cost is the need to preserve selective signal.

Because these regulated networks now pass through the highly-influential central knot, each individual 'arm' of the network has a one-to-many channel to downstream processes, instead of the one-to-one you'd get in a haphazardly evolved chemical network.  Thus, the feed-in / feed-out pathways get a _bonus to selective visibility_ by passing through the knot — even at the expense of not having fine-grained control over the output processes.  The bow-tie motif is a coalition of chemical pathways — its members trade off, and the stability of that coalition is determined by the noise floor of selection (see [§1](#1--noise-limits-the-precision-of-selection))!  AND!  The longer this coalition holds, the more highly optimized it will become, so selection will tend to *entrench* it over time.  I call this kind of selectability-driven coalition a 'coalition of the invisible'.[^8]

[^8]: Note that we are speaking of these regulatory arms as agents which act volitionally; this is loose, both in the sense that they only 'act' as driven over evolutionary timescales, not intra-lifetime, and in the sense that one could only with difficulty identify persistent 'lineages' of arms.  This is mainly a propaedeutic bridge to the next section, where it will be useful to think of organisms as agents consisting of a genome of sub-agents.

![Bowtie Kludge image](https://i.imgur.com/1cOCFxc.png)

I have been toying with the idea that the fragility of the bowtie core was not an accidental property of an optimum, but was perhaps actively evolved in order to divert selection resolution from potential mutants — rather than waste selective resolution re-purging every time there's a mutant lineage, selection might prefer mutants to 'fail-fast' by building fitness cliffs — an evolved pre-commitment to self-destruction.  I'd take ~30% that its fragility is evolved hyperopically rather than incidental.  [This paper](https://www.nature.com/articles/35085569) finds evolved fragility _in silico_, but this doesn't seem strong evidence for evolved fragility; my guess is that recombination evolves to cope with the mutational load before evolved fragility kicks in.

![clonal interference image](https://i.imgur.com/Bwc0jb2.png)
[Image from Wikipedia](https://en.wikipedia.org/wiki/Clonal_interference)
This diagram shows the dynamics of evolution in asexual reproduction.  The red 'aB' strand represents a deleterious mutation.  The 'evolved fragility' discussed above would occur if 'aB' repeatedly evolved and went extinct; you can think of the 'lost selective power' as the _area_ of 'aB''s red blob.  The _value_ of that area depends on how valuable the marginal unit of selection power is in a given situation.

---

## **4.  Obligate Co-operation can Bind Coalitions into Emergent Individuals**

*Summary*: _Under prisoners' dilemma dynamics, organisms may evolve obligate co-operation — a form of pre-commitment.  Policing and excluding defectors incentivises tighter co-operation.  Under the right circumstances, the co-operating replicators may become bound together so tightly as to constitute an effective individual — a new unit of selection._

Here I will discuss dynamics of how evolution can push groups of possibly unrelated 'individuals' to bind themselves into a single, jointly reproducing unit — a 'higher level' organism.  A quick clarificatory note: here it is useful to think in terms of agents and sub-agents, but 'actions' are not taken in the lifetime of, say, some particular gene; instead the 'actions' are successive adaptations occurring over evolutionary timescales.  We may say synonymously 'bacterium A evolved X capability', 'the lineage of bacteria A evolve X capability', or 'evolution caused those bacteria of lineage A which evolved X capability to outcompete those which did not'.  I prefer the former as being concise, but the squeamish reader is invited to mentally substitute readings with their preferred degree of teleology.

### **4.A.  Prisoners' Dilemma Dynamics can Lead to the Development of Mechanisms to Enforce Co-operation**

Consider some organisms playing prisoners' dilemma, perhaps scattered over enough isolated 'patches' that we get lots of independent trials.  Defectors prosper within patches, while co-operating patches thrive overall.  We saw above ([§2](#2--the-noise-floor-can-make-evolution-effectively-hyperopic)) that evolution can 'pre-commit' lineages to certain paths of development; it follows that it can, given enough incentive, evolve _obligate co-operation_ — biologically cauterizing away the possibility of defection.  

In order for this to be feasible, a patch needs to evolve the ability to:

1. Exclude external defectors  
2. Police defections arising from breaches or mutations
3. Suppress internal competition

These synergize with each other: exclusion usually means compartmentalization, which increases an individual replicator's incentive to police.[^9]  'Policing against mutant defectors from our posited prisoners' dilemma' looks a lot like 'policing defectors in general', which, turned inward, looks a lot like 'pre-commit to joint heritability of all replicators within the patch'.  This is not the necessary course of events, but a proof of plausibility.[^10]

[^9]: Policing is important in proportion to the degree of unrelatedness of the constituent replicators, c.f. [this paper](https://stevefrank.org/reprints-pdf/96AnBehav-Policing.pdf) — the reader is encouraged to ponder, i.a., [royal marriages](https://eu4.paradoxwikis.com/Diplomacy#Royal_marriage) and the practice of cross-shareholding common among Japan's zaibatsu conglomerates, [keiretsu (系列)](https://en.wikipedia.org/wiki/Keiretsu).
[^10]: A book I haven't read but seems good for this: [Kirschner & Gerhart 2005, _The Plausibility of Life: Resolving Darwin's Dilemma_](https://yalebooks.yale.edu/book/9780300119770/the-plausibility-of-life/).

Once these three conditions apply, the compartment becomes a unit of selection, and its constituent replicators something like its effective genome.  Natural selection will now operate on the compartments as a unit, and an 'individual' is born.  I will refer to the units of this higher level of selection as 'agent' and its constituents as 'subagents'.

Two fun/surprising questions as exercises: when dioecy evolved, why would females entirely lose the ability to reproduce parthenogenetically, rather than selectively?  If your answer is 'policing', in line with this section, why are sex ratios _not_ so policed? (c.f. [Fisher's Principle](https://en.wikipedia.org/wiki/Fisher%27s_principle))

### **4.B.  Group Selection is Feasible When Group Interests are Aligned or Orthogonal to Individuals'**

[Group Selection Wikipedia Page](https://en.wikipedia.org/wiki/Group_selection#A_revived_group_selection_theory) 

Coalitional Darwinism is subtly but importantly different from traditional 'group selection'.  Group selection is often used to mean the selection of groups in direct opposition to the interests of individuals — notably, its Wikipedia page has a ["Rejection"](https://en.wikipedia.org/wiki/Group_selection#Rejection) section, though it seems to largely be a question of when and where group selection occurs rather than if — I happen to share a name with a very handsome and smart and cool group of cells on which selection is acting as a unit.

Two mechanical differences:
- Emergent individuals are (in general) made up of _unrelated_ replicators, and must therefore rely on policing, rather than common interest, to enforce co-operation.  The subagents are also _jointly heritable_ — to be considered an 'emergent individual', the individual/group conflict has to have been sufficiently suppressed.[^11]
- Traditional group selection tries to examine the effects of group selective pressure on individuals' traits when these are ~antagonistic.  When an emergent individual arises, its subagents presumably lie along their respective fitness Pareto frontiers; group selection can freely move subagents _along_ this frontier at ~no cost to subagent fitness.  The individuals' iso-fitness curves are generically very high-dimensional, so the group can freely evolve along any such direction.  This 'decoupling of interests' probably only fails after a long period of 'domestication'.

[^11]: If all replicators were identical, they could do a crude Lobian-style co-operation — multicellular organisms and insect colonies seem to do roughly this.  As noted earlier, relatedness decreases the need for policing mechanisms.

This has an interesting interpretation: sub-agents' directions of neutral variation are the variance on which the superagent draws to optimize — but the converse is that superagents must become more 'Draconian' in proportion to the paucity of accessible variability remaining.[^12]

[^12]: A caricature of the cold war: the US started under less pressure, so could afford free markets, which are less efficient at producing strategic goods in the short term, but produce more growth in the long-term.  The USSR started at a disadvantage, resorted to state control of the economy, and was able to make remarkable gains in strategic sectors in the short-term, but grew less in the long term.  Slack at the higher and lower levels reinforce one another.


So 'coalitional Darwinism' as articulated here is group selection, but it's not 'Group Selection' in the 'is this a dominant mechanism in animals' sense — it's ultimately an attempt to cast the biological theory of the emergence of individuals-qua-superagents as a naturalized theory of agency and incoherence.  Bluntly, I want it to apply to circuits in Claude.

See also:

['Selection Processes for Subagents'](https://www.lesswrong.com/posts/d4hw4FBX9YXHGFBWQ/selection-processes-for-subagents)

['Understanding Systematization' (Sequence)](https://www.alignmentforum.org/s/MGMwqENAgdi85fiwF)

---
## **5.  Subagent-Induced Incoherence is the Byproduct of Exploration in Genome-Space**
*Summary*: _The selective pressure which creates policed individuals does not run to completion _by design_.  Constituents can compete in orthogonal or slightly-deleterious ways; this competition generates the variety on which selection acts.  Incoherence may be understood as a pre-commitment to exploration of genome-space, preserved against naive optimization by the noise floor._

As in the previous section, I will note here that we speak of agents and subagents acting volitionally — as before this is an abstraction for thinking about the tendencies induced by evolution.  Subagents' 'actions' are mutations.  This section introduces the additional complication that the 'agent' and 'subagents' may _evolve_, and thus 'act' on different timescales; for simplicity, I will speak assuming that the two levels' generations 'line up' — e.g., the genes which make up a cell reproduce when the cell does.  This could fail to be true, e.g., for endosymbionts like the mitochondria.

### **5.A.  The Noise Floor Protects (Lightly) Deleterious Subagent Mutations**
Our theme hitherto has been the need to allocate limited selection power.  From the above, note that an individual (the emergent agent of [§4](#4--obligate-co-operation-can-bind-coalitions-into-emergent-individuals)) will have a lower effective population, and will typically reproduce on a significantly longer timescale — thus, only a limited amount of selection power can be brought to bear on the subagents should they start to get uppity.  Competition among the regulators may persist to the extent that the selection acting on the agent is too weak to resolve it.  I call this room for suboptimality '*selective slack*'.

As a toy model, consider a subagent able to gain $s$ fitness at the cost of inflicting $r * s$ fitness damage to the host — then there is a regime where this defection can evolve and persist:

$$\frac{1}{N_{subagent}} \leq s \leq \frac{1}{r N_{agent}}$$

This tells us directly how much the subagents must be hobbled-by-design:  A 'parliament', dividing power equally, might have $r \sim \frac{1}{N_{subagent}}$, a 'veto' system would have $r \sim 1$, while complete redundancy of the replicators might make $r \approx 0$ (at least in the short term, before the others wise up).  Tall-poppy syndrome in action: the more say an individual subagent has in constituting the host, the more intense must be the policing.

The upshot is that 'incoherence', in the narrow sense of persistent maladaptation of an agent created specifically by conflict among its subagents, by default, persists to a greater or lesser degree in proportion to the selection pressure brought to bear on a coalitional agent.  It is not the case that coherence increases monotonically with applied optimization pressure — coherence is selected for only insofar as it is on the Pareto frontier.[^13]

[^13]: 'on the Pareto frontier' follows if you assume selection is greedy over accessible adaptations.  c.f. Ngo's [_Understanding systematization_](https://www.lesswrong.com/s/8GA5Y4kgCJP8FzbgX) sequence

### **5.B.  Neutral Variation Makes Incoherence a Cheap Form of Exploration**
*"\[Incoherence\] is the worst form of \[exploration\] except for all the others we have tried"* — W. S. Churchill

Much of the above has been about treating 'selectability' as a resource.  To operate, selection requires variation — BUT! selection is an optimizer, so it obviously should be very upset about needing to maintain a reservoir of harmful variants for a rainy day.  How does it leave itself enough slack?

Instead, we observe a highly non-trivial thing about high-dimensional optimization: the predominance of 'neutral' or 'cryptic' variation (cf. [§1.B](#1b--evolution-is-usually-nearly-neutral)).  I'll talk more about this in a follow-up post, as it relates to neural networks as well.  Suffice for now to say that this pressures the genome to be 'robust' in the sense that most mutations have small or no effect _locally_ while changing the effects of _future_ mutations.  This amounts to a population spreading itself out along a flat minimum in the fitness landscape — that is, evolution, like SGD, prefers flat minima ;)

In the context of emergent, higher-level 'individuals', whose 'genomes' are their constituent subagents, neutral variation means policing _only_ those interactions which _directly_ affect the function of the higher level organism, actively _disincentivizing_ overly Draconian policing amongst the subagents.

Now we can see why the noise floor argument from before (see [§1](#1--noise-limits-the-precision-of-selection)) was so important: the noise floor is the _mechanism_ by which the subagents maintain (lightly harmful) variability.  This is what is known in biology as 'non-adaptive complexity'[^14]; the most delightful example is introns, parasite DNA sequences which evolved the machinery needed to splice DNA — these are the likely ancestors of a bunch of the more advanced splicing technology used by the DNA.

[^14]: Lynch, [_The Origins of Genome Architecture_](https://www.goodreads.com/book/show/252216.The_Origins_of_Genome_Architecture) is the flagbearer of this idea; the parts I skimmed of this seemed great, but I have only skimmed.

#### **5.B.i.  Even Parasitic Subagents Can Drive Adaptation**
A quick cool tangent I couldn't bear to cut:
[This paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4958936/) gives two mechanisms by which parasitic agents drive higher-level evolution.  First, it pushes co-operator communities to co-ordinate more tightly in order to gain a [complexity-asymmetry](https://en.wikipedia.org/wiki/Size-asymmetric_competition), and this tighter co-ordination translates more readily to obligate co-replication.

Second, the adversarial co-evolution of parasitic elements, combined with a countervailing pressure to become 'domesticated', results in something like a technology-transfer, as in the intron example above.  Thus, in the long-run, even parasites can be adaptive.  For a fun example see [this paper on group 2 introns](https://pmc.ncbi.nlm.nih.gov/articles/PMC3140690/).

---
## **6.  Summary**
In this post I have tried to articulate five core ideas:
1. Natural selection has a noise floor, which makes 'selectability' itself a resource which a lineage must manage.
2. Noise buffers the effects of selection — on long timescales, evolution can effectively behave hyperopically.
3.  Some architectures like the 'bowtie' motif are driven by the need to efficiently utilize selective resolution; 'coalitions of the invisible' can pool their selectability and are rewarded by being entrenched by selection.
4. When benefits to co-operation are high, organisms can evolve obligate co-operation; when co-operator coalitions are incentivised to evolve policing mechanisms, this may result in the coalition binding itself into a new effective unit of selection — a superagent of which the sub-agents are the effective 'genome'.
5. This sub-/super-agent structure provides an account of the persistence of apparent incoherence in highly complex organisms: competition among subagents (genome elements) serves as the substrate of nearly-neutral variation necessary for selection to act — incoherence is an evolved precommitment to exploration of genome-space.

The skeptical reader has hopefully been gnashing their teeth that it seems that selection-for-selectability has multiplied the traditional criticism of selectionist explanations — now we can explain apparently _maladaptive_ behaviours as selectionist too!  "Parasites are good actually" — the nerve!

I claim only that these selection-for-selectability effects in principle can exist; I would not be so surprised if any of the examples I've adduced are better attributed to other causes, though I tried to pick clean examples.  But _another_ post will link a bunch of papers on genome and neural network structure, and we can tease out which parts of the story are bio-specific once we have the math under control.

To me, this is all an elaborate metaphor for neural networks[^15], for which I can just work out the math — I'll derive the correspondences and the parameter regimes (basically it falls out of dominant balance and multiscale perturbation theory, if that tickles your imagination any).  Until then, salve atque vale.

[^15]: As a teaser for flavour, I've been thinking what 'policing' might look like if we imagine 'competition between circuits' in LLMs.  Perhaps 'policing' looks like the development of anomaly detection and other 'executive function' circuits, possibly even leading to introspective ability?

---

My gratitude to Ashe Vasquez Nunez, Richard Ngo, Marcel Mroczek, and Maria Kostylew for their feedback.

["No Man is wise at all Times, or is without his blind Side"](https://en.wikipedia.org/wiki/In_Praise_of_Folly) — Erasmus
