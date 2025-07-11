---
title: "[Information Theory] Why Differential Entropy Stinks (And What to Do About It)"
date: "2025-06-24"
---

# Why Differential Entropy Stinks (And What to Do About It)

## Abstract

In this post, I argue that differential entropy is fundamentally flawed as a measure of information content in continuous random variables. The standard definition $h(X) = -\int p(x) \log p(x) dx$ can be negative, infinite, and does not satisfy the data-processing inequality.  While there is no satisfactory extension of entropy to continuous variables, I outline a formalism of the intuition that entropy loss should arise from numerically poorly conditioned operations.

---

## Introduction: The Problem with Differential Entropy

Consider a continuous random variable $X$ with probability density function $p(x)$. The standard definition of differential entropy is

$$
h(X) = -\int p(x) \log p(x) dx
$$

This definition has several fundamental problems. For one, it can be negative or infinite, unlike the entropy of most discrete distributions.  More irritatingly, the only thing that makes entropy matter is that it satisfies the data-processing inequality:
$$H(X) \geq H(f(X))$$
There is no way to process random variables which increases their entropy.  Entropy is 'the' unique object that counts distinct states and _only_ counts distinct states - it doesn't care what those states are labeled.

Measure theory gives us language to speak of probability distributions which are continuous just as well as it does over discrete.  It is in fact perfectly fine to define the KL-divergence
$$D_{KL}(p||q) = \int ~p(x) \log \frac{p(x)}{q(x)}dx$$
as long as q is nonzero whenever p is.  A hacky solution is obvious: let's take DKL and set q to one, plop a minus sign and call it a day.  That gets you the formula you want, yes.  But it doesn't make any sense - we've lost all the transformation properties that make entropy _meaningful_.  Viz: consider $X$ uniform on [0,1], which "has entropy" zero.  Yikes.  Consider that $Y=aX$ for some constant $a$ has entropy $\log a$ (more than zero!).  Yikes.  Consider the delta distribution, $\delta(X)$, which has entropy ????? (remember that this is basically the continuous analog of the deterministic distribution which has entropy zero).  This problem sorta is solved if you also have $q(x)$ transform, then the entropy isn't well defined at all because you have to specify $q$.

---

## Why Entropy is Still Reasonable Sometimes (By Accident)

Despite these fundamental flaws, differential entropy sometimes gives reasonable results. This happens when the operations under consideration are well-conditioned with respect to the natural measure on the space.

Consider a transformation $Y = f(X)$ where $f$ is differentiable and invertible. The change of variables formula gives

$$
p_Y(y) = p_X(f^{-1}(y)) \left|\frac{d}{dy}f^{-1}(y)\right|
$$

The differential entropy transforms as

