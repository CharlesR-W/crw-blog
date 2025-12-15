---
title: "[Information Theory] KL Boogaloo: Tempered KL Divergence For Metric-Aware Entropy"
date: 2025-11-04
---
# KL Boogaloo: Tempered KL Divergence For Metric-Aware Entropy

The KL divergence between two probability distributions is invariant under arbitrary permutations of the underlying space and therefore does not respect the metric.  Optimal transport is a cool alternative but it doesn't quite capture the thing I want to capture - metric-aware entropy.  I propose the tempered KL divergence as a reasonably natural choice.  By design, I want this to have a scale parameter which represents something like the scale at which you cease to be able to tell nearby numbers apart, while larger-scales are still left approximately permutation invariant. 

---

## KL’s permutation invariance (and why that’s dumb)

$$  
D_{\mathrm{KL}}(p|q)=\int p(x)\log\frac{p(x)}{q(x)},dx  
$$

is invariant under relabelings of the real line. On a metric space this is unnatural: we want $x$ and $x+\varepsilon$ to be “almost the same,” not arbitrarily permutable. You can think of bare KL here as the $t=0$ thermal “distance”: maximally coarse and indifferent to locality.

---

## Thermalization via kernels

Let $(X,d)$ be a metric space (e.g., $\mathbb{R}^n$ with Euclidean metric, or a Riemannian manifold with volume measure $dx$). Consider a Markov kernel $K_t(x,y)$ forming a semigroup $(K_t)_{t\ge0}$ with $K_0(x,y)=\delta_x(y)$. Define the “tempered” densities  

$$  
p_t(x)=\int K_t(x,y),p_0(y),dy,\qquad  
q_t(x)=\int K_t(x,y),q_0(y),dy.  
$$

(and no I _don't_ care if 'tempered density' is already taken.  For me, it means this thing.)

I'll require two natural criteria: we want a **parametrized family** $K_t$ that:
- reduces to the identity at $t=0$; and    
- as $t \to 0$, $K_t$ is equivalent to convolving with $N(\mu= d(x,y), \sigma^2 = t)$.

The canonical choice is the **heat kernel**, i.e., the transition density of the heat semigroup for the Laplacian (Laplace–Beltrami on a manifold). Varadhan’s small-time asymptotics say  

$$  
\log K_t(x,y) =-\frac{d(x,y)^2}{4t}+O(\log t)\quad(t\to0),  
$$  
so the blur scale is $d\sim \sqrt{2t}$ (constants like $\sqrt{2}$ depend on convention and I will inconsistently ignore them as I please). On $\mathbb{R}^n$ with the heat equation $\partial_t u=\Delta u$, $K_t$ is Gaussian with covariance $2t,I$, hence typical displacement $\sim \sqrt{2t}$.

Note that tempering discards information:  

$$  
D_{\mathrm{KL}}(p_0|p_t)  
=\int p_0(x)\log\frac{p_0(x)}{(K_t*p_0)(x)}dx  
= \mathrm{CE}(p_t|p_0)-H(p_0),  
$$  
where $H(p)=-\int p\log p$ and $\mathrm{CE}(r|s)=-\int r\log s$.

---

## The Tempered KL-Divergence

Define the **tempered KL** at scale $t$:  

$$  
D_t(p_0,q_0) := D_{\mathrm{KL}}(p_t|q_t)  
\quad\text{with}\quad p_t=K_t p_0, q_t=K_t q_0  
$$

Tbh that's all I wanted - a scale-sensitive way to understand information on continuous spaces.  Yes you now have the scale $t$ which is arbitrary, but I contend that this is more physical and less arbitrary than working with respect to a reference measure.
For the heat kernel (with the convention $\partial_t u=\Delta u$), two key facts hold:
- **Small-time expansion**  
  
  $$  
    D_t(p_0|q_0)=D_{\mathrm{KL}}(p_0|q_0)-t I_{\mathrm{rel}}(p_0|q_0)+o(t)\quad(t\to0),  
    $$  
    where the **relative Fisher information** is  
    
    $$  
    I_{\mathrm{rel}}(p|q)=\int p(x),\big|\nabla\log\frac{p(x)}{q(x)}\big|^2,dx.  
    $$
    
- **Exact dissipation (all $t\ge0$)**  
    
    $$  
    \frac{d}{dt}D_t(p_0|q_0)  
    =-I_{\mathrm{rel}}(p_t|q_t).  
    $$
    

Thus $D_t$ continuously interpolates from permutation-invariant KL at $t=0$ to a geometry-aware comparison at resolution $\sqrt{t}$.

---

## Wasserstein Time Baby

Here's a cute mini-connection to Wasserstein world (where, you may recall, heat flow is gradient descent on the entropy functional).  Let $S[p]=\int p\log p,dx$ (entropy up to sign). The **Wasserstein-2 gradient flow** of $S$ is the heat equation. In continuity-equation form,  

$$  
\partial_t p_t + \nabla \cdot\big(p_tv_p(t)\big)=0,  
\qquad v_p(t) = -\nabla_{W_2}S[p_t]=-\nabla\log p_t,  
$$  

so the Wasserstein gradient field is $-\nabla\log p$.

Two standard identities:

1. **Kinetic energy = Fisher**  
    
    $$  
    \mathbb E_p[|\nabla_{W_2}S[p]|^2]  
    =\int p |\nabla\log p|^2 dx  
    =I(p).  
    $$
    
2. **Relative kinetic energy = relative Fisher**  
    Evolve $p_t$ and $q_t$ under the **same** heat semigroup. Their velocity fields are $v_p(t)=-\nabla\log p_t$ and $v_q(t)=-\nabla\log q_t$. Define the **relative velocity**  
    
    $$  
    w_t = v_p(t)-v_q(t) = -\nabla\log\frac{p_t}{q_t}.  
    $$  
    Then  
    
    $$  
    I_{\mathrm{rel}}(p_t|q_t)  
    =\int p_t,|w_t|^2dx  
    =\mathbb{E}_{p_t}\big[|w_t|^2\big].  
    $$

Equivalently, if $H(\cdot):=D_{\mathrm{KL}}(,\cdot,|,\pi)$ for any fixed reference density $\pi$ (so $\nabla_{W_2}H(p)=\nabla\log(p/\pi)$), then  

$$  
\nabla_{W_2}H(p_t)-\nabla_{W_2}H(q_t)=\nabla\log\frac{p_t}{q_t},  
$$  
and the KL dissipation can be written purely in Wasserstein terms:  

$$  
\frac{d}{dt}D_{\mathrm{KL}}(p_t|q_t)  
= -\mathbb{E}_{p_t}\left[\big|\nabla_{W_2}H(p_t)-\nabla_{W_2}H(q_t)\big|^2\right]
$$


---

# Tempered entropy under general coordinate changes

Here's a shot at trying to find a version of the differential entropy that is coordinate free.  I think this ends up being a middling-to-bad answer to this question but bleh.

Let's add a decorative $g$ for the metric to heat kernel $K^g_t$.  For the love of all things holy do not make me put $g$ on every object.  I'll mark the transformed ones though.

Take a change-of-coords / diffeomorphism $\Phi:M\to M$.  
We'll use $J$ for the jacobian determinant (as opposed to the Jacobian matrix; sue me)  

$$  
J_\Phi(x) =|\det D\Phi(x)|\text{)}.  
$$  
The pushforward is  

