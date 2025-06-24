---
title: "Bayesian Entropy"
date: "2025-03-03"
---

# Thermodynamics as Approximate Bayesian Inference


## Abstract

In this paper, I illustrate that the branches of physics known as thermodynamics and statistical mechanics may be understood in their entirety as a first-order moment-matching approximation to Bayesian inference. This insight is developed by the extension of the approximation to higher orders, along with a demonstration of the asymptotic correctness of this approximation for a large class of problems. We go on to suggest a framework for generalizations of the Gibbs ensemble for use in various state-inference problems. Finally, we discuss the relationship between the thermodynamic entropy and the information-theoretic entropy in this higher-order thermodynamics.

---

## Recapitulation of the Derivation of Statistical Mechanics from the Principle of Maximum Entropy

We consider a physical system, say an ideal adiabatically isolated box full of classical, distinguishable gas molecules. Assuming for now that (somehow) one has certain knowledge of the nature of the degrees of freedom therein, we may perfectly describe the state of the system by specifying a point in the phase-space of $N$ particles, 
$$
\Omega = \mathbb{R}^{6N},
$$
where $\Omega$ will be our general notation for the set of all microstates of the system under consideration. Suppose now that an observer were to know, initially, nothing of the state of this system; such an observer might express their uncertainty over the state of the system in the form of a probability distribution over the set of all possible microstates, i.e., an element 
$$
p_0 \in \Delta \Omega,
$$
with $\Delta$ indicating the space of probability distributions over the set corresponding to the symbol on its right.

If the observer is then to make a measurement of some observable of the system—say, by obtaining the value of a function 
$$
f : \Omega \rightarrow \mathbb{R}
$$
to be equal to $F$ (with $F$ the observed value of the measurement)—then naturally some new probability distribution in $\Delta \Omega$ should be selected which reflects this information (states inconsistent with measuring $F$ should be decreased in probability). The theory of statistical mechanics revolves around incorporating such information about the system in order to "update" one's uncertainty probability distribution over the state of the system, on the basis of this new information. (We note up front that here we consider "measurements" which do not impact the state of the system—partly because we wish to elide the distinction between information obtained by measurement and information *posited* about a system; an adequate theory of quantum measurements in the service of information theory and control may be found in texts on quantum control theory.)

Statistical mechanics typically uses such information about the state to construct a probability distribution on the basis of Gibbs' "Principle of Maximum Entropy" – prescribing that, given such an observation, one's updated probability distribution should be that which has the maximum information–entropy while still satisfying the constraint that the expected value of the measurement $f$ over the constructed probability distribution is equal to the observed value $F$. Mathematically, the prescribed $p$ is that which (uniquely, by theorem) solves the following optimization problem:

$$
\begin{aligned}
\max_{p \in \Delta \Omega} \quad & -\sum_{\omega \in \Omega} p(\omega) \ln p(\omega)\\
\textrm{s.t.} \quad & \mathbb{E}_{\omega \sim p}[f(\omega)] = F
\end{aligned}
$$

The objective function is the *information* entropy of a probability distribution, which we write as $S_I[p]$.

The solution, proceeding by the method of Lagrange multipliers, gives the family of distributions:

$$
\begin{aligned}
p(\omega; \lambda) &= \frac{1}{Z(\lambda)} \exp\Bigl(-\lambda_f\, f(\omega)\Bigr)\\[0.5ex]
Z(\lambda) &= \sum_{\omega \in \Omega} \exp\Bigl(-\lambda_f\, f(\omega)\Bigr)
\end{aligned}
$$

For different values of $\lambda_f$, this distribution corresponds to a solution for different observed values $F$. The solution to the problem is that $\lambda_f$ which causes $f$ to take the expectation value $F$; we denote this choice by $\lambda^*_f(F)$. In some cases, it is profitable to consider the Lagrange multiplier to be the independent value whose specification in turn determines a corresponding value for $F$; we say $\lambda_f$ and $F$ (not $f$ the function) are "conjugate."

Applying this principle to the energy of some system—where $f$ is the total energy $E(\omega)$ of the microstate and its conjugate $\lambda_E$ is the inverse temperature—yields the Gibbs distribution for the microcanonical ensemble:

