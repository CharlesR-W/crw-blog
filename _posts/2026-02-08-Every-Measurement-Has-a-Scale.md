---
title: "Every Measurement Has a Scale"
date: 2026-02-08
tags: [math, physics, epistemology]
---

# Every Measurement Has a Scale

In this post I will try to outline an idea which I have imbibed by studying physics, but which I think is generally applicable as a tool for thinking.  This is the idea: because we can only observe imperfectly, we cannot assert that any measurement is 'exactly zero'.  The crucial consequence is that, for a number to measure something meaningful, it must not be arbitrarily sensitive to unobservable changes.

(This same idea is what makes questions like "is this neural network loss at a minimum?" or "is this gene regulatory network modular?" malformed as stated — and suggests what to ask instead.)

As our example, we'll imagine an engineer has developed a theory that a beam of some length $L$, loaded with a particular weight, will, at coordinate $x$ along its length, bend an amount given by $f(x)$.  A mathematician (a group theorist, say), has looked at the engineer's measurements of $f$ and asked what the polynomial degree of $f$ is.  Here's why this doesn't work:

## Example: Degree of a Polynomial

Consider polynomials like $f(x) = 0.3x^{3} + 7x^2 +2$.  The power of the highest term is the 'degree' of the polynomial - in this case, 3.  I claim that 'degree of the polynomial' is not a good measurement.  Why?  If $f$ is to model the shape of our beam, we will have chosen the coefficients by taking some measurements.  These measurements might be taken for, say, $x$ between $x=0$ and $x=5$.  The problem with taking 'degree' of the polynomial as having anything to do with the real beam is that, for all we know, the true answer could be

$$
f_{true}(x) = 10^{-1000}x^{26} + 0.3x^{3} + 7x^2 +2
$$

This new polynomial has degree 26 instead of 3; but along the whole beam, it makes predictions which are functionally identical.  Because no practical measurement can tell which of these models is 'correct', any measurement which requires distinguishing between them is a bad one.

Now of course, the 'degree of the polynomial describing this beam' is unimportant to the engineer.  I claim that the engineer's studied indifference comes not from a professional distaste for abstract mathematics, but a subconscious recognition of the distinction I want to outline - that some measurements are 'good' and others are 'bad', and that we can often fix bad ones if we try.

## Fixing the 'degree' : Measurements have scale

There are a few ways to fix such a problem.  One might try to devise a new measurement entirely, or perhaps study the property which we had taken 'degree of the polynomial' to be a proxy for, and see if we can't do better.  The simplest and most general, though, is to caveat our measurement with a notion of 'scale'.

We ask ourselves what we might really have meant by 'degree' of the polynomial - the most likely meaning is "if I had a very long beam, how rapidly would the shape change for large values of $x$".  So now we might write

$$
\text{degree}[f] = \lim_{x \to \infty} \frac{x f'(x)}{f(x)}
$$

You can check that in the infinite limit, this gives us degrees 3 and 26 respectively.

The definition above is unphysical, in that of course our beam cannot be made infinitely long - the point precisely!  We will kill one unphysicality with another!  Instead of taking the limit $x \to \infty$, we will make an 'operational definition' of the degree, observed at scale $L$:

$$
\text{degree}_L[f] = \frac{L f'(L)}{f(L)}
$$

In words: instead of asking "what is the degree?", we ask "what does the degree look like at scale $L$?" — and get a perfectly sensible answer.

(If you're an economics enjoyer, you may note that this is the same as the log-log derivative $\frac{d \log f}{ d \log x}\big\vert_{x=L}$ used in defining elasticities.)

You could plot this for increasing $L$ and watch the answer change, but we can just estimate what scale is required to see the $x^{26}$.

Plugging in $L = 10^5$: the $x^{26}$ term contributes about $10^{-870}$, while the $x^3$ term contributes about $10^{14}$.  Not even close.  Setting the two equal:

$$
1 = \frac{10^{-1000}L^{26}}{0.3 L^3} \to L \sim10^{43}
$$

In order to start really seeing the effect of the $x^{26}$ term (or to conclude that it's really not there), we'd need to look at beams of $L=10^{43}$ meters - longer than $10^{41}$ football fields!

The epistemological point is that, while we can't say "the polynomial degree of the beam's shape is \_\_\_\_", because of the sensitivity problem, we can back off, ask what that degree was a proxy for, and say "at scales of 10s of meters, the effective polynomial degree of the beam is 3".

Physicists speak this language in reverse; they imagine a particular 'family of theories' $f_{true}(x) = \epsilon x^{26} + 0.3x^{3} + 7x^2 +2$, and say things like "at great expense and after decades of work, CERN was able to build a steel beam 10,000 meters long, and we can confirm that $\epsilon \leq 10^{-114}$."

## Conclusion

So the takeaway is that we like to use math to describe the world, but not every property of a math object is a meaningful reflection of the thing it models.  Instead, we build a model, try to list a few perturbations to that model, and ask how well we can bound those perturbations based on our current measurements.

Exercise: Imagine you are a big Charles' law enjoyer, and think that $\frac{V}{T} = \text{const}$ (i.e. the volume of a gas is proportional to its temperature) describes how gases behave.  Your measurements are good but not great - what perturbations might you write down?  What does it feel like when you realize you'd forgotten to vary some quantity you'd been holding fixed?  Try and convince yourself that "$= \text{const}$" is always a joke.

Here are some places where this thinking has been relevant to me lately:
- Loss landscapes of neural networks, $L(\theta)$ - the 'true' loss is defined as an expectation over all possible data, but you only ever evaluate it on a finite sample.  The number of samples you use determines the scale at which you can resolve the landscape.
    - Exercise: for this reason, you can't ever ask if $\theta_0$ "is a minimum" - what's the smarter version to ask?  How might you measure it?
- Emergent Modularity: a theory goes that biological systems evolve to be modular as a response to a changing environment.  There are two timescales - the timescale of environmental variability and the timescale of selection; if either is much faster than the other, selection for modularity does not occur.  Can you say how strongly modularity should be selected for as a function of the ratio between the two timescales?

The common thread in all of these is that 'exactly equal to', 'is a minimum', etc. are all claims which cannot survive contact with finite-precision measurement.  The fix is always the same: replace the binary question with a quantitative one, and state the scale at which you're asking it.

I'll add the obvious caveat that there are times in life when this is true - if little Billy has 3 apples then it would be asinine to assert we should think of this as coming with an error bar.  I think most of discrete math and computer science fall into this category, with information theory falling somewhere in between.  In physics, topological phenomena and group-theoretic things are "sorta" discrete - story for another day.

Heraclitus said "All things flow, and nothing remains the same".  So too it is of constants - there are no constants, only scales at which things may be regarded as constant.  I find this deeply humbling - the search for knowledge should feel something like trying to bootstrap our way out of quicksand.