$$  
(\Phi_\# p)(y) = \frac{p(\Phi^{-1}(y))}{J_\Phi(\Phi^{-1}(y))}.  
$$

Recall the very cringe fact that

$$  
H(\Phi_\# p) = H(p) + \mathbb{E}_{p}\left[\log J_\Phi\right].  
$$
  
For the scaling $\Phi(x)=a x$ in $\mathbb R^\sigma$, $J_\Phi\equiv a^\sigma$, giving $H(\times_a p)=H(p)+\sigma\log a$.
This is dumb because you shouldn't be able to increase entropy by changing coordinates.  Yes there's a cope where you talk about it being entropy density or some such, but I don't like that.

Anyways.  This is about to get a little annoying because its just renaming objects and saying how they change under $\Phi$.  You should skip till later.

In terms of the pushforward metric we have:

$$  
\Phi_\# \big(K_t^{g} p\big) = K_t^{\Phi_\# g}\big(\Phi_\# p\big).  
$$

$$  
H_t^{\Phi_\# g}(\Phi_\# p_0)  
= H\left(K_t^{\Phi_\# g}(\Phi_\# p_0)\right)  
= H\left(\Phi_\# (K_t^{g} p_0)\right)  
= H\left(K_t^{g} p_0\right) + \mathbb{E}_{p_t}\left[\log J_\Phi\right].  
$$  
Okay so that's uhh annoying.  The only difference here that lets us get a kinda maybe satisfactory answer is that we can track $\Delta H_t := H_t - H_0$ instead, which is a little more natural than introducing an arbitrary reference measure.

If we take a sizeable huff of copium we can pretend that that's good enough; the additive term cancels between $H_t$ and $H$

$$  
\Delta H_t^{\Phi_\# g}(\Phi_\# p_0) = \Delta H_t^{g}(p_0).  
$$

Thus $\Delta H_t$, the 'tempering entropy' is invariant under coordinate transformations.

Note delightfully though that, as $\Delta H_t$ is the entropy lost by convolving with a random variable, this is a manifestation of the equability property of entropy, at least for small $t$ when it's Gaussian; I forget if equability holds for non-Gaussian noise.

# Entropy Generation In Dynamical Systems - "Convective Entropy"

Next we turn to considering entropy generation for dynamical systems - our formulation here gives us a nice way to characterise the intuitive notion that chaotic systems, to the extent that they are sensitive to initial conditions, should require more effective information to specify their states.  I'm not sure if this is the optimal thing to measure to this effect, but a simple quantity is, for some initial probability density $\phi(x)$,

$$\Upsilon(s,t) := H[K_s \Phi_t \phi] - H[\Phi_t K_s \phi]$$
I named it $\Upsilon$ because I think this is a really awesome application, and I want to have a canonical symbol for it, and I feel bad for $\Upsilon$.  For the sake of naming it, I'll call it the "convective entropy".  Intuitively this is of course the additional entropy accrued by considering our thermalization process as occuring before or after the pushforward.  Just as an aside because I think the formula looks neet, note first that

$$H[\Phi_t \phi] = H[\phi] + \mathbb E_{\phi}\log |D\Phi_{-t}|$$

And, for small diffusions:

$$\partial_s H[K_s \phi] = I[\phi]$$

Since we really only like our thermalisation for small $s$ anyways, and I couldn't figure out any other neat asymptotics, we can calculate $\Upsilon(s,t)\sim s[\partial_s \Upsilon](0,t) + o(s) = [\partial_{\log s}\Upsilon](0,t)$:

$$\Upsilon(t) :=\partial_{\log s} \Upsilon(0,t) = I[\Phi_t\phi] - I[\phi] - \mathbb E_{\phi}[\Delta \log |D \Phi_t|]$$

(the $\log s$ makes it a little cleaner, doesn't matter.)
So what are we to make of this?  A simple example sheds a little light - imagine $\phi$ is uniform over a sphere and 0 elsewhere, then the fisher information diverges to infinity; if $\phi$ is Gaussian with variance $\sigma^2$, the fisher information is $\frac{d}{\sigma^2}$.  This diverges as $\sigma \to 0$.  So intuitively we're measuring something that really _hates_ sharp edges.  We can understand this by looking at the fourier:

$$K_s\phi = \int \tilde \phi(k)e^{-sk^2} e^{ikx} dV_k$$

For my physics friends, it may please you to replace $s \to \frac{1}{\Lambda^2}$, so that this is just heat kernel regularization (oh... hey... hi!).

This is a property I really really like - dynamical systems by default have this notion of phase volume relating to entropy, but it makes me happy to have an entropy-like notion which is both canonical and natively aware of "sharpness", which feels good for handling things where we ask about sensitivity to initial conditions.  I think this is definitely a killer app, I'm very happy with it!

So last real quick on FTLEs, and sorta just sharing some cute objects I came across:
The Cauchy strain under $\Phi$ is

$$C(x,t) = D\Phi^T_t D \Phi_t(x)$$
which is the metric for the finite deformation at $x$.  I would have called it $g$ but it looks like there are already so many named strain tensors that the IUPAC has rules about it...

The finite time Lyapunov exponents (FTLE) $\Lambda(x,t)$ are the log eigenvalues.

$$C = P e^{2\Lambda t}P^T)$$
So, being a little cavalier with our asymptotics for the sake of illustration, for large times $t$, introducing the _instantaneous global_ maximum eigenvalue $\lambda^*(t) = \max_x \bar \lambda(x,t)$


$$\Upsilon(t) \sim (constant) ~ e^{2\lambda^*(t)~ t}$$

(and mutatis mutandis for the time reversed case).  One can get much more complicated with this, extending the integral to the forward/backward attracting FTLE sets; while that was fun, I didn't get much out of it.  In words, the convection entropy grows exponentially with the global maximum Lyapunov exponent.


# Summary
- KL divergence is invariant under permutation of the real numbers; this is cringe because it doesn't respect locality
- I give conditions for a tempering convolution which, together, sorta-kinda-uniquely specify the heat kernel (at least as $t\to0$ and modulo reparameterization)
- I use the heat kernel to define a tempered KL divergence, which is the KL divergence between the distributions after each is convolved with the heat kernel:  
  
  $$D_t(p||q) = D_{KL}(K_t*p||K_t*q)$$
  
- For small times $t$, $K_t$ is approximately a gaussian of width $\sigma = \sqrt{2t}$.  Morally, this is roughly equivalent to dividing up continuous space into discrete chunks of diameter $O(\sqrt t)$ and likewise coarse-graining any observables; then we take the (more soundly defined imo) discrete entropy.  The tempered entropy is approximately invariant under permutations with length-scale $\xi >> \sqrt t$.  Thus, gleefully, $1/\sqrt{t}$ is the 'cutoff' frequency of tempered information theory.
- I relate the tempered divergence to gradient flow in Wasserstein space.
- I introduce the (differential) tempering entropy $\Delta H_t[p]$ which quantifies how much entropy is lost by convolving with the heat kernel as a function of $t$; it is invariant under coordinate transformations, unlike the differential entropy itself $H[p]$.
- I introduced the convective entropy $\Upsilon(t)$ (depending on initial distribution $\phi$ and dynamical system $\Phi_t$) which which measures the difference in entropy between 'evolving a tempered distribution' and 'tempering an evolved distribution'.  I illustrate a schematic relationship between the convective entropy and the global maximum Lyapunov exponent.

---

LLM Usage Note: I wrote the notes for this post and asked GPT to organize and write it up, and then I edited everything for tone.  I also had it do the basic manipulations for the Wasserstein and tempered entropy.