$$
p(\omega) = \frac{1}{Z}\exp\Bigl(-\lambda_E\, E(\omega)\Bigr)
$$

Here, the parameter $\lambda_E$ is the inverse temperature of the system; indeed, taking this to be the *definition* of temperature is appealing. We note that temperature is (1) not a property of the *physical* system, but instead a parameter describing our probability distribution over it, and (2) not all such probability distributions may be described by a temperature—for example, any system whose exact microstate is known (if this state is not a ground state) is, naively, indescribable in this way.

Now we seek to connect this formulation with Bayesian probability theory.

---

### Incorporating Prior Distributions

If we wish to consider a prior probability distribution $p_0$ and use a slightly modified version of the Principle of Maximum Entropy (PME) to construct the updated distribution by maximizing the *relative* entropy of the new distribution with respect to the old, we have

$$
\begin{aligned}
\max_{p \in \Delta \Omega} \quad & -\sum_{\omega \in \Omega} p(\omega) \ln \frac{p(\omega)}{p_0(\omega)}\\
\textrm{s.t.} \quad & \mathbb{E}_{\omega \sim p}[f(\omega)] = F
\end{aligned}
$$

This yields

$$
p_{\mathrm{PME}}(\omega | F) = \frac{p_0(\omega)}{Z_f}\exp\Bigl(-\lambda_f\, f(\omega)\Bigr)
$$

