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

# Neural Generative Models as Priors Over Interaction Terms

Suppose we are studying a generative model

$$
p_\theta(x),
$$

where $x$ is a structured object: a string, an image, a vector of discrete variables, or some other collection of parts. Instead of thinking only about the model's parameters $\theta$, it can be useful to ask what kind of probability distributions those parameters make easy to represent.

A convenient way to do this is to work with the model's **action**:

$$
A_\theta(x)=-\log p_\theta(x).
$$

This puts the model in the same language as statistical physics: the probability of $x$ is high when its action is low. The question then becomes: what kinds of interaction terms does the architecture naturally put into this action?

The basic idea is that a neural-network initialization induces a prior over actions, and therefore a prior over interaction terms. More data then resolves progressively more of those terms. The useful asymptotic statement is not just "higher-order terms need more data." It is more specific:

$$
\boxed{\text{A mode is resolved when } N\eta_r \gtrsim \log M_r.}
$$

Here $N$ is the number of observations, $\eta_r$ measures how visible that mode is under both the model prior and the data geometry, and $M_r$ is the number of comparable modes being searched over. This gives an EFT-like cutoff: with little data, only a few easy directions in action-space are visible; with more data, the cutoff moves into more complex interaction terms.

## 1. From parameters to action-couplings

Choose a basis of functions on data space:

$$
\{\phi_\alpha(x)\}_{\alpha\in\mathcal A}.
$$

The index $\alpha$ can stand for many things: body order, position, feature type, frequency, compositional structure, or any other notion of complexity. For example, if

$$
x=(x_1,\ldots,x_n),
$$

then $\phi_\alpha$ might depend only on a subset $S\subseteq[n]$. In that case $|S|$ is the body order of the interaction.

Now expand the action in this basis:

$$
A_\theta(x)=A_0(x)+\sum_\alpha g_\alpha(\theta)\phi_\alpha(x).
$$

The coefficients

$$
g_\alpha(\theta)
$$

are the model's induced interaction couplings. A neural network does not choose these couplings independently. They are all produced through the same parameter vector $\theta$. So the architecture defines a map

$$
\theta \mapsto g(\theta).
$$

If the initialization is random,

$$
\theta\sim \pi_0,
$$

then this map pushes the initialization forward into a distribution over couplings:

$$
\Pi_0^g = g_\#\pi_0.
$$

This is the architecture's **prior over interaction terms**.

That prior is usually very far from uniform. A neural network does not put equal mass on all possible pairwise, three-way, ten-way, or hundred-way interactions. Instead, it puts mass on the interactions that are easy for its architecture to generate. For a transformer, this likely means interactions that can be built out of embeddings, attention patterns, residual composition, shared weights, and depth. The important point is that some high-body interactions may be cheap, while many low-body interactions may be unnatural if they do not align with the architecture.

So the right notion of complexity is not just body order. It is something more like **architectural relevance**: how easily does the parameterization generate this action-direction?

## 2. Local asymptotics: how the initialization becomes a prior in coupling-space

To see the induced prior more explicitly, look near an initialization point $\theta_0$. For a small parameter displacement $\delta\theta$, expand

$$
g_\alpha(\theta_0+\delta\theta)
=
g_\alpha(\theta_0)
+
\sum_i J_{\alpha i}\delta\theta_i
+
O(\|\delta\theta\|^2),
$$

where

$$
J_{\alpha i}=\frac{\partial g_\alpha}{\partial \theta_i}.
$$

If the initialization is locally Gaussian,

$$
\delta\theta\sim \mathcal N(0,\Sigma_\theta),
$$

then, to first order, the induced prior over couplings is also Gaussian:

$$
g\sim \mathcal N(g_0,C_g),
$$

with

$$
\boxed{C_g=J\Sigma_\theta J^\top.}
$$

This covariance matrix is the local imprint of the architecture in action-space. Directions with large variance are easy for the initialization to produce. Directions with tiny variance are suppressed. Directions outside the range of $J$ are not reachable at first order at all.

This gives a precise version of the intuition that training "slides down stairs." At initialization, some action-directions are already open: the model can move along them with very small parameter changes. Other directions only appear after nonlinear movement in parameter space. Those directions are not impossible, but they are higher-order in the local expansion.

Now add data. Suppose we have $N$ observations. Near a good fit, the likelihood is locally quadratic in the couplings, with Fisher matrix $F$. If the prior over couplings is approximately Gaussian, then the posterior precision is approximately

$$
\boxed{C_g^{-1}+NF.}
$$

