---
title: "Alternatives to Entropy; Eigenvalues of Odd Things"
date: "2026-02-03"
tags: [math, information-theory, spectral-theory]
---

# Alternatives to Entropy; Eigenvalues of Odd Things

In other posts I have argued we usually shouldn't use information theory to describe phenomena on metric spaces.  Here I'll talk about an alternative that I've found generally useful if not entirely satisfactory.  This is instead to look at the spectra of linear operators.  Since this is a question that has lived in my head for a long time, I have found a lot of cute objects by forcing myself to not use the Shannon entropy.  This isn't very thematically unified - the two connecting threads are 'things that you might use in place of entropy' and also, separately 'ways to associate eigenvalues to objects that have no business having eigenvalues'

## Exordium: Who asked?

Information theory is very useful for describing random variables whose values are discrete and incommensurable - i.e., letters in an alphabet.  This is less true of integer-valued random variables, and less still of continuous ones; the axioms of information theory jive very poorly with how we like to conceptualize real numbers and their ilk.  We have a problem then: the mutual information and related quantities are _really_ useful for describing information processing; there's a burden of proof then to show that there are other useful things one can use to speak of similar things.  Here I'll share a potpourri of these metrics which I've found useful for thinking.  I've generally found spectra a good frame for thinking also about non-information-y things, so as noted I'm not really going to try that hard to restrict myself to entropy-alternatives.

## Metric Entropy

For: sets in a metric space
(Applies to any set; has scale parameter $\epsilon$)

This is the most direct and straightforward alternative to differential entropy.  In a metric space $(\mathcal X, d)$, the metric entropy at scale $\epsilon$ of some set $X \in \mathcal X$ is defined as the logarithm of the minimum number of balls of radius $\epsilon$ required to fully cover $X$.

The comparison to traditional entropy is direct: we've essentially constructed an 'alphabet' whose symbols are these balls, and the metric entropy is the entropy of the uniform distribution over these.  $\epsilon$ determines, in effect, how coarse this alphabet is.

Metric entropy captures some nice properties of sets in metric spaces; if the set $X$ has dimension $d$, then the metric entropy will scale like $H_{\epsilon}(X) \sim d \log \frac{1}{\epsilon}$ - the dimension of the set is, effectively, the number of bits required to resolve $X$ at, say, twice the resolution.