It may be verified that this update rule is consistent (updating on one observation and then updating on a second is equivalent to updating on both at once). In fact, this update procedure is a useful generalization of Bayes' rule to allow for more general types of constraints; for details see the post sequence on Geometric Rationality by Garrabrant. Further, note that the objective function with the prior corresponds to
$$
-D_{KL}(p\parallel p_0) = H(p) - H(p,p_0)
$$
(i.e., to minimizing the relative entropy of the posterior from the prior, or equivalently maximizing the difference between the distribution's entropy and its cross-entropy with the prior).

For the remainder of this work, we shall refer to the "principle of maximum entropy with expectation constraints" (PMEEC)—that is, the principle of maximum entropy *as it is generally employed in classical thermodynamics*, with constraints only on observables' *expectations*.

---

## PME Updating Is Non-Bayesian

Bayes' rule for updating a probability distribution $p(\omega)$ upon observing $F$ may be written as

$$
p(\omega | F) = \frac{p(F | \omega)\,p(\omega)}{p(F)}
$$

However, supposing we perform a measurement of the system, it is conceptually incorrect to update on that measurement yielding the given value $F$ *in expectation*. For example, if one observes that the sky is blue, it would be foolish merely to *decrease* your estimated probability that it is in fact green—the probability should go all the way to zero (ignoring any possibility of misperception).

If one observes that the observable $f(\omega)$ takes a particular value $F$, states for which $f(\omega) \neq F$ must be updated to probability zero, while states which yield the requisite measurement have their probabilities increased uniformly (in proportion to their prior weight).

The distribution constructed from the PME with expectation constraints (hereafter "Gibbs distributions" constructed with respect to a particular set of measurements) does not fully incorporate the information from the observation.

Of course, classical thermodynamics has achieved enormous practical success in the prediction of physical phenomena; in what follows, we will show that classical thermodynamics is, in a certain sense, a first-order approximation to Bayesian updating. We will then develop this approximation for higher orders in a physical context.

---

### The Principle of Maximum Entropy with Expectation Constraints Is the First-Order Moment-Matching Approximation to Bayesian Inference

For ease of comparison, we may write the PMEEC and the correct Bayesian distribution as solutions of the following optimization problems:

$$
\begin{aligned}
\text{PMEEC:} \quad
& \max_{p \in \Delta \Omega} \quad -D_{KL}(p \parallel p_0)\\[0.5ex]
& \textrm{s.t.} \quad \mathbb{E}_{\omega \sim p}[f(\omega)] = F\\[2ex]
\end{aligned}
\qquad
\begin{aligned}
\text{Bayes:} \quad
& \max_{p \in \Delta \Omega} \quad -D_{KL}(p \parallel p_0)\\[0.5ex]
& \textrm{s.t.} \quad p(f(\omega)=F) = 1
\end{aligned}
$$

We see that PMEEC corresponds to a similar update procedure as the Bayesian update, except that only the first moment of the induced distribution $p(f(\omega))$ is constrained, rather than the entire distribution.

In fact, requiring the observation to occur with probability one is equivalent to requiring the induced distribution to be a delta function, which in turn implies that the $n$th moment equals the first moment raised to the $n$th power:

$$
p(f(\omega)=F) \propto \delta \Bigl(f(\omega) - F\Bigr)
\quad\leftrightarrow\quad
\mathbb{E}[f^n] = \bigl(\mathbb{E}[f]\bigr)^n \quad \forall\, n\in \mathbb{Z}^+
$$

(moment-matching is necessary but not sufficient in general to prove the equality of two distributions on an infinite interval.)

It is clear that classical thermodynamics offers great computational facility—and equally clear that this comes at the cost of information loss relative to the correct Bayesian updates (we will later discuss this lost information in the context of the Second Law).

We may construct a hierarchy of "higher-order" thermodynamics corresponding to increasingly strict constraints on the induced-distribution moments. We will call the "$N$th order Gibbs distribution" the solution to the problem

$$
\begin{aligned}
\max_{p \in \Delta \Omega} \quad & -D_{KL}(p \parallel p_0)\\[0.5ex]
\textrm{s.t.} \quad & \mathbb{E}_{\omega \sim p}[f^n(\omega)] = F^n \quad \text{for } n=0,\dots,N
\end{aligned}
$$

In terms of the traditional Lagrange multipliers, this yields the distribution

$$
p_N(\omega | f(\omega)=F) = \frac{1}{Z_N} \exp\Biggl(-\sum_{n=1}^N \lambda_n\, \bigl(f(\omega)\bigr)^n\Biggr)
$$

with $Z_N$ the appropriate normalization constant.

As an example, consider a measurement $f$ which takes discrete values $f_i$ for $i=1,\dots,M$ (though the state space need not be discrete). The form of the constraint is given by a Vandermonde matrix whose rank determines the number of moments necessary to achieve the delta function; let $p_i$ correspond to the probability of being in the subspace yielding measurement $f_i$ (with $p_i$ uniformly distributed over all states within that subspace). Then the constraint at order $N$ takes the form

$$
\begin{bmatrix} 
f_1 & \dots  & f_M\\[0.5ex]
\vdots & \ddots & \vdots\\[0.5ex]
f_1^N & \dots  & f_M^N 
\end{bmatrix}
\begin{bmatrix} 
p_1\\[0.5ex]
\vdots \\[0.5ex]
p_M 
\end{bmatrix}
=
\begin{bmatrix} 
F^1\\[0.5ex]
\vdots \\[0.5ex]
F^N 
\end{bmatrix}
$$

Since (by assumption) the $f_i$ are all distinct, the rank of the Vandermonde matrix is $\min(N,M)$; that is, specifying as many moments as there are distinct measurements suffices to yield the requisite delta-function distribution. Thus, for a discrete observable that can take $M$ distinct values, $M$th order thermodynamics is exactly equivalent to Bayesian updating!

Further, for an observable with a discrete spectrum having infinitely many distinct values, the $N$th order Gibbs distribution will be an approximation to the correct Bayesian update for all finite $N$. We leave to future work the more mathematically delicate question of continuous-spectrum observables.

---

## In Defence of PMEEC

That Bayes' rule should be the "gold standard" against which any update rule is measured is evidenced by consistency theorems (e.g., von Neumann–Morgenstern or Dutch–Book) and by noting that adherence to Bayes is a defining property of probability distributions.

### The Thermodynamic Limit

Thermodynamics simplifies physics by considering large-$N$ limits. We might ask whether such a limit justifies using the PMEEC instead of the full Bayesian calculation. Suppose we can define the state space $\Omega(N)$ and some observable $E$ that is well defined in the large-$N$ limit. If the error is quantified using the KL divergence, the error will typically be infinite for continuous observables (since the PMEEC will generally assign some probability density over the whole space, whereas the Bayesian distribution must be a delta function on the "true" manifold—almost all of the PMEEC mass will lie in regions where the Bayesian distribution is zero). Assuming the system is discrete, we calculate (with $p_B$ the Bayesian and $p_G$ the Gibbs distribution, using uniform priors for both):

$$
D_{KL}(p_{B}\parallel p_{G}) = \beta E_0 + \ln\!\left[\frac{\sum_{\omega} e^{-\beta E(\omega)}}{|E_N^{-1}(E_0)|}\right] = -(F_N-E_0)\beta - \ln|E_N^{-1}(E_0)| = S_G - S_B
$$

The final form shows that the divergence is the difference in the two entropies—and since $S_G$ maximizes the entropy subject to a looser constraint than $S_B$, this difference is nonnegative.

As for large-$N$ behavior, the free energy $F_N$ can be broken down into volumetric, surface, etc. terms (i.e., the component of $F$ that converges when divided by $N$, the component that converges when divided by $N^{1-1/d}$, etc.). Thus, we may write an asymptotic series for $F$ approximately as

$$
F \sim \sum_{n\leq d} f_n\, N^{1-\frac{n}{d}},
$$

(in principle, this series need not terminate, though that would be a pathological case). Different observables $E$ will have inverse images scaling differently with $N$—most observables of interest will be exponential or superexponential in $N$ (perhaps due to combinatorially many ways of arranging a given number of particles in various states), but other behaviors are possible.

This analysis is somewhat an artifact of using the KL divergence. A better analysis might involve calculating the "Earth-Mover Distance," but lacking a simple method for that here, I offer a hackier criterion: the corrections are plausibly unimportant if the Gibbs distribution converges to the Bayesian distribution blurred by a Gaussian with variance $\epsilon>0$ (i.e., take the $N$ limit for fixed $\epsilon$, and then see if the KL distance goes to zero as $\epsilon$ does):

$$
e^{-\beta E + \ln g_N(E)} \rightarrow e^{-\frac{1}{2}\left(\frac{E-E_0}{\epsilon}\right)^2}
$$

where $g_N$ is the density of states.

### Implementing Measurement Noise Need Not Yield a Gibbs Distribution

Another possible reason to prefer PMEEC over full Bayesian updating is that measurements might be noisy, so a "gentler" update is appropriate. Here we discuss how this works—and how it might not.

We have so far assumed that all measurements of the system are ideal; now, let us relax that assumption to allow for "noisy" measurements. (Note that measurements which are "coarse" in the sense of mapping many possible microstates to a single observed value—for example, the energy of a many-particle system—can be conceptually handled without explicit noise.)

Suppose that a measurement of the observable $f(\omega)$ is drawn according to a probability distribution $p(m_f | f(\omega))$. Assume for simplicity that the measurement distribution may vary depending on $f$ but not directly on the microstate $\omega$, and that the observed value is $M_f$. The Bayesian update prescription is no different than before; it may be formulated as an (unconstrained) optimization problem:

$$
\max_{p \in \Delta \Omega} \quad \Bigl\{-D_{KL}(p\parallel p_0) + \mathbb{E}_p\bigl[\ln p(M_f | \omega)\bigr]\Bigr\}
$$

That is, the Bayes posterior maximizes the difference between the expected log-likelihood of the measurement and the relative entropy (with respect to the prior).

One might inquire whether there exists a simple measurement–error profile that naturally entails the PMEEC approximation—that is, whether there exists a $p(m|\omega)$ such that the Bayes posterior given the noisy measurement value equals the Gibbs distribution for the observable measured with no error:

$$
\frac{e^{-\lambda(m_f) f(\omega)}}{Z(m_f)} = p(\omega | m_f) = \frac{p(m_f|f(\omega))\, p(\omega)}{p(m_f)}
$$

Then (assuming, for simplicity, a uniform prior),

$$
p(m_f | f(\omega)) = \frac{e^{-\lambda(m_f)[f(\omega) - m_f]}}{\tilde{Z}(m_f)}
$$

That is, for fixed $m_f$, the measurement noise is a decaying exponential in the signed distance from $f(\omega)$. The behavior as $m_f$ varies is complex, and it is not clear what to make of it, if anything.

In the moment-matching approximation, we impose the constraint that the induced distribution on $f$ of the new distribution must match the $N$th moment of the Bayesian distribution. The $N$th order approximation is derived from the optimization problem:

$$
\begin{aligned}
\max_{p \in \Delta \Omega} \quad & -D_{KL}(p\parallel p_0)\\
\textrm{s.t.} \quad & \mathbb{E}_{\omega \sim p}\Bigl[f(\omega)^n\Bigr] = \int d\omega\, \frac{p(M_f | f(\omega))\, p_0(\omega)}{p_0(M_f)}\, f(\omega)^n \quad \text{for } n=0,\dots,N
\end{aligned}
$$

Once the measurement is noisy, the constraining data need no longer be the powers of the mean $F$. For $f$ with a discrete spectrum, the argument above—that only as many moments as there are distinct values of $f$ need to be specified in order to derive the exact Bayes posterior—still holds.

---

## Example Derivation of Second-Order Maxwell–Boltzmann Velocity Distribution

Consider a classical ideal gas as is traditionally used to derive the Maxwell–Boltzmann distribution. We seek the probability distribution function that predicts the energy of each particle:

$$
Z = \int \exp\Biggl[ -\sum_{k=0}^N \beta_k\, E^k(\omega) \Biggr]\, d\omega
$$

Because the $\beta_k$ are nonnegative (arising from their origin as Lagrange multipliers), the exponent is strictly negative and strictly decreasing. Determining the $\beta_k$ given the required expectation value of $E$ is clearly nontrivial in general; nonetheless, observables may be computed—as in the traditional theory—by examining derivatives of the log-partition function $Z$.

The first problem is that even for an ideal gas (with no interactions), the partition function no longer factorizes into a product of single-particle partition functions—it now incorporates correlations between the particles. (For example, $E^2(\omega) = \Bigl[\sum_i E(\omega_i)\Bigr]^2$ is not linear in the energies of individual particles.) The velocity distribution becomes

$$
Z_N(\beta_1,\beta_2) = \int \Biggl(\prod_i d^3\vec{v}_i\Biggr) \exp\Biggl[-\beta_1 \sum_i v_i^2 - \beta_2 \Bigl(\sum_i v_i^2\Bigr)^2 \Biggr] = \frac{S_{3N-1}}{2} \int_0^\infty dX\, X^{\frac{3}{2}N - 1} e^{-\beta_1 X - \beta_2 X^2}
$$

where 
$$
S_d = \frac{2\pi^{d/2}}{\Gamma(d/2)}
$$
is the surface area of a unit sphere in $d$ dimensions, and $N$ is the number of particles.

---

## Higher Order Gibbs-Distributions Are Not Separable

Consider a gas of classical non-interacting particles. We are often interested in "extensive" quantities; let us denote such a quantity by $E(\omega)$, satisfying

$$
E(\omega) = \sum_i E(\omega_i)
$$

where $i$ indexes the subsystems (or particles) of the system, with a total of $N$ subsystems. The first-order Gibbs distribution is

$$
\begin{aligned}
p(\omega_1,\dots,\omega_N) &= \frac{1}{Z}\exp\Bigl[-\sum_i \lambda\, E(\omega_i)\Bigr] \\
&= \prod_i \frac{e^{-\lambda\, E(\omega_i)}}{Z_i} = \prod_i p_i(\omega_i)
\end{aligned}
$$

i.e. the probability distribution for each subsystem is *independent* of the others. The second-order Gibbs distribution is given by

$$
p(\omega_1,\dots,\omega_N) = \frac{1}{Z}\exp\Bigl[-\sum_i \lambda_1\, E(\omega_i) - \lambda_2\, \Bigl(\sum_i E(\omega_i)\Bigr)^2\Bigr]
$$

It is clear upon inspection that this distribution does not factor into a product of independent distributions—in fact, it introduces a nonlocal "interaction" between each pair of subsystems (which is purely inferential in nature, not physical).

For example, suppose a system consisting of 3 particles is known to have 8 total quanta of energy; if the first two particles have 2 and 4 quanta respectively, then the number of quanta assigned to the third particle cannot be independent of this information!

With this in mind, one might ask if there is a sense in which the first-order Gibbs distribution is optimal—that is, optimal among distributions that factor into independent marginals. Such an optimal distribution would solve

$$
\begin{aligned}
\min_{p \in \Delta \Omega} \quad & D_{KL}(p_B \parallel p)\\
\textrm{s.t.} \quad & p(\omega_1,\dots,\omega_N) = p_1(\omega_1) \cdots p_N(\omega_N) \quad \forall\,\omega_1,\dots,\omega_N
\end{aligned}
$$

where the equality constraint means that there exist marginal distributions $p_1,\dots,p_N$ and $p_B$ is the correct Bayesian distribution.

---

## The Second Law and Its Discontents

The second law is a cornerstone of modern physics. Grandy provides an enlightening treatment of entropy and possible caveats to the second law, which was one inspiration for the ideas in this paper. Here we offer our own perspective, with additional remarks on Landauer's limit.

For deterministic classical systems, Bayesian updating on observations does not increase the entropy. Thus, if one defines a time-dependent entropy as the entropy of the probability distribution generated from continuous-time updating (in Grandy's treatment using the PMEEC—albeit with modifications to discard certain information in order to recover the classical rules of thermodynamics), one obtains a model where measurements taken at discrete times update the probability distribution over the initial microstate.

Specifically, define

$$
\begin{aligned}
S_t = \max_{p \in \Delta \Omega} \quad & S_I[p]\\
\textrm{s.t.} \quad & p(O_i(\omega)=o_i) = 1 \quad \text{for } i=0,\dots,t
\end{aligned}
$$

for observables $O_i$ measured to have value $o_i$. In this model, $S_t$ is nondecreasing in $t$ and will decrease whenever a measurement places nontrivial constraints on the microstates. This is in contradiction to the empirically valid second law. We now turn to a discussion of Landauer's limit to understand this divergence.

Landauer's limit is a hypothetical bound on the amount of heat created during irreversible computation at a given temperature $T$, viz.

$$
\Delta Q \geq \beta^{-1} \ln 2
$$

The argument is roughly as follows: during computation, a bit register must change state; if this change is irreversible—so that information about the previous state cannot be inferred from the current state—then (by classical determinism) the lost information must be ejected into the environment. This transfer of information increases the entropy of our probability distribution over the environment, corresponding to at least one bit of heat. (If computations are reversible, as in some cases in quantum computing, this limit does not apply. Likewise, if one keeps an updated probability distribution over the environment, the limit may not apply.) Thus, Landauer's limit is not a fundamental law of nature but an implication of a particular model of how an observer stores and discards data about the environment and system.

To illustrate this, note that in the Landauer example the observer has complete knowledge of the computer system and uses a single parameter (the temperature $\beta$) to describe the probability distribution over the environment. When the state of the computer changes, this information alters the distribution—effectively updating to a new temperature $\beta'$ (assuming some prior knowledge of the environment's thermal properties implicit in its microstate structure). This represents a "project–evolve–project" motif: the environment's state is projected onto a manifold of probability distributions parameterized by $\beta$ and then parallel transported along that manifold by the dynamics of the combined system and environment.

Now, consider a generalization where the observer models the system with a vector of parameters $\beta$. Suppose we have $\omega_t = (\omega_{S,t}, \omega_{E,t})$ evolving deterministically. Assume the observer "knows" the microstate $\omega_{S,t}$ and maintains a model of the marginal $p_E(\omega_{E,t}; \beta_t)$, where $\beta_t$ is updated at each time step. The observer is then to "forget" the microstate $\omega_{S,t}$ upon learning the new state $\omega_{S,t+1}$, with a brief overlap where both states are known so that $\beta_t$ can be updated optimally. The new distribution should minimize

$$
D_{KL}\Bigl(p(\omega_{E,t+1} |\beta_{t}, \omega_{S,t}) \,\parallel\, p_E(\omega_{E,t+1}; \beta_{t+1})\Bigr)
$$

Or one might reference the globally optimal distribution $p(\omega_{E,t+1} | \{\omega_S\}_{t'\le t})$. Thus, one seeks

$$
\min_{\beta_{t+1} } \quad \int d\omega_{E,t+1}\, p(\omega_{E,t+1} | \beta_t, \omega_{S,t}) \ln p(\omega_{E,t+1} | \beta_{t+1})
$$

If we define $p(\omega_{E,t+1} | \beta_t, \omega_{S,t})$ as equal to $p(\omega_{E,t}|\beta_t)$ if there exists an $\omega_{S,t+1}$ such that $(\omega_{S,t},\omega_{E,t})$ evolves to $(\omega_{S,t+1}, \omega_{E,t+1})$, and 0 otherwise, then the change in entropy is given by $D_{KL}(\beta_{t+1} \parallel \beta_t)$.

In the case where $\beta$ is a complete parameterization of $\Delta \Omega_E$, the entropy is zero and $\beta$ updates solely to reflect time evolution.

Finally, we can discuss the geometric interpretation of the entropy: the distributions parameterized by $\beta$ form a submanifold $B$ of $\Delta \Omega$.  Projection onto $B$ is uniquely defined for any distribution in $\Delta \Omega$ by calculating the expectations of the observables conjugate to $\beta$, and then solving the corresponding constrained entropy maximization problem.  Eliding the parameters $\beta$ and the distribution they determine, this is

$$
proj_B(\omega) = argmin_\beta ~ D_{KL}(\omega || \beta) \newline \\
s.t. \mathbb{E}_{{\beta}}[O_i] = \mathbb{E}_{\omega}[O_i]
$$

The entropy $S$ is a scalar function on $\Delta \Omega$, and the system evolves under a Hamiltonian $H$ which induces a Liouville operator $L$ on $\Delta \Omega$. A point $p$ in $\Delta \Omega$ is evolved by $L$ along a path where $S$ is constant (since no information is lost under deterministic, reversible evolution, courtesy of Liouville's theorem). On $B$ however, $L$ induces an effective evolution $L_B = P_B L$ on the manifold $B$ (where $P_B$ is the projection operator from the tangent bundle $T\Delta \Omega$ to $TB$); in general, $L_B$ does not move along iso-entropy lines. In other words, the time derivative of the entropy along $L_B$ is

$$
\frac{d}{dt} S(\beta) = \nabla_{L_B} S = \mathcal{I}_B\bigl(P_B \nabla S,\, P_B L\bigr)
$$

with $\mathcal{I}$ denoting the Fisher metric (which defines the inner product on $TB$).   This perspective should not mislead one to understand that projection onto $B$ commutes with $L$ - the above formula applies only locally near $B$.

As an alternative perspective, we can understand $\Delta \Omega$ as a product space of $B$ and some fiber space which we'll denote $F$ - then we may write a point $\omega = (\beta, \phi)$.  The thermodynamic entropy is the partial maximization of the information entropy $S_T(\beta) = max_\phi S_I(\beta,\phi)$.  This is a globally valid definition, but it doesn't give us a canonical relationship between the "ambient evolution" in $\Delta \Omega$ and the evolution in $B$ - changing the 'irrelevant' $\phi$ isn't guaranteed to leave anything fixed.

Insofar as the above doesn't use any characteristic properties of the entropy, something must be missing.  Most importantly, we have not yet endowed the information entropy with any connection to "counting microstates".  There is nothing mysterious about this: the thermodynamic manifold $B$ has no particular dynamical or information-theoretical significance, and a 'true Bayesian' would pay it no mind - the magic of thermodynamics is that it deals only with systems where a 'concentration of measure' principle holds.  This condition, heuristically, amounts to an assertion that with high probability, the distribution $(\beta,\phi)$ will behave identically independent of $\phi$.  Because we started out considering distributions instead of microstates, however, this requirement appears much more idiosyncratic - there is no reason to expect it to be true in general, and it seems difficult to even characterize when it ought to hold (beyond the simple case where decomposition into subsystems is possible); this I think is a good thing, because it hints right away that thermodynamics working is a blessing granted, not a promise fulfilled - there is no reason to expect any form of this strategy to work on a generic high-dimensional system.

Note also the critical role played by the parameter $\beta$ : entropy is "generated" only to the extent that reduced dynamics on $B$ cannot replicate those on $\Delta \Omega$.  If $\beta$ is allowed to encompass a complete set of observables on the phase space such that $B = \Delta\Omega$ , there can be no entropy generation.  Landauer's principle is revealed quite clearly to be a matter only of storage.  One may go so far as to hunt for the observables which encode the most information about the system in expectation:
$$
\mathcal{O}^* = argmin_{\mathcal{O} ~:~ \Omega \rightarrow \mathbb{R}^n} \int_{\omega \in  \Delta \Omega} d \omega ~ S[proj_{\mathcal{O}}(\omega)]
$$