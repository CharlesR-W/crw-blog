---
title: "Neural Circuits as Variational Linear Algebra"
date: 2026-11-27
tags: [notes, ai]
kind: research note
math: true
---

*From me (CRW):*

These are some notes I had GPT write up based on conversations trying to develop a theory of Hebbian learning.  The core idea is that we should think of neural learners as linear algebra machines rather than computers in the traditional sense.  The basic idea is that Hebbian + anti-Hebbian weights evolve to solve a variational problem in matrix factorization, $$\inf_{X,Y}\Vert XY-A\Vert$$, with various constraints or regularizations.  There is a huge class of problems which can be solved in this form (PCA, sparse PCA, ICA, clustering, similarity-matching), which all more-or-less fall under the framework of so-called "generalized low-rank models".  The key connection is that they are solvable by iteratively updating the factor matrices; in our case, the Hebb/anti-Hebb weight matrices.  GPT sketches out a handful of applications and different possible problems we could solve this way.  This is meant to be a "list of circuits" for this worldview, similar to NAND, AND, etc. (or perhaps PMOS and NMOS gates).  I want to make it plausible to you that something like "the genome specifies the brain by encoding which regions solve which variational numerical linear algebra problems", with a ton of bells and whistles.

I've dedicated less time and care to thinking about the role of inference-time activation, but the basic idea is that population activations evolve to jointly implement something like an anytime-interruptible matvec specified by the weight matrices, though more complicated things are plausible.  Much of this is stuff GPT wrote and I will have to study still.

Lastly, I'll give a handful of applications from engineering to show the universality of linear algebra for solving practical problems: prediction, planning, control, etc.

As for limitations: we're deliberately neglecting a few things here, and the picture will be more complicated.  I mostly neglect nonlinearities and activation functions because I think they can be accommodated fairly easily.  More important, perhaps, is my neglect of Dale's law: the near-universal distinction between neurons which are excitatory and those which are inhibitory.  GPT added some comments on both of these and more at the end.  I'm still comfortable with the broad idea that variational numerical linear algebra and/or matrix factorization is how we should think about the brain.

Lastly, this is an LLM-slop note I asked Opus to clean up.  I told it to try and make it readable to my friends, but to assume that people will mostly ask their LLMs to explain it to them or provide tutorials on isolated components.  Doubtless the LLM will compulsively inform you "this is just a theory, no experiments have been run yet", lol.  I hope to write a more pedagogical essay on this later.

