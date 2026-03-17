---
title: "[Notes] Learning, Order by Order: Technical Foundations"
subtitle: "Resolvent algebra, spectral perturbation theory, Fock space, and renormalization group methods"
date: 2026-03-10
math: true
status: "Technical companion"
---

*Research notes from [MATS](https://www.matsprogram.org/) 9.0, under the mentorship of Richard Ngo.  These are Claude-generated documents that I roughly 80% endorse; treat them as research notes rather than polished publications.  I'm posting them mainly to give people a sense of what I'm working on.  Feedback welcome.  Technical companion to [Learning, Order by Order]({{ site.baseurl }}/Learning-Order-by-Order/) - each section here is self-contained and develops one piece of the mathematical machinery.  Prerequisite: the main note's setup (learner tensors $$\mathcal{K}_n$$, graded dual pairing, two hat matrices).*

---

## 1. Two hat matrices: Horner vs Jacobian

### Why this matters

The main note defines two data-dependent matrices that both generalize the kernel hat matrix $$H$$ to the nonlinear setting.  Their difference is the signature of nonlinearity, and getting this difference wrong leads to the wrong capacity measure.  This section pins down the algebra and its consequences.

### The Horner hat matrix

The Volterra series $$\hat{y} = \sum_n \frac{1}{n!} \mathcal{K}_n \cdot y^{\otimes n}$$ can be rewritten by pulling out one factor of $$y$$:

$$\hat{y} = \mathcal{K}_0 + H_{\text{eff}}(y) \cdot y$$

where the **data-dressed hat matrix** (or Horner hat matrix) is

$$H_{\text{eff}}(y)_{ij} = \sum_{n=1}^{\infty} \frac{1}{n!} \sum_{j_2, \ldots, j_n} (\mathcal{K}_n)_{ij\,j_2 \cdots j_n}\; y_{j_2} \cdots y_{j_n}$$

This is a Horner-form evaluation: built from the inside out as

$$H_{\text{eff}}(y) = \mathcal{K}_1 + \bigl[\tfrac{1}{2}\mathcal{K}_2 + [\tfrac{1}{6}\mathcal{K}_3 + \cdots] \cdot y\bigr] \cdot y$$

$$H_{\text{eff}}(y)$$ answers the question: **what linear operator, applied to this particular $$y$$, reproduces the prediction?**  It is the data-dependent matrix that makes $$\hat{y} - \mathcal{K}_0 = H_{\text{eff}}(y) \, y$$ an identity.

### The Jacobian hat matrix

The Jacobian $$J(y)_{ij} = \partial \hat{y}_i / \partial y_j$$ answers a different question: **how does the prediction respond to an infinitesimal perturbation of the data?**  From the Volterra series:

$$J(y)_{ij} = \sum_{n=1}^{\infty} \frac{1}{(n-1)!} \sum_{j_2, \ldots, j_n} (\mathcal{K}_n)_{ij\,j_2 \cdots j_n}\; y_{j_2} \cdots y_{j_n}$$

The coefficient is $$\frac{1}{(n-1)!}$$ rather than $$\frac{1}{n!}$$.  The extra factor of $$n$$ arises because $$\mathcal{K}_n$$ is symmetric in its $$n$$ data indices, so differentiating $$\frac{1}{n!}\mathcal{K}_n \cdot y^{\otimes n}$$ with respect to $$y_j$$ produces $$n$$ identical terms.

### Their relationship

By the product rule on $$\hat{y} = \mathcal{K}_0 + H_{\text{eff}}(y)\, y$$:

$$\boxed{J(y) = H_{\text{eff}}(y) + \frac{\partial H_{\text{eff}}}{\partial y} \cdot y}$$

The Jacobian is the Horner matrix plus a correction for how the dressing itself shifts when data moves.  Define the **nonlinearity tensor**:

$$\Delta(y) := J(y) - H_{\text{eff}}(y) = \frac{\partial H_{\text{eff}}}{\partial y} \cdot y$$

At order $$n$$, the coefficient in $$\Delta(y)$$ is $$\frac{1}{(n-1)!} - \frac{1}{n!} = \frac{n-1}{n!}$$, which vanishes at $$n = 1$$.  So $$\Delta(y) = 0$$ if and only if the learner is linear.  The Frobenius norm $$\lVert\Delta(y)\rVert_F$$ is a pointwise measure of nonlinearity, and its expected value $$\mathbb{E}[\lVert\Delta(y)\rVert_F]$$ measures the average nonlinearity of the learner under the data distribution.

### Why Jacobian trace gives capacity

The standard AIC/optimism argument extends beyond the linear case.  For $$y \sim \mathcal{N}(f^*, \sigma^2 I)$$, Stein's lemma gives:

$$\text{Cov}(\hat{y}_i, y_i) = \sigma^2 \, \mathbb{E}\!\left[\frac{\partial \hat{y}_i}{\partial y_i}\right]$$

The generalized degrees of freedom controlling overfitting are therefore:

$$\text{df} = \mathbb{E}[\text{tr}\, J(y)]$$

If you mistakenly use $$\text{tr}\, H_{\text{eff}}(y)$$ instead, you undercount by $$\text{tr}\, \Delta(y)$$.  For a learner with strong nonlinearity, this error can be large.  The Jacobian trace is the correct capacity because capacity measures **sensitivity to perturbation**, and that is what the Jacobian computes.

The Horner trace has its own interpretation: it measures the fraction of the prediction norm attributable to data (as opposed to the prior $$\mathcal{K}_0$$).  Both are useful; only one is capacity.

### The Horner form as a hierarchy of "kernel" problems

The nested evaluation $$H_{\text{eff}}(y) = \mathcal{K}_1 + [\frac{1}{2}\mathcal{K}_2 + [\frac{1}{6}\mathcal{K}_3 + \cdots] \cdot y] \cdot y$$ has an interpretation as a hierarchy of kernel problems, each correcting the effective kernel seen by the next level.  Read from the inside out:

1. The innermost level defines a kernel from the highest included tensor $$\mathcal{K}_N$$.
2. Contract with $$y$$ to get an operator-valued correction.
3. Add this correction to $$\mathcal{K}_{N-1}$$, producing the effective kernel at the next level out.
4. Repeat until reaching $$\mathcal{K}_1$$.

Each level modifies the *operator* that the next level works with, not the prediction directly.  This is not residual fitting (like boosting, where each stage fits the residual of the previous prediction) but something more like iterative kernel refinement: the effective hat matrix is built up by layering data-dependent corrections onto the base kernel.

When the learner tensors at each order are invertible (a weaker condition than positive definiteness), one can formally "solve" at each level - defining a residual kernel problem at each order.  Invertibility is the relevant condition here, not PSD: the nesting requires that each level's contribution be well-defined as a correction, which needs the operator to have trivial kernel, but does not require a positive inner product.  If in addition the tensors are PSD, each level induces a genuine RKHS and the hierarchy becomes a chain of nested kernel regression problems, each refining the effective kernel in its own reproducing kernel space.

This connects to the continued-fraction structure (§3): adding per-level regularization (replacing polynomial nesting with rational nesting) turns each level into a regularized kernel problem with its own bias-variance tradeoff, and the transfer matrix formalism captures how these tradeoffs compose.


## 2. Self-energy and spectral perturbation theory

### Why this matters

The kernel hat matrix $$H$$ has eigenvalues $$\eta_i \in [0,1]$$ - the learning coefficients.  Each one measures how much the learner retains of the $$i$$-th eigenmode of the kernel.  For a nonlinear learner, the Jacobian $$J(y)$$ has data-dependent eigenvalues $$\eta_i(y)$$ that fluctuate with the data realization.  We need a systematic way to compute how these effective learning coefficients shift relative to their kernel (linear-response) values.  The tool is spectral perturbation theory, organized through the self-energy and Dyson equation.

### The self-energy decomposition

Write the Jacobian as a base-plus-correction:

$$J(y) = \mathcal{K}_1 + \Sigma(y)$$

where the **self-energy** is:

$$\Sigma(y) = \sum_{n=2}^{\infty} \frac{1}{(n-1)!}\, \mathcal{K}_n \cdot y^{\otimes(n-1)}$$

The self-energy is the departure from linear response - the part of the Jacobian that depends on the data.  Its trace gives the capacity correction from nonlinearity: $$\delta\text{df}(y) = \text{tr}\,\Sigma(y)$$.  Its matrix elements $$\Sigma_{ij}(y)$$ encode how data couples different prediction-space directions.

The name "self-energy" is borrowed from quantum field theory, where it plays the same structural role: a correction to the bare propagator that arises from interactions.  Here the "interactions" are the nonlinear couplings $$\mathcal{K}_{n \geq 2}$$, and the "bare propagator" is the kernel linear response $$\mathcal{K}_1$$.

### The Dyson equation

Define the **resolvent** (Green's function) of the Jacobian:

$$G_z(y) = (zI - J(y))^{-1}$$

and the **bare resolvent** (the kernel resolvent):

$$G_z^{(0)} = (zI - \mathcal{K}_1)^{-1}$$

Using the identity $$(A - B)^{-1} = A^{-1} + A^{-1} B (A - B)^{-1}$$ with $$A = zI - \mathcal{K}_1$$ and $$B = \Sigma(y)$$:

$$\boxed{G_z(y) = G_z^{(0)} + G_z^{(0)}\, \Sigma(y)\, G_z(y)}$$

This is the **Dyson equation**.  It says: the full resolvent equals the bare resolvent plus a correction where the self-energy "scatters" the bare resolvent into the full resolvent.  It is exact, not perturbative - but it is implicit (the right-hand side contains $$G_z$$).

### The Born series

Iterating the Dyson equation gives an explicit expansion:

$$G_z(y) = G_z^{(0)} + G_z^{(0)}\,\Sigma\, G_z^{(0)} + G_z^{(0)}\,\Sigma\, G_z^{(0)}\,\Sigma\, G_z^{(0)} + \cdots$$

This is the **Born series**.  The $$k$$-th term has $$k$$ insertions of $$\Sigma$$ between $$k+1$$ bare resolvents.  It converges absolutely when $$\lVert\Sigma(y)\, G_z^{(0)}\rVert_{\text{op}} < 1$$ (operator norm) - when the nonlinear corrections are small relative to the regularized linear response.

The spectral measure $$\rho(z) = -\frac{1}{\pi}\text{Im}\,\text{tr}\, G_{z+i\epsilon}$$ encodes the eigenvalue distribution of $$J(y)$$.  Through the Born series, each insertion of $$\Sigma$$ modifies this spectral measure, giving a systematic expansion of the data-dependent spectrum in powers of the nonlinearity.

### Perturbative eigenvalue shifts

Let $$\{\eta_k^{(0)}, v_k\}$$ be the eigenvalues and eigenvectors of $$\mathcal{K}_1$$ (the kernel learning coefficients and eigenmodes).  Standard matrix perturbation theory (Rayleigh-Schroedinger) gives the shifts:

**First order:**

$$\eta_k(y) \approx \eta_k^{(0)} + \langle v_k, \Sigma(y)\, v_k \rangle$$

Each mode feels the self-energy projected onto itself.  The first-order shift is **diagonal** in the kernel eigenbasis.

**Second order:**

$$\eta_k(y) \approx \eta_k^{(0)} + \langle v_k, \Sigma(y)\, v_k \rangle + \sum_{l \neq k} \frac{|\langle v_k, \Sigma(y)\, v_l \rangle|^2}{\eta_k^{(0)} - \eta_l^{(0)}}$$

The second-order correction involves **off-diagonal** self-energy elements and denominators that diverge at degeneracies.  This expansion assumes non-degenerate kernel eigenvalues; near degeneracies, eigenvector mixing must be treated non-perturbatively (degenerate perturbation theory).  Nearly degenerate kernel modes are strongly mixed by even a small nonlinearity.

### Physical interpretation

The self-energy organizes the answer to the question: **which data modes does the nonlinearity amplify or suppress?**

Expanding $$\Sigma(y)$$ to lowest (quadratic) order:

$$\Sigma(y)_{ij} \approx \sum_k (\mathcal{K}_2)_{ijk}\, y_k$$

The first-order eigenvalue shift for mode $$k$$ is:

$$\delta\eta_k = \sum_l (\mathcal{K}_2)_{klk} \, y_l$$

This has a clear interpretation: the learning coefficient of mode $$k$$ shifts in proportion to the data projected onto $$(\mathcal{K}_2)_{k \cdot k}$$ - the "diagonal slice" of the leading nonlinearity tensor.  Modes of $$\mathcal{K}_2$$ that align with the data increase the effective learning coefficient (the learner pays more attention to those modes); modes that anti-align decrease it.

Taking expectations:

$$\mathbb{E}[\delta\eta_k] = \sum_l (\mathcal{K}_2)_{klk} \, \mathbb{E}[y_l] = (\mathcal{K}_2)_{k \cdot k} \cdot M_1$$

The expected shift is the diagonal slice of $$\mathcal{K}_2$$ contracted with the data mean.  For centered data ($$M_1 = 0$$), the first-order expected shift vanishes and the leading effect comes from second order, involving $$\mathcal{K}_3$$ contracted with the covariance.  This is the capacity correction $$\frac{1}{2} c_2 \cdot \text{Cov}(y)$$ from the main note.

### Distributional shift as self-energy perturbation

The Born series gives a natural framework for transfer learning and distributional shift.  If the data distribution shifts from $$P$$ to $$P' = P + \delta P$$, the expected self-energy shifts: $$\mathbb{E}_{P'}[\Sigma(y)] = \mathbb{E}_P[\Sigma(y)] + \delta\bar{\Sigma}$$, where $$\delta\bar{\Sigma}$$ encodes how the distributional shift modifies the nonlinear corrections to the learner.  The Born series then computes how the resolvent - and hence the spectral structure (learning coefficients, capacity) - shifts in response:

$$\bar{G}_z^{(P')} \approx \bar{G}_z^{(P)} + \bar{G}_z^{(P)} \, \delta\bar{\Sigma} \, \bar{G}_z^{(P)} + \cdots$$

Each term tells you which modes of the learner are most affected by the distributional shift, and whether the shift opens or closes spectral gaps.  Modes where $$\delta\bar{\Sigma}$$ has large diagonal elements (in the kernel eigenbasis) shift the most; modes where $$\delta\bar{\Sigma}$$ has large off-diagonal elements get mixed.

This connects to the K-calculus (§6): the algebraic composition law tells you how learner tensors combine under sequential training on different distributions, while the Born series tells you how the spectral structure responds to the distributional change.  Together, they give complementary algebraic and spectral perspectives on transfer.

### Expected resolvent and effective medium

Taking expectations of the Dyson equation gives:

$$\bar{G}_z = G_z^{(0)} + G_z^{(0)} \, \bar{\Sigma}(z) \, \bar{G}_z$$

where $$\bar{G}_z = \mathbb{E}[G_z(y)]$$ and $$\bar{\Sigma}(z)$$ is the **proper self-energy** - the part of $$\mathbb{E}[\Sigma\, G_z]$$ that cannot be factored through $$\bar{G}_z$$.  Computing $$\bar{\Sigma}$$ requires approximation (it depends on correlations between $$\Sigma$$ and $$G_z$$, which involve the full data distribution).  The simplest approximation - replacing $$\bar{\Sigma}(z)$$ by $$\mathbb{E}[\Sigma(y)]$$ - is the **average-field** or **virtual crystal** approximation, exact to first order in the self-energy.  Higher-order approximations (CPA, etc.) systematically include fluctuation effects.


## 3. Continued fractions and nested hierarchies

### Why this matters

The Volterra framework treats nonlinearity perturbatively: higher-order corrections to a linear base case.  But deep networks have a different structure - they compose many layers, each contributing its own nonlinearity and regularization.  The question is whether the Volterra hierarchy can be organized to capture **depth**.  The answer is yes, through a continued-fraction structure where each level of nesting corresponds to a layer (or a perturbative order), with its own regularization, and the per-mode capacity composes multiplicatively.

### The nested kernel hierarchy

Consider a hierarchy of kernel operators $$K_0, K_1, \ldots, K_M$$ (one per level/layer), coupled through bridge operators $$B_m$$ and per-level regularization parameters $$\lambda_m$$.  The dressed kernel at level $$m$$ satisfies:

$$\tilde{K}_m = K_m + \varepsilon_m\, B_m\, \tilde{H}_{m+1}\, B_m^\top$$

where $$\tilde{H}_{m+1} = \tilde{K}_{m+1}(\tilde{K}_{m+1} + \lambda_{m+1} I)^{-1}$$ is the dressed hat matrix at the next level.  Each level's kernel is augmented by the dressed hat matrix of the level above, projected through the bridge.

This recursion has the same nesting structure as the Horner form $$H_{\text{eff}}(y) = \mathcal{K}_1 + [\frac{1}{2}\mathcal{K}_2 + \cdots]\cdot y$$, but with an inversion $$K \mapsto K(K + \lambda I)^{-1}$$ at each level.  The inversions turn polynomial nesting into **rational** nesting - continued fractions.

### Moebius recursion for per-mode shrinkage

The general hierarchy requires numerical solution because the operators at different levels do not commute.  However, when all $$K_m$$ and $$B_m$$ share an eigenbasis (e.g., in certain architectures or after basis rotation), the per-mode recursion decouples.

In this **commutative case** ($$K_m$$, $$B_m$$ with shared eigenbasis $$\{v_k\}$$, eigenvalues $$\sigma_k^{(m)}$$, coupling strengths $$\beta_k^{(m)}$$), the dressed shrinkage per mode $$k$$ satisfies the scalar recursion:

$$\boxed{\tilde{h}_k^{(m)} = \frac{\sigma_k^{(m)} + \varepsilon_m\, (\beta_k^{(m)})^2\, \tilde{h}_k^{(m+1)}}{\sigma_k^{(m)} + \varepsilon_m\, (\beta_k^{(m)})^2\, \tilde{h}_k^{(m+1)} + \lambda_m}}$$

This is a **Moebius transformation** $$z \mapsto \frac{az + b}{cz + d}$$ in the variable $$\tilde{h}_k^{(m+1)}$$, with $$a = \varepsilon_m (\beta_k^{(m)})^2$$, $$b = \sigma_k^{(m)}$$, $$c = \varepsilon_m (\beta_k^{(m)})^2 + \lambda_m$$, $$d = \sigma_k^{(m)} + \lambda_m$$.

The point is that Moebius transformations compose by matrix multiplication.  Write:

$$T_k^{(m)} = \begin{pmatrix} \varepsilon_m (\beta_k^{(m)})^2 & \sigma_k^{(m)} \\ \varepsilon_m (\beta_k^{(m)})^2 + \lambda_m & \sigma_k^{(m)} + \lambda_m \end{pmatrix}$$

Then the overall per-mode shrinkage is:

$$\tilde{h}_k^{(0)} = \text{Moeb}\!\left(T_k^{(0)}\, T_k^{(1)} \cdots T_k^{(M)}\right)[\tilde{h}_k^{(M+1)}]$$

where $$\text{Moeb}(T)[z] = \frac{T_{11} z + T_{12}}{T_{21} z + T_{22}}$$.  The per-mode capacity of the full hierarchy is encoded in a **transfer matrix product** of $$2 \times 2$$ matrices.

### The $$\frac{1}{4}$$ bound on per-level capacity transmission

How much capacity can a single level transmit?  At level $$m$$ with input shrinkage $$h_{\text{in}}$$ and base eigenvalue $$\sigma$$, regularization $$\lambda$$, the output shrinkage is:

$$h_{\text{out}} = \frac{\sigma + \varepsilon \beta^2 h_{\text{in}}}{\sigma + \varepsilon \beta^2 h_{\text{in}} + \lambda}$$

The **capacity transmission** - the fraction of input capacity passed through - is the derivative $$\partial h_{\text{out}} / \partial h_{\text{in}}$$:

$$\tau = \frac{\varepsilon \beta^2 \lambda}{(\sigma + \varepsilon \beta^2 h_{\text{in}} + \lambda)^2}$$

Since $$\sigma \geq 0$$ and $$h_{\text{in}} \geq 0$$, the denominator satisfies $$(\sigma + \varepsilon \beta^2 h_{\text{in}} + \lambda)^2 \geq (\varepsilon \beta^2 + \lambda)^2$$.  By AM-GM on the numerator factors, $$\varepsilon \beta^2 \cdot \lambda \leq \left(\frac{\varepsilon \beta^2 + \lambda}{2}\right)^2$$, giving:

$$\boxed{\tau \leq \frac{1}{4}}$$

Each level transmits **at most one quarter** of the capacity fed into it.  This bound is tight (achieved when $$\varepsilon \beta^2 = \lambda$$ and $$\sigma = 0$$, i.e., the level's own kernel vanishes and it acts as a pure relay).

### Anderson localization of capacity

Over $$M$$ levels, the per-mode capacity is:

$$\tilde{h}_k^{(0)} = \prod_{m=0}^{M} \tau_k^{(m)} \cdot (\text{source terms})$$

If the per-level transmissions $$\tau_k^{(m)}$$ are independent random variables (e.g., from random initialization), then:

$$\log \tilde{h}_k^{(0)} = \sum_{m=0}^{M} \log \tau_k^{(m)} + \cdots$$

By the law of large numbers, $$\frac{1}{M}\log \tilde{h}_k^{(0)} \to \mathbb{E}[\log \tau_k]$$ as $$M \to \infty$$.  Since $$\tau_k \leq \frac{1}{4}$$, we have $$\log \tau_k \leq -\log 4 < 0$$, so:

$$\tilde{h}_k^{(0)} \sim e^{-\gamma_k M}, \qquad \gamma_k = -\mathbb{E}[\log \tau_k^{(m)}] > 0$$

The capacity in each mode **decays exponentially with depth**, with rate $$\gamma_k$$ (the Lyapunov exponent for mode $$k$$).  This is structurally parallel to **Anderson localization** in disordered systems, where products of random transfer matrices produce exponential decay of quantum-mechanical wavefunctions.  The mathematical structure - products of random $$2 \times 2$$ matrices, Lyapunov exponents, Furstenberg's theorem - is genuinely shared, though how far the physics intuitions carry is an open question.

Not all modes decay equally.  The Lyapunov exponent $$\gamma_k$$ depends on the distribution of $$\tau_k^{(m)}$$, which depends on the per-level eigenvalues $$\sigma_k^{(m)}$$.  Modes with strong eigenvalues at every level have $$\tau_k^{(m)}$$ close to 1 and small $$\gamma_k$$ - these propagate through depth with little attenuation.  Modes with weak eigenvalues have large $$\gamma_k$$ and decay rapidly.

By analogy with the mobility edge in 3D Anderson transitions, one can define a **spectral boundary** separating modes that benefit from depth (small $$\gamma_k$$, capacity propagates) from modes that are better served by a shallow kernel (large $$\gamma_k$$, capacity is exponentially suppressed).  Whether this analogy extends beyond the mathematical level - e.g., whether there are phase transitions in the capacity spectrum as parameters vary - is an open question.

Regardless of the physics analogy, the capacity framework itself gives a concrete criterion for **when depth helps**: a mode benefits from a deeper hierarchy only if its per-level transmission is strong enough to overcome the geometric decay imposed by the $$\frac{1}{4}$$ bound.


## 4. Fock space and Carleman linearization

### Why this matters

Nonlinear learners are hard to analyze because the superposition principle fails: $$\mathcal{K}[y_1 + y_2] \neq \mathcal{K}[y_1] + \mathcal{K}[y_2]$$.  But the Volterra expansion hints at a way to recover linearity by paying for it with dimension.  The idea: lift the data into a larger space where the nonlinear map becomes linear.  This is the **Carleman linearization**, and the larger space turns out to be a **bosonic Fock space** - the same symmetric tensor algebra that underlies the quantum theory of identical bosons.  The algebraic structure (symmetric tensor products, creation/annihilation operators, commutation relations) is identical.  Whether this algebraic coincidence is deep enough to import Fock space *tools* (not just notation) into learning theory is a question this section begins to address.

### The Carleman lift

The Volterra series maps data $$y$$ to prediction $$\hat{y}$$ through the sequence of tensor powers $$y, y^{\otimes 2}, y^{\otimes 3}, \ldots$$  Define the **Carleman state**:

$$|y\rangle\!\rangle = \begin{pmatrix} 1 \\ y \\ y^{\otimes 2} \\ y^{\otimes 3} \\ \vdots \end{pmatrix} \in \bigoplus_{n=0}^{\infty} (\mathbb{R}^N)^{\otimes n}$$

The Volterra series $$\hat{y} = \sum_n \frac{1}{n!} \mathcal{K}_n \cdot y^{\otimes n}$$ is then a **linear** operation on this state:

$$\hat{y} = \mathbf{K} \, |y\rangle\!\rangle, \qquad \mathbf{K} = \begin{pmatrix} \frac{1}{0!}\mathcal{K}_0 & \frac{1}{1!}\mathcal{K}_1 & \frac{1}{2!}\mathcal{K}_2 & \cdots \end{pmatrix}$$

The nonlinear map $$\mathcal{K}$$ has become a linear map $$\mathbf{K}$$ acting on the infinite-dimensional Carleman space.  The cost of linearization is the dimension: $$\mathbb{R}^N$$ becomes $$\bigoplus_n (\mathbb{R}^N)^{\otimes n}$$.

### Block-upper-triangular structure

The Carleman lift is useful beyond predictions.  If the learner itself evolves dynamically (e.g., an iterated map $$y \mapsto f(y)$$), then the induced map on the Carleman state is:

$$|f(y)\rangle\!\rangle = \mathbf{F}\, |y\rangle\!\rangle$$

where $$\mathbf{F}$$ is a **block-upper-triangular** operator on the graded space.  The diagonal block at grade $$n$$ is the $$n$$-th symmetric tensor power $$\text{Sym}^n(\mathcal{K}_1)$$ - the linear response acting independently on each factor.  The off-diagonal blocks involve the higher learner tensors.  The triangularity reflects the same structure as the ODE hierarchy for $$\mathcal{K}_n(t)$$ from the main note: grade $$n$$ is driven by lower grades but does not feed back into them.

Truncating at grade $$N$$ gives a **polynomial kernel** of degree $$N$$.  At $$N = 1$$, this is the NTK (neural tangent kernel) - the linearization of the learner around its initialization.  At $$N = 2$$, you get the NTK plus the leading nonlinear correction (the dNTK of Bai & Lee).  Each additional grade adds one more order of nonlinearity.

### Bosonic Fock space

Since $$\mathcal{K}_n$$ is symmetric in its data indices, only the symmetric part of $$y^{\otimes n}$$ contributes.  The relevant space is therefore:

$$\mathcal{F} = \bigoplus_{n=0}^{\infty} \text{Sym}^n(\mathbb{R}^N)$$

This is a **bosonic Fock space** - the same space that describes systems of identical bosons in quantum mechanics.  The $$n$$-th grade $$\text{Sym}^n(\mathbb{R}^N)$$ is the $$n$$-particle sector.  The "particles" here are data points (or more precisely, data-index contractions), and the symmetry reflects that the order of contraction does not matter.

### Creation and annihilation operators

Define the **creation operator** $$a_j^\dagger$$ that "adds a data point in direction $$j$$":

$$(a_j^\dagger \, \psi)_{i_1 \cdots i_{n+1}} = \text{Sym}(\psi_{i_1 \cdots i_n} \otimes e_j)$$

where $$\text{Sym}$$ symmetrizes over all indices.  The adjoint is the **annihilation operator** $$a_j$$, which removes a data direction by partial trace.  These satisfy the canonical commutation relations:

$$[a_j, a_k^\dagger] = \delta_{jk}, \qquad [a_j, a_k] = [a_j^\dagger, a_k^\dagger] = 0$$

The Carleman state is a **coherent state**:

$$|y\rangle\!\rangle = \exp\!\left(\sum_j y_j\, a_j^\dagger\right)|0\rangle$$

where $$\vert 0\rangle = (1, 0, 0, \ldots)$$ is the vacuum (the "no data" state).  This is the exponential generating function for the symmetric tensor powers.

The learner operator $$\mathbf{K}$$ can be written in second-quantized form:

$$\mathbf{K} = \sum_{n=0}^{\infty} \frac{1}{n!} \sum_{i, j_1, \ldots, j_n} (\mathcal{K}_n)_{i\, j_1 \cdots j_n}\; |i\rangle\, a_{j_1} \cdots a_{j_n}$$

Each term annihilates $$n$$ data quanta and produces a prediction component.  The learner is a Fock space operator that converts data quanta into predictions.

### Metric entropy as complexity

Each learner tensor $$\mathcal{K}_n$$ induces a reproducing kernel Hilbert space $$\mathcal{H}^{(n)}$$ of functions on $$\mathcal{X}^n$$ (where $$\mathcal{X}$$ is the data domain).  The function class at order $$n$$ consists of all $$n$$-linear forms with coefficients in the symmetric part of $$\mathcal{K}_n$$.

The **metric entropy** of the unit ball of $$\mathcal{H}^{(n)}$$ under the data distribution $$P$$ - the logarithm of the covering number at scale $$\epsilon$$ - is a complexity measure for the $$n$$-th order learner.  Summing across orders gives a total complexity:

$$\mathcal{C}(\epsilon) = \sum_{n=0}^{\infty} \log \mathcal{N}(\epsilon, \mathcal{H}^{(n)}, L_2(P))$$

This generalizes VC dimension and Rademacher complexity to the nonlinear setting.  At $$n = 1$$, it reduces to the standard kernel complexity.  At higher orders, it measures the complexity of the genuinely nonlinear components.  The grading by $$n$$ means that complexity decomposes along the same axis as the learner-data pairing: each order of nonlinearity has its own complexity budget.

The connection to standard learning-theoretic quantities is via Dudley's entropy integral: the Rademacher complexity of the learner at order $$n$$ is bounded by $$\int_0^{\infty} \sqrt{\frac{\log \mathcal{N}(\epsilon, \mathcal{H}^{(n)}, L_2(P))}{N_{\text{data}}}} \, d\epsilon$$.  The total generalization bound decomposes as a sum over orders, with higher orders paying exponentially more in sample complexity.


## 5. Renormalization group and Polchinski flow

### Why this matters

The Volterra series has a natural truncation parameter: the maximum order $$N$$.  As $$N$$ increases, more nonlinear structure is included, and the learner tensors must adjust to accommodate the newly included orders.  This is exactly the structure of the renormalization group (RG): a flow parameterized by a scale (here $$N$$), describing how effective parameters change as you integrate in or out degrees of freedom.  The Polchinski exact RG equation provides the technology to analyze this flow.  The payoff is a classification of learner behaviors into universality classes - broad families of learners that flow to the same fixed point under coarsening.

### The dictionary

The Polchinski RG equation describes how the effective action $$S_\Lambda$$ of a field theory changes as the UV cutoff $$\Lambda$$ is lowered.  The map to the Volterra hierarchy is:

| Field theory | Volterra framework |
|---|---|
| Effective action $$S_\Lambda$$ | Learner functional $$\mathcal{K}_N$$ (truncated at order $$N$$) |
| Field $$\phi$$ | Data $$y$$ |
| UV cutoff $$\Lambda$$ | Truncation order $$N$$ |
| Propagator $$C_\Lambda$$ | Kernel matrix $$K$$ |
| Coupling constants | Learner tensor components $$(\mathcal{K}_n)_{ij\ldots}$$ |
| Relevant operators | Low-order learner tensors that grow under flow |
| Irrelevant operators | High-order learner tensors that shrink under flow |

The "scale" here is not spatial or energetic but **order of nonlinearity**.  "Coarsening" means integrating out high-order nonlinear structure, retaining only its effective contribution to lower orders.  This is what happens when you approximate a nonlinear learner by a polynomial truncation: the truncated tensors absorb effective corrections from the discarded higher orders.

### Beta functions

Define the **beta functions** for the learner tensors:

$$\beta_n = N \frac{\partial \mathcal{K}_n}{\partial N}$$

These describe how the $$n$$-th order learner tensor changes as the truncation order $$N$$ is varied.  Concretely, if you compute $$\mathcal{K}_n^{\text{eff}}$$ by integrating out all orders above $$N$$ and absorbing their effects into the remaining tensors, $$\beta_n$$ describes the rate of change.

By analogy with the Polchinski equation, the beta functions should take the form (at leading order):

$$\beta_n \sim \sum_{p+q=n+2} \mathcal{K}_p \cdot K \cdot \mathcal{K}_q$$

This is conjectural - it follows from the dictionary above if the correspondence is exact, but has not been derived independently.  The structure is quadratic in the tensors (as in the Polchinski equation, which is quadratic in the couplings) with the kernel playing the role of the propagator.

### Fixed points and universality classes

A **fixed point** of the beta functions is a set of learner tensors $$\{\mathcal{K}_n^*\}$$ satisfying $$\beta_n(\mathcal{K}^*) = 0$$ for all $$n$$.  The Gaussian fixed point $$\mathcal{K}_n^* = 0$$ for $$n \geq 2$$ (the pure kernel learner) is always a fixed point.  Other fixed points correspond to **universality classes of learners** - families of learners that, despite differing in microscopic detail, have the same macroscopic behavior at coarse scales.

Near a fixed point, linearizing the beta functions gives **scaling dimensions** for each learner tensor:

$$\beta_n \approx (n - n_*)\, \mathcal{K}_n + \cdots$$

where $$n_*$$ is a critical dimension.  Tensors with $$n < n_*$$ are **relevant** (they grow under the flow and must be tracked); tensors with $$n > n_*$$ are **irrelevant** (they shrink and can be neglected at long "scales").  This is a precise version of the intuition that high-order nonlinearities matter less than low-order ones, but with corrections: the scaling dimensions can be anomalous, shifted from naive dimensional counting by the fixed-point couplings.

### Capacity conservation conjecture

In the field-theory RG, conserved quantities constrain the flow.  The analog here is capacity.

**Conjecture:** The total capacity $$\mathcal{C} = \sum_n \mathcal{C}_n$$, where $$\mathcal{C}_n$$ is the capacity contribution from order $$n$$, is **conserved** under the Polchinski flow.  Capacity shifts between orders but is neither created nor destroyed.

If true, this would mean that truncating high-order terms does not lose total capacity - it redistributes it into effective corrections to lower-order capacity tensors.  The conjecture is motivated by the following: the total capacity $$\text{tr}\, J(y)$$ is a property of the full learner $$\mathcal{K}$$, independent of how it is decomposed into orders.  If the RG flow is a reparametrization that preserves the full learner functional while changing the order-by-order decomposition, total capacity should be invariant.

The conjecture would fail if the truncation introduces approximation error that leaks capacity.  Testing it - analytically for simple learners, numerically for networks - is an open problem.

### Early stopping as order-dependent regularization

Training for time $$t$$ generates order-dependent effective regularization.  From the linear case, $$\eta_i(t) = 1 - e^{-\mu_i t}$$, so finite $$t$$ acts as regularization.  For the nonlinear terms, the triangular hierarchy means that $$\mathcal{K}_n(t)$$ activates later than $$\mathcal{K}_1(t)$$ (it needs the lower orders to be established first).  At any finite training time, high-order tensors are more strongly suppressed than low-order ones.

This is an **order-dependent regularization**: early stopping damps high-order nonlinearities more than low-order ones.  In the RG picture, it means that early stopping biases the learner toward the Gaussian fixed point (the pure kernel learner).  The crossover time $$t_n^*$$ at which $$\mathcal{K}_n(t)$$ becomes significant marks the transition from the kernel regime to the $$n$$-th order nonlinear regime.

This may explain the empirical observation that early-stopped networks often behave similarly to kernel methods: they have not trained long enough for the higher-order tensors to activate.  The RG interpretation sharpens this - it says that the "kernel regime" is the basin of attraction of the Gaussian fixed point, and early stopping keeps the learner within that basin.


## 6. Composition laws and K-calculus

### Why this matters

A single learner is described by its tensor hierarchy $$\{\mathcal{K}_n\}$$.  But learning algorithms compose: SGD is a composition of mini-batch steps; curriculum learning composes learners trained on different distributions; transfer learning composes pre-training with fine-tuning.  We need rules for how learner tensors compose under these operations.  The result is a "calculus of learners" - algebraic rules for combining, decomposing, and transforming learner descriptors.

### The Faa di Bruno formula for composed learners

If learner $$\mathcal{A}$$ is followed by learner $$\mathcal{B}$$ (composing their functionals: $$\mathcal{C} = \mathcal{B} \circ \mathcal{A}$$), the $$n$$-th learner tensor of the composition is:

$$\boxed{(\mathcal{C})_n = \sum_{k=1}^{n} (\mathcal{B})_k \cdot B_{n,k}\!\left((\mathcal{A})_1,\; (\mathcal{A})_2,\; \ldots,\; (\mathcal{A})_{n-k+1}\right)}$$

where $$B_{n,k}$$ are the **partial Bell polynomials** - the combinatorial objects that organize the higher-order chain rule.  The Bell polynomial $$B_{n,k}(x_1, \ldots, x_{n-k+1})$$ enumerates all ways to partition $$n$$ items into $$k$$ nonempty blocks, with the block sizes weighted by the $$x_i$$.

### Worked orders

**Order 1:**

$$(\mathcal{C})_1 = (\mathcal{B})_1 \cdot (\mathcal{A})_1$$

Matrix multiplication.  The linear responses compose as matrices.  This is the chain rule at first order and recovers the fact that composed linear maps are linear.

**Order 2:**

$$(\mathcal{C})_2 = (\mathcal{B})_1 \cdot (\mathcal{A})_2 + (\mathcal{B})_2 \cdot \bigl[(\mathcal{A})_1 \otimes (\mathcal{A})_1\bigr]$$

Two terms, corresponding to two sources of quadratic nonlinearity in the composition:
1. $$(\mathcal{B})_1 \cdot (\mathcal{A})_2$$: the inner learner $$\mathcal{A}$$ is quadratic, and the outer learner $$\mathcal{B}$$ passes it through linearly.
2. $$(\mathcal{B})_2 \cdot [(\mathcal{A})_1 \otimes (\mathcal{A})_1]$$: both inner contributions are linear, but the outer learner combines them quadratically.

**Order 3:**

$$(\mathcal{C})_3 = (\mathcal{B})_1 \cdot (\mathcal{A})_3 + (\mathcal{B})_2 \cdot \bigl[(\mathcal{A})_1 \otimes (\mathcal{A})_2 + (\mathcal{A})_2 \otimes (\mathcal{A})_1\bigr] + (\mathcal{B})_3 \cdot \bigl[(\mathcal{A})_1^{\otimes 3}\bigr]$$

Three sources: (i) inner cubic, outer linear; (ii) inner produces one linear and one quadratic output, outer combines them quadratically; (iii) inner is purely linear but outer combines three copies cubically.  The Bell polynomial structure enumerates all such partitions.

### The graded monoid

The Faa di Bruno composition gives the space of learner descriptors $$\mathcal{L} = \bigoplus_n \text{Sym}^n(\mathbb{R}^N)^* \otimes \mathbb{R}^M$$ a **graded monoid structure**.  The identity element is $$(\mathcal{K}_0 = 0, \mathcal{K}_1 = I, \mathcal{K}_{n \geq 2} = 0)$$ - the identity map.

Properties:
- **Associative**: $$(A \circ B) \circ C = A \circ (B \circ C)$$, inherited from function composition.
- **Not commutative**: $$\mathcal{B} \circ \mathcal{A} \neq \mathcal{A} \circ \mathcal{B}$$ in general.
- **Graded**: the composition law respects the grading.  The $$n$$-th tensor of the composition depends on tensors of order $$\leq n$$ from both factors.  You never need order $$> n$$ to compute order $$n$$.
- **Not a group**: generic learner functionals are not invertible, so there is no general inverse.

In the kernel case (all tensors zero except grade 1), the monoid reduces to the **multiplicative monoid of matrices** - composition is matrix multiplication.  The Faa di Bruno structure is the nonlinear generalization of matrix multiplication.

### Composition rules for common operations

The monoid structure gives algebraic rules for relating different learning procedures:

**SGD vs GD.**  A single SGD step on mini-batch $$B$$ is a learner $$\mathcal{K}^{(B)}$$.  The full-batch GD learner is $$\mathcal{K}^{(\text{full})}$$.  If mini-batches are sampled uniformly, the expected SGD step is:

$$\mathbb{E}_B[(\mathcal{K}^{(B)})_n] \neq (\mathcal{K}^{(\text{full})})_n \quad \text{for } n \geq 2$$

The difference arises because averaging a composition (the Faa di Bruno product of multiple SGD steps) is not the same as composing the averages - this is Jensen's inequality for a nonlinear operation.  At first order, the expected SGD step matches GD (the linear responses average correctly).  At second order and above, the noncommutativity of composition introduces a correction proportional to the variance of the mini-batch tensors.  This is a Volterra-language description of the familiar observation that SGD's noise induces implicit regularization; the framework does not explain it so much as organize it - identifying which tensor orders are affected and by how much.

**Curriculum learning.**  Training on distribution $$P_1$$ for time $$t_1$$, then switching to $$P_2$$ for time $$t_2$$, gives a composed learner $$\mathcal{K}_{t_2}^{(P_2)} \circ \mathcal{K}_{t_1}^{(P_1)}$$.  The Faa di Bruno formula decomposes the composed tensors into contributions from each phase.  The grade profile of the composed learner reflects both the ordering of the curriculum and the grade profiles of the individual phases.

**Transfer learning.**  Pre-training produces a learner $$\mathcal{A}$$ (with trained tensors $$\{(\mathcal{A})_n\}$$); fine-tuning applies a learner $$\mathcal{B}$$ on top.  The composed learner $$\mathcal{B} \circ \mathcal{A}$$ has tensors given by the Faa di Bruno formula.  The first-order transfer is $$(\mathcal{B})_1 \cdot (\mathcal{A})_1$$ - the fine-tuner's linear response modulated by the pre-trainer's linear response.  Higher-order transfer involves the nonlinear interactions between the two stages.

A subtlety: post-training operates not on raw data but on the pre-trainer's representations.  The relevant data distribution for the post-training learner $$\mathcal{B}$$ is the **pushforward** $$\mathcal{A}_* P$$ - the distribution over the pre-trainer's outputs.  The data moment tensors for $$\mathcal{B}$$ are therefore $$M_n^{(\mathcal{B})} = \mathbb{E}_P[(\mathcal{A}[y])^{\otimes n}]$$, which themselves depend on $$\mathcal{A}$$'s learner tensors composed with the original data moments via the graded pairing.  This gives a recursive structure: the data geometry seen by the post-trainer is itself a function of the pre-trainer's learner geometry.  The Born series perspective (§2) complements this by describing how the spectral structure shifts when the effective distribution changes from $$P$$ to $$\mathcal{A}_* P$$.

### The meta-kernel trick

The Volterra expansion maps a nonlinear learner $$\mathcal{K}$$ into a graded space $$\mathcal{L}$$ where the expected prediction is a linear functional (the graded pairing with data descriptors $$\mathcal{D}$$).  This is structurally parallel to the kernel trick:

| Kernel trick | Volterra linearization |
|---|---|
| Maps **data** into feature space | Maps **learner** into descriptor space |
| Learner acts linearly in feature space | Data coupling is linear in descriptor space |
| Feature map: $$x \mapsto \phi(x)$$ | Learner map: $$\mathcal{K} \mapsto (\mathcal{K}_0, \mathcal{K}_1, \ldots)$$ |
| Inner product: $$\langle \phi(x), \phi(x') \rangle = k(x, x')$$ | Pairing: $$\langle \mathcal{L}, \mathcal{D} \rangle = \mathbb{E}[\hat{y}]$$ |

The kernel trick linearizes the **data side** at the cost of dimension.  The Volterra expansion linearizes the **learner side** at the cost of dimension.  Together, they suggest a doubly-linearized picture where both learner and data live in infinite-dimensional graded spaces, and the full learner-data interaction is a bilinear pairing between them.

The Faa di Bruno composition law is the "multiplication" in learner descriptor space.  It plays the same role as the kernel product $$k \cdot k'$$ in data feature space.  The monoid structure on $$\mathcal{L}$$ (from Faa di Bruno) and the commutative algebra structure on $$\mathcal{D}$$ (from the tensor product of distributions) are dual structures, coupled through the graded pairing.


## 7. Connected kernels and cumulant pairing

### Why this matters

Moments and cumulants are different coordinate systems on distribution space.  The moment expansion $$\mathbb{E}[\hat{y}] = \sum \frac{1}{n!} \mathcal{K}_n \cdot M_n$$ uses moments; switching to cumulants reshuffles the learner tensors.  The reshuffled tensors - the **connected Volterra kernels** - turn out to be the natural objects for capacity, RG flows, and the Fock space interpretation.  They strip out the "disconnected" contributions (products of lower-order effects) and isolate the genuinely $$n$$-body nonlinear interactions.

### The moment-cumulant relation

The standard moment-cumulant relation expresses moments as sums over set partitions of products of cumulants:

$$M_n = \sum_{\pi \in \Pi(n)} \prod_{B \in \pi} \kappa_{|B|}$$

where $$\Pi(n)$$ is the set of all partitions of $$\{1, \ldots, n\}$$ and $$\kappa_m = \kappa_m(P)$$ is the $$m$$-th cumulant tensor.  The inverse relation expresses cumulants in terms of moments via the Moebius function on the partition lattice.

Substituting into the expected prediction:

$$\mathbb{E}[\hat{y}] = \sum_{n=0}^{\infty} \frac{1}{n!}\, \mathcal{K}_n \cdot \sum_{\pi \in \Pi(n)} \prod_{B \in \pi} \kappa_{|B|}$$

Rearranging (grouping by the cumulant structure rather than by the moment order) gives:

$$\mathbb{E}[\hat{y}] = \sum_{n=0}^{\infty} \frac{1}{n!}\, \mathcal{K}_n^c \cdot \kappa_n$$

where the **connected Volterra kernel** $$\mathcal{K}_n^c$$ is the learner tensor reshuffled to pair naturally with cumulants.

### Definition of connected kernels

The connected kernels are defined by the inversion of the moment-cumulant relation applied to the learner side:

$$\mathcal{K}_n = \sum_{\pi \in \Pi(n)} \prod_{B \in \pi} \mathcal{K}_{|B|}^c$$

or equivalently (by Moebius inversion on the partition lattice):

$$\mathcal{K}_n^c = \sum_{\pi \in \Pi(n)} (-1)^{|\pi|-1} (|\pi|-1)! \prod_{B \in \pi} \mathcal{K}_{|B|}$$

Order by order:
- $$\mathcal{K}_1^c = \mathcal{K}_1$$ (the linear response is already connected)
- $$\mathcal{K}_2^c = \mathcal{K}_2 - \mathcal{K}_1 \otimes \mathcal{K}_1$$ (subtract the disconnected part)
- $$\mathcal{K}_3^c = \mathcal{K}_3 - 3\,\mathcal{K}_2 \otimes \mathcal{K}_1 + 2\,\mathcal{K}_1^{\otimes 3}$$

(Here the tensor products and subtractions require care about index placement.  The products $$\mathcal{K}_p \otimes \mathcal{K}_q$$ are taken with appropriate symmetrization over the data indices.)

### Why connected kernels are natural

**For capacity:** The capacity tensors $$c_m = \text{tr}_1(\mathcal{K}_{m+1})$$ pick up only the connected part of the $$(m+1)$$-th learner tensor when contracted with cumulants.  The disconnected pieces produce contributions that can be expressed in terms of lower-order capacity tensors.  So the capacity corrections from nonlinearity are organized by the connected kernels:

$$\delta\text{df} = \sum_{m=1}^{\infty} \frac{1}{m!}\, \text{tr}_1(\mathcal{K}_{m+1}^c) \cdot \kappa_m$$

Each connected kernel captures the genuinely new capacity contribution at that order.

**For RG:** The Polchinski flow equation is naturally expressed in terms of connected couplings.  The beta functions simplify: the connected learner tensors do not mix with products of lower-order tensors under the flow.  This is the same reason that in field theory, the effective action (generating function for connected correlators) has simpler RG equations than the partition function (generating function for full correlators).

**For the Fock space:** The connected kernels correspond to **normal-ordered** operators in the Fock space.  Normal ordering subtracts vacuum expectation values (lower-order contributions), leaving only the genuinely interacting part.  The complexity measure $$\mathcal{C}_n = \log \mathcal{N}(\epsilon, \mathcal{H}^{(n)}_c, L_2(P))$$ for the connected kernel's RKHS measures the genuinely $$n$$-body complexity, not contaminated by lower-order effects.

### The connected-cumulant pairing

The graded pairing rewrites as:

$$\boxed{\mathbb{E}[\hat{y}] = \sum_{n=0}^{\infty} \frac{1}{n!}\, \mathcal{K}_n^c \cdot \kappa_n}$$

Connected learner kernels pair with cumulants.  Disconnected learner kernels pair with moments.  The two decompositions are related by the moment-cumulant resummation on both sides simultaneously.

This is the analog of the linked-cluster theorem in field theory: the logarithm of the partition function (the free energy) is a sum over connected diagrams only.  Here, the "free energy" is $$\log \mathbb{E}[e^{\mathcal{K}[y]}]$$ (the cumulant generating function of the prediction), and its cumulant expansion involves only the connected kernels $$\mathcal{K}_n^c$$.


## 8. Open questions and conjectures

### Capacity conservation

Does total capacity $$\mathcal{C} = \sum_n \mathcal{C}_n$$ remain invariant under the Polchinski flow?  If so, the total overfitting budget of a learner is a topological invariant of its universality class - independent of the truncation order used to analyze it.  A proof would likely use the trace structure of the capacity tensors and the quadratic form of the Polchinski equation.  A counterexample would indicate that truncation introduces genuine information loss, not just reparametrization.

### Per-order regularization in the Volterra expansion

The nested kernel hierarchy has per-level regularization $$\lambda_m$$, producing continued fractions.  The Horner form of the Volterra series has no such regularization - it is polynomial, not rational.  Is there a natural way to introduce per-order regularization into the Volterra expansion, turning the polynomial nesting into a continued fraction?  This would unify the two hierarchies (Volterra order and depth) into a single framework.

### Anomalous dimensions

Near the Gaussian fixed point, the naive scaling dimension of $$\mathcal{K}_n$$ is $$n$$ (each additional order is suppressed by one power of data scale).  Interactions shift this to $$n + \gamma_n$$ where $$\gamma_n$$ is the **anomalous dimension**.  Computing $$\gamma_n$$ for specific learner architectures would determine which nonlinear orders are more or less relevant than dimensional analysis suggests.  For learners with strong low-order nonlinearities, $$\gamma_n$$ could be negative for some $$n$$, making those orders more relevant than expected.

### Spectral boundary for depth benefit

The transfer matrix analysis (Section 3) identifies a spectral boundary separating modes that benefit from depth from those that do not.  Computing this boundary for specific architectures (e.g., ResNets with skip connections, Transformers with attention) would give testable predictions about which features are learned via depth and which are already available in a shallow kernel.  Skip connections should shift the boundary by providing direct (non-attenuated) pathways for some modes.

### Optimal coordinates

Given a learner $$\mathcal{K}$$ and a data distribution $$P$$, what coordinate system on $$\mathcal{D}$$ (the data descriptor space) makes the learner tensors $$\{\mathcal{K}_n\}$$ simplest?  "Simplest" could mean: sparsest, most diagonal, lowest effective rank.  Finding such coordinates is a well-posed optimization problem, and the solution would reveal the natural features for a given learner-data pair.  For the kernel case, the answer is the kernel eigenbasis.  For a nonlinear learner, it should depend on the higher-order tensors.

### The bi-graded expansion

The Volterra order $$n$$ (nonlinearity in data) and the $$1/\text{width}$$ expansion from PDLT (finite-width corrections to the kernel limit) are independent gradings.  A full treatment should be bi-graded: each term labeled by both Volterra order and width order.  The Faa di Bruno formula mixes these across layers.  Working out the bi-graded structure explicitly, and understanding how the two truncation parameters interact, would clarify when width and when depth is the bottleneck for learning a given $$n$$-point data structure.

### Convergence

The Volterra series is a formal power series.  Under what conditions does it converge?  The Boyd-Chua theorem guarantees uniform approximability for fading-memory causal operators, but convergence of the full series (not just truncations) requires analyticity of $$\mathcal{K}$$ in a suitable sense.  For neural networks with smooth activations (GELU, softplus), analyticity is plausible.  ReLU networks are piecewise linear and not strictly smooth, but ReLU is the $$\epsilon \to 0$$ limit of smooth approximations, and the Volterra expansion applies to any such smoothing.  Whether the Volterra series of smooth approximations converges term-by-term to something useful for ReLU networks is itself an open question.  The convergence radius, when finite, measures how far the learner's behavior extends from its linearization.

### Mori-Zwanzig decomposition

The Volterra hierarchy naturally splits into "slow" (low-order, large-eigenvalue) and "fast" (high-order, small-eigenvalue) subspaces.  The Mori-Zwanzig projection formalism should give an exact equation for the slow subspace, with a memory kernel encoding the back-reaction of fast modes.  This would explain why perturbing high-order features can non-locally affect low-order behaviors - through the memory kernel's off-diagonal elements.  Deriving this memory kernel explicitly for simple architectures is feasible and would connect to empirical observations about feature entanglement.

---

*Technical companion to [Learning, Order by Order]({{ site.baseurl }}/Learning-Order-by-Order/).  Written with Claude.*
