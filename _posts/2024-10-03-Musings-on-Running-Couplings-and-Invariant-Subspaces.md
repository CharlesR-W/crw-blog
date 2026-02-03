---
title: "[Musing] Musings on Running Couplings and Invariant Subspaces"
date: 2024-10-03
tags: [physics]
---

In this post I want to outline a connection between the renormalization-semigroup and invariant subspaces in renormalization theory. It's written mostly for fun / to share and discuss with friends.  Consider this water-cooler brainstorming.

Consider the Ising Hamiltonian

$$
H = J \sum_{ij} \sigma_i \sigma_j + h \sum_i \sigma_i
$$

In typical renormalization-semigroup analyses, we 'zoom out', writing the Hamiltonian $H(\{\sigma\})$ in terms of some new renormalized degrees of freedom $\hat{H}(\{\hat{\sigma}\})$. Oftentimes, we like to have a continuous parameter (here we'll use $\lambda$) which tells us 'how far' the renormalization process has gone. This yields, in effect, a dynamical system over the set of possible Hamiltonians, parameterized by $\lambda$. Though by no means required, a next step commonly taken is to _assert_ (-qua-approximation) that, as $\lambda$ increases (i.e., as $H$ evolves), it suffices to determine the two variables $J$ and $h$ as functions of $\lambda$ — no additional terms (e.g. quartic in $\sigma$, non-local terms, etc.) are added to the Hamiltonian:

$$
H(\lambda) = J(\lambda) \sum_{ij} \sigma_i \sigma_j + h(\lambda) \sum_i \sigma_i
$$

Here I'll be discussing the concept of invariant subspaces in this renormalization context, mostly because it seems interesting.  I wanted to discuss Koopmann invariant subspaces (i.e. those where some _finite_ handful of _functions_ of the Hamiltonian-parameters form a closed linear dynamical system), but I didn't have much success in proposing an interpretive significance for that.  What follows is exploratory and should be construed as brainstorming, with the hope that this different picture leads to some insights (or something).

### Renormalization Semigroup - Flows on Systems
We're not really concerned with renormalization _per se_; the basic point of relevance to us is that the 'renormalization semigroup' has us thinking about "dynamics" in the space of possible theories (let's use 'theory', 'system', and 'model' interchangeably). By that, I mean we're relatively unconcerned about what this flow has to do with 'renormalization'; here we'll consider the case where the degrees-of-freedom don't change as the system flows (usually people talk about 'integrating out' degrees of freedom, but I prefer to keep the dynamical systems approach at the forefront). The equation of interest is

$$
\frac{d}{d\lambda} H_\lambda = f(H)
$$

where $H$ is the Hamiltonian function which defines the time-evolution of the underlying degrees of freedom.

### Invariant Subspaces of the Flow
Let's go back to thinking about the Ising model considered at the start—for almost any given renormalization procedure or flow on systems, it will _not_ be sufficient to merely track the 'running couplings' (i.e., $J$ and $h$ as functions of $\lambda$). This is because, in general, the system will flow such that new terms are added (unless a flow is chosen which specifically avoids this). 

Suppose we have some parameter family $\theta$ which is sufficient to describe the Hamiltonian system, so that we can equate the system flow over $H$ with a dynamical system in terms of the $\theta$. We then have

$$
\frac{d}{d\lambda}\theta = f(\theta)
$$

for some function $f$ (which for renormalization, is determined by the renormalization procedure). The theory of phase transitions is in large part about studying the fixed points of this equation.

Now, as for "invariant subspaces", we mean any scenario where you can take a strict subset of the dynamical variables (probably you could extend this to a set of well-chosen functions of the $\theta$, by point-transformations),  $\theta_1$, (call the remaining variables $\theta_{-1}$) and organize them such that their time evolution is closed:

$$
\frac{d}{d\lambda} 
\begin{bmatrix} 
\theta_1 \\ 
\theta_{-1} 
\end{bmatrix} 
=
\begin{bmatrix} 
f(\theta_1) \\ 
g(\theta_1, \theta_{-1}) 
\end{bmatrix}
$$

In this case, thinking of the Ising approximation (i.e. looking at running couplings for $J$ and $h$ without adding new kinds of terms to the Hamiltonian), we can see that the approximation being made can be understood as demanding that the renormalization flow have ($J$,$h$) make an invariant subspace of the flow (and all the other infinity of co-ordinates are set to zero and stay there).  If selecting the renormalization procedure amounts to selecting a flow map $\dot{H} = f(H)$, the running coupling method implicitly restricts us to choosing $f$'s with the correct properties.

