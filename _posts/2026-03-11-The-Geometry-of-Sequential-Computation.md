---
title: "The Geometry of Sequential Computation"
date: 2026-03-10
math: true
---

*Research notes in progress, developed at MATS 9.0 under the mentorship of Richard Ngo.  The mathematical content is established -- operator theory, realization theory, functional analysis -- and the synthesis is mine.  I'm sharing this for feedback and to find collaborators, not to announce results.*

---

## 1. The problem

A Turing machine gives you a concrete, inspectable state: the tape.  At every step, you can look at the tape and see what the machine is working with.  But this description is not canonical -- two Turing machines computing the same function can have wildly different tape contents at intermediate steps, using different alphabets, different numbers of tapes, different usage patterns.  A bubble sort and a merge sort computing the same permutation have tapes that look nothing alike.  The tape tells you what *this particular machine* is doing, not what *the computation* is doing.

For discrete computation, this is annoying but manageable -- you have other tools (complexity classes, circuit lower bounds) to reason about computation abstractly.  For sequential computation in continuous spaces, the problem is worse.  A transformer processes a sequence through layers, each updating a residual stream $x_l \in \mathbb{R}^{n \times d}$.  An SSM maintains a continuous state.  An RNN has hidden states.  We can inspect these -- but what are we looking at?  The residual stream of GPT at layer 7 and the residual stream of Qwen at layer 22 live in different vector spaces, possibly of different dimension, with no canonical correspondence.  Even for a single model, the choice of basis for the residual stream is a gauge freedom: any invertible transformation of the state space, compensated by corresponding transformations of the weight matrices, produces identical behavior.

The problem is to find a canonical, basis-free description of the state of a sequential computation -- one that tells you what is being computed in a way that is comparable across different implementations.  There are other approaches to formalizing "computation in continuous spaces" -- notably Murfet and Troiani's identification of programs with singularities in parameter space via linear logic (arXiv:2504.08075) -- but these tend to route through discrete computation (Turing machines) as an intermediate formalism.  This note takes a different path: rather than embedding discrete computation into continuous spaces, it works natively in the continuous setting, arguing that a particular operator on input-output sequences -- the Hankel operator -- provides a canonical description of sequential computation, at least for linear systems, with a clear path toward nonlinear extensions.

I have been thinking of this broader programme -- reconstructing internal computational structure from input-output behavior -- under the heading *computational holography*, though the name is aspirational.  The core idea is simply that the internal degrees of freedom of a computation are fully determined by its input-output map, and that the effective dimensionality of the interior is controlled by the behavioral complexity, not by the apparent size of the state space.  This note develops the first piece of that programme.

### Why not information theory?

The natural impulse is to reach for information-theoretic quantities -- mutual information between past and future, channel capacity, rate-distortion.  This impulse is wrong, or at least seriously incomplete.

