---
title: "Everybody is a Quantum Bayesian"
date: 2024-10-06
---
# Everyone is a Quantum Bayesian
(and no interpretations of QM meaningfully contradict this)

Disclaimer: this post is written about interpretations of quantum mechanics, on which there's a lot of literature and a lot of philosophy - I'm not an expert, merely musing etc. etc.

By "Quantum Bayesian", I mean the belief that the 'wave function' is a fundamentally subjective entity, representing a state of an agent's belief about the world (more specifically, the 'predictions' of quantum mechanics are normative statements about how an agent _should_ reason, in a sense analogous to those of probability theory).  In this post I'll argue that (a) quantum mechanics should be interpreted subjectively along the lines advocated for by, i.a., QBism; Further I'll argue that (b) it is non-sensical to describe reality as "stochastic" except in reference to agents therein, and (c) standard QM does not permit access to the 'underlying ontology'.

For this post, let's draw a distinction between the wave-function (WF) as an epistemic thing (representing an agent's beliefs) and the WF as an ontological thing (i.e. a real thing which meaningfully can be said to exist in physical reality).  It is undeniable that the WF _at least_ can be used to represent an agent's beliefs - if you think that WF is 'real', then these are just beliefs derived from - and directly representing - the state of reality, derived the same way that your eating an ice cream cone tends to induce the belief that you're eating an ice cream cone.  Thus, let's call wave-function-qua-belief the epistemic wave-function (EWF), and the wave-function-qua-real-thing the ontological wave-function (OWF).  EWF is for agents making decisions, OWF exists entirely independent of any agents (if you believe in it).

### Probability is subjective; QM predicts probabilities

There are to me, two knock-down arguments to believe that probabilities are fundmantally epistemic: (1) Cox' theorem and (2) Dutch Book arguments

Cox' theorem shows that any mathematical representation of inference under uncertainty (satisfying certain highly reasonable axioms-qua-desiderata) must be isomorphic to probability.  You can object to the axioms therein, but frankly its pretty hard to find fault with them; pace the literature of objections thereto, I'll take as fact the following assertion: 
*Any set of beliefs about degrees-of-plausibility of outcomes must be expressible as a probability distribution over those outcomes, obeying the probability axioms, on pain of irrationality* (i.e. no _alternative_ structures are 'as good' nor better than a probability distribution)

A more ecumenical, equally true, description is that, if you have some handful of beliefs to which you want to assign numerical degrees of plausibility, those beliefs will be 'coherent' if the relationships between all of those belief-numbers satisfy certain constrants (viz. being representable by a probability distribution).

Note that the above is pretty normative - it's saying you _prudentially_ 'should' structure your knowledge in some way - the Dutch book argument is related but more explicit; Dutch book arguments are another pillar of the case for using probability distributions to represent uncertainty.  You can look up the details on wikipedia and work through the proof on your own, but the gist of it is: 
Suppose you're forced to write prices at which you'd be okay with buying _or_ selling a bet (e.g. "how much would you pay ex ante for a certificate granting '35$ if horse 2 wins the race and horse 1 comes in third'? ").  Those prices had better be the odds derived from a probability distribution - if not, there exists a 'Dutch book' of bets which someone can buy from you and win money with certainty.  If you don't see the significance, note that life is such a series of forced-choice bets.  This is the "money pump" argument.  Use probabilities or you're the chump.

More about 'objective probabilities in a moment', but note that SIC-POVMs, beloved tools of the QBists, show that the WF is equivalent to a probability distribution (if usually a more elegant representation).  If you like to think of the WF as 'real', this should make you suspicious - what are the odds that some physical piece of reality _just so happens_ to have the exact same structure* as the sole natural way of representing beliefs about the world?  Does that sound plausible?

*quantum probability distributions can be reasonably interpreted as having _more_ enforced structure than normal ones - schematically, you add 'measure' and 'wait' to your list of special verbs that you can conjoin to form possible experiments (analogous to 'and' and 'given' in classical probability), then you have constraints between beliefs related by those verbs.

### Normativity and 'non-determinism'
In the classical world, classical mechanics is 'correct'.  It makes only correct predictions.  No observation is ever made which is not precisely as Newton would have it.  Specifically, it is not a 'good' theory, which one might compare to other potentially 'better' or 'worse' theories.

Mathematically, "better" and "worse" require some implied measure over the space of possible experiments. The classical world does not require such a measure - there is a brutal, but natural, complete order, call it $\preceq$, on theories; let $\mathcal{T}$ be the set of theories:

$$
T_1 \preceq T_2 \iff \mathrm{"}T_2 \text{ makes the correct prediction in every situation"}
$$

There is a maximal element of $\mathcal{T}$ - classical mechanics ($CM$) satisfies 

$$T \preceq CM \quad \forall T \in \mathcal{T}$$

and further, imperiously,

$$CM \preceq T \Rightarrow T=CM$$