My limited understanding of the 'exact' renormalization group is that it amounts to removing this auxiliary restriction on $f$ (but I'm not that sure at all).  More to below on what kinds of $f$ can be called renormalization flows.

This sort of restriction is reminiscent of the constrainted dynamics which is so often used to motivate Lagrangian mechanics for undergraduates.  I'm interested to think about what the analogue of the 'constraining force' (e.g., the force exerted by the wire for a bead on a wire) would be or mean.

### What kinds of flows are renormalization?
Here I'll switch gears away from "renormalization as dynamical system" to "renormalization as progressively integrating something out" (tbh I'm not that well versed yet on how to reconcile these two perspectives, so this section especially should be taken cum grano salis. Hitherto I've been assuming $f(H)$ has whatever niceness properties I needed, but to have this discussion I think I need to do precisely the opposite and talk about the sorts of $f$ which make it the renormalization _semi_group (i.e. aren't invertible, aren't smooth etc).  

(Here I'm following wikipedia/renormalization_group/exact_renormalization_group_equations rather heavily with modified notation).  The exact renormalization semigroup is defined by requiring that the partition function is independent of the renormalization parameter $\lambda$.

$$
Z = \int_{B(\lambda)} \mathcal{D}\sigma_{\lambda} ~ \mathrm{exp}( H_{\lambda} \left[ \sigma_{\lambda} \right] )
$$

$B(\lambda)$ is family of sets, nonincreasing (maybe strictly decreasing?) in $\lambda$.
Since we're interested in the Hamiltonian, the transformation is

$$
\mathrm{exp}(H_{\lambda_2}) = \int_{B(\lambda_1) - B(\lambda_2)} \mathcal{D}\sigma ~ \mathrm{exp}( H_{\lambda_1} \left[ \sigma \right] )
$$

If I understand correctly, it's not very well defined to talk about $\frac{dH}{d\lambda}$ here because they have different domains (you lose the DoFs which are integrated out), and so there's a "Polchinski" version of the ERSG which has a soft cutoff that makes this problem go away.  Anyways, you choose some soft-cutoff function then you impose the condition $\frac{dZ_\lambda}{d\lambda} = 0$, and any trajectory $H(\lambda)$ which solves that works.

I'm not sure if this gets us to deriving RSG 'lossiness', in the sense of no longer being able to uniquely determine $H(\lambda)$ from initial conditions.  I'm a bit too tired to think more on this now, and as ever painfully aware that 'good enough' is the enemy of 'at all' as regards my writing.


### Are Some Renormalization Procedures Better Than Others?  And Other Miscellaneous Neat Ideas That Occurred to Me While Writing
Let's suppose we can meaningfully define a metric function in the (tangent-spaces-to-the-) parameter-space over flows, $g$ (presumably dictated by the problem at hand). This entails a distance function (the length of a geodesic; one could also postulate this directly) between two points $d(\theta_1, \theta_2)$.  Considering the renormalization flow as 'coarse-graining', we can then start to ask questions about which of these coarse-grainings is 'best' with respect to this metric.  Perhaps one could devise optimization problems based on such criteria?  E.g.

$$
\begin{aligned}
    \text{Minimize}_{f \in \text{Valid RSG Flows}} \quad & \Gamma\left[ \theta \right] \\
    \text{Subject to:} \quad & \frac{d\theta}{d\lambda}=f(\theta) \\
\end{aligned}
$$

Think about adding sparsity criteria / normalization to design a flow which will find the system with N terms that's the best approximation to some other system?

$$
\begin{aligned}
    \text{Minimize}_{f \in \text{Valid RSG Flows}} \quad & ||\theta(\lambda_f)||_1 \\
    \text{Subject to:} \quad & \frac{d\theta}{d\lambda}=f(\theta) \\
\end{aligned}
$$

Or perhaps, since the flow defines a dynamical system, we could go meta and ask about flows over flows?  I can think of a lot of things that are schematically maybe representable this way - perhaps outer-flow = learning-rule, inner-flow = online-learning for control systems, or maybe analogously for optimization-algorithms in general

$$
\begin{aligned}
    \text{Minimize}_{f_o \in \text{Valid RSG Flows}} \quad & \Gamma\left[ \theta_o, \theta_i \right] \\
    \text{Subject to:} \quad & \frac{d\theta_o}{d\lambda_o}=f(\theta_o) \\
    \text{Subject to:} \quad & \frac{d\theta_i}{d\lambda_i}=f_i \left[\theta_o\right](\theta_i) \\
\end{aligned}
$$

(where $i$ and $o$ are 'outer' and 'inner' respectively)

Of course if one goes meta once you have to go meta again by asking what happens if you do that infinitely many times?

$$
\begin{aligned}
    \text{Minimize}_{f_{\infty} \in \text{Valid RSG Flows}} \quad & \Gamma\left[ \{\theta_i\}_{i \in \mathbb{Z}_{++}}\right] \\
    \text{Subject to:} \quad & \frac{d\theta_i}{d\lambda_i}=f[\theta_{i+1}](\theta_i) \quad \forall i \in \mathbb{Z}_{++}\\
\end{aligned}
$$

($i$ now an integer index) I have no good idea what that could mean or be used for, but seems neat! You could also do away with the optimization framing.  I won't mention that you could maybe also do ontologically devious things like (1) make a continuum limit for $i$ and get a PDE or (2) ask about fixed points of that map + stability.  The fun need never end!

The PDE for (1) I think should look like

$$
\frac{\partial}{\partial \lambda}\frac{\partial}{\partial x} \theta (\lambda,x) = \frac{\partial \theta}{\partial x}^T \left[ \nabla_1 f + \nabla_2 f \right] (\theta(x,\lambda), \theta(x,\lambda)) 
$$

(where we represent $f_{\theta_1}(\theta_2) = f(\theta_1, \theta_2)$ and the index of $\nabla$ indicates the gradient with respect to the first or second argument).

Do you think we could require $\lambda$ to trade off against accuracy at a pre-determined rate (I have in mind saying that $\lambda$ is e.g. number of flops available compute some observable, and asking what the best system to simulate is - sounds hard but neat idea! (any relation maybe to the role of compute in ML scaling laws??))

### Does this matter if we only care about fixed points?
Not that I can tell or think of readily.  Maybe if you're concerned about moving the fixed points around.  I wrote this mostly thinking about renormalization as 'coarse graining' in that you use it to extract some high level dynamical features of a system by zooming out some finite amount, as opposed to specifically looking for fixed points, phase transitions, etc.  I suspect if I knew more / read more about RG I could say more interesting things.  I'm also interested to think more about other types of 'systems of systems' more broadly.
