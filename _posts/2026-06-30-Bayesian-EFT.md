---
title: "[AI-Written] Bayesian EFT"
date: 2026-06-30
math: true
kind: research note
---

# Bayesian EFT

*Author's note (CRW, not GPT-generated):*

I've been thinking for a while about how to get a model where we can think of LLMs and co. as doing some sort of "progressive resolution" of higher moments of the distribution, based on the "moment-bias" work.  I have an intuition that this has to depend lots on inductive biases above a certain level of N-grams.  I got GPT to write a reasonably good version of this theory - enough to give me the language I wanted, and enough to be comfortable that this isn't likely to tell us anything useful (perhaps if you do some crazy MFT calculations?).  Since I'm less excited by it now, I'll just share this writeup as GPT wrote it, for the sake of being able to point to the idea in the future.

*This work was done as part of the Iliad fellowship under the mentorship of Dmitry Vaintrob.*

*Everything below this point was written by GPT5.5-Pro.*

---

# Mean-field theory for neural networks: a physicist’s tutorial

I’ll use **MFT** to mean the family of large-width, weak-coupling, self-consistent theories for neural networks. The unifying picture is simple:

> A neuron/channel in a wide layer receives a sum of many weakly dependent random contributions. In the large-width limit, the microscopic variables become exchangeable, the effective field seen by one representative neuron becomes Gaussian or a self-consistent stochastic process, and the network is described by a few macroscopic order parameters: variances, correlations, kernels, response functions, and empirical parameter distributions.

That sentence is the neural-network analogue of the Curie-Weiss or spin-glass move: replace (N) microscopic variables by order parameters, but the relevant order parameter is usually **not a scalar magnetization**. In modern NN mean-field theory, the central order parameters are often **kernels over data points**, and during training they may also depend on **two training times**.

The most useful schools for understanding neural nets are:

1. **Signal-propagation / Gaussian-process MFT at initialization.** This gives variance and correlation recursions, ordered/chaotic phases, edge-of-chaos initialization, gradient explosion/vanishing, and NNGP kernels.

2. **NTK / lazy-training theory.** This describes infinite-width training when features barely move. It is often the cleanest solvable baseline.

3. **Mean-field training as interacting particles.** For two-layer networks, neurons become particles whose empirical distribution follows a Wasserstein gradient-flow PDE. This is the cleanest feature-learning mean-field theory.

4. **Dynamical mean-field theory and tensor-program / (\mu)P limits for deep feature learning.** These generalize the statphys DMFT spirit to training dynamics in deep networks, where order parameters become time-dependent kernels.

I will emphasize what is useful for analyzing real networks and will mostly avoid limits that are mathematically beautiful but operationally distant.

---

## 1. What is “mean field” in neural networks?

In statphys, mean field often means replacing local fluctuations by an average field. In neural networks, that phrase is slightly misleading. A useful neural-network MFT does **not** usually say “every neuron is equal.” Rather, it says:

$$
\text{one representative neuron sees a random effective field whose law is determined self-consistently.}
$$

The reason is the (1/\sqrt n) weight scaling. If layer (\ell) has width (n_{\ell}), a preactivation has the form

$$
h_i^{\ell}(x)
=============

b_i^\ell
+
\sum_{j=1}^{n_{\ell-1}} W_{ij}^{\ell},x_j^{\ell-1}(x),
\qquad
W_{ij}^{\ell}\sim \mathcal N!\left(0,\frac{\sigma_w^2}{n_{\ell-1}}\right).
$$

Each term is small; there are many of them; and the sum has (O(1)) variance. Thus the effective field becomes Gaussian under broad assumptions. This is the neural-network analogue of the local field in a spin glass, except that the covariance of this field is indexed by input examples, layers, and sometimes training times.

At initialization, the central order parameter is a two-input covariance,