*Everything below this line is AI-written: drafted by GPT over several research conversations, then reorganized, checked and rewritten by Claude.  The interactive companion, [Neurons as Matrix Factorization Machines](https://charlesr-w.github.io/NeuralMatrixFactorization/), runs one such circuit live in the browser.*

---

## The picture in one paragraph

A population of neurons with Hebbian feedforward synapses and anti-Hebbian lateral synapses is, to a good approximation, an online algorithm for factorizing a matrix.  Which matrix, and under which constraints, is set by physiology: what the inputs are and how they are paired, whether firing rates can go negative, where the thresholds sit, what the homeostatic rules hold fixed.  Change those parameters and the same circuit computes PCA, whitening, sparse coding, nonnegative factorization or clustering.  On a faster timescale the same population's activity relaxes to the solution of a linear (or constrained) system defined by the synapses, so the circuit also applies inverses, projections and matrix functions to each new input.  Most practical engineering computation (regression, filtering, control, planning, policy evaluation) reduces to these operations.  The proposal is to treat these as the gates of neural computation, and to build a dictionary of them together with rules for wiring them together.

Almost every individual construction below is an established result.  The synthesis, and the claim that this is the right level at which to describe what brains compute, is the proposal.

## 1. The family of problems: generalized low-rank models

Let $$X\in\mathbb R^{d\times N}$$ hold $$N$$ observations as columns.  Plain low-rank approximation finds a dictionary $$D\in\mathbb R^{d\times k}$$ and codes $$Z\in\mathbb R^{k\times N}$$ minimizing

$$
\frac12\Vert X-DZ\Vert_F^2 .
$$

Udell, Horn, Zadeh and Boyd's [Generalized Low Rank Models](https://arxiv.org/abs/1410.0342) (GLRMs) generalize this to

$$
\min_{D,Z}\ \sum_{(i,t)\in\Omega}\ell_{it}\big(X_{it},(DZ)_{it}\big)+R_D(D)+R_Z(Z),
$$

with a set $$\Omega$$ of observed entries, per-entry losses $$\ell$$, and regularizers (possibly hard constraints) on each factor.  Each choice of ingredients gives a familiar problem.  (Since $$DZ=(cD)(Z/c)$$, a penalty on one factor only means something if the other factor's scale is fixed.)

| Ingredient | Problem |
|---|---|
| Squared loss, no constraints | PCA / truncated SVD |
| Nonnegative factors | Nonnegative matrix factorization (NMF) |
| $$\ell_1$$ penalty on codes, norm bound on dictionary atoms | Sparse coding |
| $$\ell_1$$ penalty on dictionary, norm bound on codes | Sparse PCA / sparse factor models |
| One-hot codes | $$k$$-means |
| Missing entries | Matrix completion |
| Robust loss (e.g. Huber, $$\ell_1$$) | Robust PCA |
| Logistic, ordinal or categorical losses | Factorization of non-Gaussian data |

Two properties make this family a good candidate for "what neurons do".

1. **These problems are solved by iteratively updating the factors.**  Alternating or simultaneous gradient steps on $$D$$ and $$Z$$, with a projection or proximal step for the constraints, are the standard algorithms.  When the factors are synaptic weights and activities, those updates are plasticity rules and neural dynamics.
2. **The knobs are physiological.**  A constraint or regularizer on a factor is a property of a synapse or a neuron: firing rates are nonnegative, neurons have thresholds, synapses decay, homeostasis holds firing statistics near targets.  Section 3 makes this list concrete.

### Reconstruction versus similarity

Instead of reconstructing the data, a population can reconstruct the data's pairwise similarities:

$$
\min_Z\ \frac12\Vert X^\top X-Z^\top Z\Vert_F^2 .
$$

With no constraints this has the same answer as PCA.  If $$X=U\Sigma V^\top$$ with a gap $$\sigma_k>\sigma_{k+1}$$, reconstruction is solved by $$D=U_kG^{-1}$$, $$Z=G\Sigma_kV_k^\top$$ for any invertible $$G$$, and similarity matching by $$Z=Q\Sigma_kV_k^\top$$ for any orthogonal $$Q$$.  Both recover the top-$$k$$ principal subspace, with different invariances.  With constraints they part ways: nonnegative similarity matching is not the same problem as NMF.

The two are closer than they look.  To factorize any rectangular matrix, $$A\approx UV^\top$$, stack the factors as $$H=\begin{pmatrix}U\\V\end{pmatrix}$$.  Then

$$
HH^\top=\begin{pmatrix}UU^\top&UV^\top\\VU^\top&VV^\top\end{pmatrix},
$$

so rectangular factorization is similarity matching in which only the off-diagonal block of a positive-semidefinite Gram matrix is fitted.  Similarity matching factorizes relations within one set of entities; rectangular factorization, relations between two sets; collective factorization (section 6), relations among many sets; matrix completion, partially observed relations.  This is an equivalence of objectives, not of learning rules.

### A constraint can change the answer qualitatively: manifold tiling

Sengupta et al., [Manifold-tiling Localized Receptive Fields are Optimal in Similarity-preserving Neural Networks](https://papers.nips.cc/paper_files/paper/2018/hash/ee14c41e92ec5c97b54cf9b74e25bd99-Abstract.html) (2018), shift the target similarity and require nonnegative activities:

$$
\min_{Z\ge0}\ \frac12\Vert X^\top X-\alpha\mathbf 1\mathbf 1^\top-Z^\top Z\Vert_F^2 .
$$

The intuition: for a pair of inputs less similar than $$\alpha$$, the target inner product is negative.  Nonnegative activity vectors cannot have a negative inner product; the closest they can get is zero, which means the two inputs activate disjoint sets of neurons.  (The pairs are coupled through the shared codes, so this is a pressure, not a pairwise solution.)  The outcome is localized receptive fields that tile the input manifold (place-cell-like fields on a ring or a sphere), rather than the global, oscillating modes PCA would give.  The shift $$\alpha$$ and the sign constraint, two physiological quantities, decide the geometry of the representation.  The paper's analysis works mostly with a simplified objective, NSM-1, which drops the quartic term in favour of a per-input activity budget:

$$
\max_{Z\ge0,\ \Vert z_t\Vert^2\le\beta}\ \mathrm{Tr}\big[(X^\top X-\alpha\mathbf 1\mathbf 1^\top)Z^\top Z\big].
$$

For symmetric manifolds (ring, sphere) it derives a necessary optimality condition whose solutions are localized, tiling fields, matches them numerically, and shows similar behaviour numerically in less symmetric settings.  A recent extension to a unified online framework covering clustering, tiling and sparse coding is Sridharan, Bahroun and Sengupta, [Flexible Online Representation Learning Based on Similarity Matching](https://arxiv.org/abs/2606.01546) (2026).

## 2. One circuit: Hebbian/anti-Hebbian similarity matching

Pehlevan, Sengupta and Chklovskii, [Why Do Similarity Matching Objectives Lead to Hebbian/Anti-Hebbian Networks?](https://arxiv.org/abs/1703.07914) (2018), show that similarity matching can be rewritten as a min-max problem over two weight matrices and the activities.  Up to constants,

$$
\min_{W}\max_{M}\ \mathbb E_x\Big[\min_z\big(-2z^\top Wx+z^\top Mz\big)\Big]+\mathrm{Tr}\,W^\top W-\frac12\mathrm{Tr}\,M^\top M .
$$

Each piece is a neural mechanism:

- **Fast activity.**  For each input, the activities minimize the bracket, which they do by the recurrent dynamics
  $$\tau_z\dot z=Wx-Mz,$$
  feedforward drive $$Wx$$ minus lateral inhibition $$Mz$$.  At equilibrium $$z^*=M^{-1}Wx$$.
- **Slow feedforward plasticity** (descent in $$W$$): $$\dot W=\eta_W\,(zx^\top-W)$$, averaged over inputs.  This is Hebbian with decay.
- **Slow lateral plasticity** (ascent in $$M$$): $$\dot M=\eta_M\,(zz^\top-M)$$.  Correlated outputs strengthen the inhibition between them, so this is anti-Hebbian.

All three updates are local: each synapse needs only the activities of the two neurons it connects.  At a fixed point of learning the synapses store output statistics, $$W=\langle zx^\top\rangle$$ and $$M=\langle zz^\top\rangle$$ (positive semidefinite; the fast minimization needs $$M\succ0$$, which holds when no output direction is silent or redundant, and is imposed by initializing $$M\succ0$$).  At the *stable* fixed points, the population's responses span the top principal subspace of the input second moment (of the covariance, if inputs are centred); other fixed points, on lower-variance eigenspaces, exist but are unstable.

Compare this with deriving a network directly from reconstruction, $$\frac12\Vert x-Dz\Vert^2$$.  Gradient descent in $$z$$ gives the same fast dynamics, $$\tau_z\dot z=D^\top x-D^\top Dz$$, with $$W=D^\top$$ and $$M=D^\top D$$, but now $$M$$ is tied to $$W$$ rather than learned on its own:

| | Reconstruction | Similarity matching |
|---|---|---|
| Fast dynamics | $$Wx-Mz$$ | $$Wx-Mz$$ |
| Feedforward rule | $$\langle zx^\top\rangle-\langle zz^\top\rangle W$$ | $$\langle zx^\top\rangle-W$$ |
| Lateral weights | $$M=WW^\top$$ (tied) | learned, anti-Hebbian |
| Slow objective | minimization | min-max |

**The same activity architecture implements different factorization algorithms depending on its plasticity rules.**  This is the first sense in which physiology programs the computation.

### Losses become populations, through duality

Min-max structure is not special to similarity matching.  Any convex loss can be written as a maximization over a dual variable,

$$
\ell(r)=\sup_p\ \big[p^\top r-\ell^*(p)\big],
$$

and for squared loss the maximizer is the residual itself.  So reconstruction can be implemented with an explicit **error population** $$p$$:

$$
\tau_p\dot p=x-Dz-p,\qquad \tau_z\dot z=D^\top p,\qquad \dot D=\eta\,\langle pz^\top\rangle .
$$

The dictionary update is now a local correlation between error and representation activity, the architecture of predictive coding.  Changing the loss changes the error population's dynamics; changing the regularizers changes the representation's.  The recipe generalizes: write down a factorization or variational problem, introduce dual variables where convenient, derive primal-dual or proximal gradient dynamics, and read off populations and plastic synapses.  Lipshutz et al., [Normative Framework for Deriving Neural Networks with Multicompartmental Neurons and Non-Hebbian Plasticity](https://arxiv.org/abs/2302.10051) (2023), carries this programme furthest, to generalized eigenproblems and NMF.

## 3. The physiological knobs

The bet behind the genome slogan is that a small number of physiological parameters select which problem a circuit solves.  Here is a working table.  Rows marked † are worked out and checked numerically for the circuit in the [companion site](https://charlesr-w.github.io/NeuralMatrixFactorization/); the others follow from the derivations in this note or the cited papers.

| Physiological parameter | Algorithmic role | Effect |
|---|---|---|
| Feedforward weight decay | Ridge penalty on $$W$$ | Sets the scale of the fitted similarity† |
| Lateral decay, $$\dot M\propto zz^\top-\gamma M$$ | Penalty on $$M$$ | PCA subspace / similarity matching† |
| Homeostatic covariance target, $$\dot M\propto zz^\top-\gamma I$$ | Lagrange multiplier for $$\langle zz^\top\rangle=\gamma I$$ | Whitening† |
| Rectification (rates are nonnegative) | Constraint $$Z\ge0$$ | NMF-like, parts-based or localized codes† |
| Firing threshold | $$\ell_1$$ penalty on activities | Sparse coding† |
| Adaptive threshold (intrinsic plasticity) | Dual variable for a shifted similarity $$X^\top X-\alpha\mathbf 1\mathbf 1^\top$$ | Narrower, tiling receptive fields† |
| Self-inhibition $$M_{aa}$$ | Diagonal of the quadratic form | The neuron's gain, $$1/M_{aa}$$† |
| Ratio of lateral to feedforward learning rates | Step sizes | Whether learning converges, not what it converges to† |
| Divisive normalization / activity budget | Norm constraint $$\Vert z\Vert^2\le\beta$$ | The activity budget in Sengupta et al.'s NSM-1 tiling objective |
| Which signals arrive together at a synapse | The pairs $$(x,y)$$ the rule sees | Which matrix is learned (section 5) |
| Gating of error signals | The observed set $$\Omega$$: residual $$m\odot(x-Dz)$$ with mask $$m$$, in both inference and plasticity | Matrix completion (silencing an input alone would fit zeros instead) |
| Nonlinearity of an error population | The loss $$\ell$$ via its conjugate | Robust or non-Gaussian losses |
| Gain modulation (neuromodulation, attention) | Coefficients on a basis of operators | An input-dependent matrix (section 5) |
| Short-term plasticity | A third, intermediate timescale | Temporary matrices: fast weights (section 5) |

Two of these deserve comment.  The self-weight sets the slope of a neuron's f-I curve, so in this picture gain is not an independent parameter but part of the matrix.  And the learning-rate ratio matters for dynamics only: on the companion site, whitening with equal rates on a spread spectrum diverges, while the same objective learns with a faster lateral rate.  That is the kind of fact the dictionary should record.

## 4. Two timescales: learning a solver versus being one

Write $$\theta$$ for synapses, $$x$$ for the current input, $$z$$ for activities, with

$$
\tau_z\dot z=F(z,x;\theta),\qquad \tau_\theta\dot\theta=G(z,x;\theta),\qquad \tau_z\ll\tau_\theta .
$$

The fast dynamics process one stimulus; the slow dynamics change the machinery.  When the fast dynamics are a gradient flow on a convex energy (and converge), the computation on a given input is

$$
z^*(x;\theta)=\arg\min_z E_\theta(z;x):
$$

the input poses a problem instance, the synapses fix its structure, and the activities settle on the solution.  The energy need not be represented anywhere; it describes the dynamics, as a potential describes an overdamped particle.

The simplest example is the linear rate model $$\tau\dot z=b-Mz$$.  If $$M$$ is symmetric it is gradient flow on $$E=\frac12z^\top Mz-b^\top z$$, and if $$M\succ0$$ it settles at

$$
z^*=M^{-1}b .
$$

**A recurrent population applies a matrix inverse just by equilibrating.**  This is the sense of "anytime-interruptible".  Starting from $$z=0$$,

$$
z(t)=M^{-1}\big(I-e^{-tM/\tau}\big)b,
$$

so stopping early returns the answer with each eigencomponent filtered by $$1-e^{-t\lambda/\tau}$$: the large-eigenvalue directions are solved first, and waiting longer refines the rest.  (The discrete analogue, Richardson iteration, gives a truncated Neumann series.)  Non-symmetric $$M$$ also converges if its eigenvalues have positive real part, but then there is no energy and errors can grow transiently before they shrink.  The precedent is the Hopfield and Tank tradition of analog optimization; see [Computing with Neural Circuits: A Model](https://doi.org/10.1126/science.3755256) (1986).

The same inverse problem can be split between the timescales in two ways.  To solve $$Az=b$$ for many $$b$$:

- **Learn the solution operator.**  Train $$W$$ to minimize $$\Vert AW-I\Vert_F^2$$; with minimum-norm selection $$W=A^+$$, and each new problem is a single matrix-vector product $$z=Wb$$.  The cost is paid once, during learning.
- **Solve each instance.**  Run $$\tau\dot z=A^\top(b-Az)$$ from $$z=0$$; it converges to $$A^+b$$ without ever storing $$A^+$$.  The cost is paid at every inference.

The first is amortization; the second is iterative inference.  A factorization problem can describe either the construction of synaptic machinery or the computation that machinery performs, and section 7 adds a middle ground.

## 5. The dictionary of primitives

This is the "list of gates".  Each row is an elementary mechanism and the linear-algebra operation it implements.

| Neural mechanism | Operation |
|---|---|
| Weighted summation | Matrix-vector product |
| Converging pathways | Addition |
| Reciprocal connections (weights tied) | Applying the transpose |
| Hebbian accumulation | Outer-product sums: matrix multiplication, covariances |
| Error-driven (delta-rule) plasticity | Regression, solving matrix equations |
| Recurrent relaxation | Applying an inverse |
| Transient recurrent dynamics | Matrix powers, exponentials, spectral filters |
| Normalization | Norm constraints, eigenvector extraction |
| Thresholds and rectification | Proximal maps: constrained and sparse inference |
| Auxiliary populations | Dual variables: losses and constraints |
| Multiplicative gain modulation | Input-dependent operators |
| Short-term plasticity | Temporary matrix memory |

### Synaptic primitives (slow)

**Hebbian accumulation is matrix multiplication.**  $$BC=\sum_i b_ic_i^\top$$, a sum of outer products of the columns of $$B$$ and rows of $$C$$.  A synapse matrix updated by $$A\leftarrow A+b_ic_i^\top$$ while the pairs are presented in turn computes $$BC$$, a streaming matrix product.  Presenting random paired samples computes a cross-moment matrix instead.

**The delta rule solves regression, and through the choice of training pairs, many other things.**  The rule $$\dot A=\eta\,\langle(y-Ax)x^\top\rangle$$ (Widrow-Hoff / LMS) is gradient descent on $$\frac12\langle\Vert Ax-y\Vert^2\rangle$$ and converges to $$A^*=C_{yx}C_{xx}^{-1}$$ (pseudoinverse if $$C_{xx}$$ is singular).  What it learns depends on what it is shown:

| Pairs $$(x,y)$$ presented | Learned matrix |
|---|---|
| Arbitrary | Best linear predictor |
| $$(x,Bx)$$, rich enough $$x$$ | The forward operator $$B$$ |
| $$(Bx,x)$$, rich enough $$x$$ | $$B^{-1}$$ when $$B$$ is invertible |
| $$(Be_i,e_i)$$ over basis vectors | $$B^+$$, with minimum-norm selection |
| $$(s_t,s_{t+1})$$ | Best linear transition operator |
| $$(\phi(s_t),\phi(s_{t+1}))$$ | A finite Koopman approximation (EDMD) |

One fixed learning rule implements a family of matrix algorithms, programmed by the statistics of its inputs.

**Competition and normalization give spectral operations.**  Oja's rule, $$y=w^\top x$$, $$\dot w=\eta\,y(x-yw)$$, finds the leading principal component.  With more structure:

| Operation | Variational form |
|---|---|
| Low-rank approximation | $$\min_{U,V}\Vert A-UV^\top\Vert_F^2$$ |
| Leading eigenvector ($$A$$ symmetric) | $$\max_{\Vert u\Vert=1}u^\top Au$$ |
| Leading singular pair | $$\max_{\Vert u\Vert=\Vert v\Vert=1}u^\top Av$$ |
| Generalized eigenvector ($$B\succ0$$) | $$\max_{u^\top Bu=1}u^\top Au$$ |
| NMF | $$\min_{U,V\ge0}\Vert A-UV^\top\Vert_F^2$$ |
| Whitening | Fix the output covariance to $$I$$ |
| CCA | Maximize cross-correlation subject to whitening |

Some of these have local learning rules (Oja, similarity matching, whitening); others need tied weights or extra populations.

### Activity primitives (fast)

**Relaxation.**  The dynamics $$\tau\dot z=b-Mz$$, with different choices of $$M$$ and $$b$$ wired in, compute:

| $$M$$ | $$b$$ | Equilibrium |
|---|---|---|
| $$I$$ | $$Ax$$ | $$Ax$$ |
| $$A\succ0$$ | $$x$$ | $$A^{-1}x$$ |
| $$A^\top A$$ | $$A^\top x$$ | Least squares (from $$z=0$$: the minimum-norm solution) |
| $$A^\top A+\lambda I$$ | $$A^\top x$$ | Ridge regression |
| $$L+\lambda I$$ ($$L$$ a graph Laplacian) | $$\lambda x$$ | Smoothing $$x$$ on the graph |
| $$I-\gamma P$$ ($$P$$ a Markov matrix, $$\gamma<1$$) | $$r$$ | A discounted value function |

The last row is stable even though $$P$$ is not symmetric; it just has no energy function.

**Transients.**  Equilibria are not the only useful output.  $$\dot z=-Az$$ from $$z(0)=x$$ gives $$z(t)=e^{-tA}x$$; repeated propagation gives $$A^kx$$; combining steps gives $$p(A)x$$ for a polynomial $$p$$.  If the synapses encode a graph Laplacian, they specify a geometry and the dynamics diffuse over it.  The normalized dynamics $$\dot z=Az-(z^\top Az)z$$ ascend the Rayleigh quotient on the unit sphere and find the top eigenvector.

**Nonlinearities as proximal maps.**  Adding a regularizer $$r$$ to the energy gives

$$
z^*(x)=\arg\min_z\ \tfrac12z^\top Mz-z^\top Wx+r(z),
$$

solved by proximal-gradient steps $$z\leftarrow\mathrm{prox}_{\eta r}\big(z+\eta(Wx-Mz)\big)$$, or by an LCA-style circuit (Rozell et al., [Sparse Coding via Thresholding and Local Competition in Neural Circuits](https://doi.org/10.1162/neco.2008.03-07-486), 2008).  The ReLU is the proximal map of the constraint $$z\ge0$$; soft thresholding is the proximal map of an $$\ell_1$$ penalty.  So two familiar neural nonlinearities are exactly the steps that impose nonnegativity and sparsity.  Other constraints give competitive allocation (simplex), normalized codes (norm ball) or discrete assignment (one-hot).

**Constraints as populations.**  For $$\min_z\frac12z^\top Mz-b^\top z$$ subject to $$Cz=d$$, a population $$\lambda$$ of Lagrange multipliers gives

$$
\dot z=b-Mz-C^\top\lambda,\qquad \dot\lambda=Cz-d,
$$

which converges, under standard conditions (e.g. $$M\succ0$$, $$C$$ full row rank), to the KKT point.  See Feijer and Paganini, [Stability of Primal-Dual Gradient Dynamics](https://doi.org/10.1016/j.automatica.2010.08.011) (2010).

### Dynamic operands: when the matrix changes per input

Everything so far computes $$x\mapsto A^{-1}x$$ with $$A$$ fixed in the synapses.  General computation needs $$(A,x)\mapsto A^{-1}x$$, with $$A$$ supplied on the fly.  Three ways to get it:

1. **Operator bases.**  Store operators $$A_1,\dots,A_k$$ and let another population's activity $$c$$ weight them, $$A(c)=\sum_ic_iA_i$$; a solver runs $$\dot z=b-A(c)z$$.  This needs multiplicative gain modulation of pathways.  One population specifies the problem another solves.
2. **Fast weights.**  On an intermediate timescale, $$A_t=A_{t-1}+v_tk_t^\top$$, so a query returns $$A_tq=\sum_iv_i(k_i^\top q)$$: unnormalized linear attention (Schlag, Irie and Schmidhuber, [Linear Transformers Are Secretly Fast Weight Programmers](https://proceedings.mlr.press/v139/schlag21a.html), 2021).  The same temporary plasticity could estimate covariances, regress or invert, not just accumulate.
3. **Matrices held in activity.**  A population can represent a whole matrix.  $$\dot Z=A^\top(B-AZ)$$ from $$Z=0$$ converges to $$A^+B$$; the pair $$\dot U=(A-UV^\top)V$$, $$\dot V=(A-UV^\top)^\top U$$ is gradient flow on $$\frac12\Vert A-UV^\top\Vert_F^2$$.  Gradient flow on the residual of $$AX+XB=C$$ solves Sylvester and Lyapunov equations, central to control theory; the solution is unique when no eigenvalue of $$A$$ and eigenvalue of $$B$$ sum to zero.  The cost is bilinear interactions between activities (a weighted sum cannot multiply two activity-encoded matrices) and nonconvexity for factorization.  Recurrent solvers of this kind have a long engineering literature, e.g. Wang, [A Recurrent Neural Network for Real-Time Matrix Inversion](https://doi.org/10.1016/0096-3003%2893%2990007-2) (1993).

## 6. Composition

The gates are only half of a computer; the other half is wiring them together.  Several distinct mechanisms compose these primitives.

**Sequential composition.**  $$x\mapsto Ax\mapsto BAx$$, or chains of optimization-defined maps $$x\mapsto z^*(x)\mapsto w^*(z^*(x))$$ (as in OptNet-style layers).  Stacking linear maps adds no new functions, and nested PCA on the same data just returns nested subspaces, so new power has to come from constraints, feedback, changing operators, or new data.

**Shared factors.**  If two datasets describe the same things, $$X\approx AZ$$ and $$Y\approx BZ$$, a shared code $$Z$$ links them.  At inference either observation constrains it,

$$
z^*=\arg\min_z\ \tfrac12\Vert x-Az\Vert^2+\tfrac12\Vert y-Bz\Vert^2+r(z),
$$

and dropping one term gives associative completion from the other.  In general, relations $$R_{ab}$$ between entity types with factors $$H_a$$ give collective matrix factorization (Singh and Gordon, [Relational Learning via Collective Matrix Factorization](https://www.cs.cmu.edu/~ggordon/singh-gordon-kdd-factorization.pdf), 2008).  Shared factors are the interfaces between modules.

**Joint inference and feedback.**  A hierarchy $$X\approx AZ_1$$, $$Z_1\approx BZ_2$$ inferred jointly,

$$
\min_{z_1,z_2}\ \tfrac12\Vert x-Az_1\Vert^2+\tfrac\beta2\Vert z_1-Bz_2\Vert^2+r_1(z_1)+r_2(z_2),
$$

lets higher levels revise lower-level interpretations.  With two input channels $$x,y$$ feeding local codes $$u,v$$ and a shared code $$h$$, an ambiguous $$x$$ is read differently depending on $$y$$, because $$y$$ moves $$v$$, which moves $$h$$, which moves $$u$$.  With fixed dictionaries and convex penalties this is still one convex problem.  Precedents: hierarchical predictive coding (Rao and Ballard, [Predictive Coding in the Visual Cortex](https://doi.org/10.1038/4580), 1999) and Obeid, Ramambason and Pehlevan, [Structured and Deep Similarity Matching via Structured and Deep Hebbian Networks](https://arxiv.org/abs/1910.04958) (2019), which shows contextual disambiguation through feedback.  A practical rule: compose the objectives first, then derive the dynamics.  Terms that are constant for an isolated module stop being constant when its inputs are themselves inferred.

**Elimination: Schur complements.**  Couple two linear populations,

$$
\dot u=x-Au-Bv,\qquad \dot v=y-B^\top u-Cv .
$$

At equilibrium, solving for $$v=C^{-1}(y-B^\top u)$$ and substituting gives

$$
\big(A-BC^{-1}B^\top\big)u=x-BC^{-1}y .
$$

The effective operator is the Schur complement of $$C$$.  (If the block matrix $$\begin{pmatrix}A&B\\B^\top&C\end{pmatrix}$$ is positive definite, the coupled dynamics are a gradient flow and converge to this equilibrium.)  Wiring two populations together and letting them settle has produced matrix addition, multiplication, transposition and inversion at once.  The nonlinear version is partial minimization, $$E_{\text{eff}}(u)=\min_vE(u,v)$$: integrating out internal degrees of freedom to get effective interactions.  This is the same move as Kron reduction of electrical networks (Dörfler and Bullo, [Kron Reduction of Graphs with Applications to Electrical Networks](https://doi.org/10.1109/TCSI.2012.2215780), 2013) and Gaussian elimination in graphical models.  The equivalence holds at equilibrium; eliminating a population from the time-dependent dynamics leaves memory effects unless it is fast.

**A module, then, is specified by**: its variables (inputs, outputs, internal state); which are clamped and which inferred; its local objective and constraints; its persistent synapses; its fast and slow dynamics; and its stability.  When modules couple variationally, the network is a sum of local energies $$E(z;x)=\sum_aE_a(z_{\partial a};x)$$ over overlapping variable sets, which is a factor graph.  This is a different thing from a one-way cascade: jointly minimizing summed energies sends feedback upstream and changes the answer, which is the point of the previous paragraph but must be chosen deliberately.  Composition means identifying shared variables, adding objectives, eliminating internal variables, or letting one module set another's operators.  The open question is how much can be built from a short catalogue of such modules, especially when they learn the operators they manipulate.

## 7. Learning as the discovery of computational coordinates

Between storing a whole solution operator and solving every problem from scratch there is a middle ground.  Suppose a system keeps solving instances $$z^*(x)=\arg\min_zE(z;x)$$.  Factorize the solutions it has seen, $$Z^*\approx DH$$, then solve new instances in the learned coordinates,

$$
h^*(x)=\arg\min_h E(Dh;x),\qquad z\approx Dh^*(x).
$$

The columns of $$D$$ might be characteristic trajectories, motor synergies or predictive modes.  This tightens the link between factorization and computation: **the point of learning a factorization is to find coordinates in which later computations are cheap.**  Variants learn a preconditioner, a warm start, an approximate inverse, a compressed operator, or the parameters of a truncated solver.  These correspond to reduced-order modelling, learned preconditioning, amortized inference and algorithm unrolling; Gregor and LeCun, [Learning Fast Approximations of Sparse Coding](https://icml.cc/2010/papers/449.pdf) (2010), is the simplest neural example.  Learning finds structure; computation exploits it.

## 8. Applications: engineering is mostly linear algebra

These show how far the primitives reach.  Each is a standard algorithm rewritten as accumulation, relaxation and readout.

**In-context regression.**  Given a temporary dataset $$(x_t,y_t)$$, two Hebbian accumulators build $$C=\lambda I+\sum_tx_tx_t^\top$$ and $$B=\sum_ty_tx_t^\top$$.  For a query $$q$$, relax $$\dot z=q-Cz$$ and read out $$\hat y=Bz$$.  At equilibrium $$\hat y=BC^{-1}q$$, exact ridge regression on the temporary data, with no change to long-term synapses.  Three gates (accumulate, invert by relaxation, apply) make a recognizable learning algorithm.  This is closely related to work on in-context learning in transformers (Akyürek et al., [What Learning Algorithm Is In-Context Learning?](https://arxiv.org/abs/2211.15661), 2023; von Oswald et al., [Transformers Learn In-Context by Gradient Descent](https://proceedings.mlr.press/v202/von-oswald23a.html), 2023).

**Inverse kinematics.**  To move a limb's endpoint by $$\Delta x$$, solve damped least squares on the configuration-dependent Jacobian $$J(q)$$:

$$
\Delta q^*=(J^\top J+\lambda I)^{-1}J^\top\Delta x .
$$

This needs an operator that depends on the current state, and a regularized inverse solver.  Learned motor synergies $$D$$ restrict the search to $$\Delta q=Dh$$, which is section 7 in action.

**Model predictive control.**  For linear dynamics $$s_{t+1}=As_t+Bu_t$$, the states over a horizon are $$S=Ps_0+GU$$ for matrices $$P,G$$ built from $$A,B$$.  Tracking a target trajectory $$R$$ with a control penalty means

$$
\min_U\ \tfrac12\Vert Ps_0+GU-R\Vert^2+\tfrac\lambda2\Vert U\Vert^2,
$$

solved by $$\dot U=G^\top(R-Ps_0)-(G^\top G+\lambda I)U$$.  The activities hold a whole planned control sequence; execute the first action and re-solve.  Constraints enter through projections or multipliers.  Planning becomes an inverse problem, not a separate faculty.

**Policy evaluation.**  A fixed policy's value function solves $$v=r+\gamma Pv$$, so $$v=(I-\gamma P)^{-1}r$$, reached by relaxing $$\dot v=r+\gamma Pv-v$$.  (Choosing actions takes more machinery.)

**Prediction and filtering.**  Learning a code jointly with its dynamics, minimizing $$\Vert X-DZ\Vert^2+\mu\Vert Z_{\text{next}}-TZ_{\text{prev}}\Vert^2$$ with the scale of $$Z$$ fixed (otherwise shrinking the codes trivially shrinks the second term), can keep directions that matter for prediction even when they have little variance, which PCA-then-fit would discard.  For linear-Gaussian models, inferring a state sequence is the quadratic problem

$$
\sum_t\Vert x_t-Dz_t\Vert^2_{R^{-1}}+\Vert z_{t+1}-Tz_t\Vert^2_{Q^{-1}}
$$

(plus a prior), a block-tridiagonal linear system whose solution is Kalman smoothing.

## 9. A provisional analogy with digital computation

| Digital | Variational neural |
|---|---|
| Gate | Elementary operator or solver |
| Register | Population activity |
| Memory | Synapses, persistent activity |
| Wiring | Coupling between variables |
| Instruction | Applying or modifying an operator |
| Program | A structured set of coupled problems |
| Execution | Propagation and relaxation |
| Compilation | Learning good coordinates and solvers |
| Inlining a subroutine | Eliminating variables (Schur complements) |

"Matrix factorization" and "variational numerical linear algebra" name overlapping territory: factorization is the learning-and-representation half, variational linear algebra the inference half (inverse problems, matrix equations, optimization-defined maps).  The proposal needs both.

## 10. What is being neglected, and whether it breaks the picture

The derivations above use signed, linear, symmetric, noiseless rate units.  Real neurons are none of these.  The useful question is which of these simplifications change the computational level and which only constrain how it is implemented.  Throughout, separate **physical synaptic connectivity** from **effective operators**: there is no reason the effective operator a circuit applies has to obey the sign rules of its synapses.

### Dale's law

Dale's principle says each neuron's outgoing synapses all have one sign: with $$W_{ij}$$ the connection from $$j$$ to $$i$$, each column of $$W$$ is all nonnegative (excitatory neuron) or all nonpositive (inhibitory).

**This is a different distinction from Hebbian versus anti-Hebbian.**  E/I is about the sign of a synapse's effect; Hebb/anti-Hebb is about how correlation changes it.  An inhibitory synapse of strength $$g_{ij}\ge0$$ with $$\dot g_{ij}=\eta(r_ir_j-\lambda g_{ij})$$ has signed weight $$W_{ij}=-g_{ij}$$, so $$\dot W_{ij}=-\eta r_ir_j-\eta\lambda W_{ij}$$: Hebbian in magnitude, anti-Hebbian in signed weight.  The lateral weights $$-M$$ of section 2 are of this kind where $$M$$ is entrywise nonnegative (e.g. with nonnegative activities); with signed activities $$-M$$ can have mixed signs, and is an effective lateral operator that itself needs an E/I realization, as below.

**Dale's law turns one matrix into a factorization.**  Split the population into excitatory rates $$e$$ and inhibitory rates $$i$$, with all four weight matrices entrywise nonnegative:

$$
\tau_E\dot e=b-e+Ae-Bi,\qquad \tau_I\dot i=-i+Ce-Di .
$$

(As linear equations, read $$e$$ and $$i$$ as deviations around a positive baseline, or as valid within a region where all rates stay positive; otherwise the rectified version below applies.)

If $$I+D$$ is invertible (e.g. spectral radius $$\rho(D)<1$$), at equilibrium $$i^*=(I+D)^{-1}Ce^*$$, and substituting,

$$
\big[I-A+B(I+D)^{-1}C\big]\,e^*=b .
$$

When $$M_{\text{eff}}$$ is invertible the circuit still applies an exact inverse, $$e^*=M_{\text{eff}}^{-1}b$$; the effective operator has more structure.  With no inhibitory-to-inhibitory coupling, $$M_{\text{eff}}=I-A+BC$$, and building a desired effective operator $$M_0$$ from Dale-compliant parts is the constrained factorization

$$
\min_{A,B,C\ge0}\ \Vert M_0-(I-A+BC)\Vert_F^2 .
$$

The negative effective couplings come from the excitatory matrix $$A$$; the positive ones (net inhibition) must pass through the inhibitory pathway as a nonnegative product $$BC$$.  With no further constraints, one interneuron is enough: take global inhibition $$B=c\mathbf 1$$, $$C=\mathbf 1^\top$$ and let excitation cancel the excess, $$A=c\mathbf 1\mathbf 1^\top-(M_0-I)$$, which is nonnegative once $$c\ge\max_{ij}(M_0-I)_{ij}$$.  That solution is a strongly self-exciting network held in check by a single inhibitory unit, which shows that bare representability is the wrong question.  Once excitation is bounded or sparse, or stability is required, the rank and nonnegative rank of $$BC$$ (how many interneurons, wired how) become real limits.  This is the construction used by Zhu and Rozell, [Modeling Inhibitory Interneurons in Efficient Sensory Coding Models](https://doi.org/10.1371/journal.pcbi.1004353) (2015), to make sparse-coding circuits Dale-compliant.  It is also Schur-complement elimination (section 6) of the inhibitory population.

**Inhibitory populations as dual variables.**  Take the saddle function

$$
\mathcal L(e,i;b)=\tfrac12e^\top Qe-b^\top e+i^\top Ce-\tfrac12i^\top Hi,\qquad H\succ0,
$$

with excitatory activity descending and inhibitory activity ascending:

$$
\tau_E\dot e=b-Qe-C^\top i,\qquad \tau_I\dot i=Ce-Hi .
$$

Excitation drives inhibition and inhibition suppresses excitation, with $$C\ge0$$ on both pathways.  With $$Q=I-A$$ and $$H=I+D$$ (symmetric $$A,D\ge0$$) this is the Dale-compliant network above with tied weights $$B=C^\top$$.  It needs $$H\succ0$$ and $$Q+C^\top H^{-1}C\succ0$$; if $$Q$$ itself is indefinite (strong recurrent excitation), convergence also needs inhibition to be fast enough.  Maximizing over $$i$$ gives $$i^*=H^{-1}Ce$$ and an effective objective for the excitatory population,

$$
E_{\text{eff}}(e;b)=\tfrac12e^\top\big(Q+C^\top H^{-1}C\big)e-b^\top e ;
$$

with $$H=I$$ the interneurons impose the penalty $$\frac12\Vert Ce\Vert^2$$.  **Inhibitory populations can act as the auxiliary or dual variables of a variational problem, their feedback enforcing penalties and constraints.**  This min-max is on the fast timescale, distinct from the slow min-max of similarity-matching plasticity; a circuit can have both.  It does rely on the I→E weights being the transpose of the E→I weights.  Li and Pehlevan, [Minimax Dynamics of Optimally Balanced Spiking Networks of Excitatory and Inhibitory Neurons](https://proceedings.neurips.cc/paper_files/paper/2020/hash/33cf42b38bbcf1dd6ba6b0f0cd005328-Abstract.html) (2020), derive Dale-compliant spiking networks from objectives of this kind.  Qin et al., [Coordinated drift of receptive fields in Hebbian/anti-Hebbian network models](https://www.nature.com/articles/s41593-022-01225-z) (2023), extend nonnegative similarity matching to separate interneurons in their supplement.

### Nonlinearities

**Rectification keeps the linear algebra and picks the matrix.**  For nonnegative rates, $$\min_{e\ge0}\frac12e^\top Me-b^\top e$$ with $$M\succ0$$ has optimality conditions

$$
e\ge0,\qquad Me-b\ge0,\qquad e_j(Me-b)_j=0,
$$

a linear complementarity problem.  On the support $$S=\{j:e_j>0\}$$, $$e_S=(M_{SS})^{-1}b_S$$, and the rest are silent; self-consistency requires $$e_S>0$$ and $$M_{S^cS}e_S\ge b_{S^c}$$ (each silent neuron's net drive is nonpositive).  The input chooses which neurons are active, which chooses which submatrix gets inverted.  For symmetric positive-definite $$M$$ the map from $$b$$ to $$e$$ is continuous and piecewise linear.  This is the mechanism behind manifold tiling: conditional computation and local codes, built on linear algebra.

**Smooth nonlinearities linearize around an operating point.**  If $$r=\phi(Wr+b)$$, small changes obey

$$
\delta r=(I-GW)^{-1}G\,\delta b,\qquad G=\mathrm{diag}(\phi'),
$$

(when $$I-GW$$ is invertible at the fixed point): again an inverse, now of a state-dependent operator: the gains select the matrix.

### Signs, symmetry and stability

- **Nonnegative rates cannot represent signed quantities directly.**  They need a baseline or a push-pull pair of populations.  Baker, Zhu and Rosenbaum, [Nonlinear Stimulus Representations in Neural Circuits with Approximate Excitatory-Inhibitory Balance](https://doi.org/10.1371/journal.pcbi.1008192) (2020), make this sharp for balanced networks: under their assumptions, for any invertible Dale-compliant connectivity, infinitely many excitatory inputs make the linear balanced-state prediction demand negative rates.  That argues for constrained linear algebra (the complementarity problem above), not against the framework.
- **Symmetric and transposed weights are the more serious idealization.**  Exact symmetry is what makes the fast dynamics a gradient flow; transposes ($$D$$ and $$D^\top$$, $$C$$ and $$C^\top$$) are what make the primal-dual derivations work.  Dale's law can usually be absorbed by one more factorization; weight transport cannot.  It has to emerge from learning (symmetric Hebbian rules do tend to produce symmetric lateral weights), or the computation has to be shown robust to its absence.
- **Stability is not inherited.**  Two circuits with the same equilibrium map can have very different transients.  Slow inhibition can make an E/I circuit oscillate or blow up; this is the territory of inhibition-stabilized networks and the stabilized supralinear network (Ahmadian, Rubin and Miller, [Analysis of the Stabilized Supralinear Network](https://arxiv.org/abs/1202.6670), 2013).  A fixed point that cannot be reached is not a solver.
- **Imperfect connectivity is a conditioning question.**  If a circuit meant to solve $$Mz=b$$ actually has operator $$M+\Delta M$$, its error relative to the exact solution $$z$$ is, to first order, $$\delta z\approx-M^{-1}\Delta M\,z$$, and with $$\epsilon=\Vert\Delta M\Vert/\Vert M\Vert$$ and condition number $$\kappa(M)$$,

  $$
  \frac{\Vert\delta z\Vert}{\Vert z\Vert}\le\frac{\kappa\epsilon}{1-\kappa\epsilon}\qquad(\kappa\epsilon<1).
  $$

  Well-conditioned operations tolerate sloppy wiring; ill-conditioned ones do not.  Regularization, preconditioning and learned coordinates (section 7) improve robustness, which gives biology another reason to learn good factorizations.  Conditioning also sets speed: for $$\tau\dot z=b-Mz$$, the slowest mode relaxes at rate $$\lambda_{\min}(M)/\tau$$.

### A rough ranking of constraints

| Constraint | How much it matters here |
|---|---|
| Stability and finite settling time | Essential |
| Dale's law | High, but on microscopic connectivity, not on effective operators |
| Nonnegative rates | High: signed quantities need a baseline or a push-pull code |
| Limited numbers of interneurons | High: rank limits on effective interactions |
| Local plasticity | High for claims about learning; less so for existence proofs of computation |
| Exact symmetry / transposed weights | Potentially the biggest problem |
| The exact activation function | Secondary, beyond positivity and saturation |
| Spikes, delays, noise | Postponable unless they change stability |

### Three levels

The resulting picture has three descriptive levels: a **computational** level (factorizations, inverse problems, spectral operations, inference), an **effective population** level (signed operators, coupled solvers, primal-dual dynamics, effective energies), and a **microscopic** level (Dale-compliant connectivity, nonnegative rates, local plasticity, interneurons).  The maps between levels are themselves factorizations and eliminations.  In physics language, the unconstrained linear-algebra models are candidate effective theories of population computation; the work is to find which microscopic constraints survive coarse-graining and which merely restrict how an effective operator can be realized.

### Open questions

- Does a given circuit actually solve its problem, or only descend its objective?  Factorization objectives are usually nonconvex, and descending one is not the same as finding its global optimum.
- Which parts of a problem can be supplied as input rather than hard-coded in synapses?
- Can modules be connected without re-deriving the whole system?
- How much of the structure the composed circuits need (tied weights, multiplicative interactions, interneuron counts) can learning produce?
- Writing a computation as an optimization is cheap: almost any function is the argmin of something.  The claim has content only where the objective has useful structure and falls out of the dynamics naturally.

## References

**Core.**
- Udell, Horn, Zadeh, Boyd (2016), [Generalized Low Rank Models](https://arxiv.org/abs/1410.0342).
- Pehlevan, Sengupta, Chklovskii (2018), [Why Do Similarity Matching Objectives Lead to Hebbian/Anti-Hebbian Networks?](https://arxiv.org/abs/1703.07914)
- Sengupta et al. (2018), [Manifold-tiling Localized Receptive Fields are Optimal in Similarity-preserving Neural Networks](https://papers.nips.cc/paper_files/paper/2018/hash/ee14c41e92ec5c97b54cf9b74e25bd99-Abstract.html).
- Lipshutz et al. (2023), [Normative Framework for Deriving Neural Networks with Multicompartmental Neurons and Non-Hebbian Plasticity](https://arxiv.org/abs/2302.10051).
- Sridharan, Bahroun, Sengupta (2026), [Flexible Online Representation Learning Based on Similarity Matching](https://arxiv.org/abs/2606.01546).

**Neural factorization.**
- Oja (1982), [A Simplified Neuron Model as a Principal Component Analyzer](https://doi.org/10.1007/BF00275687).
- Olshausen, Field (1996), [Emergence of Simple-cell Receptive Field Properties by Learning a Sparse Code for Natural Images](https://doi.org/10.1038/381607a0).
- Lee, Seung (1999), [Learning the Parts of Objects by Non-negative Matrix Factorization](https://doi.org/10.1038/44565).
- Rozell et al. (2008), [Sparse Coding via Thresholding and Local Competition in Neural Circuits](https://doi.org/10.1162/neco.2008.03-07-486).
- Obeid, Ramambason, Pehlevan (2019), [Structured and Deep Similarity Matching via Structured and Deep Hebbian Networks](https://arxiv.org/abs/1910.04958).

**Analog solvers and optimization.**
- Hopfield, Tank (1986), [Computing with Neural Circuits: A Model](https://doi.org/10.1126/science.3755256).
- Wang (1993), [A Recurrent Neural Network for Real-Time Matrix Inversion](https://doi.org/10.1016/0096-3003%2893%2990007-2).
- Wang (1993), [Recurrent Neural Networks for Solving Linear Matrix Equations](https://doi.org/10.1016/0898-1221%2893%2990003-E).
- Feijer, Paganini (2010), [Stability of Primal-Dual Gradient Dynamics and Applications to Network Optimization](https://doi.org/10.1016/j.automatica.2010.08.011).
- Boyd, Vandenberghe (2004), [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/).
- Parikh, Boyd (2014), [Proximal Algorithms](https://web.stanford.edu/~boyd/papers/prox_algs.html).

**Composition.**
- Singh, Gordon (2008), [Relational Learning via Collective Matrix Factorization](https://www.cs.cmu.edu/~ggordon/singh-gordon-kdd-factorization.pdf).
- Rao, Ballard (1999), [Predictive Coding in the Visual Cortex](https://doi.org/10.1038/4580).
- Kschischang, Frey, Loeliger (2001), [Factor Graphs and the Sum-Product Algorithm](https://doi.org/10.1109/18.910572).
- Dörfler, Bullo (2013), [Kron Reduction of Graphs with Applications to Electrical Networks](https://doi.org/10.1109/TCSI.2012.2215780).
- Amos, Kolter (2017), [OptNet: Differentiable Optimization as a Layer in Neural Networks](https://proceedings.mlr.press/v70/amos17a.html).

**Fast weights and learned solvers.**
- Gregor, LeCun (2010), [Learning Fast Approximations of Sparse Coding](https://icml.cc/2010/papers/449.pdf).
- Schlag, Irie, Schmidhuber (2021), [Linear Transformers Are Secretly Fast Weight Programmers](https://proceedings.mlr.press/v139/schlag21a.html).
- Akyürek et al. (2023), [What Learning Algorithm Is In-Context Learning? Investigations with Linear Models](https://arxiv.org/abs/2211.15661).
- von Oswald et al. (2023), [Transformers Learn In-Context by Gradient Descent](https://proceedings.mlr.press/v202/von-oswald23a.html).

**Control and dynamics.**
- Buss (2004/2009), [Introduction to Inverse Kinematics with Jacobian Transpose, Pseudoinverse and Damped Least Squares Methods](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/ikmethods/).
- Amos et al. (2018), [Differentiable MPC for End-to-End Planning and Control](https://arxiv.org/abs/1810.13400).
- Williams, Kevrekidis, Rowley (2015), [A Data-Driven Approximation of the Koopman Operator: Extending Dynamic Mode Decomposition](https://arxiv.org/abs/1408.4408).

**Excitation and inhibition.**
- Zhu, Rozell (2015), [Modeling Inhibitory Interneurons in Efficient Sensory Coding Models](https://doi.org/10.1371/journal.pcbi.1004353).
- Ahmadian, Rubin, Miller (2013), [Analysis of the Stabilized Supralinear Network](https://arxiv.org/abs/1202.6670).
- Li, Pehlevan (2020), [Minimax Dynamics of Optimally Balanced Spiking Networks of Excitatory and Inhibitory Neurons](https://proceedings.neurips.cc/paper_files/paper/2020/hash/33cf42b38bbcf1dd6ba6b0f0cd005328-Abstract.html).
- Baker, Zhu, Rosenbaum (2020), [Nonlinear Stimulus Representations in Neural Circuits with Approximate Excitatory-Inhibitory Balance](https://doi.org/10.1371/journal.pcbi.1008192).
- Qin et al. (2023), [Coordinated drift of receptive fields in Hebbian/anti-Hebbian network models](https://www.nature.com/articles/s41593-022-01225-z).
