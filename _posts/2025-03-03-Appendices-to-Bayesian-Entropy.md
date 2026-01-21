---
title: Appendices to Bayesian Entropy
date: 2025-03-03
tags: [math, information-theory]
---

# Physics Flavored Appendices to 'Thermodynamics as Approximate Bayesian Inference'
---
This post contains sketches of some ideas I had while working on the post "Thermodynamics as Approximate Bayesian Inference", which were too 'physics-brained' to fit in the main post.  The first section discusses perturbation theory methods in higher-order thermodynamics.  The second presents a simple way to recast the thermodynamic language used in Grandy's "Entropy and the Time Evolution of Macroscopic Systems" in a way that preserves entropy but is still 'first-order' in the moment-matching sense.
## Perturbation Theory and Higher-Order Thermodynamics

As noted, the (first-order) Gibbs distribution is remarkable for the facility with which it allows one to calculate expectation values of observables. This fact is often exploited to perform perturbative calculations, reducing observable calculations in the perturbed system to expansions of expectations in the (first-order) equilibrium system.

Higher orders of the moment-matching expansion may be approximated as perturbations of the first-order Gibbs distribution, with the higher moment terms providing the perturbation.

Consider a system modeled by an unperturbed Hamiltonian $H_0(\omega)$ and a perturbing potential $H_I(\omega)$. The associated Gibbs distribution at order $N$ is

$$
p(\omega) = \frac{ \exp\Biggl(-\sum_{k=0}^N \beta_k\, \Bigl[H_0(\omega) + H_I(\omega)\Bigr]^k \Biggr)}{\int \exp\Biggl(-\sum_{k=0}^N \beta_k\, \Bigl[H_0(\omega) + H_I(\omega)\Bigr]^k \Biggr) d\omega}
$$

Two separate expansions are required—the first with respect to the perturbing potential, and the second with respect to the higher-order moments. Let $O(\omega)$ be an observable; its expectation is

$$
\langle O \rangle_{N} = \int d\omega\, O(\omega)\, p(\omega)
$$

Here, $\langle \cdot \rangle_{k}$ denotes the expectation with respect to the $k$th order Gibbs distribution (to full order in $H_I$), while we reserve $\langle \cdot \rangle_{k,0}$ to mean the expectation with respect to the *unperturbed* $k$th order Gibbs distribution (so $\langle \cdot \rangle_{0,0}$ refers to the traditional first-order unperturbed distribution).

We may develop perturbation expansions as follows:

$$
\begin{aligned}
\langle O \rangle_{N} &= \frac{\Bigl\langle O\, \exp\Bigl[-\sum_{k=1}^N \beta_k\Bigl((H_0 + H_I)^k - H_0^k\Bigr)\Bigr]\Bigr\rangle_{N,0}}{\Bigl\langle \exp\Bigl[-\sum_{k=1}^N \beta_k\Bigl((H_0 + H_I)^k - H_0^k\Bigr)\Bigr]\Bigr\rangle_{N,0}}\\[1ex]
\langle O \rangle_{N} &= \frac{\Bigl\langle O\, \exp\Bigl[\beta_1 H_0 - \sum_{k=1}^N \beta_k\Bigl((H_0 + H_I)^k\Bigr)\Bigr]\Bigr\rangle_{0,0}}{\Bigl\langle \exp\Bigl[\beta_1 H_0 - \sum_{k=1}^N \beta_k\Bigl((H_0 + H_I)^k\Bigr)\Bigr]\Bigr\rangle_{0,0}}
\end{aligned}
$$

The first equation is useful if an analytic or otherwise tractable form of the $N$th order Gibbs distribution is available (e.g., if it is the delta distribution corresponding to an exactly constrained total energy in the absence of interactions), while the second describes the expectation with respect to the traditional first-order Gibbs distribution of thermal equilibrium. Perturbation expansions may then be carried out by Taylor expanding the exponentials; as in traditional field theory, a diagrammatic expansion of the numerator and denominator implies that the answer can be taken as the sum over connected diagrams only.

