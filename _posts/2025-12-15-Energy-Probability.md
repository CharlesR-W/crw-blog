---
title: "Probabilities as Energies; and, Cluster Decomposition of Joint Distributions"
date: 2025-12-16
tags: [math, information-theory]
---

Here I will outline the precise connection between probability and statistical mechanics. This is something I think some people take for granted and others don’t appreciate at all; either way, even after a lot of working in the area, I’ve never seen an explicit correspondence put together in one place. Writing this helped me appreciate some subtleties I wasn’t previously aware of. The biggest one is the role of **cluster decompositions** and **Möbius inversion**: a canonical and fully general way to factorize arbitrary joint distributions into a hierarchy of multi-body interactions.

TLDR: the mainline of statistical physics is literally identical to probability theory just with different letters. This can be shown **without** any approximations or limits. The “thermodynamic limit” is not baked into statistical physics; it’s a technique to make otherwise-impossible probability calculations tractable once you add structural assumptions (locality, extensivity, homogeneity, etc). The bridge is the energy function; the moment generating function in probability is the partition function with sources, and the cumulant generating function is the free energy (up to the usual normalization constant).

## Approximate ToC

1. **Energy ↔ probability** with β = 1 and ($p = e^{-H}$).
2. **Cluster decomposition**: any joint $p(x_1,\dots,x_N)$ has a canonical decomposition into irreducible (|S|)-body interaction terms.
3. **Möbius inversion**: the mechanism that turns “marginal energies” into “connected interaction energies” (and also does the same thing for entropies).
4. **Maximum entropy inference**: constraints on marginals ↔ keep some interaction terms, set the rest to zero (plus a toy example).

### An Energy-Probability Translation Dictionary

I set $\beta=1$. I’m also going to keep two _different_ energy-like objects around.  We'll call $H$ any energy function which is normalized, and $V$ anything which is "like an energy" but fails to satisfy some conditions (which will depend what we are talking about).  

