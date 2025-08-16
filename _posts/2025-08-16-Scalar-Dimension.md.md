---
title: "[Math] Scale-Dependent Geometry from Diffusion"
date: 2025-08-16
---
# Scale–Dependent Geometry from Diffusion

## Abstract

In this note I propose a at-least-to-me-novel perspective on the notion of 'dimension'.  Inspired by physical desiderata, we start from the celebrated formulas of spectral geometry, use the short-time behavior of diffusion processes to characterize geometry.  The essential project is to take turn these formulae inside-out, redeveloping a framework where the familiar geometric quantities are one limiting case of a more general 'scale-dependent' geometry, defined with respect to any diffusion process.  Thus we develop notions of the effective dimension _between_ two points at a given _scale_, and likewise for their distance.  We show how these effective metrics can be derived from variational principles, and, in particular, that the thermal-distance between two points is analogous to the tempered geodesic distance when the path-length functional is taken to be the Onsager-Machlup action.

## Exordium
I'm not aware that any results here are fundamentally novel - instead I hope to provide a novel _perspective_ relating famous results.  If nothing else, I hope to introduce the reader to some of the exciting results from spectral geometry, the study of which continuously surprised and delighted me.

The line of thinking which got me here is this: in physics, we often ride roughshod over the rules of mathematics - the archetypal example is assuming smoothness of whatever functions we deal with - the rationale being that 1. *natura non facit saltus* and 2. a 'true' discontinuity (a la a shockwave, and excepting more pathological Weierstrass-y things) is worthy of study, and the best way to study it is basically always going to be to smooth it by $\epsilon$ and examine the asymptotics as $\epsilon$ gets small.  

That's thread 1, here's thread 2, then I'll bring it together: we have one notion of dimension which is "number of coordinates needed to specify a point", and this is an integer by definition - but we do know there are, irl, physical systems that show something like a low "effective dimension" - thermodynamics can often do damn well reducing $O(10^{23})$ dimensions to 1 or 2 (say, temperature and potential energy) - basically because integers are cringe and I hate them, we should be able to come up with a "scalar notion of dimension".  Fractal dimension does not fulfill me on this regard for two related reasons - one, the abstract 'fractal' property is fragile under most sorts of noising - if your measurement apparatus has resolution X and you're looking at an honest-to-god space-filling 1D curve with real 2D volume, it will walk like and qualk like a 2D volume.  Second is that fractal dimensions feel too "integer"-y to me --- if you take $\mathbb R$ as the "ontic unit" of your thought, upon which integers are a contrived abstraction, fractal dimension is a doubly-contrived abstraction.  Instead, I'm looking for what I call a "scalar-native" version of dimension.

Tying it together, then, I'm writing this because I find spectral geometry as outlined here to provide a novel perspective on how to think about dimension, and if I take intellectually seriously the idea that we should take such a scalar dimension as """more fundamental""", this suggests likewise about geometry too.  That is, below, when we talk about the thermal-distance between two points $d(x,y,\beta)$, I'm thinking of this not as a convoluted crap way of measuring the real geodesic distance, but instead that the real geodesic distance is a limiting simplified case of this thermal distance.  I've found it leads me to ask interesting questions, and thus is of value.

---

## Recapitulation of Spectral Geometry

Spectral geometry takes its task as studying linear operators (often the Laplacian) on some space, and relating the eigenvalues of the laplacian to the geometry of the space.  By physical analogy, this corresponds to studying something's shape by examining its vibrational modes; I am obligated to describe this by referencing the archetypal question "Can you hear the shape of a drum?" (the answer is no but you can get _really_ far and its awesome).

Start with some space $\Omega$ (manifold, graph, this is really astonishingly general).  Assuming you can define a Laplacian $\Delta$, you can study the heat-diffusion process, whose PDE is
$$\partial_t u = \Delta u$$
(by the way, we study the Laplacian in particular because, at least in $\mathbb R^n$, you can show that all operators which are equivariant under rotation+translation can be written as a power-series in $\Delta$).
To make a long story short, you can define the *heat kernel* as the Green's function that solves this equation:

$$
K(x,y,t) = \big(e^{t\Delta}[\delta_x]\big)(y)
$$
You can also understand this probabalistically: if you have an SDE with increments
$$dx = 0 dt + \sqrt{2}{dW_t}$$
then you can derive the corresponding Fokker-Planck equation for the probability to go from x --> y in time t