The main result which tells us that metric entropy is useful and not a mere flight of fancy is the [global Fano method](https://projecteuclid.org/journals/annals-of-statistics/volume-27/issue-5/Information-theoretic-determination-of-minimax-rates-of-convergence/10.1214/aos/1017939142.full) (Yang and Barron, 1999): the minimax estimation error over a function class is governed by the _critical radius_ $\epsilon_n$ at which the metric entropy balances the sample size, i.e. $\log N(\epsilon_n, \mathcal F) \asymp n\epsilon_n^2$.  Below this scale, there are more distinguishable hypotheses than the data can discriminate between, so estimation error cannot be smaller than $\epsilon_n$.  This jives with the above: to match to scale $\epsilon$, you basically need to specify the value of the function at the center of each ball of size $\epsilon$, so the metric entropy tells you how many points that is.

## Laplacian

For: Graphs, shapes, manifolds

This one is very cool, but is only distantly related to information theoretic entropy - I'm including it because it's fun.

If you have a manifold $\mathcal M$, it comes with its own Laplacian $\Delta_{\mathcal M}$ (suppressing $\mathcal M$ hereafter).  Then, by calculus magic, you can find a complete set of orthonormal eigenfunctions on $\mathcal M$ with eigenvalues $\lambda_i \geq 0$.  These eigenvalues tell you how fast heat packets placed on the manifold will decay - if the manifold has a high dimension, they decay rapidly, and less so if not.

Two super-cool theorems:

[Weyl's law](https://en.wikipedia.org/wiki/Weyl_law): The density of eigenvalues of the Laplace operator scales as $\lambda^{d/2}$ - i.e. the density of eigenvalues lets you read off the dimension.

[Heat kernel asymptotics](https://en.wikipedia.org/wiki/Minakshisundaram%E2%80%93Pleijel_zeta_function#Applications): You can calculate some neat differential geometry stuff if you know how heat flows over short times.

I promised a recurring theme would be the importance of scale in defining our measurements; I'll leave it as an exercise how one derives an entropy measurement from the heat-kernel asymptotics, but the essential thing governing the scale is the time $t$ you wait after dropping your heat source.

## Spectral Entropy

For: anything where you already have eigenvalues

This one kinda applies any time you have the spectrum of some thing, rather than being an interesting spectrum itself.  Essentially, it tells you 'effective number of directions', in the same way that the traditional entropy tells you 'effective bits communicated per symbol'.

If you have some eigenvalues $\lambda_i$ (or if you prefer SVD, that works too), the spectral entropy is the entropy of the probability distribution

$$
p_i := \frac{\lambda_i^2}{\sum_j \lambda_j^2}
$$

$$
H[\{\lambda_i\}] = H[p_i]
$$

This is less hacky than it might sound at first, if you think about how it relates to coding theory.  The noisy-channel coding theorem says that if you have a noisy channel, the channel-capacity is how much information you can transmit if you allocate a fixed unit of power against some fixed profile of noise.  On the other hand, if you have a matrix $A$ and multiply it against a random vector of fixed energy, the spectral entropy is the number of 'significant' components you'd expect to see.  ([Roy and Vetterli, 2007](https://www.eurasip.org/Proceedings/Eusipco/Eusipco2007/Papers/a5p-h05.pdf))

## System operators

For: dynamical systems and linear operators

If you have a dynamical system $y = \mathcal G(u)$, then $\mathcal G$ has its own set of norms - if $\mathcal G$ is LTI, basically these are just [operator norms](https://www.mathworks.com/help/robust/gs/interpretation-of-h-infinity-norm.html); if not, I guess go read a book on nonlinear control theory.  Recall that an operator norm (for a _linear_ operator $T$) is

$$
\lVert T \rVert_{1 \to 2} = \sup_{x} \frac{\lVert T x \rVert_2}{\lVert x \rVert_1}
$$

(the 1 and 2 refer to the norm with respect to the input vs output space, resp.)

So then you can play a game where you specify different norms on each space.  The $\mathcal H_\infty$ norm is the induced $L^2 \to L^2$ operator norm - it is the worst-case amplification of the system (equivalently, the supremum of the largest singular value of the transfer function over all frequencies).  The $\mathcal H_2$ norm is _not_ an induced operator norm at all; it is instead more like a Frobenius norm of the transfer function, and corresponds to the RMS output to white noise input.  (The analogy to matrices is exact: $\mathcal H_\infty$ is to the spectral norm as $\mathcal H_2$ is to the Frobenius norm.)

## Koopman, Hankel

For: dynamical systems

This is a whole rabbit-hole so I won't go into too much depth.  Tl;dr is that for any nonlinear system $x_{t+1} = f(x_t)$, you can do the Heisenberg trick and instead of looking at states, treat them as fixed and measurements as evolving.  The Koopman operator is the dynamical systems version of this (i.e., just a different letter, functionally).  For a measurement function $g(x)$, the Koopman operator $\mathcal K$ acts as

$$
\mathcal K[g](x) := g(f(x))
$$

$\mathcal K$ is linear, and therefore - you guessed it - has eigenvalues!  The eigenbasis is something like 'measurement functions which determine their own time-evolution without needing to know anything else about the underlying state', and the eigenvalues are the rates of growth or decay thereof.  $\mathcal K$ is generally phenomenally complicated, but boy is it cool, and control engineers often actually calculate with approximations for it.  ([Steve Brunton's lecture](https://www.youtube.com/watch?v=qOdwRel-1xA) is a nice introduction.)

Hankel is the cousin of Koopman.  If Koopman evolves measurements forward in time, Hankel maps input sequences to output sequences.  These can be made much more linguistically close, but I'll do it in a pretty different way instead; suppose you have some alphabet $\Sigma$; then if you have a function $f$ on strings drawn from $\Sigma$, the [Hankel matrix](https://proceedings.mlr.press/v70/balle17a/balle17a.pdf) of $f$ is:

$$
H[f]_{u,\, v} = f(u \cdot v)
$$

(where $u, v$ are any strings, $\cdot$ is concatenation, and the matrix is reaaaaaally big).

Of course, $H$ is a matrix and so it, too, has eigenvalues!  Again this is a bit of a rabbithole, but tl;dr, the eigenvalues are best understood as listing off 'how important' different features are for predicting $f$, and you can actually reconstruct approximations to $f$ by truncating.  I'll write more about this later since I find it conceptually useful for thinking about how computation 'should work'.

## Summary

I listed some cool math objects I like.  Some of them are alternatives to entropy for use in metric spaces, and others are things that are related-to-that-in-my-head-only.