$$
Q_\ell(x,x')
============

\mathbb E\big[h_i^\ell(x)h_i^\ell(x')\big].
$$

During training, a richer theory may require

$$
Q_\ell^{\alpha\beta}(t,t')
==========================

\frac{1}{n_\ell}
\sum_{i=1}^{n_\ell}
h_i^\ell(x_\alpha,t),h_i^\ell(x_\beta,t'),
$$

and analogous order parameters for activations, backpropagated errors, responses, and tangent kernels. This is where the analogy with dynamical MFT becomes closest.

Historically, the statphys DMFT lineage enters neural networks through random recurrent networks, where Sompolinsky, Crisanti, and Sommers derived a self-consistent (N\to\infty) theory predicting a transition from stationary to chaotic dynamics. That same conceptual move—replace a high-dimensional random network by a self-consistent stochastic process—reappears in modern deep-network signal propagation and feature-learning DMFT. ([APS Link][1])

---

# Part I. Mean-field theory at initialization

## 2. The basic random feedforward network

Consider a fully connected network with scalar nonlinearity (\phi). For inputs (x\in\mathbb R^{n_0}),

$$
x^0(x)=x,
$$

and for (\ell=1,\dots,L),

$$
h_i^\ell(x)
===========

b_i^\ell
+
\sum_{j=1}^{n_{\ell-1}}
W_{ij}^\ell x_j^{\ell-1}(x),
\qquad
x_i^\ell(x)=\phi(h_i^\ell(x)).
$$

Assume

$$
W_{ij}^\ell\stackrel{\text{i.i.d.}}{\sim}
\mathcal N!\left(0,\frac{\sigma_w^2}{n_{\ell-1}}\right),
\qquad
b_i^\ell\stackrel{\text{i.i.d.}}{\sim}
\mathcal N(0,\sigma_b^2).
$$

This is the standard scaling: the summed input to each neuron has (O(1)) variance as width grows.

Let (x_\alpha,x_\beta) be two fixed data points. Conditional on the previous-layer activations, the pair

$$
\big(h_i^\ell(x_\alpha),h_i^\ell(x_\beta)\big)
$$

is Gaussian, because it is a linear combination of Gaussian weights. Its conditional covariance is

$$
\mathbb E!\left[
h_i^\ell(x_\alpha)h_i^\ell(x_\beta)
,\middle|,
x^{\ell-1}
\right]
=

\sigma_b^2
+
\frac{\sigma_w^2}{n_{\ell-1}}
\sum_{j=1}^{n_{\ell-1}}
x_j^{\ell-1}(x_\alpha)
x_j^{\ell-1}(x_\beta).
$$

Now take (n_{\ell-1}\to\infty). The empirical average self-averages:

$$
\frac{1}{n_{\ell-1}}
\sum_j
x_j^{\ell-1}(x_\alpha)x_j^{\ell-1}(x_\beta)
\longrightarrow
\mathbb E!\left[
\phi(u)\phi(v)
\right],
$$

where ((u,v)) is a centered Gaussian pair with covariance determined by the previous layer. Therefore the covariance recursion is

$$
Q_\ell(x_\alpha,x_\beta)
========================

\sigma_b^2
+
\sigma_w^2,
\mathbb E_{(u,v)\sim \mathcal N(0,\Sigma_{\ell-1}^{\alpha\beta})}
\big[\phi(u)\phi(v)\big],
$$

with

$$
\Sigma_{\ell-1}^{\alpha\beta}
=============================

\begin{pmatrix}
Q_{\ell-1}(x_\alpha,x_\alpha) & Q_{\ell-1}(x_\alpha,x_\beta)\
Q_{\ell-1}(x_\beta,x_\alpha) & Q_{\ell-1}(x_\beta,x_\beta)
\end{pmatrix}.
$$

This recursion is the core of the **neural-network Gaussian process** picture: for any finite set of inputs, the random function computed by an infinite-width network converges to a Gaussian process whose kernel is obtained by iterating this covariance map. Neal observed the shallow version, and later work extended and formalized the deep fully connected case. ([Glizen][2])

The derivation is worth internalizing. There are only three ingredients:

$$
\text{weak coupling }(1/\sqrt n)
\quad+\quad
\text{exchangeability}
\quad+\quad
\text{law of large numbers / CLT}.
$$

Everything else is bookkeeping.

---

## 3. Variance recursion: avoiding exploding or dying activations

For one input, define

$$
q_\ell(x)=Q_\ell(x,x).
$$

If all inputs have the same norm, or if we focus on a typical input, write simply (q_\ell). Then

$$
q_\ell
======

\sigma_b^2
+
\sigma_w^2
\mathbb E_{z\sim\mathcal N(0,1)}
\left[
\phi!\left(\sqrt{q_{\ell-1}},z\right)^2
\right].
$$

A stable deep network needs (q_\ell) not to explode or vanish with (\ell). Thus one chooses (\sigma_w,\sigma_b,\phi) so that the map

$$
q \mapsto V(q)
==============

\sigma_b^2
+
\sigma_w^2
\mathbb E_z[\phi(\sqrt q z)^2]
$$

has a useful fixed point (q_\star), and the network is initialized near it.

For ReLU with zero bias,

$$
\phi(h)=\max(0,h),
$$

we have

$$
\mathbb E[\operatorname{ReLU}(\sqrt q z)^2]
===========================================

\frac{q}{2}.
$$

So

$$
q_\ell = \frac{\sigma_w^2}{2}q_{\ell-1}.
$$

The critical variance-preserving choice is

$$
\sigma_w^2=2,
$$

which is the usual He initialization. In this sense, He initialization is a one-line mean-field fixed-point calculation.

For tanh-like nonlinearities, the recursion has a nontrivial saturating structure. Large (\sigma_w) pushes activations into saturation; small (\sigma_w) kills signal. The variance recursion is the first diagnostic, but it is not enough: two inputs can still collapse to the same representation, and gradients can still vanish.

---

## 4. Correlation recursion: order, chaos, and expressivity

Define the normalized correlation

$$
c_\ell(x,x')
============

\frac{Q_\ell(x,x')}
{\sqrt{Q_\ell(x,x)Q_\ell(x',x')}}.
$$

Assume for simplicity that both inputs have reached the same variance fixed point (q_\star). Then the correlation recursion becomes a one-dimensional map,

$$
c_{\ell+1}=F(c_\ell),
$$

where

$$
F(c)
====

\frac{
\sigma_b^2
+
\sigma_w^2
\mathbb E[\phi(u)\phi(v)]
}
{q_\star},
$$

with

$$
(u,v)\sim \mathcal N!\left(
0,
q_\star
\begin{pmatrix}
1 & c\
c & 1
\end{pmatrix}
\right).
$$

The fixed point (c=1) always corresponds to identical inputs. The question is whether nearby inputs become more similar or less similar as depth increases. Linearizing near (c=1),

$$
1-c_{\ell+1}
\approx
\chi(1-c_\ell),
$$

where

$$
\chi
====

\sigma_w^2
\mathbb E_{z\sim\mathcal N(0,1)}
\left[
\phi'(\sqrt{q_\star}z)^2
\right].
$$

This (\chi) is one of the most important quantities in neural-network MFT.

If

$$
\chi<1,
$$

then correlations flow toward (1). Distinct inputs become indistinguishable at large depth. This is the **ordered phase**.

If

$$
\chi>1,
$$

then nearby inputs separate exponentially until nonlinear saturation. This is the **chaotic phase**.

If

$$
\chi=1,
$$

the network is at the **edge of chaos**. The correlation depth scale

$$
\xi_c \sim -\frac{1}{\log \chi}
$$

diverges as (\chi\to 1^-), so information can propagate through many layers. Poole et al. and Schoenholz et al. developed this signal-propagation picture for deep random networks and connected it to expressivity and trainability. ([arXiv][3])

The intuition is physically familiar: (F'(1)) is a Lyapunov-like local expansion factor in representation space. The “phase transition” is not mystical; it is the stability change of the (c=1) fixed point.

---

## 5. ReLU example: the arc-cosine kernel

For ReLU at zero bias, if both preactivations have variance (q) and correlation (c),

$$
\mathbb E[\operatorname{ReLU}(u)\operatorname{ReLU}(v)]
=======================================================

\frac{q}{2\pi}
\left[
\sqrt{1-c^2}
+
(\pi-\arccos c)c
\right].
$$

With (\sigma_w^2=2), the variance is preserved, and the correlation map is

$$
F(c)
====

\frac{1}{\pi}
\left[
\sqrt{1-c^2}
+
(\pi-\arccos c)c
\right].
$$

This is the classic ReLU kernel recursion. It is also a good exercise: derive it by writing two correlated Gaussians as

$$
u=\sqrt q,z_1,
\qquad
v=\sqrt q,(cz_1+\sqrt{1-c^2}z_2),
$$

then integrate over the wedge where (u>0,v>0).

For ReLU, (F'(1)=1), so the network sits at a marginal edge when variance is preserved. However, because ReLU is nonsmooth, the approach to (c=1) is not the same as the smooth-(\phi) tanh case. In practice this is one reason ReLU networks tolerate depth better than saturating sigmoids under naive initialization, though residual connections and normalization matter far more in modern architectures.

---

## 6. Backpropagation MFT: why (\chi) also controls gradients

Now consider backpropagated errors

$$
\delta_i^\ell
=============

\frac{\partial \mathcal L}{\partial h_i^\ell}.
$$

They obey

$$
\delta_i^\ell
=============

\phi'(h_i^\ell)
\sum_{k=1}^{n_{\ell+1}}
W_{ki}^{\ell+1}\delta_k^{\ell+1}.
$$

Under the usual large-width independence approximation, which can be made rigorous in several infinite-width frameworks, the variance evolves as

$$
\tilde q_\ell
=============

\sigma_w^2
\mathbb E[\phi'(h^\ell)^2]
\tilde q_{\ell+1}.
$$

At a forward fixed point (q_\star),

$$
\tilde q_\ell
=============

\chi,
\tilde q_{\ell+1}.
$$

Therefore

$$
\tilde q_\ell
\approx
\chi^{L-\ell}
\tilde q_L.
$$

So the same (\chi) controls both the separation of nearby inputs in the forward pass and the explosion or vanishing of gradients in the backward pass. This is the core practical reason edge-of-chaos initialization matters.

However, (\chi=1) only controls the **mean squared singular value** of the input-output Jacobian. Good training may require more: ideally, all singular values of the Jacobian should concentrate near (1). That stronger condition is called **dynamical isometry**. Pennington, Schoenholz, and Ganguli used random-matrix/free-probability methods to study the full Jacobian singular-value distribution, showing that controlling the whole spectrum is more informative than controlling only the mean. ([arXiv][4])

The hierarchy is:

$$
\text{variance stability}
\quad<\quad
\text{gradient norm stability}
\quad<\quad
\text{dynamical isometry}.
$$

Mean-field variance recursions give the first two. Random-matrix MFT gives the third.

---

# Part II. Infinite-width networks as kernels

## 7. NNGP: the Bayesian prior induced by a random network

The covariance recursion from Part I says that an infinite-width random network defines a Gaussian process:

$$
f(x)\sim \mathcal{GP}(0,K_{\mathrm{NNGP}}(x,x')).
$$

For regression with Gaussian observation noise, Bayesian inference in the infinite-width network is just Gaussian-process regression with this kernel. For classification, one gets the corresponding GP classification problem.

This is a useful theoretical baseline because it isolates the **architecture-induced prior**. Depth, activation, convolution, pooling, residual connections, and normalization all change the kernel. Tensor-program methods broadened the set of architectures for which such infinite-width kernels can be derived, including many feedforward, recurrent, convolutional, attention, skip-connection, batch-normalization, and layer-normalization computations expressible in that formalism. ([arXiv][5])

But the NNGP is a prior or Bayesian posterior story. It is not, by itself, the same as SGD feature learning. It tells you what functions random networks like before training, or what an infinitely wide Bayesian network does after posterior inference.

---

## 8. NTK: training dynamics when features barely move

Now take a finite network (f_\theta(x)) trained by gradient flow on parameters (\theta). Let the training set be ({(x_\alpha,y_\alpha)}_{\alpha=1}^P). Define the neural tangent kernel

$$
\Theta_t(x,x')
==============

\nabla_\theta f_{\theta(t)}(x)\cdot
\nabla_\theta f_{\theta(t)}(x').
$$

The derivation of NTK dynamics is immediate. Gradient flow gives

$$
\dot\theta
==========

-\nabla_\theta \mathcal L.
$$

Therefore

$$
\frac{d}{dt}f_t(x)
==================

# \nabla_\theta f_t(x)\cdot \dot\theta

*

\sum_{\beta=1}^P
\Theta_t(x,x_\beta)
\frac{\partial \mathcal L}{\partial f_t(x_\beta)}.
$$

For squared loss,

$$
\mathcal L
==========

\frac12
\sum_{\alpha=1}^P
(f_t(x_\alpha)-y_\alpha)^2,
$$

the residual vector

$$
r_t=f_t(X)-y
$$

obeys

$$
\dot r_t
========

-\Theta_t(X,X)r_t.
$$

The NTK theorem says that, under the usual infinite-width scaling, (\Theta_t) converges to a deterministic limit (\Theta_0) and stays constant during training. Then

$$
r_t
===

e^{-\Theta_0 t}r_0.
$$

So infinite-width training becomes kernel gradient descent. Jacot, Gabriel, and Hongler introduced this NTK description and showed that, in the infinite-width limit, the kernel is deterministic and fixed during training. ([arXiv][6])

The punchline is:

$$
\boxed{
\text{NNGP describes the random function at initialization;}
\quad
\text{NTK describes gradient descent around initialization.}
}
$$

The NTK limit is powerful because it makes optimization linear. But precisely because it is linearized around initialization, it cannot by itself explain substantial representation learning.

---

## 9. NTK recursion from the same mean-field machinery

For fully connected networks, the NTK can be computed by a recursion parallel to the NNGP recursion.

Let (K_\ell(x,x')) be the forward covariance at layer (\ell). Define

$$
\dot K_{\ell+1}(x,x')
=====================

\sigma_w^2
\mathbb E_{(u,v)\sim \mathcal N(0,\Sigma_\ell)}
$$
\phi'(u)\phi'(v)
].
$$

Then, up to convention-dependent placement of (\sigma_w^2) and bias terms, the NTK recursion is

$$
\Theta_{\ell+1}(x,x')
=====================

K_{\ell+1}(x,x')
+
\dot K_{\ell+1}(x,x'),
\Theta_\ell(x,x').
$$

The interpretation is clean. The first term is the contribution of the new layer’s parameters. The second term propagates the sensitivity of earlier layers through the new layer. This recursion is just backpropagation written at the level of mean-field order parameters.

This is one of the best places to see that NNGP and NTK are siblings: both are kernel recursions generated by the same Gaussian effective field. The NNGP tracks activations; the NTK tracks parameter sensitivities.

---

## 10. Lazy training and what it misses

A network is in the **lazy regime** when

$$
f_{\theta(t)}(x)
\approx
f_{\theta(0)}(x)
+
\nabla_\theta f_{\theta(0)}(x)\cdot(\theta(t)-\theta(0)).
$$

That is, the model behaves like its first-order Taylor expansion. Chizat, Oyallon, and Bach emphasized that lazy training is not uniquely a neural-network phenomenon; it is a scaling regime in which a nonlinear model behaves like its linearization around initialization. They also argued that forcing practical deep networks into the lazy regime can harm performance, especially when feature adaptivity matters. ([arXiv][7])

This is important because NTK theory is sometimes oversold. Its strengths are real:

$$
\text{optimization becomes convex-like, analyzable, and stable.}
$$

But its weakness is equally real:

$$
\text{the representation is essentially fixed.}
$$

A useful diagnostic in experiments is the relative kernel drift,

$$
\frac{|\Theta_t-\Theta_0|}{|\Theta_0|}.
$$

If this remains tiny, a kernel theory may be a good model. If it becomes (O(1)), the network is doing feature learning, and an NTK-only story is incomplete.

---

# Part III. Mean-field training as interacting particles

The cleanest feature-learning MFT is for two-layer networks. This is worth understanding deeply because it is the prototype for richer theories.

## 11. Two-layer network as an empirical measure

Consider

$$
f_N(x)
======

\frac{1}{N}
\sum_{i=1}^N
\sigma_\star(x;\theta_i),
$$

where

$$
\theta_i=(a_i,w_i),
\qquad
\sigma_\star(x;\theta_i)=a_i\phi(w_i\cdot x).
$$

Define the empirical measure over neuron parameters,

$$
\rho_N
======

\frac{1}{N}
\sum_{i=1}^N
\delta_{\theta_i}.
$$

Then

$$
f_N(x)
======

\int \sigma_\star(x;\theta),\rho_N(d\theta).
$$

In the (N\to\infty) limit, (\rho_N) becomes a deterministic probability measure (\rho), and the network function becomes

$$
f_\rho(x)
=========

\int \sigma_\star(x;\theta)\rho(d\theta).
$$

This is the basic mean-field lift:

$$
{\theta_1,\dots,\theta_N}
\quad\longrightarrow\quad
\rho(\theta).
$$

The nonconvex finite-dimensional particle problem becomes an infinite-dimensional flow over measures.

Mei, Montanari, and Nguyen derived such a limiting description of SGD dynamics for two-layer networks in terms of a nonlinear PDE; Rotskoff and Vanden-Eijnden developed the interacting-particle viewpoint; Chizat and Bach connected this to Wasserstein gradient flows and global convergence under appropriate conditions. ([arXiv][8])

---

## 12. Deriving the mean-field PDE

Let the population risk be

$$
\mathcal R(\rho)
================

\mathbb E_{(x,y)}
\left[
\ell(f_\rho(x),y)
\right].
$$

For squared loss,

$$
\ell(f,y)=\frac12(f-y)^2.
$$

The functional derivative of (\mathcal R) with respect to (\rho) is

$$
\Psi(\theta;\rho)
=================

# \frac{\delta \mathcal R}{\delta \rho}(\theta)

\mathbb E_{(x,y)}
\left[
\partial_1 \ell(f_\rho(x),y),
\sigma_\star(x;\theta)
\right].
$$

For squared loss,

$$
\Psi(\theta;\rho)
=================

\mathbb E_{(x,y)}
\left[
(f_\rho(x)-y),
\sigma_\star(x;\theta)
\right].
$$

Now suppose the particles follow the gradient-flow ODE

$$
\dot\theta_i
============

-\nabla_\theta \Psi(\theta_i;\rho_N).
$$

Then for any smooth test function (\varphi),

$$
\frac{d}{dt}
\int \varphi(\theta)\rho_N(d\theta)
===================================

\frac{1}{N}
\sum_i
\nabla\varphi(\theta_i)\cdot \dot\theta_i
=========================================

*

\int
\nabla\varphi(\theta)\cdot
\nabla_\theta\Psi(\theta;\rho_N)
,\rho_N(d\theta).
$$

Passing to the limit gives

$$
\frac{d}{dt}
\int \varphi(\theta)\rho_t(d\theta)
===================================

*

\int
\nabla\varphi(\theta)\cdot
\nabla_\theta\Psi(\theta;\rho_t)
,\rho_t(d\theta).
$$

Integrating by parts, the weak form is equivalent to

$$
\boxed{
\partial_t\rho_t
================

\nabla_\theta\cdot
\left(
\rho_t\nabla_\theta\Psi(\theta;\rho_t)
\right).
}
$$

This is a nonlinear continuity equation. It is also the Wasserstein gradient flow of (\mathcal R(\rho)).

The descent identity is immediate:

$$
\frac{d}{dt}\mathcal R(\rho_t)
==============================

\int
\frac{\delta \mathcal R}{\delta\rho}(\theta)
\partial_t\rho_t(d\theta)
=========================

\int
\Psi
\nabla\cdot(\rho_t\nabla\Psi)
,d\theta
========

*

\int
|\nabla_\theta\Psi(\theta;\rho_t)|^2
\rho_t(d\theta)
\le 0,
$$

assuming boundary terms vanish.

This is the most important derivation in the two-layer mean-field theory. It shows why the limiting dynamics is simpler than the finite network: instead of tracking (N) interacting neurons, we track a deterministic density moving down a measure-space risk landscape.

---

## 13. Adding noise: mean-field Langevin dynamics

If the particle dynamics includes isotropic noise,

$$
d\theta_i
=========

-\nabla_\theta\Psi(\theta_i;\rho_N),dt
+
\sqrt{2\tau},dB_i(t),
$$

then the limiting PDE becomes

$$
\partial_t\rho_t
================

\nabla\cdot(\rho_t\nabla\Psi)
+
\tau\Delta\rho_t.
$$

Equivalently,

$$
\partial_t\rho_t
================

\nabla\cdot
\left[
\rho_t\nabla
\left(
\Psi+\tau\log\rho_t
\right)
\right].
$$

So the noisy dynamics is the Wasserstein gradient flow of the free energy

$$
\mathcal F(\rho)
================

\mathcal R(\rho)
+
\tau\int \rho(\theta)\log\rho(\theta),d\theta.
$$

This is close in spirit to equilibrium statphys: risk plays the role of energy, SGD noise produces an entropy term, and the stationary density is shaped by an energy-entropy tradeoff. Real minibatch SGD noise is not generally isotropic or constant-temperature, but this Langevin version is the analytically clean reference model.

---

## 14. Output dynamics and the evolving kernel

The PDE gives an illuminating bridge between mean-field feature learning and NTK.

Differentiate

$$
f_t(x)=\int \sigma_\star(x;\theta)\rho_t(d\theta).
$$

Using the PDE,

$$
\dot f_t(x)
===========

-\int
\nabla_\theta\sigma_\star(x;\theta)
\cdot
\nabla_\theta\Psi(\theta;\rho_t)
,\rho_t(d\theta).
$$

For squared loss,

$$
\nabla_\theta\Psi(\theta;\rho_t)
================================

\mathbb E_{(x',y')}
\left[
(f_t(x')-y')
\nabla_\theta\sigma_\star(x';\theta)
\right].
$$

Therefore

$$
\dot f_t(x)
===========

*

\mathbb E_{(x',y')}
\left[
H_{\rho_t}(x,x')
(f_t(x')-y')
\right],
$$

where

$$
H_{\rho_t}(x,x')
================

\int
\nabla_\theta\sigma_\star(x;\theta)
\cdot
\nabla_\theta\sigma_\star(x';\theta)
,\rho_t(d\theta).
$$

This (H_{\rho_t}) is a tangent kernel, but it evolves because (\rho_t) evolves.

Thus:

$$
\boxed{
\text{NTK: } \dot f=-H_{\rho_0}(f-y)
\quad\text{with fixed kernel.}
}
$$

$$
\boxed{
\text{Mean-field feature learning: } \dot f=-H_{\rho_t}(f-y)
\quad\text{with evolving kernel.}
}
$$

This is a conceptual bridge worth remembering. Feature learning is not “non-kernel” in the sense that no kernel exists. It is better thought of as **kernel evolution**.

---

## 15. Scaling: why different limits give different theories

A subtle but crucial point: the limit depends on how output scale, learning rate, and time scale with width.

For

$$
f_N(x)=\frac1N\sum_{i=1}^N\sigma_\star(x;\theta_i),
$$

the ordinary parameter gradient satisfies

$$
\nabla_{\theta_i}\mathcal R_N
=============================

\frac1N\nabla_\theta\Psi(\theta_i;\rho_N).
$$

Thus if we use unscaled gradient flow,

$$
\dot\theta_i=-\nabla_{\theta_i}\mathcal R_N,
$$

then particles move only (O(1/N)) over (O(1)) time. To get (O(1)) particle motion, one studies the rescaled flow

$$
\dot\theta_i
============

# -N\nabla_{\theta_i}\mathcal R_N

-\nabla_\theta\Psi(\theta_i;\rho_N).
$$

Equivalently, one rescales learning rate or training time. This is not a technical nuisance; it is exactly the distinction between lazy and feature-learning limits.

A useful mental model is:

$$
\begin{array}{ccl}
\text{ordinary infinite-width NTK scaling}
&\Longrightarrow&
\text{parameters barely move; features fixed;}[3pt]
\text{mean-field / rich scaling}
&\Longrightarrow&
\text{neurons move }O(1)\text{; features evolve.}
\end{array}
$$

This is why two papers can both say “infinite width” and derive different answers. The width limit is not a theory until the parameterization and learning-rate scaling are specified.

---

## 16. Why the two-layer PDE is useful

The two-layer mean-field PDE gives several concrete benefits.

First, it gives a **closed training dynamics** in terms of a distribution (\rho_t). This removes permutation symmetry among neurons and avoids tracking individual units.

Second, it explains why overparameterization can smooth the landscape. The function (f_\rho) is linear in (\rho), and if the loss is convex in (f), then the lifted objective is convex in a suitable measure space. The finite particle parameterization remains nonconvex, but the infinite-particle limit is much better behaved.

Third, it gives a rigorous way to discuss feature learning: the representation changes because the support and density of (\rho_t) move.

Fourth, it gives a natural route to finite-width corrections: (\rho_N) fluctuates around (\rho), and one can study a CLT for the empirical measure.

The caveat is that the clean PDE theory is most mature for shallow networks. Deep feature learning needs more elaborate order parameters.

---

# Part IV. Deep feature learning and dynamical MFT

## 17. Why deep feature learning is harder

In a two-layer network, a neuron’s parameter (\theta_i=(a_i,w_i)) is a relatively self-contained particle. In a deep network, a hidden unit in layer (\ell) interacts with upstream and downstream layers through a hierarchy of forward activations and backward gradients.

Training changes the distribution of weights, which changes the distribution of activations, which changes the gradients, which changes the weights. A static kernel is insufficient.

The right order parameters are no longer just

$$
Q_\ell^{\alpha\beta}
====================

\frac1{n_\ell}
\sum_i h_i^\ell(x_\alpha)h_i^\ell(x_\beta),
$$

but time-dependent objects like

$$
Q_\ell^{\alpha\beta}(t,t')
==========================

\frac1{n_\ell}
\sum_i
h_i^\ell(x_\alpha,t)
h_i^\ell(x_\beta,t'),
$$

and backward analogues such as

$$
\widetilde Q_\ell^{\alpha\beta}(t,t')
=====================================

\frac1{n_\ell}
\sum_i
\delta_i^\ell(x_\alpha,t)
\delta_i^\ell(x_\beta,t').
$$

One also often needs response functions, because during training the effective noise is not independent of the trajectory. This is the familiar statphys lesson: once dynamics and disorder interact, correlations and responses both matter.

---

## 18. Dynamical MFT template: random recurrent networks

It helps to recall the classic random recurrent network:

$$
\dot h_i(t)
===========

-h_i(t)
+
\sum_{j=1}^N J_{ij}\phi(h_j(t)),
\qquad
J_{ij}\sim \mathcal N(0,g^2/N).
$$

For large (N), the recurrent input

$$
\eta_i(t)=\sum_j J_{ij}\phi(h_j(t))
$$

becomes a Gaussian process with covariance

$$
\mathbb E[\eta(t)\eta(t')]
==========================

g^2
C(t,t'),
$$

where

$$
C(t,t')
=

\mathbb E[\phi(h(t))\phi(h(t'))].
$$

Thus the (N)-dimensional system becomes a single stochastic process

$$
\dot h(t)
=========

-h(t)+\eta(t),
$$

with (\eta) self-consistently determined by the law of (h). The transition to chaos occurs when the gain (g) crosses a critical value. This is the Sompolinsky-Crisanti-Sommers story, and it is the cleanest dynamical mean-field analogy for neural networks. ([APS Link][1])

Deep feature-learning DMFT uses the same logic, but the “time” variable is training time, and there is also a layer index.

---

## 19. Self-consistent kernel dynamics in wide feature-learning networks

Recent deep feature-learning DMFT constructs deterministic order parameters that are inner-product kernels of activations and gradients at pairs of inputs and training times. These kernels define the law of hidden activations, the evolution of the NTK, and the output predictions. Bordelon and Pehlevan formulated such a self-consistent dynamical field theory for kernel evolution in wide neural networks, recovering the stochastic-process description obtained by tensor programs in the appropriate infinite-width feature-learning regime. ([arXiv][9])

The schematic structure is:

$$
\text{network trajectory}
\quad\longrightarrow\quad
\text{empirical kernels } Q,\widetilde Q,R
\quad\longrightarrow\quad
\text{self-averaging saddle point}
\quad\longrightarrow\quad
\text{effective stochastic process}
\quad\longrightarrow\quad
\text{self-consistency equations}.
$$

In a path-integral derivation, one inserts delta functions enforcing definitions such as

$$
Q_\ell^{\alpha\beta}(t,t')
==========================

\frac1{n_\ell}
\sum_i
h_i^\ell(x_\alpha,t)h_i^\ell(x_\beta,t'),
$$

introduces conjugate fields, integrates over microscopic weights/neurons, and takes (n_\ell\to\infty). The resulting saddle-point equations are the neural-network analogue of DMFT equations.

This is more involved than the initialization MFT, but the philosophy is identical:

$$
\text{many weakly coupled coordinates}
\quad\Rightarrow\quad
\text{self-consistent stochastic process for one coordinate.}
$$

The practical payoff is that this theory can describe **time-varying kernels**, hence representation learning, while still being lower-dimensional than the full network.

---

## 20. Tensor programs and (\mu)P: a practical infinite-width feature-learning limit

The tensor-program line of work asks a very practical question:

> Which parameterizations have stable, nontrivial infinite-width limits, and which of those limits actually learn features?

Yang and Hu showed that standard and NTK parameterizations do not admit infinite-width limits that learn features in the required sense, and proposed modifications that allow feature learning at infinite width. The broader tensor-program framework gives a language for computing wide-network limits across many architectures. ([arXiv][10])

The practical descendant is **maximal update parameterization**, or (\mu)P. The principle is:

$$
\boxed{
\text{scale parameters and learning rates so that preactivation updates remain }O(1)
\text{ as width grows, without diverging.}
}
$$

This is a mean-field idea in operational form. If updates shrink with width, one gets a lazy/kernel limit. If updates blow up with width, training destabilizes. The “maximal” update is the largest width-stable feature-learning update.

The (\mu)Transfer result is striking: under (\mu)P, many optimal hyperparameters become approximately stable across model width, so one can tune a smaller model and transfer hyperparameters to a larger one. Yang et al. demonstrated this on Transformers and ResNets, including BERT- and GPT-style scaling experiments. ([arXiv][11])

For theoretical work, (\mu)P matters because it gives a deep-network infinite-width limit that is not merely NTK. For practical work, it matters because it suggests a way to make scaling experiments less wasteful.

---

# Part V. High-dimensional statphys limits

## 21. A different “mean field”: (d,n,p\to\infty) teacher-student limits

There is another school closer to classic statistical mechanics of learning: take input dimension (d), sample size (p), and sometimes width (n) to infinity with fixed ratios. The order parameters are overlaps with teacher weights, training/test errors, correlation and response functions, and sometimes replica order parameters.

This can yield sharp learning curves and phase diagrams, especially for Gaussian-mixture classification, generalized linear models, random-feature models, and teacher-student two-layer networks. Mignacco, Krzakala, Urbani, and Zdeborová applied dynamical MFT to SGD in high-dimensional Gaussian-mixture classification, emphasizing that their “mean field” is not a width limit but a high-dimensional statphys DMFT limit. ([arXiv][12])

These limits can be extremely insightful, but they are often specialized to synthetic data distributions. For analyzing practical NNs, I would use them when the scientific question is about:

$$
\text{sample complexity, high-dimensional geometry, SGD noise, teacher-student recovery, or phase transitions.}
$$

I would not use them as the first tool for architecture-level questions like initialization, depth scales, residual connections, or hyperparameter transfer.

---

# Part VI. Finite-width corrections and effective field theory

## 22. Infinite width is a starting point, not the whole theory

The strict (n=\infty) limit is often too simple. Real networks are finite, and finite-width effects can be beneficial or harmful.

At initialization, infinite width gives a Gaussian process. Finite width gives non-Gaussian corrections. At training time, infinite-width NTK gives a fixed kernel. Finite width permits kernel drift and representation learning, unless the parameterization already has feature learning at infinite width.

There are several complementary approaches:

$$
\text{large-width expansions, Feynman diagrams, effective field theory, and finite-width DMFT fluctuations.}
$$

Dyer and Gur-Ari developed a Feynman-diagram method for asymptotics of wide networks, including higher-order corrections to training dynamics. Roberts, Yaida, and Hanin developed an effective-theory approach in which depth-to-width aspect ratio controls deviations from the infinite-width Gaussian description. More recent work analyzes (O(1/\sqrt{\text{width}})) fluctuations of DMFT order parameters in feature-learning networks. ([arXiv][13])

The useful physics analogy is:

$$
n=\infty
\quad\text{is the saddle point,}
\qquad
1/n
\quad\text{corrections are interactions/fluctuations.}
$$

This is one reason I would not dismiss infinite-width theory just because real networks are finite. The saddle may be wrong in detail but still gives the right variables and expansion scheme.

---

# Part VII. What results should you remember?

## 23. The core formulas

### Forward variance

$$
q_{\ell+1}
==========

\sigma_b^2
+
\sigma_w^2
\mathbb E_z
\left[
\phi(\sqrt{q_\ell}z)^2
\right].
$$

Use this to prevent exploding or dying activations.

### Forward correlation

$$
c_{\ell+1}=F(c_\ell),
$$

with

$$
F(c)
====

\frac{
\sigma_b^2
+
\sigma_w^2
\mathbb E[\phi(u)\phi(v)]
}
{q_\star}.
$$

Use this to diagnose ordered versus chaotic representations.

### Edge-of-chaos parameter

$$
\chi
====

\sigma_w^2
\mathbb E_z
\left[
\phi'(\sqrt{q_\star}z)^2
\right].
$$

Ordered if (\chi<1), chaotic if (\chi>1), critical if (\chi=1).

### Backpropagated gradient variance

$$
\tilde q_\ell
\approx
\chi^{L-\ell}
\tilde q_L.
$$

Use this to diagnose vanishing/exploding gradients.

### NTK dynamics

$$
\dot f_t(x)
===========

*

\sum_{\beta}
\Theta_t(x,x_\beta)
\frac{\partial\mathcal L}{\partial f_t(x_\beta)}.
$$

In the infinite-width NTK limit,

$$
\Theta_t=\Theta_0.
$$

For squared loss,

$$
r_t=e^{-\Theta_0 t}r_0.
$$

### Mean-field particle PDE

$$
\partial_t\rho_t
================

\nabla_\theta\cdot
\left(
\rho_t\nabla_\theta
\frac{\delta\mathcal R}{\delta\rho}(\theta)
\right).
$$

For squared loss,

$$
\frac{\delta\mathcal R}{\delta\rho}(\theta)
===========================================

\mathbb E_{(x,y)}
[(f_\rho(x)-y)\sigma_\star(x;\theta)].
$$

### Feature-learning kernel evolution

$$
\dot f_t(x)
===========

*

\mathbb E_{(x',y')}
\left[
H_{\rho_t}(x,x')
(f_t(x')-y')
\right],
$$

where

$$
H_{\rho_t}(x,x')
================

\int
\nabla_\theta\sigma_\star(x;\theta)\cdot
\nabla_\theta\sigma_\star(x';\theta)
\rho_t(d\theta).
$$

NTK is the special case where (H_{\rho_t}\approx H_{\rho_0}).

---

## 24. The conceptual map

The most compact map is:

$$
\begin{array}{c|c|c|c}
\text{Theory} & \text{Order parameter} & \text{Training?} & \text{Feature learning?}\
\hline
\text{Signal propagation} & Q_\ell(x,x') & \text{No} & \text{No}\
\text{NNGP} & K_{\mathrm{NNGP}}(x,x') & \text{Bayesian posterior} & \text{No SGD features}\
\text{NTK} & \Theta_0(x,x') & \text{Yes} & \text{No / lazy}\
\text{Two-layer MF} & \rho_t(\theta) & \text{Yes} & \text{Yes}\
\text{Deep DMFT} & Q(t,t'),\widetilde Q(t,t'),R(t,t') & \text{Yes} & \text{Yes}\
\text{(\mu)P / tensor programs} & coordinate distributions / kernels & \text{Yes} & \text{Yes, by scaling}
\end{array}
$$

The practical diagnostic is:

$$
\text{Does the representation or tangent kernel move by }O(1)?
$$

If no, use NTK/NNGP-style tools. If yes, use mean-field particle dynamics, DMFT, (\mu)P, or finite-width corrections.

---

# Part VIII. How to use MFT as an analysis tool

## 25. A practical workflow

Suppose you have a neural architecture and want to understand it with MFT.

### Step 1: Identify the large parameter

Usually this is width or channel count. For Transformers, it may be (d_{\mathrm{model}}), MLP width, attention head dimension, or a coupled scaling of these.

Ask:

$$
\text{Which dimensions go to infinity, and which remain finite?}
$$

Output dimension, vocabulary size, number of classes, sequence length, and dataset size may or may not scale. The answer changes the theory.

### Step 2: Write the microscopic recurrence

For each layer, write

$$
h^\ell = W^\ell x^{\ell-1}+b^\ell,
\qquad
x^\ell=\phi(h^\ell),
$$

or the corresponding residual/attention/normalization equations.

Do not begin with a kernel. Begin with the computation graph.

### Step 3: Choose the order parameters

At initialization, use

$$
Q_\ell^{\alpha\beta}
====================

\frac1{n_\ell}
h^\ell(x_\alpha)\cdot h^\ell(x_\beta).
$$

For backprop, add

$$
\widetilde Q_\ell^{\alpha\beta}
===============================

\frac1{n_\ell}
\delta^\ell(x_\alpha)\cdot\delta^\ell(x_\beta).
$$

For training with feature learning, add time indices:

$$
Q_\ell^{\alpha\beta}(t,t'),
\qquad
\widetilde Q_\ell^{\alpha\beta}(t,t'),
\qquad
R_\ell^{\alpha\beta}(t,t').
$$

For two-layer mean-field, use the empirical distribution

$$
\rho_t(\theta).
$$

### Step 4: Derive the self-consistency map

At initialization, this is usually a Gaussian integral:

$$
Q_{\ell+1}
==========

\sigma_b^2+\sigma_w^2\mathcal C_\phi(Q_\ell).
$$

For training, it may be a PDE, kernel-evolution equation, or DMFT saddle.

### Step 5: Linearize around the fixed point

This gives stability, depth scales, gradient scales, and phase boundaries. The edge-of-chaos calculation is the archetype:

$$
\chi
====

\sigma_w^2
\mathbb E[\phi'(\sqrt{q_\star}z)^2].
$$

### Step 6: Compare to finite networks

Measure:

$$
q_\ell,\quad c_\ell,\quad
|\Theta_t-\Theta_0|/|\Theta_0|,
\quad
\text{Jacobian singular values},
\quad
\text{activation RMS},
\quad
\text{gradient RMS}.
$$

If the finite network disagrees strongly with the saddle, ask whether the problem is finite width, too much depth, normalization, optimizer effects, data correlations, or being in the wrong parameterization.

---

## 26. What assumptions are doing real work?

The main assumptions are:

**Large width.** Self-averaging requires many channels. Corrections are often (O(1/\sqrt n)) for fluctuations and (O(1/n)) for averaged correlators, though depth and training can amplify them.

**Weak coupling.** The (1/\sqrt n) scaling is not cosmetic; it is what gives (O(1)) fields.

**Exchangeability.** Neurons/channels in a layer should be statistically symmetric at initialization. Convolutions preserve a related channel-exchangeability; attention and normalization require more careful bookkeeping.

**Finite depth, or controlled depth.** If depth grows too fast with width, finite-width corrections accumulate. Criticality and residual scaling are ways to keep depth under control.

**Gaussian or CLT-compatible weights.** Exact Gaussianity is convenient, but finite-variance non-Gaussian weights often yield the same limit by CLT. Heavy-tailed weights can change the story.

**Small-step gradient flow or controlled SGD.** Many training-limit derivations assume gradient flow or infinitesimal learning rate. Discrete learning-rate effects, momentum, Adam, weight decay, and batch noise can change the effective dynamics.

**Parameterization.** This is enormous. NTK, standard, mean-field, and (\mu)P scalings can produce different infinite-width limits.

**Data scaling.** Fixed finite dataset, population loss, and (p,d,n\to\infty) proportional limits are different theories.

---

# Part IX. Where the theory is most trustworthy

## 27. High-confidence uses

I would trust MFT most for:

**Initialization and trainability.** Variance, correlation, gradient propagation, and Jacobian conditioning are exactly what signal-propagation MFT was designed to analyze.

**Kernel baselines.** NNGP and NTK give principled infinite-width baselines. If a trained finite model performs similarly to its NTK/NNGP baseline, feature learning may not be central.

**Scaling comparisons.** (\mu)P and related maximal-update reasoning are directly about how hyperparameters and update sizes behave as width grows.

**Controlled shallow feature learning.** The two-layer mean-field PDE is a real theory of feature learning, not merely a metaphor.

**Diagnosing finite-width effects.** Effective-theory and DMFT fluctuation approaches give a language for when infinite-width predictions fail.

---

## 28. Lower-confidence uses

I would be cautious when using MFT to claim:

**Full explanations of LLM behavior.** Transformers have attention, layer norm, residual streams, optimizer effects, token correlations, and data curricula. MFT can isolate mechanisms, not magically solve the whole system.

**Precise predictions far from the scaling regime.** Width 128 may or may not behave like (n=\infty), especially at large depth.

**Generalization claims without data structure.** Kernel spectra and teacher-student overlaps can predict generalization only after specifying data assumptions.

**Replica-only conclusions without finite-size checks.** Replica calculations can be insightful, but for practical NN analysis they should be paired with simulations or other consistency checks.

---

# Part X. Derivations worth doing yourself

## 29. Derivation 1: edge of chaos

Start from

$$
c_{\ell+1}=F(c_\ell).
$$

Let (c=1-\epsilon). Represent

$$
u=\sqrt{q_\star}z,
\qquad
v=\sqrt{q_\star}
\left[
(1-\epsilon)z+\sqrt{2\epsilon},\xi
\right]
+O(\epsilon^{3/2}).
$$

Expand

$$
\phi(v)
=

\phi(u)
+
\phi'(u)(v-u)
+
\frac12\phi''(u)(v-u)^2+\cdots.
$$

The leading change in covariance gives

$$
1-F(1-\epsilon)
===============

\chi\epsilon+o(\epsilon),
$$

with

$$
\chi
====

\sigma_w^2
\mathbb E[\phi'(\sqrt{q_\star}z)^2].
$$

This derivation makes clear why the squared derivative appears: correlation sensitivity is controlled by how much the nonlinearity amplifies infinitesimal differences.

---

## 30. Derivation 2: gradient explosion/vanishing

Use

$$
\delta_i^\ell
=============

\phi'(h_i^\ell)
\sum_k W_{ki}^{\ell+1}\delta_k^{\ell+1}.
$$

Square and average over (i). Cross terms vanish by independence and zero mean:

$$
\mathbb E[(\delta_i^\ell)^2]
============================

\mathbb E[\phi'(h_i^\ell)^2]
\sum_k
\mathbb E[(W_{ki}^{\ell+1})^2]
\mathbb E[(\delta_k^{\ell+1})^2].
$$

Since

$$
\mathbb E[(W_{ki}^{\ell+1})^2]=\frac{\sigma_w^2}{n_\ell},
$$

and there are (n_{\ell+1}\approx n_\ell) terms,

$$
\tilde q_\ell
=============

\sigma_w^2
\mathbb E[\phi'(h)^2]
\tilde q_{\ell+1}.
$$

At the fixed point, this is

$$
\tilde q_\ell=\chi\tilde q_{\ell+1}.
$$

---

## 31. Derivation 3: NTK dynamics

Let

$$
\mathcal L(\theta)
==================

\sum_\alpha
\ell(f_\theta(x_\alpha),y_\alpha).
$$

Then

$$
\dot\theta
==========

# -\nabla_\theta\mathcal L

-\sum_\beta
\frac{\partial\ell_\beta}{\partial f_\beta}
\nabla_\theta f_\theta(x_\beta).
$$

Therefore

$$
\dot f_\alpha
=============

# \nabla_\theta f_\theta(x_\alpha)\cdot\dot\theta

-\sum_\beta
\underbrace{
\nabla_\theta f_\theta(x_\alpha)\cdot
\nabla_\theta f_\theta(x_\beta)
}*{\Theta*{\alpha\beta}}
\frac{\partial\ell_\beta}{\partial f_\beta}.
$$

That is the NTK equation. The infinite-width theorem adds that (\Theta_{\alpha\beta}) self-averages and stays fixed.

---

## 32. Derivation 4: two-layer Wasserstein PDE

Start with

$$
\rho_N=\frac1N\sum_i\delta_{\theta_i}.
$$

If

$$
\dot\theta_i=-\nabla\Psi(\theta_i;\rho_N),
$$

then

$$
\frac{d}{dt}\int\varphi,d\rho_N
===============================

-\int\nabla\varphi\cdot\nabla\Psi,d\rho_N.
$$

In the limit,

$$
\frac{d}{dt}\int\varphi,d\rho_t
===============================

-\int\nabla\varphi\cdot\nabla\Psi,d\rho_t.
$$

By integration by parts,

$$
\partial_t\rho_t
================

\nabla\cdot(\rho_t\nabla\Psi).
$$

This is the whole derivation. The hard parts in rigorous papers are proving convergence, handling noncompact parameters, controlling SGD noise, and proving global convergence under appropriate assumptions.

---

# Part XI. How I would position the “schools”

## 33. Signal-propagation school

Use this for:

$$
\text{initialization, depth scales, edge of chaos, gradient flow, dynamical isometry.}
$$

Representative results: ordered/chaotic phases, trainability near criticality, NNGP covariance recursions, Jacobian spectra. ([arXiv][3])

This is probably the first MFT tool to teach a physicist entering NN theory.

---

## 34. Kernel / NTK school

Use this for:

$$
\text{solvable training dynamics, spectral bias, kernel baselines, infinite-width lazy training.}
$$

Representative result:

$$
r_t=e^{-\Theta_0t}r_0.
$$

This is mathematically clean and often a good null model. But if your goal is representation learning, treat it as the “non-feature-learning control condition.” ([arXiv][6])

---

## 35. Interacting-particle / Wasserstein mean-field school

Use this for:

$$
\text{two-layer feature learning, particle interpretations, measure-space convexity, PDE training dynamics.}
$$

Representative result:

$$
\partial_t\rho_t
================

\nabla\cdot
\left(
\rho_t\nabla
\frac{\delta\mathcal R}{\delta\rho}
\right).
$$

This is the best pedagogical entry point to feature-learning MFT. ([arXiv][8])

---

## 36. Tensor-program / (\mu)P / deep feature-learning school

Use this for:

$$
\text{deep infinite-width feature learning, scaling rules, hyperparameter transfer.}
$$

Representative principle:

$$
\text{choose scaling so that preactivation updates are }O(1)
\text{ across width.}
$$

This is currently among the most practically relevant mean-field-inspired lines because it connects theory to hyperparameter transfer in large models. ([arXiv][10])

---

## 37. Statphys high-dimensional / replica / DMFT school

Use this for:

$$
\text{teacher-student learning curves, sample complexity, SGD noise, high-dimensional phase diagrams.}
$$

This is closest to classic statistical mechanics, but often farther from arbitrary modern architectures. It is excellent when its assumptions match the phenomenon. ([arXiv][12])

---

# Final synthesis

Mean-field theory for neural networks is not one theory. It is a toolkit organized around one idea:

$$
\boxed{
\text{wide random networks self-average, and their macroscopic behavior is governed by self-consistent order parameters.}
}
$$

At initialization, those order parameters are covariance kernels, giving variance propagation, correlation maps, NNGP priors, and edge-of-chaos criteria.

During lazy training, the order parameter is the NTK, and gradient descent becomes kernel gradient descent.

During two-layer feature learning, the order parameter is the empirical distribution of neurons, and training becomes a Wasserstein gradient flow.

During deep feature learning, the order parameters are time-dependent activation and gradient kernels, leading to dynamical MFT or tensor-program stochastic processes.

The main practical lesson is:

$$
\text{First identify the scaling regime. Then choose the mean-field theory.}
$$

If features do not move, NTK is appropriate. If features move, use mean-field particle dynamics, deep DMFT, (\mu)P/tensor-program limits, or finite-width effective theory. The most useful MFT is not the one with the most elegant limit; it is the one whose order parameters actually move in the same way as the network you are trying to understand.

[1]: https://link.aps.org/doi/10.1103/PhysRevLett.61.259?utm_source=chatgpt.com "Chaos in Random Neural Networks | Phys. Rev. Lett."
[2]: https://glizen.com/radfordneal/ftp/thesis.pdf?utm_source=chatgpt.com "Bayesian learning for neural networks - glizen.com"
[3]: https://arxiv.org/abs/1606.05340?utm_source=chatgpt.com "Exponential expressivity in deep neural networks through transient chaos"
[4]: https://arxiv.org/abs/1711.04735?utm_source=chatgpt.com "Resurrecting the sigmoid in deep learning through dynamical isometry: theory and practice"
[5]: https://arxiv.org/abs/1910.12478?utm_source=chatgpt.com "Tensor Programs I: Wide Feedforward or Recurrent Neural Networks of Any Architecture are Gaussian Processes"
[6]: https://arxiv.org/abs/1806.07572?utm_source=chatgpt.com "Neural Tangent Kernel: Convergence and Generalization in Neural Networks"
[7]: https://arxiv.org/abs/1812.07956?utm_source=chatgpt.com "On Lazy Training in Differentiable Programming"
[8]: https://arxiv.org/abs/1804.06561?utm_source=chatgpt.com "A Mean Field View of the Landscape of Two-Layers Neural Networks"
[9]: https://arxiv.org/abs/2205.09653?utm_source=chatgpt.com "Self-Consistent Dynamical Field Theory of Kernel Evolution in Wide Neural Networks"
[10]: https://arxiv.org/abs/2011.14522?utm_source=chatgpt.com "Feature Learning in Infinite-Width Neural Networks"
[11]: https://arxiv.org/abs/2203.03466?utm_source=chatgpt.com "Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer"
[12]: https://arxiv.org/abs/2006.06098?utm_source=chatgpt.com "Dynamical mean-field theory for stochastic gradient descent in Gaussian mixture classification"
[13]: https://arxiv.org/abs/1909.11304?utm_source=chatgpt.com "Asymptotics of Wide Networks from Feynman Diagrams"


---

*LLM Usage Statement:* Everything below the CRW note at the top was written by GPT5.5-Pro based on its conversation with me.

Conversation: [ChatGPT share link](https://chatgpt.com/share/6a43eb3f-63f0-83eb-9e56-34931eefd62f)
