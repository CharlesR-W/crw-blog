---
title: "[Notes] Learning, Order by Order"
subtitle: "Decomposing how data structure enters learning algorithms via the Volterra series"
date: 2026-03-10
math: true
status: "Research note"
---

*Research notes from [MATS](https://www.matsprogram.org/) 9.0, under the mentorship of Richard Ngo.  These are Claude-generated documents that I roughly 80% endorse; treat them as research notes rather than polished publications.  I'm posting them mainly to give people a sense of what I'm working on.  Feedback welcome.  A [technical companion]({{ site.baseurl }}/Learning-Order-by-Order-Technical-Foundations/) develops the heavier machinery (resolvent algebra, Fock space, RG flow).*

---

## The problem

What determines how a learning algorithm responds to the structure of its training data?

This is the central question of statistical learning theory, but the existing answers are surprisingly coarse.  Information theory gives scalar summaries - mutual information, channel capacity, compression rates - that measure *how much* a learner extracts from data but not *what kind of structure* it extracts or *how*.  VC theory and Rademacher complexity bound worst-case errors but say nothing about the geometric relationship between learner and data.  Kernel theory gives complete, satisfying answers - but only in the linear regime.

The situation is analogous to pre-Fourier signal processing.  Before Fourier analysis, you could measure the energy of a signal and bound its bandwidth.  After Fourier analysis, you could decompose the signal into components and ask which frequencies carry the information.  We have the energy bounds for learning.  We don't yet have the decomposition.

This note develops one candidate.  The starting point is a natural one: any analytic learning algorithm admits a Volterra series expansion - a functional Taylor series - whose coefficients separate what is intrinsic to the learner from what is intrinsic to the data.  The expected prediction then factors, order by order, as a pairing between **learner tensors** (encoding the algorithm's sensitivity to different orders of nonlinearity) and **data tensors** (encoding the statistical moments of the distribution).  Kernel regression is the first-order truncation.  The full series organizes the interaction between learner and data into a graded hierarchy where each level couples a specific order of algorithmic nonlinearity to a specific order of data statistics.

The mathematical tools here are not new individually.  The Volterra series is classical in nonlinear systems theory (Rugh 1981, Boyd & Chua 1985).  The perturbative approach to neural networks is developed in Roberts & Yaida's *Principles of Deep Learning Theory*, which expands in inverse width; Yang's *Tensor Programs* works a related but distinct perturbative hierarchy.  The connection to influence functions goes back to von Mises and Hampel.  What this note attempts is to organize these tools into a coherent decomposition of the learner-data interaction, and to develop the algebraic structure (the graded pairing, capacity tensors, composition laws) that emerges when you take the Volterra expansion seriously as a framework rather than a one-off calculation.

This is not a finished theory.  It is an attempt to lay foundations - to identify the right mathematical objects and the right structural decompositions - so that questions about learner-data interaction that are currently only expressible informally can be formalized and, eventually, answered.


## Why this matters for alignment

My interest in this framework comes from AI safety.  Most theoretical work in alignment proceeds top-down: formalize concepts like "goals" or "knowledge" and try to connect them to learning systems.  The approach here is bottom-up: develop mathematical tools for how learning algorithms interact with data structure, and see what concepts emerge once the foundations are in place.

The hope is that the right decomposition of learner-data interaction will make it possible to formalize questions that are currently out of reach: what aspects of the data distribution a model has internalized, how those aspects change during training, and how they respond to distributional shift.  This is a bet on infrastructure - the framework does not yet answer alignment-relevant questions directly, but it should provide vocabulary for asking them precisely.


## The kernel case: the exactly solvable model

Before tackling the general case, consider the regime where everything is understood.

Supervised learning, stripped to its bones: training data $$y \in \mathbb{R}^N$$, a learning algorithm that produces a prediction $$\hat{y} \in \mathbb{R}^M$$.  Write this as

$$\hat{y} = \mathcal{K}[y]$$

where $$\mathcal{K} : \mathbb{R}^N \to \mathbb{R}^M$$ is the **learning functional** - the full input-output map of the algorithm.

When $$\mathcal{K}$$ is linear, $$\hat{y} = H y$$ for a matrix $$H$$.  This is kernel regression, ridge regression, Gaussian processes - the exactly solvable base case that plays the role in learning theory that the harmonic oscillator plays in physics.

For ridge regression with kernel matrix $$K$$ and regularization $$\lambda$$:

$$H = K(K + \lambda I)^{-1}, \qquad H = \sum_i \eta_i \, v_i v_i^\top$$

The **learning coefficients** $$\eta_i = \mu_i / (\mu_i + \lambda) \in [0, 1]$$ are the fraction of each kernel eigenmode the learner retains.  The **capacity** $$\text{df} = \text{tr}(H) = \sum_i \eta_i$$ counts effective degrees of freedom - a measure of the learner's susceptibility to noise, controlling overfitting via the AIC correction.

The key structural observation: when the data is random ($$y \sim P$$), everything factors.

$$\mathbb{E}[\hat{y}] = H \, \mathbb{E}[y], \qquad \text{Var}[\hat{y}] = H \, \text{Cov}(y) \, H^\top$$

The expected prediction depends only on the mean.  The variance depends only on the covariance.  Higher data statistics - skewness, kurtosis, tails - are invisible.  Learner geometry ($$H$$) and data geometry ($$\mathbb{E}[y]$$, $$\text{Cov}(y)$$) live on opposite sides of a factorization, coupled through matrix multiplication.

The question this note answers: **does this factorization generalize to nonlinear $$\mathcal{K}$$, or is it an artifact of linearity?**

The answer: it generalizes, but the factorization becomes *graded*.  Instead of a single matrix $$H$$ pairing with a single data vector $$\mathbb{E}[y]$$, there is a hierarchy of tensor pairings $$\mathcal{K}_n \cdot M_n$$ - one for each order of nonlinearity - and these pairings together reconstruct the full interaction.


## The Volterra decomposition

If $$\mathcal{K}$$ is analytic, expand it:

$$\mathcal{K}[y] = \sum_{n=0}^{\infty} \frac{1}{n!} \, \mathcal{K}_n \cdot y^{\otimes n}$$

where $$\mathcal{K}_n = \delta^n \mathcal{K} / \delta y^n \vert_{y=0}$$ is the $$n$$-th **learner tensor** - a symmetric $$(n+1)$$-tensor that encodes the learner's $$n$$-th order sensitivity to data.  This is a [Volterra series](https://en.wikipedia.org/wiki/Volterra_series), the standard tool for analyzing nonlinear systems in engineering and physics.

The learner tensors are **intrinsic to the algorithm**.  They are computed from $$\mathcal{K}$$ alone, with no reference to any particular dataset or distribution.  They are determined by the algorithm alone.

Order by order:

- $$\mathcal{K}_0 = \mathcal{K}[0]$$: the learner's prediction with no data.  Its prior.
- $$\mathcal{K}_1$$: a matrix.  The **linear response**.  In the kernel case this *is* $$H$$, and all higher tensors vanish.
- $$\mathcal{K}_2$$: a 3-tensor.  The **leading nonlinearity**.  $$(\mathcal{K}_2)_{i\,jk}$$ measures how prediction $$i$$ responds to the product $$y_j y_k$$ - to pairwise structure in the data.
- $$\mathcal{K}_n$$: an $$(n+1)$$-tensor.  The $$n$$-th order nonlinearity.

The kernel case is the truncation $$\mathcal{K}_1 = H$$, all else zero.  What the Volterra expansion does is replace a single matrix with a hierarchy of tensors, each capturing a different order of nonlinear response.

To give a sense of the objects involved: the compact notation $$\mathcal{K}_n \cdot y^{\otimes n}$$ hides a lot of indices.  Written out, the fifth-order contribution to the $$i$$-th prediction is:

$$\hat{y}_i^{(5)} = \frac{1}{120} \sum_{j_1, j_2, j_3, j_4, j_5 = 1}^{N} (\mathcal{K}_5)_{i\, j_1 j_2 j_3 j_4 j_5} \; y_{j_1}\, y_{j_2}\, y_{j_3}\, y_{j_4}\, y_{j_5}$$

The tensor $$\mathcal{K}_5$$ has $$M \times N^5$$ components.  For $$N = 1000$$ data points, that is $$10^{15}$$ entries per prediction component - not something you compute directly.  The framework's value is not in evaluating these tensors but in knowing they exist and understanding their algebraic structure: how they pair with data moments, how they compose under training, how their traces control capacity.  The compact notation is not laziness; it is the only way to work with these objects at all.

**Caveats.**  The expansion is taken around $$y = 0$$, which is a choice - for learners whose interesting behavior happens far from zero, expanding around the data mean $$\mathbb{E}[y]$$ or another reference point may be more natural and give better convergence.  More fundamentally, the expansion requires $$\mathcal{K}$$ to be smooth.  For neural networks with smooth activations (GELU, softplus), this is immediate.  For ReLU networks, $$\mathcal{K}$$ is piecewise linear and not differentiable at the kinks.  In practice this is not a serious obstacle: ReLU is the $$\epsilon \to 0$$ limit of smooth approximations (softplus, GELU), and the Volterra expansion applies to any such smoothing.  Throughout this note, I treat the expansion as formal and focus on the algebraic structure.

### The graded dual pairing

Now let the data be random.  The learner tensors are deterministic, so expectations pass through:

$$\mathbb{E}[\hat{y}] = \sum_{n=0}^{\infty} \frac{1}{n!} \, \mathcal{K}_n \cdot M_n$$

where $$M_n = \mathbb{E}[y^{\otimes n}]$$ is the $$n$$-th **data moment tensor**.  Each term is a full contraction of a learner tensor with a data tensor.

| Order | Learner tensor | Data tensor | What it captures |
|---|---|---|---|
| 0 | $$\mathcal{K}_0$$ (prior) | 1 | Data-independent prediction |
| 1 | $$\mathcal{K}_1$$ (hat matrix) | $$M_1 = \mathbb{E}[y]$$ | Linear response to mean |
| 2 | $$\mathcal{K}_2$$ | $$M_2 = \mathbb{E}[y \otimes y]$$ | Quadratic response to correlations |
| 3 | $$\mathcal{K}_3$$ | $$M_3 = \mathbb{E}[y^{\otimes 3}]$$ | Cubic response to skewness |

The expected prediction is an **inner product** between a "learner vector" in a graded space of learner descriptors and a "data vector" in a graded space of data descriptors:

$$\boxed{\mathbb{E}_P[\mathcal{K}[y]] = \langle \mathcal{L}(\mathcal{K}),\; \mathcal{D}(P) \rangle = \sum_{n=0}^{\infty} \frac{1}{n!} \, \mathcal{K}_n \cdot M_n}$$

This is the organizing principle of the framework.  The identity itself is a direct consequence of Taylor expansion and linearity of expectation - the content is not that it holds, but that it is *productive*: that organizing the learner-data interaction this way reveals structure that other decompositions miss.  The factorization between learner and data that characterizes the kernel case *does* survive nonlinearity - but it becomes a **graded dual pairing** in a symmetric tensor algebra.  The kernel case is the pairing at grade 1.  A nonlinear learner spreads its weight across higher grades, and *which* grades carry the weight tells you which statistical features of the data affect the learner's predictions.

A learner that is mostly grade-1 behaves like a kernel method: it responds to the mean of the data and ignores higher-order structure.  A learner with significant weight at grade 2 is sensitive to pairwise correlations.  At grade 3, to skewness and three-point structure.  The **grade profile** of a learner - how its weight distributes across the hierarchy - is a fingerprint of its nonlinear character.

A terminological note: $$\mathcal{K}_1$$ is literally a kernel (the hat matrix).  $$\mathcal{K}_2$$ is a kernel-on-pairs - it takes two data inputs and produces a prediction.  $$\mathcal{K}_n$$ is a kernel-on-$$n$$-tuples.  When $$\mathcal{K}_n$$ is positive definite as a multilinear form on the data indices, it induces a genuine RKHS $$\mathcal{H}^{(n)}$$ at that order, and the standard kernel toolkit (representer theorem, kernel PCA, complexity bounds) applies to $$n$$-point interactions.  When $$\mathcal{K}_n$$ is indefinite, you lose the RKHS structure at that order and enter Kreĭn space territory (indefinite inner product spaces).  The practical significance of indefiniteness shows up through the self-energy (see [companion note]({{ site.baseurl }}/Learning-Order-by-Order-Technical-Foundations/), §2): the data-dependent eigenvalue shifts $$\delta\eta_k = \langle v_k, \Sigma(y) v_k \rangle$$ can be positive or negative, meaning nonlinearity redistributes capacity across modes - amplifying some and suppressing others for a given data realization.  Whether the net effect adds or subtracts capacity depends on the interaction between the learner tensors and the particular data.

There is a suggestive connection to the **features and meta-features** framework in Roberts & Yaida's PDLT.  In their perturbatively quadratic regression, the linear part $$h(x)$$ learns features and the quadratic correction $$h(x)^2$$ learns *functions of features* - meta-features.  In the Volterra framework, $$\mathcal{K}_1$$ plays the role of the feature-learning kernel and $$\mathcal{K}_2$$ captures how the learner responds to products of data components - structurally analogous to meta-features.  Higher learner tensors $$\mathcal{K}_n$$ would correspond to meta$${}^n$$-features.  The two expansions are not identical (PDLT expands in $$1/\text{width}$$; the Volterra series expands in data nonlinearity), but they play analogous roles, and the Volterra framework may provide a natural setting in which the features/meta-features hierarchy can be made systematic.


## What this buys you

The graded pairing is a lens.  Here is what you can see through it.

### Capacity beyond kernels

In the kernel case, the capacity $$\text{df} = \text{tr}(H)$$ counts effective parameters.  For a nonlinear learner, the natural generalization uses the **Jacobian** $$J(y) = \partial \hat{y} / \partial y$$ rather than the hat matrix.  For Gaussian data ($$y \sim \mathcal{N}(f^*, \sigma^2 I)$$), Stein's lemma gives the identity $$\text{Cov}(\hat{y}_i, y_i) = \sigma^2 \mathbb{E}[\partial \hat{y}_i / \partial y_i]$$, so the generalized degrees of freedom controlling overfitting are:

$$\boxed{\text{df} = \mathbb{E}[\text{tr}\, J(y)]}$$

(This formula is exact for Gaussian data; for non-Gaussian distributions, it remains a natural definition of effective capacity but is no longer tied to the optimism correction by Stein's lemma.)

The Volterra expansion decomposes the Jacobian trace into **capacity tensors** $$c_m = \text{tr}_1(\mathcal{K}_{m+1})$$ - the $$(m+1)$$-th learner tensor traced over its output index and first data index (i.e., $$(c_m)_{j_1 \cdots j_m} = \sum_i (\mathcal{K}_{m+1})_{i\,i\,j_1 \cdots j_m}$$):

$$\overline{\text{df}} = \sum_{m=0}^{\infty} \frac{1}{m!} \; c_m \cdot M_m$$

The same structure as the expected prediction, with learner tensors replaced by their traces.  At zeroth order, $$c_0 = \text{tr}(\mathcal{K}_1)$$ is the kernel capacity.  Each higher term measures how the data distribution's $$m$$-th moment inflates or deflates the effective capacity beyond the kernel baseline.

For centered data, the leading correction is:

$$\overline{\text{df}} \approx \text{tr}(\mathcal{K}_1) + \tfrac{1}{2}\, c_2 \cdot \text{Cov}(y) + \cdots$$

The covariance of the data interacts with the third learner tensor, traced, to modify capacity.  Computing $$\mathcal{K}_n$$ for a real neural network involves tensors of size $$N^n \times M$$, which is intractable even at $$n = 2$$ for realistic data dimensions.  The value at this stage is structural: the framework identifies *which* quantities control the capacity correction, even when those quantities cannot yet be computed directly.

### Training dynamics: lower orders first

When a learner evolves during training (e.g., gradient flow), the learner tensors become time-dependent: $$\mathcal{K}_n(t)$$.  The equations governing their evolution form a **triangular hierarchy** - the equation for $$\mathcal{K}_n(t)$$ depends on $$\mathcal{K}_1(t), \ldots, \mathcal{K}_n(t)$$ but never on higher orders.

For gradient flow from a kernel-regime initialization ($$\mathcal{K}_{n \geq 2}(0) \approx 0$$), this means: grade 1 (linear response) activates first.  Grade 2 can only grow once grade 1 is established (it's driven by grade 1).  Grade 3 needs grades 1 and 2.  The triangular structure, combined with the initialization, produces an ordering: lower-order data structure is learned before higher-order structure.  (If the initialization already has significant nonlinearity - e.g., from architecture - the ordering can be different.)

This connects to empirical observations that neural networks learn to match moments of the data distribution in order - lower moments first, higher moments later.  The Volterra framework gives this observation a mathematical home: what is being measured is the activation of successive learner tensors $$\mathcal{K}_n(t)$$ in the triangular hierarchy.

Furthermore, the learner tensors compose across time intervals via the **Faà di Bruno formula** (the higher-order chain rule), giving the space of learner descriptors a graded monoid structure.  In the kernel case this reduces to matrix multiplication.  For nonlinear learners, it encodes how sensitivity to different data moments compounds over training.

### Comparing loss functions

The learner tensors $$\mathcal{K}_n$$ depend on the full learning algorithm, including the loss function.  This gives a concrete way to compare the effects of different losses: same architecture, different loss → different learner tensors → different grade profile → different coupling to data moments.

For MSE (quadratic loss), the loss contributes no additional nonlinearity beyond what the architecture provides - the loss is quadratic in predictions, so it acts linearly on the learner functional.  Cross-entropy, by contrast, involves $$\log \hat{y}$$ and is nonlinear in predictions.  Taylor-expanding the loss around its minimum, any smooth loss is locally quadratic, so MSE is always the leading-order approximation.  Cross-entropy and other non-quadratic losses generate corrections at higher orders in the learner tensors - effectively exciting higher Volterra grades even for a fixed architecture.  The framework identifies *which* grades are excited and by how much, giving a structured comparison between loss functions in terms of their coupling to data geometry.

This observation has a useful converse.  Near a minimum of any smooth training loss, the loss is locally quadratic, and the learning problem is locally a kernel problem - the local kernel being the Gauss-Newton kernel $$K_{GN} = J_\theta^T J_\theta$$ (Jacobian of predictions w.r.t. parameters at the minimum).  If we expand the learner functional around the converged prediction rather than around $$y = 0$$, the expansion is dominated by $$\mathcal{K}_1\vert_{y^*}$$ - the local hat matrix at convergence - because the gradient vanishes at a minimum and the leading behavior is quadratic.  The higher $$\mathcal{K}_n$$ evaluated at convergence measure departures from this local kernel regime.  So the kernel case is not just a pedagogical base case; it is the *universal local approximation* near any smooth minimum, and the Volterra expansion is an expansion in departures from it.

### Influence functions: the full hierarchy

The learner tensors $$\mathcal{K}_n$$ are the higher-order influence functions of the learning algorithm.  The **von Mises expansion** of a statistical functional is a Volterra series on distribution space, and the standard influence function analysis (Koh & Liang 2017) uses only the $$\mathcal{K}_1$$ term.  The Volterra expansion is the systematic higher-order generalization: the second-order term defines **pairwise interactions** where the influence of datum $$y_j$$ is modulated by $$y_k$$ with coupling $$(\mathcal{K}_2)_{ijk}$$.  These interaction effects are invisible to first-order influence functions and could matter for data attribution in nonlinear models.


## Coordinates on data space

Moments are one way to parameterize a distribution, but not the only one.  **Cumulants** separate genuinely new statistical information at each order ($$\kappa_2 = \text{Cov}(y)$$ strips out the mean's contribution to $$M_2$$; $$\kappa_3$$ strips out lower-order structure from the third moment).  Re-expressing the graded pairing in cumulant coordinates reshuffles the learner tensors into **connected Volterra kernels** (developed in the [companion note]({{ site.baseurl }}/Learning-Order-by-Order-Technical-Foundations/)).

The pairing itself is **coordinate-invariant**.  What changes is how you decompose it order by order: moments give a monomial decomposition; cumulants give a connected decomposition; kernel embeddings give a spectral decomposition.  The question of which decomposition is "right" is the question of which coordinates on distribution space make the learner's structure simplest - which basis diagonalizes the learner tensors, or at least makes them sparse.  (This connects to an idea in [Nonlinear Calculi]({{ site.baseurl }}/Nonlinear-Calculi/): different choices of "addition" yield different Taylor-like expansions of the same underlying object.)


## The technical companion: a preview

The framework above is self-contained, but there is substantially more structure available.  A [companion note]({{ site.baseurl }}/Learning-Order-by-Order-Technical-Foundations/) develops these in detail; here I'll state the results without proof to give a sense of where this goes.

### Self-energy and spectral perturbation theory

Write the Jacobian as $$J(y) = \mathcal{K}_1 + \Sigma(y)$$, where $$\Sigma(y)$$ is the **self-energy** - the departure from linear response.  The resolvent $$G_z(y) = (zI - J(y))^{-1}$$ satisfies a Dyson equation relative to the bare (kernel) resolvent, and iterating gives a Born series for the spectral structure.  This computes how the eigenvalues of the Jacobian - the data-dependent learning coefficients - shift under nonlinear corrections, using the same perturbation theory that governs energy levels in quantum mechanics.

### Continued fractions and nested hierarchies

The Volterra series admits a Horner evaluation (polynomial nesting).  When each level of nesting carries its own regularization, the polynomial structure promotes to **continued fractions** and the per-mode capacity composes as a **transfer matrix product** of $$2 \times 2$$ Möbius transformations.  This gives a sharp $$\frac{1}{4}$$-bound on per-level capacity transmission (from AM-GM).  Over many levels, the multiplicative composition of transmission factors leads to exponential decay of capacity in each mode - a structural parallel to Anderson localization in disordered systems.  The mathematical structure (products of random $$2 \times 2$$ matrices, Lyapunov exponents, mode-dependent decay rates) is genuinely shared; how far the physics intuitions carry is an open question.

### Fock space and second quantization

The Carleman linearization lifts the nonlinear learner into a block-upper-triangular operator on a bosonic Fock space $$\bigoplus_n \text{Sym}^n(\mathbb{R}^N)$$.  "Adding a datapoint" is a creation operator.  The algebraic structure of the symmetric tensor algebra is genuinely identical to that of a bosonic Fock space, which suggests that Fock space tools (metric entropy, complexity measures) may transfer to give graded generalizations of VC/Rademacher complexity.  The companion note develops this in detail.

### Renormalization group flow

The Polchinski exact RG equation maps onto the Volterra hierarchy, with truncation order playing the role of RG scale.  Beta functions $$\beta_n = N \partial_N \mathcal{K}_n$$ describe how the learner tensors flow under coarsening, and their fixed points are **universality classes of learners**.  Early stopping generates order-dependent effective regularization - high-order nonlinearities are more strongly damped - which may explain why early-stopped networks tend to stay close to the kernel regime.


## The bigger picture

The framework developed here is a bet that the right decomposition of learner-data interaction will make a large class of currently informal questions precise.

Here are some:

**What does a learner "know" about its data?**  The learner tensors $$\mathcal{K}_n$$ specify, at each order, which statistical features of the data the learner is sensitive to.  A learner that has nonzero weight at grade $$n$$ "knows" $$n$$-point structure.  The grade profile is a concrete measure of what kind of statistical knowledge the learner has acquired.

**How does distributional shift affect a learner?**  If the data distribution shifts from $$P$$ to $$P'$$, the change in expected prediction is $$\sum_n \frac{1}{n!} \mathcal{K}_n \cdot (M_n' - M_n)$$.  The learner is vulnerable to shifts in the data moments it couples to, and robust to shifts in moments it ignores.  A learner with weight concentrated at low grades is robust to changes in higher-order statistics; one with significant high-grade weight is fragile to them.

**What is the "right" representation of a data distribution for a given learner?**  The coordinates on data space that make the learner tensors simplest.  If there is a basis in which most $$\mathcal{K}_n$$ are sparse or diagonal, that basis reveals the natural features for that learner-data combination.  Finding such a basis is a well-posed optimization problem.

None of these questions are answered here.  The point is that they become *askable* once you have the graded pairing - they have precise mathematical formulations that can, in principle, be analyzed.  This is the infrastructure-building stage: getting the vocabulary right so that the real work can begin.

---

## References

- Roberts & Yaida, *The Principles of Deep Learning Theory* (2022).  The perturbative expansion in $$1/\text{width}$$ that motivated this framework.
- Yang, *Tensor Programs I-V* (2019-2022).  A related perturbative hierarchy, expanding in width via a different formalism.
- Rugh, *Nonlinear System Theory: The Volterra/Wiener Approach* (1981).  Standard reference on Volterra series.
- Boyd & Chua, "Fading memory and the problem of approximating nonlinear operators with Volterra series" (1985).  Approximation theorem for causal fading-memory operators.
- Efron, "How biased is the apparent error rate of a prediction rule?" (1986).  Generalized degrees of freedom and the optimism framework.
- Ye, "On Measuring and Correcting the Effects of Data Mining and Model Selection" (1998).  Extension of generalized degrees of freedom.
- Koh & Liang, "Understanding Black-box Predictions via Influence Functions" (2017).  First-order influence functions for neural networks.
- Hampel, "The influence curve and its role in robust estimation" (1974).  The classical influence function.
- Fernholz, *Von Mises Calculus for Statistical Functionals* (1983).  The von Mises expansion as functional Taylor series.
- Polchinski, "Renormalization and effective Lagrangians" (1984).  The exact RG equation used in the [companion note]({{ site.baseurl }}/Learning-Order-by-Order-Technical-Foundations/).

*Written with Claude.*