First: $H$ is equivalent to $p$ - up to normalization (which we'll assume $H$ obeys just as we do for $p$, though sometimes we want to yoink it out as the free energy),

$$p(x) = e^{-H(x)}$$

$$H(x) = -\log p(x)$$

**Normalization Condition**

$$\int dx~ e^{-H(x)} = \int dx~p(x) = 1.$$

Again, free energy $F$ is baked into $H$.  Don't worry - there is a canonical way to get it out, I'll show you later.  But for now we'll be a little nonstandard, just for the sake of brevity

**With sources** ($J$)

$$Z[J] := \int dx~e^{-H(x) - J\cdot x}, \qquad F[J] := -\log Z[J].$$

(so note that $Z[0]=1$ and $F[0]=0$)
The _probability_ cumulant generating function (CGF) is then the normalized free energy:

$$\psi(J) := \log \mathbb E_p[e^{J\cdot X}] = \log\left(Z[-J]\right) = -F[-J].$$

(the signs are just an annoying convention, morally they're the same!  I found the other conventions even more annoying, sorry.)

**Expectations**

$$\mathbb E_p[f(X)] = \int dx~p(x)f(x)=\int dx~e^{-H(x)}f(x).$$

**Shannon entropy** (I'm going to use $S$ for entropy as $H$ is taken.  Which sucks because it should be reserved for action, lol):

$$S[p] := -\int dx~p(x)\log p(x) = \mathbb E_H[H].$$

(note we switch freely between $\mathbb E_H$ and $\mathbb E_p$)

We see that entropy 'is expected energy' in this convention, because $H=-\log p$.  Neat eh?  More to come.

**KL divergence**:

$$D_{KL}(p|q)=\int dx~p(x)\log\frac{p(x)}{q(x)}=\mathbb E_{H_p}[H_q - H_p].$$

**Marginalization**

$$p(x)=\int dy~p(x,y), \qquad H(x)=-\log\int dy~e^{-H(x,y)}.$$

This is cute for sure, but there actually is something novel and interesting that falls out of this - a canonical decomposition of the energy into a sum over N-body interaction terms.

### Warm-up: 2 variables (the mutual information cameo)

Let's inspire ourselves by asking how we might decompose $H$:

$$H(x,y) = H_x(x) + H_y(y) + H_{xy}(x,y).$$

Intuitively, we should probably set $H_x$ and $H_y$ by the marginals $-\log p(x)$ and $-\log p(y)$.  Subtract those out and you'll find we have:

$$H_{xy}(x,y)=-\log\frac{p(x,y)}{p(x)p(y)}.$$

That is the **pointwise mutual information** (PMI).  Woooah neat, yeah?
"The 2-body interaction energy is the pointwise mutual information!"

Okay cool.  Next I'll show you how this generalizes, then we'll talk about Mobius inversions (which are a general tool to derive these sorts of relations - you'll see)

## Cluster decomposition of a joint distribution

Given a joint $p(x_1,\dots,x_N)$, we can write a decomposition  into "local Hamiltonians"

$$H(x_1,\dots,x_N) = \sum_{S\subseteq\{1,\dots,N\}} H_S(x_S),$$

where each $H_S$ encodes the part of the joint that is "irreducibly S" (in physics, we usually have permutation invariance, so we get a bunch of the $H_S$ reduces to something like "$\|S\|$-body potentials".

A term looks like

$$H_{1,7,22}(x_1,x_7,x_{22}) = 37x_1^{-2} x_7^{-6} x_{22}^{-4} - \{stuff\}$$

where "stuff" will enforce the "gauge" condition below.  (even powers for no reason except I dislike writing absolute value signs)

This ends up a big decomposition into an obscene number of parts, but it is _canonical_ (once we set the 'gauge'), and at least highly suggestive of what kinds of approximations one might make - do you really think you _should_ be modeling irreducible 45-body interactions?  Maybe don't.  Definitely don't.

### Set a gauge

By default you can imagine moving pieces from $H_2$ into $H_{2,95}$, but there is a nice canonical 'gauge' condition we can set - 
For every nonempty $S$ and every $i\in S$,  

$$\int dx_i~H_S(x_S) = 0 \quad\text{for all fixed } x_{S\setminus\{i\}}.$$

Interpretation: $H_S$ has zero “shadow” on any strict subset; it’s 'irreducible' to  $S$.  So the example above would be

$$H_{1,7,22}(x_1,x_7,x_{22}) = 37x_1^{-2} x_7^{-6} x_{22}^{-4} - \{stuff\}$$

$$\{stuff\} = \left[\int dx_1 + \int dx_7 + \int dx_{22} \right](37x_1^{-2} x_7^{-6} x_{22}^{-4})$$

This seems somewhat brutish inclusion-exclusion hackery - and it is, but also it is an instance of something much more general called Mobius inversion!

To come clean, the above condition isn't complete - think of what you could choose to be added in but which still shouldn't be included.  Mobius inversion fixes those.  The fastest way to show you is to show you.

---

## Connected and disconnected: Möbius Inversion on Subsets

TLDR for physicists: the thing that generically converts between “connected” and “disconnected” components (of basically anything indexed by subsets) is 'Möbius inversion'. (This is not the Möbius transform $f(z)=\frac{az+b}{cz+d}$) It’s the 'inclusion–exclusion' thing like Venn diagrams but just much more general.

TLDR for mathematicians: go read the wikipedia page, it knows better than me.

### The 'zeta transform' and its inverse

Let $a(S)$ and $b(S)$ be functions on sets $S$ (== quantities "indexed by S").  If we define  

$$a(S)=\sum_{T\subseteq S} b(T),$$

Mobius inversion is how you back out $b$:

$$b(S)=\sum_{T\subseteq S}\mu(S,T)\,a(T),$$

For the case we care about, which is the "subset lattice" $\mu$ is:

$$\mu(S,T)=(-1)^{|S|-|T|}.$$

Note that this looks a lot like a matrix multiplication!  We can write a nice multiplication notation:
$a = 1 * b$ and $b = \mu * a$ .  Here $1$ is the function $1(S,T)=1$, which lets us write $\mu = (1)^{-1}$, (lol seethe and cope).  In general, the '\*' is "Dirichlet convolution", and '1\*' is the 'zeta transform'.  Afaik, no relation to Herr Riemann's $\zeta$.  The thing people generalize to is by running the sum over something other than 'all possible subsets of a given parent'.

### Apply it to probabilities

Let $p_T(x_T)$ be the marginal on $x_T$. Define the marginal log-probability

$$V_T(x_T):=-\log p_T(x_T).$$

Then the irreducible interaction term $E_S$ is given by the Möbius inversion:

$$H_S(x_S) = \sum_{T\subseteq S} (-1)^{|S|-|T|}~V_T(x_T).$$

This is the canonical "cluster decomposition" I promised: you compute marginal energies, then apply inclusion–exclusion to strip off everything explainable by strict subsets.  You can verify by induction that this satisfies the "gauge" condition from before.  It's just "don't double count" but fancy: $\mathcal{DON'T~ DOUBLE~-~COUNT}$.

### The same trick gives you “multi-way information” from subsystem entropies

From the Shannon entropy of a marginal distribution $S[p_T]$, the "connected entropy" / "interaction information" / "co-information", $I(T)$

$$I(T) := \sum_{T'\subseteq T} (-1)^{|T|-|T'|}S(T).$$

(okay yeah didn't plan far enough ahead when I chose $S$ for entropy.  Sorry lol.)

### Gauge-fixing

Stare at the discussion above until you have convinced yourself that the Mobius inversion canonically selects out the localised bits for each $S$ from any $V(x)$, and also note that you can, if feeling cheeky, take $H_{\emptyset} = F$ the free energy.

---

## Maximum Entropy Inference (The Killer App)

Now here’s the thing that gives this meaning beyond the combinatorics.

Consider the MaxEnt problem of inferring a distribution given its marginals:

$$\text{maximize } S[q] \ \ \text{subject to}\ \ q|_{R_i}=p|_{R_i}\ \ \forall i\in\{1,\dots,m\},$$

In the energetic picture, this is clean
- Each marginal constraint $q\|_{R_i}=p\|_{R_i}$ pins down the marginal energy $E_{R_i}=\log p_{R_i}$
	- it also specifies the 'descendant' marginals - these have to agree or the problem is infeasible
- Use Mobius transform to calculate these energies
- then the optimal $q^*$ is the sum of all energies specified by the constraints (including the descendants, counted only once).

So very concretely, with a bit of Occamite flavouring, this means you back out the maximum entropy inferred distribution by taking the energies you know you have to have, and setting the higher order ones to be zero.

Take $\mathcal R$ to be the set of marginals specified, $H_{p,R_i}$, plus also descendants of the $R_i$'s; then

$$H_{q}^* = \sum_{S\subseteq \mathcal R} H_{p,S}$$


## A Gibbsian Aside

The Gibbs distribution from which all thermodynamics arises solves

$$\max_p S[p] ~~s.t. ~~ \mathbb E_p[\mathcal O_i] = o_i, \forall i$$

where $i$ labels the constraints on different observables $\mathcal O_i$.  You are doubtless most familiar with the case where there is one constraint, $\mathbb E[H] = U$ ($U$ is the internal energy, $H$ the Hamiltonian / honest-to-god energy), and whose lagrange multiplier is the inverse temperature $\beta$.

I just want to point out how very nice the solution to this problem looks in the energy language.  For 10 seconds I'll switch to using $E$ for the energy of our distribution (the thing we're optimizing), so we don't confuse it with the system's Hamiltonian, and physical states are $\omega$:

$$E^*(\omega) = F + \sum_i \lambda_i \mathcal O_i(\omega) $$

You can choose to specify either $\lambda_i$ or $o_i$ for each constraint; $F$ depends on the choice of all of them.

---

## Summary

- probability distributions can be specified by $p = e^{-H}$ or $H = -\log p$
- Writing things in terms of $H$, large chunks of probability theory can be made identical to statistical mechanics.
	- Expected values of energies yield entropies
- Any joint energy like $H(x_1,...x_N)$ can be canonically decomposed into energies on subsets of the variables $S$.  This 'isolates' dependencies to each subset, maximizing the amount of information accounted for by the smaller subsets and only assigning to larger sets that component of the interaction which cannot be accounted for at a lower level.
- The technique to back out those subset interactions is the Mobius inversion.
- This same decomposition can be applied to information / entropy, which provides a simple way to derive the 'interaction' informations.
- Inference of a distribution based on its marginals is simple when written in terms of energies: the marginals specify the interaction potential $H_S$ for for the given set and its own marginals, and the maximum entropy distribution is that which matches the energies specified without adding anything else.
- The energy formulation makes the Gibbs distribution look very nice and affine and pretty.  Reasonably so!
- In defining this decomposition of the energy over subsets, the Mobius inversion can be seen as a gauge-fixing condition.

---

*Edit 17 Jan 2026: After writing this, I've learned that much of this theory is subsumed under the name of 'Hoeffding decomposition', which in fact applies to more general functions and is used in so-called "U-statistics".  Hoeffding's version is also nicer in that it uses the expectation value instead of a raw integral.*