$$
h(Y) = h(X) + \mathbb{E}[\log |f'(X)|]
$$

Now if you think of the continuum as being the basic thing we're concerned with, this doesn't help.  If you're willing to put on your numerical hat, however, we can still come to an understanding with our old friend...

---

## The Discrete Limiting Density Approach

The standard approach to "fix" differential entropy is to consider a sequence of discrete approximations. Let $\mathcal{X}_n$ be a sequence of increasingly fine discretizations of the continuous space, with mesh size $\Delta_n \to 0$. Define the discrete entropy

$$
H_n(X) = -\sum_{i} p_i^{(n)} \log p_i^{(n)}
$$

where $p_i^{(n)}$ is the probability mass in the $i$-th bin of the $n$-th discretization.

The hope is that $H_n(X) - \log(\Delta_n) \to h(X)$ as $n \to \infty$. However, this limit depends crucially on the choice of mesh.  If we use a uniform grid, we implicitly assume a uniform measure on the space. More generally, we need a reference measure $\mu$ and define entropy relative to it:

$$
h_\mu(X) = -\int p(x) \log \frac{p(x)}{\mu(x)} dx = D_{KL}(p || \mu)
$$

Same as before, eh?  But with a different interpretation - $\mu$ is now the relative density of limiting points.  For concreteness, if we take the mesh to be have constant spacing between points, $\mu$ will be constant; if we take it to have logarithmically spaced points, $\mu$ will be exponential.  Compare: "We can represent real numbers using N+N bits, dedicating N bits to the integer part and N to the fractional part" ---> Linearly spaced points, $2^{-N}$ apart.  Or, "We can represent real numbers as 2^X where X is \[the same thing as above\] - a float with no significand" - then points are spaced logarithmically with their _ratio_ constant at $2^{2^{-N}}$.  (I'll be honest it seems like this should work for general floats but I haven't had the patience to sit down and do all the limits carefully).

So if we commit to some $\mu$ and say this is the asymptotic density our number-representation would have in the limit of infinite bits, we can make sense of differential entropy again.  More straightforwardly, your continuous distribution is really a discrete distribution if you consider finite-precision representations of numbers.  Let's get to work figuring out where that entropy goes.

---

## Conjugate Unary Operation Formalism

To understand irreversibility properly, we need a framework that respects the structure of operations. We'll do it once for unary operations, and another for binary ones, just to get the flavor of it.  Consider a general unary operation of the form

$$
G_f[X] = f^{-1}(g(f(X)))
$$

where $f$ is a fixed bijection and $G$ is some unary operation (in my mind, G is exponentiation, for concreteness). For binary operations, we define

$$
X \oplus_f Y = f^{-1}(f(X) + f(Y))
$$

This formalism captures two main examples we'll consider:

- **Addition**: $f(x) = x$, so $X \oplus Y = X + Y$
- **Multiplication**: $f(x) = \log(x)$, so $X \oplus Y = XY$
(and also some weirder ones like harmonic and, in a funky limit, tropical calculus - see my post 'Nonlinear Calculi')

The key insight is that the "natural" measure for an operation depends on the function $f$. For addition, the natural measure is uniform (fixed-point representation). For multiplication, the natural measure is logarithmic.  Specifically, $\mu$ is the Haar measure induced by $f$
$$\mu_{Haar}(x) = \frac{1}{|f'(x)|}$$
In this post we're gonna be a bit wishy-washy about the rigorous way to do this because I don't like trying to order limits if I can help it.  The Haar measure is what you're finite-precision representation wants to be in the limit of infinite bits.  Also, whether the Haar measure is of a point or of an interval is determined from context: $\mu(x) = \mu([x,x+dx])$.  For a finite interval $\mu([a,b]) = \int_{[a,b]} d\mu(x)$
## Real Irreversibility Measures Many-to-One-ness (Duh!)

The fundamental source of irreversibility is many-to-one mappings, but we're mostly considering invertible functions since that's what's interesting here.  The trick is that invertible functions aren't invertible when they make you lose precision (c.f. nine trillion engineer-hours designing stable matrix inversion algorithms and counting).

Consider an interval $[x, x+dx]$ and an operation $g$ that maps it to $[g(x), g(x+dx)]$. The irreversibility ratio is

$$
R(x) = \frac{\mu([g(x), g(x+dx)])}{\mu([x, x+dx])}
$$

where $\mu$ is the measure induced by the number representation. If $R < 1$, the operation is many-to-one and we lose information (and otherwise we don't).  For fixed-point numbers $\mu$ is constant, and the ratio is $g'(x)$; for exponent-only floating points, $\mu$ is linear, and the ratio is $\frac{d \log g(x)}{d \log x}$. The number of nats ("yes, I can only code in python how could you tell") lost is

$$
\Delta H_{g,x} = -\log(R(x))
$$
Test: if $g(x)=e^x$, we lose $x$ bits for fixed-point, and $\log x$ for exponent-only floating-point (really its the ReLU of this, since we never gain entropy).

Let's rerun the tape for a binary operation (which is just a curried unary operation, since we'll assume one of the variables is "overwritten" and the other isn't, otherwise of course you lose no entropy):

Take $g(x) = x \oplus a$ ($x$ is the 'overwritten' variable).  Then if $\oplus$ is $+$, we lose 0 nats in linear (and a weird $\log(1 + \frac{a}{x})$ in log rep), and if $\oplus$ is $\times$, we lose $\log a$ nats in linear space, and 0 bits in log-space.  Kinda feels like it makes sense?  

This formalism of course has the weird caveat that it only captures ill-conditioning in "one direction" - (in linear space) you lose bits by multiplying by a big number, but never by a small number.  This is easy enough to fix but it just involves some annoying conditionals and would be boring to read.  Also, no overflow errors, of course.

---

## Vector Operations and Privileged Bases

The framework extends naturally to vector operations, but with an important caveat: encoding each coordinate separately induces a privileged basis.

Consider a vector $\mathbf{x} = (x_1, x_2, \ldots, x_n)$ and a coordinate-wise operation

$$
\mathbf{y} = (f_1^{-1}(g_1(f_1(x_1))), f_2^{-1}(g_2(f_2(x_2))), \ldots, f_n^{-1}(g_n(f_n(x_n))))
$$

The irreversibility now depends on the choice of coordinate system (you can go through the derivations if you want; the density is the product of each individual density).  In particular, think about how if you're in log-space, the density of points at a given radius from the origin is _not isotropic_.  This means (exponent-only) floating-point breaks symmetry of space and induces a "priveleged basis" (this is also true for real floating points in a more complicated way of course).

---

## Conclusion: Summary and OT is Better

Differential entropy is fundamentally flawed but we can come up with a hacky way to make it still kinda respectable by considering the finite-precision number representation we actually end up using in computing.  All you have to do is interpret every continuous variable you see as a float and you can make everything discrete up to the float's bit depth - then take the limit of high bit-depth.  

In this framework, any operation that takes a number from where representable numbers are dense to somewhere where they are sparse must be a many-to-one mapping, and thus destroy 'entropy'.

For all that, it's still a hack, obviously.  Entropy is at the end of the day permutation invariant (you can _arbitrarily rearrange_ the points on a Gaussian and it will still have the same entropy).  This is almost always reasonable for discrete things.  It is not for real numbers.  No healthy mind knowingly and willfully uses the topologists' distance where $10^{-100}$ is as different from $0$ as $10^{+100}$.  Real numbers always have a metric attached - they have size and distance.  $\delta(x-1)$ should be closer to $\delta(x - 0)$ than to $\delta(x-153)$.

Strictly speaking, there's a broad family of metric-aware distances, but the most important and most common (and the ones I like the most) are the optimal transport distances like the Wasserstein distance (a superset of the "earth mover's distance").
$$
W_n(p || q) = \left[\inf_{\gamma \in \Pi(p,q)} \int d\gamma(x,y)~ d(x,y)^n \right]^{1/n}
$$
(the d inside the integral is the metric - absolute value for $\mathbb{R}$).
Wasserstein has its own _practical_ problems (c.f. sample complexity, Sinkhorn regularization etc.), but at least theoretically it's a far far cleaner and more principled way to handle continuous data - if you use differential entropy of a continuous random variable, you're probably making a mistake.