The modes that matter are the eigenvectors of

$$
\boxed{C_g^{1/2}FC_g^{1/2}.}
$$

Write

$$
C_g^{1/2}FC_g^{1/2}u_r=\eta_r u_r.
$$

Then $\eta_r$ measures the combined effect of two things:

1. how much prior mass the architecture gives to mode $r$, and
2. how visible that mode is in the data distribution.

The basic resolution criterion is

$$
\boxed{N\eta_r\gtrsim 1.}
$$

If we are scanning many comparable modes, there is a multiple-comparisons or model-selection penalty. If $M_r$ comparable modes are being searched over, the criterion becomes roughly

$$
\boxed{N\eta_r\gtrsim \log M_r.}
$$

Equivalently, the critical sample size for resolving mode $r$ is

$$
\boxed{N_r^{\mathrm{crit}}\sim \frac{\log M_r}{\eta_r}.}
$$

This is the main asymptotic result. It says that a model's effective theory at sample size $N$ consists of the action-modes whose architecture-weighted visibility is above the statistical noise floor.

This also reframes the role of high-order interactions. High-body terms are not automatically inaccessible. A high-body term can be visible with relatively little data if the architecture gives it large prior variance and the data makes it Fisher-visible. Conversely, a low-body term can be hard to resolve if it lies in a direction the architecture strongly suppresses.

A useful scaling notation is

$$
\operatorname{Var}(g_\alpha)\asymp m^{-2\Delta_\alpha},
$$

where $m$ is width or another size parameter. Then

$$
\Delta_\alpha
$$

acts like an architecture-induced relevance dimension. Smaller $\Delta_\alpha$ means the operator is easier; larger $\Delta_\alpha$ means it is more suppressed. The corresponding sample complexity scales like

$$
\boxed{N_\alpha^{\mathrm{crit}}
\sim
\frac{\log M_\alpha}{F_\alpha}\,m^{2\Delta_\alpha}.}
$$

This is the EFT-style power counting: the architecture assigns different scaling dimensions to different interaction operators.

## 3. Infinite-width / mean-field version

In a large-width or mean-field limit, the same idea can often be computed more directly. Randomly initialized networks frequently converge to Gaussian processes in function space. For a generative model, the logits become random functions; the action

$$
A_\theta(x)=-\log p_\theta(x)
$$

therefore becomes a random function too.

For an autoregressive model,

$$
p_\theta(x_{1:T})=\prod_{t=1}^T p_\theta(x_t\mid x_{<t}),
$$

so the action is

$$
A_\theta(x_{1:T})
=
-\sum_{t=1}^T \log p_\theta(x_t\mid x_{<t}).
$$

If the initialized logits have a limiting covariance kernel, then the initialized action has an induced covariance kernel

$$
K_A(x,x')=
\operatorname{Cov}_{\theta\sim\pi_0}
\left[A_\theta(x),A_\theta(x')\right].
$$

Projecting this kernel into the interaction basis gives the prior covariance over couplings:

$$
\boxed{C^g_{\alpha\beta}
=
\langle \phi_\alpha, K_A\phi_\beta\rangle.}
$$

So the mean-field calculation gives the same object as the local parameter calculation:

$$
\text{initialization} \quad\Rightarrow\quad \text{action covariance} \quad\Rightarrow\quad \text{prior over interaction terms}.
$$

Once we have $C_g$, the finite-data cutoff is again governed by

$$
C_g^{1/2}FC_g^{1/2}.
$$

This is the clean bridge between neural-network initialization and an EFT-like description of learned generative models. The architecture supplies the prior covariance over action-operators. The data supplies the Fisher geometry. Their product determines which interactions are statistically resolvable at a given sample size.

In this language, the inductive bias of a transformer is not simply that it prefers low-order terms. A better statement is that it puts prior mass on a structured, sparse family of action directions, some of which may correspond to quite high-order interactions. These high-order terms become learnable when they are both architecturally cheap and statistically visible.

The resulting picture is:

$$
\text{few observations}
\quad\Rightarrow\quad
\text{only high-prior, high-visibility modes are resolved};
$$

$$
\text{more observations}
\quad\Rightarrow\quad
\text{the cutoff moves into weaker or more complex modes}.
$$

That is the sense in which more data lets the model progressively resolve higher-order structure.


---

*LLM Usage Statement:* Everything below the CRW note at the top was written by GPT5.5-Pro based on its conversation with me.

Conversation: [ChatGPT share link](https://chatgpt.com/share/6a43eb3f-63f0-83eb-9e56-34931eefd62f)
