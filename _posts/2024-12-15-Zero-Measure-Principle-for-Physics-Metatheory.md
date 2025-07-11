---
title: "[Musing; Physics] Zero Measure Principle for Physics Metatheory"
date: 2024-12-15
---

#Sketch of a Metaprinciple for Physics

###Physics Paradigms
There are a few "big-deal" trends in the history of physics - probably more than I as a practitioner am aware of.  One is mathematization - the use of mathematical language to describe physical phenomena; this makes descriptions precise, falsifiable, and establishes a "search space" of "nearby equations" should your first attempt prove wrong.  Another, a big part of the paradigm under which we now labor, is symmetry - the idea that mechanical systems have certain symmetries, and these symmetries entail things about the system which are usually pretty important.  This has been elevated to such a level that the completion of the standard model might be colloquially described as "trying to guess the right symmetry group".  The really shockingly _original_ application of this idea to generating theories about physical reality is the creation of special relativity from symmetries of the Maxwell equations.

There are two veins of question that nag at me about this - one, _why_ can we guess symmetries and have this meaningfully work? - and two, what is the general principle from which we can derive new theory-guessing techniques (i.e. the 'successor' to symmetry-based guessing)?  To the first, I would be reasonably satisfied with an explanation that goes like "yeah we're guessing symmetry groups, which would seem to entail we're supposing that our theories are actually described by however many tens of bits it takes to identify a few lie groups, but in actuality, all the bits of our theory-specification comes from machinery that we build _on top of_ this symmetry game, and it 'just-so-happens' that the machinery that worked for doing this in QED was robust enough to get QCD too".

###Whither Simplicity?

My basic intuition is that its unjustifiable to assume that the correct theory of nature should be fundamentally simple, and the seeming fact that doing physics _as if_ it were works really well has to say more about the meta-level framework in which we build theories than physical reality being actually governed by a QFT Lagrangian with a low-double-digit number of terms.

So lets take a step back and think through the Lorentz example: Galilean relativity seems to be a symmetry of the world as we humans experience it; we discover electromagnetism, and find out that Maxwell's equations don't obey this symmetry (all our other theories do, but for reasons approximately like 'by construction').  In fact, they obey a Lorentzian symmetry, which _reduces_ to the Galilean one in the limit of some parameter.  Thus, we can say "the universe obeys Lorentzian symmetry, and our experience of Galilean symmetry is just because we inhabit a particular limited regime of parameter space, thus the two are concordant".  The next natural development is GR, which says "ah but Lorentz symmetry is actually only true in the weak-field limit of gravity" - moreover, GR starts from the fundamental principle of covariance, which I'd heuristically state as "the laws of physics are the same in all reference frames (and thus have to include recipes for comparing them between different reference frames)".

###Zero Measure Principle (name provisional)

I'm trying to build up here to articulating a "principle of zero measure", which my first draft of would be "if your theory has some property which is not generally true for other members of the broader class of theories, it's not an accident" (if your theory is a 'set of measure zero' in some broader theory-space, it's not by chance).  Maxwell equations' Invariance under Lorentz transformations is a property of measure zero in the space of all such equations.  Galilean symmetry is too!

This leads me to articulate the second principle which ties in to this: "Assuming the universe is fundamentally complicated (has arbitrarily high Kolmogorov complexity), any simple description of it that approximately works must only work in some limited regime".

I can think of basically three ways that you end up with a description of physical law that has a measure-zero property: 1) the ontology you're working with builds it in, 2) the theory's area of applicability is the limit of some parameter ε s.t. the symmetry exists only asymptotically as ε goes to zero or (relatedly), 3) some underlying dynamics exists which (for 'most' initial conditions) will limit to some solution where that property effectively holds.

### Examples

Examples for (2) are SR and GR, and really anything to do with asymptotics - this is the most familiar to us.  It also includes all the obvious cases where your theory is actually just the first term in an expansion of that parameter.

For (1), an example is something like determinism in classical mechanics - no one was really guessing probabilistic theories, but the second you consider them you have to stop and go "woah wait a minute 0% of the theories in this enlarged space have the property that I thought it should, yikes" - I think this is the hardest of the 3 to really work with, since ontology is kinda fraught.  Maybe Kant solved this 200 years ago, idk.

For (3) an example is classicality arising from QM; as WKB approximation indicates, classical mechanics is definitely _not_ the limit of quantum mechanics in the same way that Galilean relativity is of Lorentzian, even after accounting for the difference due to non-determinism.  The small hbar limit corresponds to the large n eigenvalue limit, and the n-th eigenfunction literally does not converge to the classical probability distribution (for the normal definition of 'converge').

I don't think those three reasons are exhaustive, but they cover all the examples I have in mind.
Morally, my point is that every time you can show that a theory has some cool geometrical property (which they should!  Reality approximately has those!), you should think "ah this is the limit of some bigger theory which recovers this property only in some limit" - specifically I claim not that that _can_ be true, but that it should basically _always_ be true!

The problem I was thinking of that had me cogitating on this is the fact that Newtonian gravity has this nice 1/r potential - which is one of two potentials satisfying Bertrand's theorem, s.t. all bound orbits are closed.  That latter property has nothing to do with anything and I have no idea how to cash that out into a higher theory that would dynamically recover that (even though I _know_ that GR is that theory- this shows that it's not trivial to apply this meta-theory!).  This got me to thinking about if the Einstein equations _assume_ or _imply_ 1/r gravity (i.e., if gravity had an exponent 6.52... does GR have a twin that yields that in the classical limit?).  I spent half a day thinking about this and reading about f(R) gravity, but I don't know because I'm a n00b in GR and the higher-end QFT stuff.

###Why Time Travel, FTL, Etc. Are All Possible ("The no-no-go theorem")

Another great example I had in mind while writing this is Weinberg's paper "testing quantum mechanics" where he discusses non-linear schrodinger equations etc. and figures out bounds for what we could detect and what we would expect to be properties such solutions would have.  This is one of the reasons I like to say time travel and FTL and communication with other Everett-branches are all 'definitely possible' - sorta as a joke since they probably aren't practical (but who knows what the limits of technology are), and they may end up being impossible for reasons of ontology, but hey fun to think about!
