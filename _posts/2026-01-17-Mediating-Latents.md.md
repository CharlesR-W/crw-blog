---
title: "Introducing Mediating Latent Variables for Fun and Profit"
date: 2026-01-17
---
A short note with a cute magic trick: given any joint distribution $p(x_1,...,x_N)$, introduce mediating latent variables $y$ so that the $p(x|y) = \Pi_i p(x_i | y)$ (i.e., the x's are conditionally independent).  This is inspired by / a physics bastardization / example of Sam Eisenstat's fun ['condensation' paper](https://www.sameisenstat.net/doc/condensation-25-07.pdf).  Perhaps a post on that later.  I had GPT5.2 write this post based on a note outlining the important equations I wanted to cover.  In this particular case, it was trash, but I will leave you with the following masterpiece:

>>And yes: this is also basically **Eisenstat’s condensation** — just field-theory flavored.  Like Doritos: not good for you, but flavorful.

---

## Auxilliary Fields and You: Exact Renormalization

So if you've got some observables $x$, we want to introduce latent variables $y$ which absorb all the couplings; the probability conservation condition can be written:

$$e^{-S_x(x)} = \int dy ~ e^{-(S_y(y) + S_{int}(x,y))}$$

with some conditions on $S_{int}$ - I wrote it this way because this is structurally identical to the exact renormalization condition

>Physicist who's only seen renormalization be like 'getting major renormalization vibes from this'

The $y$'s are like “reverse renormalization”: instead of integrating out degrees of freedom to *produce* complicated effective interactions, we're adding them.  Reverse renormalization teehee.  This is a super general thing one can do, and I'm going to present a special case where it's especially field theory-y.

---
## Sleight-of-Hand

We'll assume we want to mediate the joint distribution $p(x_1,...x_N)$, whose energy/action we will with oracular verve call $S_{eff}(x)$

Consider now _any_ joint action $S(x,y)$ and define the effective action on $x$ by integrating out $y$:

$$e^{-S_{eff}(x)} := \int dy~ e^{-S(x,y)}$$

As a useful specific form of this, do $S(x,y) = S_x(x) + S_y(y) - V(x,y)$ (all of which we are yet free to set as pleases):

$$e^{-S_{eff}(x)} = e^{-S_x(x)}\int dy~e^{-S_y(y)}~e^{V(x,y)}$$

So, as a general rule:

$$\boxed{S_{eff}(x) = S_x(x) - \log \left\langle e^{V(x,y)}\right\rangle_{S_y}}$$

Please clap.

To elaborate : if you want to achieve a particular $S_{eff}(x)$, you the choose some nice free actions $S_x$, $S_y$ to match against the interaction $V$.  It remains to be shown that there's a good way to do this -- onwards!

## Linear-ish interaction

Now let's choose the humble

$$V(x,y) = J(x)\cdot y$$
Now for any free action of $y$, $S_y$ we'll need its cumulant function

$$W(J) := -\log\left\langle e^{J\cdot y}\right\rangle_{S_y}$$

And wow - almost like I planned this:

$$S_{eff}(x) = S_x(x) + W(J(x))$$

Expand $W$ with the cumulant tensors $\kappa^{(y)}_{[n]}$ (each of which is an $n-th$ order tensor)

$$W(J) = \sum_{n}\frac{1}{n!}~\kappa^{(y)}_{[n]} \cdot J^{[n]}$$

so

$$S_{int,eff}(x) = S_{eff}-S_x = \sum_{n}\frac{1}{n!} ~\kappa^{(y)}_{[n]} \cdot J(x)^{[n]}$$

As a super-simple example , let's assume all our variables are continuous, and take $S_x \sim \mathcal N(0,I), ~ S_y \sim \mathcal{N}(\mu,\Sigma)$, and we'll find a nice form for $J$:

$$S_{eff} = \frac{1}{2}\|x\|^2 + \mu \cdot J(x) + \frac{1}{2}\Sigma \cdot J(x)^{[2]} ~(+const.)$$

Note that if you're a based sigma terrachad, you can go so far as to set $\Sigma=0$, make $\mu$ the unit field (one index for each $x$), and make $J$ proportional to a delta function, so you get 

$$\mu \cdot J(x) \to \int dx_0 ~\mu_{x_0}J_{x_0}(x)= \int dx_0 ~ \delta(x-x_0) [S_{eff}(x) - \frac{1}{2}\|x\|^2]$$
ey lmao.  What a silly little game we have made for ourselves.  So ye, you basically have so much freedom in introducing these latent variables that even after like 6 simplifying assumptions we can still absorb basically any type of correlations in a nearly-maximally simple model of the interactions.  I thought a little bit about selection principles for these kinds of representations, but nothing productive came out of it.  Eisenstat, iirc, does show that you can get by with at worst $2^N$ latents (one for each subset of interactions).

---
#### An As-Yet-Useless Aside

(This is an incomplete, probably unfruitful, though yet perhaps interesting train of thought)
If we consider more general forms of $V$, we might do some kind of eigenfunction / library expansion

$$V(x,y) = \sum_a ~\phi_a(x) ~\psi_a(y_a)$$
(note the that each term is associated to different latents $y_a$; this just makes the form below work out, its not exactly necessary) Now the effective action is still just 

$$S_{eff}(x) = S_x(x) - \log \left\langle e^{V(x,y)}\right\rangle_{S_y} = S_x(x) + \sum_a W_a(\phi_a(x))$$
With $W_a$ the CGF _of the pushforward by_ $\psi_a$ (not of $y$ directly) under the free action $S_{y_a}$.  If one were in the business of making unwarranted assumptions, one might wish to posit that the $\phi_a = W_a^{-1} \circ \tilde \phi_a$ (the inverse isn't guaranteed to exist but I think it might for nice CGFs), getting

$$S_{eff}(x) = S_x(x) + \sum_a \tilde \phi_a(x)$$

And now its off to the races, yeah?  You can kinda do anything you want.  As an example for why this might not be infinity bullshit is if you take $\psi_a(y_a)$ to be from an exponential family, which should have pretty nice CGFs.

---

## Summary

- Any time you have a joint distribution on observables $x$, you can introduce latent variables $y$ to absorb all the correlations between $x$'s, rendering them conditionally independent.
- If we take $S(x,y) = S_x(x) + S_y(y) - V(x,y)$ Integrating out $y$ gives
  $$S_{eff}(x) = S_x(x) - \log \left\langle e^{V(x,y)}\right\rangle_{S_y}$$
  
- Even a linear-ish coupling like $V(x,y) = J(x)\cdot y$ can screen basically any correlations if you introduce some nuts amount of latents.
- (Condensation theory talks about equivalences between different latent variables for the same observables)