Differential entropy in continuous spaces can be negative, is not invariant under change of variables, and does not satisfy the data-processing inequality that makes discrete entropy meaningful.  (I've written about this [elsewhere](https://crw.dev/posts/Why-Differential-Entropy-Stinks/).)  Mutual information $I(X;Y)$ is better-behaved in principle, but requires density estimation in practice -- either intractable or dominated by approximation error.

But the deeper problem isn't computational.  Even exact $I(\text{past};\text{future})$ gives a single scalar.  It tells you *how much* the past predicts the future, but not *what* it predicts, *in which directions*, or *with what priority*.  To understand computation -- what a model represents, how representations are structured, which aspects of the input drive the output -- we need a decomposition into ranked modes with definite geometric content.

## 2. The Hankel operator

### Setup

Consider a sequential system -- a transformer, an SSM, an RNN -- processing inputs and producing outputs.  We observe the system's input-output behavior: for each input history, we record the resulting output.  Concretely, fix an observable $f$ (a linear probe, a projection onto a subspace, the output logits), and consider the operator that maps input histories to future outputs as seen through $f$.

The **Hankel operator** of this pair has rows indexed by input histories (pasts) and columns indexed by future continuations:

$$H_f(\text{past}, \text{future}) = f\!\bigl(\text{state after processing past} \cdot \text{future}\bigr)$$

In the discrete setting (sequences over an alphabet $\Sigma$):

$$H_f(u, v) = f(u \cdot v)$$

In the continuous-time setting, this becomes the operator mapping past input functions to future output functions:

$$(\Gamma u)(t) = \int_0^\infty h(t + \tau) u(\tau)\, d\tau, \quad t \geq 0$$

In either case, $H_f$ is a purely behavioral object.  It records every past-future relationship without reference to how the computation is implemented.  Two systems with different architectures but identical behavior produce identical Hankel operators.

### The fundamental theorem

The first reason to care about this operator is a classical result connecting it to state complexity:

> **Theorem (Fliess, 1974; Carlyle-Paz, 1971).**  $\operatorname{rank}(H_f)$ equals the minimal state-space dimension of any *linear* sequential system (weighted finite automaton) that realizes $f$.

This is a hard lower bound extracted from behavior alone.  No linear implementation can beat it.  The class of linear sequential systems is broad -- it includes HMMs, linear dynamical systems, probabilistic automata, and predictive state representations -- so this invariant has teeth.

### The SVD as canonical geometry

The SVD $H_f = U \Sigma V^\top$ provides the canonical geometry of the computation:

- **Singular values** $\sigma_1 \geq \sigma_2 \geq \cdots$ rank the computational modes by importance.
- **Left singular vectors** (columns of $U$) are **canonical past features** -- the directions in history space that matter for predicting the future.
- **Right singular vectors** (columns of $V$) are **canonical future features** -- the directions in continuation space that the past can predict.
- The **balanced realization** $\alpha_f(u) = \Sigma^{1/2} U^\top e_u$ gives the canonical state that the computation assigns to each history.

This balanced realization is the canonical state representation for linear sequential systems -- a basis-free, importance-ranked description that is unique up to unitary transformation.  It is what the Turing machine tape would be if it were canonical.  The singular values give the importance of each direction; the singular vectors give their meaning in terms of inputs and outputs.

### Gauge invariance

Here's the precise sense in which this is canonical.  Any two minimal realizations of the same input-output map are related by an invertible linear transformation $T$.  (This is a standard result: if $(A_1, B_1, C_1)$ and $(A_2, B_2, C_2)$ are both minimal, then $A_2 = T A_1 T^{-1}$, $B_2 = T B_1$, $C_2 = C_1 T^{-1}$.)  The Hankel singular values are invariant under all such transformations.  They aren't the complete invariants of the input-output map (two different transfer functions can share the same singular values), but they are the complete *continuous* invariants of the balanced realization under its residual unitary gauge freedom.

Two systems computing the same (or similar) functions have the same (or close) Hankel spectra, with quantitative perturbation bounds: $|\sigma_k(\Gamma_1) - \sigma_k(\Gamma_2)| \leq \|\Gamma_1 - \Gamma_2\|_{\text{op}}$ (Weyl's inequality for singular values of compact operators).  This gives you canonical coordinates in which GPT layer 7 and Qwen layer 22 can be directly compared -- corresponding singular vectors point to corresponding computational modes, ranked by importance.

### Optimal truncation

> **Theorem (Adamjan, Arov, Krein, 1971).**  The distance from $\Gamma$ to the nearest Hankel operator of rank at most $r$ equals $\sigma_{r+1}(\Gamma)$.

AAK says the best rank-$r$ *Hankel* approximation (not just the best rank-$r$ matrix, but the best one that is itself a Hankel operator) achieves error exactly $\sigma_{r+1}$.  Combined with Fliess-Carlyle-Paz, this means the best $r$-dimensional linear system approximation is characterized by the Hankel singular values, and can be explicitly constructed.

## 3. Scope: what class of computations?

How broad is this framework?  A classical result delineates its scope:

> **Theorem (Boyd and Chua, 1985).**  Any time-invariant operator with the **fading memory property** can be uniformly approximated by a Volterra series on any compact set of inputs.

Fading memory means the operator is continuous when past inputs are weighted by exponential decay.  This is the natural condition for any system with bounded resources: you cannot perfectly remember arbitrarily distant inputs.

Boyd-Chua is to sequential computation what Stone-Weierstrass is to static function approximation: Volterra series are universal for fading-memory operators.  This justifies the Volterra *approximation* -- it does not, by itself, extend the clean Hankel results (Fliess, AAK) to nonlinear systems.  The Hankel operator encodes the complete structure of the linear (first-order Volterra) part; each higher Volterra order contributes its own Hankel-type structure, but the optimality guarantees don't straightforwardly generalize.  I'll develop the Volterra hierarchy in a separate post.

The regularity of a system controls how well it can be approximated:

> **Theorem (Peller, 1980).**  The Hankel operator belongs to Schatten class $S^p$ (i.e., $\sum_k \sigma_k^p < \infty$) if and only if its symbol (the impulse response) belongs to the Besov space $B^{1/p}_{p,p}$.

Peller gives a precise dictionary: smooth impulse responses yield rapidly decaying spectra (low-rank descriptions work well); systems with long memory or sharp transitions have slowly decaying spectra and require many modes.

## 4. The kernel connection

The Hankel operator has a natural factorization that reveals a connection to the kernel methods familiar in ML theory.

The operator factors as $\Gamma = \mathcal{O} \circ \mathcal{C}$, where $\mathcal{C}$ maps past inputs to states (the "controllability" map) and $\mathcal{O}$ maps states to future outputs (the "observability" map).  The inner products of these maps define **Gram matrices** -- $W_c = \mathcal{C}\mathcal{C}^*$ on the input side, $W_o = \mathcal{O}^*\mathcal{O}$ on the output side -- and the Hankel singular values are the square roots of the eigenvalues of $W_c W_o$.

In the linear case, these Gram matrices are kernel matrices, and the identification is exact: the SVD of the Hankel operator recovers the same decomposition as kernel PCA applied to the input-output map.  The balanced realization is the canonical feature representation in which the input-side and output-side Gram matrices are simultaneously diagonalized.

If you already work with kernel eigendecompositions, NTK spectra, or RKHS embeddings, you're already working with objects that have this Hankel structure.  The contribution here is making the *sequential* structure explicit -- vocabulary for how these kernels encode temporal/layer-wise computation, not just static function properties.

To make this concrete: consider a transformer's residual stream at layer $l$.  The output-side Gram matrix encodes the geometry of how activations $x_l$ project onto future outputs.  The input-side Gram matrix encodes how past inputs reach $x_l$.  The Hankel singular values identify which directions in $x_l$ are simultaneously reachable and observable -- these are the canonical features of the computation at that layer.

## 5. What the spectrum tells you

**Memory capacity.**  Dambre et al. (2012) defined the information processing capacity of a reservoir as the total $R^2$ -- the sum of squared correlations between outputs and time-lagged inputs, bounded by the state dimension.  For linear reservoirs with white-noise inputs, this can be expressed in terms of the Hankel singular values.  It's algebraic, computable from second-order statistics, requiring no density estimation -- spectral, not information-theoretic.

**Spectral shape as complexity signature.**  Peller's theorem (Section 3) links spectral decay to regularity.  But the *shape* of the spectrum carries more information than its rate of decay.  Exponential decay indicates a finite-dimensional process.  Power-law decay $\sigma_k \sim k^{-\alpha}$ indicates scale-free structure, with $\alpha$ encoding the effective dimensionality.  A spectral gap indicates a clean separation between dominant modes and noise.  None of this is captured by a single scalar like mutual information.

**Containment of information theory.**  Under appropriate kernel choices, $\|H_f\|_F^2 = \sum_k \sigma_k^2$ equals the Hilbert-Schmidt Independence Criterion (HSIC) between past and future (Gretton et al., 2005), which has the structure of a Renyi-2 dependence measure.  So the Hankel spectrum *contains* something information-theoretic -- as one summary statistic of the full spectral object.  (I worked through this chain of identities in more detail in the [earlier post](https://crw.dev/posts/Characterizing-Predictive-Salience-via-Hankel-Spectra/).)

**Two sequential axes.**  A transformer processes information along two axes: the **token axis** (sequence position) and the **layer axis** (depth).  The Hankel framework applies to both, with opposite desiderata.  Along the token axis, fading memory is *desirable* -- the rate of spectral decay defines the effective context length.  Along the layer axis, *convergence* is desirable -- deeper layers should refine representations, not amplify noise.  These are the same mathematical objects applied along two sequential dimensions with dual requirements.

## 6. Internal computation

The most speculative application is to the *internal* structure of sequential computation.

Consider a transformer generating a long sequence autoregressively.  At each token position $t$, the residual stream encodes both (a) information directly relevant to predicting the next token and (b) information being "written to the internal tape" for use many tokens later.  Category (a) is roughly what interpretability work calls linear features -- directions that project cleanly onto output logits.  Category (b) is where less-understood nonlinear structure lives: intermediate computation, scratch work, setup for future operations.

The Hankel framework offers a way to begin distinguishing these.  Consider the Hankel operator $H_f^{(t)}$ defined as follows: fix a prefix (the tokens up to position $t$), and let the "past" and "future" be the tokens before and after $t$ respectively, with $f$ projecting onto the model's output behavior (e.g., logits).  (One could also average over prefixes to get a distribution-level object; the right definition depends on the application.)  The rank-$r$ truncation captures the part of the state directly relevant to output prediction at fidelity level $r$.  The *residual* -- what the truncation misses -- captures structure present in the state that is not yet visible in the output.

If this residual is large at position $t$ but the corresponding structure becomes output-relevant at some later position $t' > t$, that is a signature of internal computation: the model wrote to its tape at $t$ and reads from it at $t'$.  The balanced realization gives canonical coordinates in which to ask *what* was written -- without committing to a particular basis for the residual stream.

This needs further formalization -- in particular, specific-prefix versus distribution-averaged definitions, and estimation from finite data.  But the structure points toward a principled version of a question interpretability currently addresses only heuristically: what is the model computing *on*, as distinct from what it's outputting?

## 7. Limitations and what comes next

**Linearity.**  The strongest results (Fliess, AAK, the Gram matrix factorization) apply to linear systems.  Neural networks are nonlinear.  Generalizations exist -- empirical Gram matrices, Koopman methods, the Volterra hierarchy -- but they lack the clean optimality guarantees of the linear theory.  Extending these guarantees is the central mathematical challenge.

**Tractability.**  Estimating Hankel spectra from queries to large models is an open problem.  The estimation theory for this -- translating "black-box access to a neural network" into spectral estimates with quantitative error bounds -- is needed and does not yet exist.

**What this is.**  This is a language and a set of principles for thinking about sequential computation in continuous spaces, backed by classical theorems that establish what the objects mean and why they are canonical.  For linear systems, the Hankel singular values provide a gauge-invariant description of the computation's state structure; the balanced realization gives a canonical coordinate system; the spectral decomposition ranks modes by importance with exact optimality guarantees.  The extension to nonlinear systems is the main open problem.

The full vision -- reconstructing a computation's internal structure from its input-output behavior, what I've been calling computational holography -- is a programme, not a result.  But the mathematical foundations are solid, the objects are well-defined, and the gap between this and current approaches to understanding sequential neural networks seems worth closing.  I would be glad to talk to anyone interested in working on this.

## References

- Adamjan, V.M., Arov, D.Z., Krein, M.G. (1971).  Analytic properties of the Schmidt pairs of a Hankel operator and the generalized Schur-Takagi problem.  *Math. USSR Sbornik*, 15(1), 31-73.
- Boyd, S. and Chua, L.O. (1985).  Fading memory and the problem of approximating nonlinear operators with Volterra series.  *IEEE Trans. Circuits and Systems*, 32(11), 1150-1161.
- Carlyle, J.W. and Paz, A. (1971).  Realizations by stochastic finite automata.  *J. Computer and System Sciences*, 5(1), 26-40.
- Dambre, J., Verstraeten, D., Schrauwen, B., and Massar, S. (2012).  Information processing capacity of dynamical systems.  *Scientific Reports*, 2, 514.
- Fliess, M. (1974).  Matrices de Hankel.  *J. Math. Pures et Appliquees*, 53, 197-222.
- Gretton, A., Bousquet, O., Smola, A., and Scholkopf, B. (2005).  Measuring statistical dependence with Hilbert-Schmidt norms.  *ALT 2005*, 63-77.
- Lall, S., Marsden, J.E., and Glavaski, S. (2002).  A subspace approach to balanced truncation for model reduction of nonlinear control systems.  *Int. J. Robust and Nonlinear Control*, 12(6), 519-535.
- Peller, V.V. (1980).  Hankel operators of class $S_p$ and their applications (rational approximation, Gaussian processes, the problem of majorization of operators).  *Math. USSR Sbornik*, 41(4), 443-479.

---

*Written with Claude.*
