---
title: "Renormalization for Pyrrhonists, Pyrrhonism for Particle Physicists"
kind: essay
date: 2026-11-20
math: true
tags: [personal]
---

In the more serious half of this essay I will argue that:

- all our measurements are of finite precision; we should assume our theories are of finite validity;
- we have no particular reason to imagine that there is no 'new physics' below the Planck scale;
- therefore we should by default subscribe to a certain strong form of the [totalitarian principle](https://en.wikipedia.org/wiki/Totalitarian_principle): 'everything not forbidden is mandatory and nothing is forbidden except in the sense of being forbidden _below a certain energy scale_'.

Every ontology is only an effective ontology; [every tail comes apart](https://slatestarcodex.com/2018/09/25/the-tails-coming-apart-as-metaphor-for-life/).  The only question is whether your rules or your ontology breaks first.  I intend to write a related post on [Quantum Suicide](https://en.wikipedia.org/wiki/Quantum_suicide_and_immortality) soon.

[Pyrrhonism](https://en.wikipedia.org/wiki/Pyrrhonism) is a capital 'S' Skeptical Greek philosophy which has a [similar metaphysics to Buddhism](https://en.wikipedia.org/wiki/Pyrrhonism#Similarities_between_Pyrrhonism_and_Indian_philosophy), but I like it more because the Greek words sound cooler to me.  The less serious latter half of this essay is more like a written response to a Greek-philosophy-shaped Rorschach test.

## Renormalization Completes the System of German Idealism[^meme]

"Renormalization" is a cursed word that refers to a ton of different techniques in physics.  For our purposes, it means "I have a theory of physics that applies in some limited regime - there's some underlying thing happening with atoms and stuff, but that all washes out into a few 'constants', so I can measure those constants and ignore the microscopic structure".

### Example 1
Fluids like water and mercury are described by the same theory - fluid mechanics - with the microscopic differences washing out into a few constants like viscosity and density.  In this example we have changed the variables of inquiry (density and velocity of fluid 'parcels' rather than the position and momentum of the individual molecules).  We don't always 'change variables' in this way.

### Example 2
In quantum field theory, we like to pretend that there are individual particles that have things like mass and charge.  In fact, should you do the math, you'll find out that a particle is always "dressed" by a cloud of other virtual particles, as dictated by the uncertainty principle.  This cloud of particles interacts with the 'bare' particle, and i.a. makes it harder to move.  For most purposes, this cloud is too small to participate in interactions, and in practice, we simply add its mass to the 'bare' electron mass.  But!  In reality we can't turn off this cloud of particles, so the 'bare electron' does not, strictly speaking, 'exist' - we must content ourselves with measuring the dressed mass.

At very high energies though, these clouds can begin to affect interactions.  The most delightful example is the fine-structure "constant", $$\alpha$$, which says how strong the electromagnetic force is.  Usually, it is about $$\alpha \approx 1/137$$.  But!  When you work at big ol' particle colliders you find yourself having to use $$\alpha \approx 1/128$$ (or so) instead!  The "value of the constant" changes.

### Example 3
There's no such thing as zero.  As an example, let's imagine the function $$y = x^4 + 0x^2 + 0$$ (foreshadowing).  Aren't those zeroes there?  Let us now account for the [transcendental limits of our inquiry](https://en.wikipedia.org/wiki/Critique_of_Pure_Reason), in a toy way, by supposing that, on querying the value at a particular point $$x$$, we smudge the microscope a bit and end up taking the average of the function over a very small region of size $$\beta$$: $$y_{\text{eff},\beta}(x) = \mathbb E[y(x+\beta \xi)]$$ with $$\xi$$ a standard Gaussian random variable.  So in fact we observe $$y_{\text{eff},\beta}(x) = x^4 + 6\beta^2 x^2 + 3\beta^4$$: both zeroes have been filled in, by terms that vanish only as our microscope becomes perfect.  This is why physicists do not say that "there is no quadratic component to this function", but instead "the quadratic component can be no larger than $$10^{-34}$$".

### There Are No Integers, Only Effective Integers at Low Energy

In fact, I claim (controversially but confidently) that the _converse_ is true: that every number used in science is the result of a process like this.[^singular]  The "viscosity" constant was always going to depend on temperature, or magnetic field; the spring 'constant' was always going to depend on how far you stretch the spring.  More precisely, let us suppose there is an abstract "space of all possible physical theories", large swathes of which look the same at very low energies.  If we observe that some property like a symmetry seems to hold 'exactly', it will in fact always be a better explanation which is able to say that _if_ there was a violation of this symmetry, there is some mechanism by which it will be suppressed - this explanation simply has more mass in probability space.

I have talked at extreme length (h/t [Erez Abrams](https://www.lesswrong.com/users/erez-abrams)) with those who insist that one should use a Solomonoff prior, which perhaps _could_ assign enough measure to zero-measure solutions for this argument to not apply.  On my view, this is correct iff we are in a simulation run as a Turing-like computation.  If we are in base reality, "[I]t depends on what the meaning of the word 'is' is".

This holds in a different way for definitions.  This will be a delightful instance of ['the tails come apart'](https://www.lesswrong.com/posts/dC7mP5nSwvpL65Qu5/why-the-tails-come-apart).  Consider the speed of light in vacuum - in practice we mean at least two different things in saying 'the speed of light': the speed at which a photon travels, and the speed at which causal information propagates.  If one supposes there is a nonzero breaking of gauge symmetry which has been suppressed by renormalization, almost certainly well past the energy scales at which photons exist, possibly past the Planck scale, one can _technically_ pull out a term that looks like a photon mass.  Thus whether photons propagate at the speed of light is a question of which breaks down first - the gauge symmetry or spacetime itself.

This is why [dimensional regularization](https://en.wikipedia.org/wiki/Dimensional_regularization)[^dimreg] works - there really are $$d = 4 \pm \epsilon$$ dimensions, so whatever effective theory we have in $$d=4$$ must be stable to perturbations in this number.  Though the concept extends beyond string theory, string theory is famous for proposing that there are 10 (or, in M-theory, 11) dimensions, of which the unobservable ones [are 'compactified'](https://en.wikipedia.org/wiki/Compactification_(physics)).  There are no integers - only effective integers at low energies.

## Pyrrhonism

> Pyrrhonism is an Ancient Greek school of philosophical skepticism which rejects dogma and advocates the suspension of judgment over the truth of all beliefs. It was founded by Aenesidemus in the first century BCE, and said to have been inspired by the teachings of Pyrrho and Timon of Phlius in the fourth century BCE.
>
> — [Wikipedia](https://en.wikipedia.org/wiki/Pyrrhonism)

The goal of Pyrrhonism is the achievement of a state of tranquility, known as 'ataraxia'.  It is plausibly a violence to the philosophy to think of its epistemics without reference to its moral aspects.  At time of writing, [nobody has yet stopped me](https://www.youtube.com/watch?v=91YS3fNegmE).

The _epistemic_ core of Pyrrhonism is the principle of 'epoche' - the 'suspension of judgement'.  They claim that 'dogma', to believe that one has come to truth in '[non-evident matters](https://en.wikipedia.org/wiki/Our_Mathematical_Universe)',[^tegmark] is what prevents one from obtaining tranquility.

The Pyrrhonists may be divided into three classes according to how they go about achieving this 'suspension of judgement'.  Fantastic vocab words.  I can only infer the meaning of two of the three from Wikipedia,[^fakefan] so we'll ignore 'the ephectic' ones.

The **'aporetic'** Pyrrhonist seeks to reach a state of confusion by continually refuting arguments for or against various ideas.

The **'zetetic'** Pyrrhonist is more adversarial - their suspension of judgement is _in service to_ their continued search for a reason to cease their suspension of judgement.

### Humility and Hubris in the Search for Truth

What is the relationship to this renormalization group stuff?  Certainly my position implies a deep skepticism.  If I may `</shitpost>`, I will say that I think renormalization is the most _sublime_ insight physics has to offer.  Renormalization builds into our theories a recognition of the fundamentally limited nature of our quest for knowledge.  Applied Kantianism!  Not just that, but it works!  There are textbooks on it with equations and numbers and experiments!  I think this zetetic spirit - confusion in service of the search for truth - is not a tool, but the thing which imbues science with personal meaning - which makes it good for the soul.

I see in myself much of the aporetic.  My journey in intellectual life has been a continual humbling - to be ever the less sure, to regard so much as strictly provisional - aspirationally, to be the more open.  I think often about the way in which love changes one's values - here I feel this deep confusion, a true impasse of the soul.  What is one to make of partisanship amongst one's intertemporal parliament of selves?  Parts of me have fundamentally different values, and there really is only the solution of 'epoche' - to agree to disagree and do our best together.

I think the zetetic the more noble.  I find that the more I think of myself as 'a scientist', the stronger the part of me which wishes to build, to construct, to leap outwards towards truth rather than to shuffle gingerly along the edge of our knowledge as though it were a cliff-ledge.  There is a me quick with snide remarks about every research agenda under the sun.  There is also a me which sees itself in the daring to try.  This part of me wants to be less quick to argue, to criticize - it wishes to think of others not as threats but as fellows to be held up and stood by.  Actualizing this better me is at base an act of 'unseeing', of 'desymbolization', of being confused so as to learn to see more clearly.

---

> _πάντα ῥεῖ καὶ οὐδὲν μένει_[^pantarhei]
>
> — Heraclitus (attributed)

[^meme]: [Know Your Meme](https://knowyourmeme.com/videos/161508-donald-trump).

[^singular]: Exceptions to this are singular limits, though they prooobably aren't well thought of as implying new metaphysics.  The book "Devil in the Details" by Robert Batterman is enjoyable for this.

[^dimreg]: Construed broadly.  This technique often regularizes a case where only the negative side of the limit works, which I think makes mine the wrong interpretation for those cases.  Sue me.

[^tegmark]: That link is a joke; Max doesn't deserve my being mean to him, lol.

[^fakefan]: Yes, I'm a very fake fan.

[^pantarhei]: _Panta rhei kai ouden menei_: "everything flows, and nothing stays still."  Traditionally attributed to Heraclitus, though this exact wording is a later paraphrase; the oldest version is Plato's report in the _Cratylus_ (402a) that Heraclitus says _πάντα χωρεῖ καὶ οὐδὲν μένει_, "everything gives way and nothing stays fixed."