$$\partial_t p_t(y|x) = \Delta p_t(y|x)$$
Nice, ain't it!  Dwell on your own time - we have to keep moving.
![[HeatKernel1]]
It is the case that, for a manifold with geodesic distance (I'll write it the formula just for comparison later) 
$$d^2_G(x,y) = \inf_{\gamma:~ [0,1]\to\mathbb \Omega} \int_0^1 dt ~g_{\gamma(t)}(\dot \gamma, \dot \gamma) $$
you can show that as $t \to 0$, the awesome Varadhan's formula gives the leading behavior

$$
K(x,y,t) \sim (4\pi t)^{-\sigma/2}\exp\left[ -\frac{d_G^2(x,y)}{4\,t} \right] \big(1 + O(t)\big)
$$

where $d_G(x,y)$ is the geodesic distance with respect to the underlying metric.  Here $\sigma$ is the dimension ($d$ was already in use sorry - pretend it stands for 'spectral dimension').

Another standard short–time asymptotic is given by the *average return probability*

$$
P(t) \equiv \frac{1}{\mathrm{Vol}(\Omega)} \int_\Omega K(x,x,t)\, dx
$$
which behaves as

$$
P(t) \sim t^{-\sigma/2} \big(1 + O(t)\big)
$$

In what follows, we will “unfreeze” these definitions, promoting both the geodesic distance

$$
d_G(x,y) = \lim_{t\to 0} \sqrt{-4t\,\log K(x,y,t)}
$$

and the spectral dimension

$$
\sigma = \lim_{t\to 0}-2\,\frac{d\log K(x,x,t)}{d\log t} 
$$

into *scale–dependent* quantities.  (by the way, note this definition of $\sigma$ is the scaling dimension of the sub-level sets of P, if you're familiar from, say, singular learning theory).

## Turning the Definition Inside–Out: Scale–Dependent Distance and Dimension

So first things first let's put the form of K back in front of is so we can poke it:

$$
K(x,y,t) \sim (4 \pi t)^{-\sigma/2}\exp(-\frac{d_G^2(x,y)}{4 t})(1 + O(t))
$$
Now basically what I want to do is just absorb the $O(t)$ terms in and redefine $\sigma$ and $d$ - you have a degree of freedom in pushing terms between the two new quantities, so I ended up deciding the $\sigma$ gets the diagonal terms and $d$ gets the off diagonal ones:
$$\sigma(x,t) = -2 \frac{\log K(x,x,t)}{\log 4 \pi t}$$

$$ d(x,y,t) = \sqrt{4t\log{\frac{K(x,x,t)}{K(x,y,t)}}}$$


So for $t \to 0$, these give us back our "pure geometry" - dimension and distance.
For $t \to \infty$, you get - hilariously, or cosmically saddeningly - 
$$K(x,y,\infty) = \frac{Vol(y)}{Vol(\Omega)}$$
Independent of x and t, so 
$$\sigma(x, \infty) = 0$$
$$d(x,y, \infty) = \delta(x-y)$$
Zero dimensions of freedom, each point an island, the widening gyre... o wretched post-thermal wasteland.

(aside: the result for $d$ actually holds only if there is a "spectral gap" - i.e. the Laplacian's first eigenvalue is finite and > 0.  This is one of those weird order-of-limits things, where if you take the limit where your space, say for concreteness $[-L,L], L\to \infty$, it depends on if you do that or the $t$ limit first, and its not clear that either way is a cringe technicality soooo eh.  But if the manifold is compact and either has no boundary or dirichlet BCs, you have a gap.)

## Including Drift: Diffusion in a Potential Landscape
Since it'll be useful to have a more concrete example in mind, we'll also talk about what happens when you have a drift.  This will help us build in some dynamics, so if you have a dimension where it costs 100 trillion Terrajoules to move an inch to the left, that kinda doesn't count as a dimension most of the time.

Pure diffusion is generated by the Laplacian $\Delta$.  
If we add a drift term from a potential $V(x)$, the stochastic differential equation becomes

$$
dx_t = -\nabla V(x_t)\, dt + \sqrt{\frac{2}{\beta}}\, dW_t
$$

Here $\beta$ plays the role of an inverse temperature (or, equally well, a diffusion constant).  
The corresponding generator $\mathcal{A}$ acting on functions $\phi(x)$ is

$$
\mathcal{A}[\phi] = \frac{1}{\beta}\,\Delta \phi - \nabla V \cdot \nabla \phi
$$

The heat kernel with drift is the same

$$
K_V(x,y,t) = \big(e^{t\mathcal{A}}[\delta_x]\big)(y)
$$

For small $t$, the drift term basically does nothing at first order so the dimension and geodesic distance are the same.

As $t \to \infty$, $K_V$ approaches the stationary distribution:

$$
K_V(x,y,t) \to \frac{1}{Z_\beta} \exp\big[ -\beta V(y) \big] \,\big(1+O(e^{-\lambda_1t})\big)
$$

where $Z_\beta = \int_\Omega e^{-\beta V(z)}\, dz$ is the partition function (same note as b4 re: spectral gap).

So this is a little funky - diffusion on manifolds is cool because you have a canonical process you study and it just whispers to you about geometry, and the drift feels kinda like it just makes that more complicated than need be?  The trick, that got me to consider this in the first place, is that I really care about situations where you have a "built in" potential function to hand - gradient flow!  But $t\to 0$ stuff can't capture drift - so I'm fiddling with this to see if there's anything to be had looking at the intermediate regime where there's a lil' bit o geometry and a smidge of physics in happy coexistence.

Just for completeness, I think we'll want to redefine $\sigma$ for drift:
$$\sigma_V(x,t) = -2 \frac{K(x,\Phi^V_t(x),t)}{\log 4\pi t}$$
With $\Phi^V_t(x)$ the deterministic evolution of $x$ under $V$.  Then $d$ has to become
$$d^{fwd}_V(x,y,t) = \sqrt{4t \log \frac{ K(x,\Phi^V_t(x),t)}{K(x,\Phi^V_t(y),t)}}$$
Okay kinda annoying but it does seem like the natural thing to do - if you think about $t$ as plain old time, it's not that clear this is the best, since maybe the "distance from x to y" really should be measured in terms of real dynamical travel time - but if you think of $t$ as just some scale parameter, I feel like we want to be measuring distance and dimension "at the same $t$".  And ofc, $d$ has the $fwd$ superscript because you're evolving $y$ forward - you could just as well pull $x$ backwards.

Let's do an example:
### Example: Quadratic Potential here
![[HeatDriftDiffusion]]

Let $V(x) = \frac{k}{2}\,\|x\|^2$ in $\mathbb{R}^n$.  
The SDE is

$$
dx_t = -k\,x_t\, dt + \sqrt{2} dW_t
$$

This is the $n$–dimensional Ornstein–Uhlenbeck process.  We have
$$\Phi^V_t(x) = e^{-kt}x$$
Its transition kernel is Gaussian:

$$
K_V(x,\Phi^V_t(y),t) = \frac{1}{\big( 2\pi\,v_t \big)^{n/2}} 
\exp\left[ -e^{-2kt}\frac{\parallel y - x\parallel^2}{2v_t} \right]
$$

where, since we can't use $\sigma$, we use $v_t$ the variance:

$$
v_t = \frac{1}{k}\big(1 - e^{-2kt}\big)
$$
Then we get
$$\sigma_V(x,t) = n\frac{\log 2 \pi v_t}{\log 4\pi t }$$
$$d_V(x,y,t) = \parallel y-x\parallel e^{-kt}\sqrt{\frac{2t}{v_t}}$$

Okay so what means?  We see $\sigma_V$ goes to zero as $t$ goes to infinity: for sufficiently large times, you have no real freedom of motion - you're just gonna get pushed back to the origin and any deviations therefrom are damped.  $d_V$ likewise.

I don't think that's infinitely enlightening, but it does at least feel right.

---

## Inverse Problem: From Transition Probabilities to Geometry

So let's see how far we can dig the rabbit-hole: so far we have assumed the existence of a generator $\mathcal{A}$ — either the Laplacian $\Delta$ or the drift–modified operator $\beta\Delta - \nabla V \cdot \nabla$.  
But suppose we start with nothing more than a transition density

$$
p(y \vert x) \quad\text{for}\quad x,y \in \Omega
$$

obtained, say, from data or as the output of some simulation.  ON ANY MATHEMATICAL OBJECT!
Can we recover a generator $\mathcal{A}$ such that

$$
p(y \vert x) = \big(e^{\mathcal{A}}\big)(x,y)
$$

for *unit* time?

If so, then $p(y \vert x)$ defines a one–step evolution, and $\mathcal{A}$ defines a continuous “time” parameterization.  
Given $\mathcal{A}$, we can run the diffusion for any real (or, if we are feeling mischievous, complex or even vector–valued) $t$:

$$
K_t(x,y) = \big(e^{t\mathcal{A}}\big)(x,y)
$$

From there, all our scale–dependent distances and dimensions follow automatically.  Meaning that if you can give me $p(y|x)$, I could define a dynamics-aware distance and dimension on your pseudo-Grothendieck Markov sheaf whatever-category - EVERYTHING IS PHYSICS - HAHAHA I WIN!

Under some reasonable conditions (I'll be honest I don't know or care what they are, but like just make sure $p$ is a probability distribution, maybe with full support for each $x,y$ and I'm sure you're fine most of the time), you can just take the matrix logarithm:

$$
\mathcal{A} = \log p(\,\cdot\ \vert \,\cdot\,)
$$
So we see: any ("any") transition density can be made into dynamics of a stochastic process.  This stochastic process presents a dynamics-aware notion of the local geometry - a geometry of space which is _fundamentally_ inextricable from the potential landscape (and here at least, that's what we _want_).

Nice, eh?

---
## Variational Formulation and Path Integrals

Okay so now let's talk about variational principles - we all know the particle is only moving that way because god wants it to so let's calculate what god wants.

For a process $x_t$ with generator $\mathcal{A}$, the probability of a path $\gamma$ from $x$ to $y$ in time $t$ can be expressed (formally) as

$$
p_t(\gamma) = \frac{1}{Z_t}\,\exp\big[ -t\,\mathcal{A}(\gamma) \big]
$$

where $\mathcal{A}(\gamma)$ is the **Onsager–Machlup action**:

$$
\mathcal{A}_t(\gamma) = \int_0^t \mathcal{L}\big(\gamma(\tau), \dot{\gamma}(\tau)\big)\, d\tau
$$

For a pure Laplacian, $\mathcal{L}$ is proportional to $\|\dot{\gamma}\|^2$; with drift, extra terms appear.  Also, inside the path integral, we can do just unit-speed paths and take $\mathcal A_t \to t \mathcal{A}_1$.

The kernel is the sum over all such paths:

$$
K(x,y,t) = \int_{\gamma: x \to y} \mathcal{D}\gamma\; p_t(\gamma)
= \frac{1}{Z_t} \int_{\gamma: x \to y} \exp\big[ -t\,\mathcal{A}(\gamma) \big]\,\mathcal{D}\gamma
$$

Taking logs:

$$
\log K(x,y,t) = \log\!\int_{\gamma: x \to y} \frac{e^{-t\,\mathcal{A}(\gamma)}\mathcal{D}\gamma}{Z_t}
$$
This structure parallels the **tempered geodesic distance**.  (It's just the geodesic distance but plus a little bit in proportion to the tempering temperature - by the way, 'temper' as a verb can be used this way to mean 'modified to include temperature', cute eh?).  This is written (two ways, variationally and path integral-y):

$$
d_\beta(x,y) = \inf_{\pi} \mathbb{E}_{\gamma \sim \pi}[L(\gamma)] + \frac{1}{\beta} S[\pi] = \frac{-1}{\beta} \log \int \mathcal D \gamma~ \frac{\exp -\beta L(\gamma)}{Z_\beta}
$$

where $L(\gamma)$ is a length functional and $S[\pi]$ is the entropy of the path–distribution $\pi$.  

Here, $t$ plays the role of $\beta$, $L$ is replaced by $\mathcal{A}$, and $K$ encodes the entropic sum over paths:

$$\frac{-1}{t}\log K(x,y,t) = \inf_{\pi}\mathbb E_{\gamma \sim \pi} [\mathcal A(\gamma)] + \frac{1}{t}S[\pi]$$

Indeed, we can write:

$$
\sigma_V(x,t) = \frac{-2}{\log 4 \pi t} \log \int_{\gamma: x \to \Phi^V_t(x)}\frac{e^{-t\mathcal A(\gamma)}}{Z_t}
$$

Stare at this stuff for a minute or two and you'll see that $\mathcal A(\gamma)$ is a _logit_!!!  Cool right!

Two nice interpretations for $\sigma$ (up to some constants) then:
One: $\sigma_V(x,t)$ is the logprob of a particle at $x$ just following the plain-old deterministic path and ending up at $\Phi^V_t(x)$.

Two is a bit harder to show, but $\sigma$ is the scaling dimension of the sub-level sets of $K_V(x,\Phi^V_t(x),t)$:
Suppress $x$ and $V$ and watch this! (this is a pretty cute trick btw, so try it out if you haven't already):

$$\frac{d}{dT}Vol(t | K(t)<T) = \int_t dt ~\delta(K(t)-T) = \frac{d}{dT} K^{-1}(T)$$
Then, $K(t) = t^{-\sigma(t)/2}$ is the definition of the sublevel set scaling exponent (except this holds for all $t$, not just asymptotically!).  So "For a particle starting at $x$, after a time $t$, the probability of it being at the maximum-likelihood point $\Phi^V_t(x)$ has scaling exponent $\sigma(x,t)$"

## Saying The Same Stuff But With Different Letters: SGD

![[DiffusionTransport]]
Okay so confession, I don't like physics per se that much, I just like applying mathematics.  For this reason I love machine learning (yes the zeitgeist gets me too; I'm only human).  Let's repeat some stuff in the context of SGD:
$$d\theta = -\nabla_{\theta} L(\theta) dt + \sqrt{\frac{2}{\beta}}dW_t$$
(yes I'm ignoring the metric tensor, yes I'm a hypocrite, its just more letters than its worth writing).
Motion is generated by
$$\mathcal A = \frac{1}{\beta} \Delta - \nabla L \cdot \nabla$$
Then
$$K_L(\theta, \theta', t, \beta) = p_{t,\beta}(\theta' | \theta)= e^{\frac{t}{\beta} \mathcal A}[\delta_{\theta}](\theta')$$
The diffusion kernel gives us our posterior over the trained weights

$$d_L(\theta_0,\theta, t, \beta) = \sqrt{4 t \log \frac{K(\theta_0, \Phi^L_t(\theta_0),t, \beta)}{K(\theta_0, \Phi^L_t(\theta),t,\beta)}}$$
Read this as "The squared thermal distance between initialized and trained weights is four times the training-time times times the log-likelihood ratio of the pushforward of those weights by gradient flow."

$$\sigma(\theta,t,\beta) = -2\frac{\log K(\theta, \Phi^V_t(\theta),t,\beta)}{\log 4 \pi t}$$

The thermal dimension between initialized and trained weights is the scaling exponent of the posterior.

---
## Differential Geometry from $d_V$

You'll have noted that for finite $t$, $d_V(x,y,t)$ isn't symmetric - but it is positive definite and satisfies a triangle inequality : thus it's actually a divergence more than a distance.  That said, if you have a divergence, you can define a differential geometry, so let's go poke about over there; I'm just gonna write down the cookbook for you to ponder on your own time, as I didn't find that much interesting:

Everything in coordinates for simplicity.  This actual gives you a "conjugate connection manifold" a la information geometry, but if you care about that you already know how to write the rest of the cookbook here.

Metric tensor
$$g_{ij}(x) = \frac{\partial}{\partial x_i}\frac{\partial}{\partial y_j}d_{V,t}(x,y,t)\vert_{x=y}$$
Chrsitoffels
$$\Gamma_{ij,~ k} = - \frac{\partial}{\partial x_i}\frac{\partial}{\partial x_j} \frac{\partial}{\partial y_k}d_{V,t}(x,y,t)\vert_{x=y}$$
Connection
$$\nabla_i X^j = \partial_i X^j - \Gamma_{ik}^j ~X^k $$
etc etc.

In principle, this means you have a differential geometry which meaningfully and principledly incorporates the potential function $V$.  The downside is that calculating this stuff is kinda torturous and I couldn't find any of the above which actually feel insightful to do.  Perhaps if one were doing numerics?

---
## Summary

We have mostly been re-labeling familiar objects:

- The geodesic distance from Varadhan’s formula becomes $d_G(x,y;t)$ when we refuse to take the $t \to 0$ limit.
- The spectral dimension from return–probability scaling becomes $\sigma(x,y,t)$ when we keep $t$ finite and the endpoints explicit.
- Diffusion with drift is handled by replacing $\Delta$ with $\mathcal{A} = \\Delta - \nabla V \cdot \nabla$, whose heat kernel gives the same definitions.
- These notions of distance and dimension naturally bring dynamics into the realm of the geometry, allowing us to, i.a., screen out 'irrelevant' dimensions, talk about effective distances etc.
- We can identify some variational principles that give us something like these notions od geometry back out
- Given any ("any") transition density $p(y|x)$, we can define from this a canonical diffusion process, and in turn use this to study the geometry of the structure in question
- These notions of geometry apply as well to gradient descent.  More on this to come?