For QM this is obviously not the case - it predicts probabilities, not outcomes.  If we want to take QM on its own, probabilistic terms, the best we can do is say that there's a natural _partial_ order on non-deterministic theories:

$$T_1 \preceq T_2 \iff \text{For every experiment, the probability assigned to each outcome by } T_2 \text{ is closer than that of } T_1 \text{ in absolute value to that obtained by repeating the experiment infinite times}$$

Taking as fact that there is an underlying deterministic ontology (e.g. as in Bohmian mechanics), this partial order is obviously unfair!  The obviously best theory is the one which knows the hidden variables and spits out the correct answer every time (we presumably can't find it, but it sure is an element of $\mathcal{T}$.  If there's an underlying reality to which we have no access (i.e. hidden variables), then experiments cannot be made equivalent because you can't control for the hidden variables.  So now we have a partial order which appeals to repeated experiments for probabilistic theories, and a complete order for deterministic ones.

I'm having a hard time pinning down the question I want to address here, but I think it comes down to suggesting that we should have a two-layer perspective: the closer, subjective-epistemic layer with the EWF, and the underlying ontological layer where the 'real stuff' happens - and that that second layer _must_ be conceived of as deterministic.  Non-determinism would require the existence of _objective_ probabilities.  Objective probabilities are only definable in the frequentist sense, but these would be in-principle unmeasurable and _necessarily isomorphic_ to a deterministic ontology with that stochasticity moved 'up a layer' to the subjective/epistemic uncertainty.

Put another way: we're concerned with quantum foundations insofar as there are a whole bunch of different ontologies that can all reproduce QM, but they all suggest radically different ways to expand on QM - that's the value.  Asking if the universe is 'fundamentally stochastic' is not such a question - that assertion is always equivalent to a subjective uncertainty over objective determinism.  Probability is the natural companion of subjective uncertainty, so given a choice between a world model with probabilites in the objective vs. subjective layer, the latter is, if not the only choice, the obviously better one.  All this to defend determinism lol.

### Naming the knowledge we are forbidden
Let's try and build a toy model / mind-map of how quantum foundations is actually going to be useful to science instead of being sophistry:

Suppose there's some objectively real "actual reality ", $\mathcal{M}$, which has a bunch of states $s$, and evolves deterministically from one state to another according to $\dot{s} = f_{\mathcal{M}}(s)$ (I tried to think how to not posit 'time' directly but its too hard for me to think about for now).  We as agents make some observations $o$ which reveal information about the state of reality, and there's some deterministic "bridge-transform" $\mathfrak{B}_{\mathcal{M}}: s \rightarrow o$ which maps states to observations.  We can use observations to update our beliefs about future observations according to normal quantum mechanics and Bayes.

$$
\mathcal{M} \xrightarrow[]{\mathfrak{B}_{\mathcal{M}}} \{ o \} \leftrightarrow \psi
$$

Every underlying ontology that we talk about (Bohm, Everett, etc.), <span>$(\mathcal{M}, \mathfrak{B}_{\mathcal{M}})$</span> is _chosen_ so that Bayesian updates based on $o$ reproduce the normal quantum mechanical predictions.  Crucially, a $\psi$ encoding beliefs about experiment outcomes, along with a (possibly arbitrary) prior over <span>$\mathcal{M}$</span>, can be used to write a probability distribution over $\mathcal{M}$ the underlying state of reality.  This can be time-evolved with $f_{\mathcal{M}}$.

The _game_ is to take different <span>$(\mathcal{M}, \mathfrak{B}_{\mathcal{M}), f_{\mathcal{M}})$</span>, propose slight perturbations, and see if this gives 'new physics' (cashed out as different predictions from normal QM).

A good example is Bohmian mechanics - as I understand it, $\psi$ (as OWF) is a real dynamical variable, which evolves in such a way that for most priors over the hidden variables, Bayesian-updating will converge you to Born-rule predictions _dynamically_- a testable difference!  Or you could just propose that the hidden variables actually couple in some way that sometimes lets you see them.

Another example I have in mind is Weinberg's nonlinear quantum mechanics with Everett: Everettian mechanics gets all of its probabilities from the bridge-transform (which in this case is approximately equivalent to anthropic reasoning) - adding any nonlinearities / cross-talk between diverged branches of the wave-function corresponds to changing the dynamics $f$.

The goal of 'finding new physics' is then synonymous with assigning some prior to which of these ontology-triplets is correct - by which we mean that a small perturbation to that ontology generates a more accurate model of the world - and performing experiments which have the maximum expected value for a given cost.  Presumably most of those perturbations we would test and just set a super low upper bound on how big the putative coupling is.  A pragmatic problem with this perspective is that we're so partisan for or against certain theories that we could plausibly have an odds-ratio for a given ontology of 10^5 - we should probably be humbly ecumenical and even admit the (imho) silly collapse-based theories into consideration.  Perhaps that expected value calculation could even be weighted by utility or coolness - discovering that spacetime causes all superposition-collapses would be less interesting (imo) than the FTL communication implied by nonlinear Everettian QM