---

## Information-Preserving First-Order Thermodynamics

Grandy develops time-dependent thermodynamics by considering constraints that fix the expected value of an observable $F$ at the time when the time-dependent distribution $\rho_t$ is calculated, namely $\langle F(t) \rangle_t$. This yields

$$
\rho_t = \frac{1}{Z_t}\exp\Biggl(-\beta H - \int_0^t \lambda(t')\, F(t')\, dt'\Biggr)
$$

At each time $t$, the Lagrange multiplier $\lambda(t)$ is set to fix

$$
\langle F(t) \rangle_t = \operatorname{Tr}\Bigl(\rho_t F(t)\Bigr) = - \left[ \frac{\delta}{\delta \lambda(t)} \ln Z_t \right]_{\lambda(t)=\lambda^*(t)}
$$

While this method allows one to develop a time-dependent thermodynamics, the procedure is not consistent; although it fixes the expectation values $\langle F(t')\rangle_{t'}$ at the time of measurement, these values are not constrained at later times—i.e., $\langle F(t')\rangle_t \neq \langle F(t')\rangle_{t'}$ even after constraining $F(t')$ by measurement.

This issue can be remedied within first-order thermodynamics by replacing $\lambda(t')$ with $\lambda_t(t')$; then, at each time $t$, the entire set of Lagrange multipliers must be redetermined. One then has

$$
\rho_t = \frac{1}{Z_t}\exp\Biggl(-\beta H - \int_0^t \lambda_t(t')\, F(t')\, dt'\Biggr)
$$

with the multipliers determined by requiring

$$
\langle F(t')\rangle_t = - \left[ \frac{\delta}{\delta \lambda_t(t')}\ln Z_t \right]_{\lambda_t=\lambda^*_t} \quad \forall\, 0\le t'\le t
$$

That is, the multipliers are now determined by a *functional* equation rather than a single nonlinear equation. This adds considerable complexity; moreover, the common short-memory approximation (i.e., that system correlations decay rapidly) suggests that constraining information from far in the past is irrelevant. Nonetheless, in discussions of apparent irreversibilities it is important to acknowledge that such approximations entail the discarding of information.

The entropy of the system is then given by

$$
\frac{1}{k} S_t = \ln Z_t - \beta \langle H \rangle_t - \int_0^t \lambda_t(t')\, \langle F(t')\rangle_t \, dt'
$$

It may be observed that the time derivative of the density matrix (i.e. the change in the density matrix due solely to changes in the information used to construct it, rather than due to unitary time evolution) satisfies

$$
\partial_t \rho_t = \rho_t \Biggl[ \int_0^t \partial_t \lambda_t(t')\, \Bigl(\overline{F(t')} - \langle F(t')\rangle_t\Bigr)\, dt' + \lambda_t(t)\,\Bigl(\overline{F(t)}-\langle F(t)\rangle_t\Bigr) \Biggr]
$$

where the overbar denotes the generalized Kubo transform of the operator (taken with respect to $\ln \rho_t$). The time derivative of an operator's expectation can be written as

$$
\frac{d}{dt}\langle C(t)\rangle_t = \langle \dot{C}(t)\rangle_t + \lambda_t(t)\, K_{CF}^t(t,t) + \int_0^t \partial_t \lambda_t(t')\, K_{CF}^t(t',t) \, dt'
$$

which in turn leads to the definition of the source $\sigma_C(t)$ (heuristically, the extent to which the expectation of $C$ changes due to the updating of the density matrix):

$$
\sigma_C(t) = \frac{d}{dt}\langle C(t)\rangle_t - \langle \dot{C}(t)\rangle_t = \lambda_t(t)\, K_{CF}^t(t,t) + \int_0^t \partial_t \lambda_t(t')\, K_{CF}^t(t',t) \, dt'
$$
