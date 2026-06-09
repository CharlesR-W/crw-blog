# The Kolmogorov 1941 (K41) Theory of Turbulence

> *Part 1 of a series on turbulence theory, following Frisch's* Turbulence: The Legacy of A.N. Kolmogorov.

This tutorial develops the K41 theory from its axioms to its principal results, including a detailed derivation of the four-fifths law --- the only exact, nontrivial result in fully developed turbulence. We also explain why K41 cannot be the final word (Landau's objection), setting the stage for the intermittency corrections covered in later tutorials.

---

## 1. Setup: The Equations of Motion

### 1.1 Incompressible Navier-Stokes with Forcing

We work with the incompressible Navier-Stokes equations on a periodic domain $\mathbb{T}^3 = [0, L]^3$:

$$\partial_t v_i + v_j \partial_j v_i = -\partial_i p + \nu \Delta v_i + f_i,$$

$$\partial_i v_i = 0,$$

where $v_i(\mathbf{r}, t)$ is the velocity field, $p(\mathbf{r}, t)$ the pressure (divided by density), $\nu$ the kinematic viscosity, and $f_i(\mathbf{r}, t)$ an external forcing that injects energy at large scales. Repeated indices are summed. The pressure is not an independent dynamical variable: incompressibility $\nabla \cdot \mathbf{v} = 0$ determines it as a functional of $\mathbf{v}$ via a Poisson equation obtained by taking the divergence of the momentum equation.

The forcing $f_i$ is taken to be a statistically stationary, homogeneous, isotropic random field with support concentrated at wavenumbers $|\mathbf{k}| \sim k_f \sim 1/L_0$, where $L_0$ is the *integral scale* (the scale of the largest eddies). The forcing does two things: it injects energy at rate $\varepsilon_{\text{in}}$, and it breaks the time-reversal and other symmetries of the Euler equations. In the statistically stationary state, the mean energy injection rate equals the mean dissipation rate:

$$\varepsilon_{\text{in}} = \langle f_i v_i \rangle = \nu \langle |\nabla \mathbf{v}|^2 \rangle = \varepsilon.$$

Here $\langle \cdot \rangle$ denotes an ensemble average (or, equivalently by ergodicity, a space-time average in the stationary state).

### 1.2 The Reynolds Number and Scale Separation

The Reynolds number is

$$\mathrm{Re} = \frac{U L_0}{\nu},$$

where $U$ is a characteristic velocity at the integral scale (e.g., $U = \sqrt{\langle |\mathbf{v}|^2 \rangle}$). Fully developed turbulence corresponds to $\mathrm{Re} \gg 1$. In this regime, there is an enormous separation between the scale $L_0$ at which energy is injected and the *Kolmogorov dissipation scale*

$$\eta = \left(\frac{\nu^3}{\varepsilon}\right)^{1/4}$$

at which viscosity becomes important. The ratio is $L_0/\eta \sim \mathrm{Re}^{3/4}$. The range of scales $\eta \ll \ell \ll L_0$ is the **inertial range**, where neither forcing nor dissipation plays a direct role, and the dynamics is governed by the nonlinear energy transfer (cascade) alone.

### 1.3 Velocity Increments: The Fundamental Object

The central objects in the K41 theory are not the velocities themselves but the **velocity increments**:

$$\delta v_i(\mathbf{r}, \boldsymbol{\ell}) = v_i(\mathbf{r} + \boldsymbol{\ell}) - v_i(\mathbf{r}).$$

Here $\boldsymbol{\ell}$ is a spatial separation vector. The increment isolates the contribution of scales $\sim |\boldsymbol{\ell}|$ to the velocity field: by subtracting $v_i(\mathbf{r})$, we remove the contributions of scales much larger than $|\boldsymbol{\ell}|$ (which are nearly uniform over the separation), leaving only the fluctuations at scale $\sim |\boldsymbol{\ell}|$ and smaller.

The **longitudinal velocity increment** is the component of $\delta \mathbf{v}$ along the separation direction:

$$\delta v_\|(\boldsymbol{\ell}) = \frac{\delta v_i(\mathbf{r}, \boldsymbol{\ell})\, \ell_i}{|\boldsymbol{\ell}|}.$$

The **structure functions** of order $p$ are

$$S_p(\ell) = \langle |\delta v_\|(\boldsymbol{\ell})|^p \rangle = \langle |\delta v_\|(\ell)|^p \rangle,$$

where the second equality holds when the statistics are isotropic (so the result depends only on $\ell = |\boldsymbol{\ell}|$). These are the quantities that K41 makes predictions about.

Why increments rather than the velocity itself? Three reasons:

1. **Galilean invariance.** The increment $\delta \mathbf{v}$ is invariant under uniform boosts $\mathbf{v} \to \mathbf{v} + \mathbf{U}_0$, while $\mathbf{v}$ is not. Since the Navier-Stokes equations are Galilean-invariant, the physically meaningful statistics should be too.

2. **Infrared insensitivity.** In the infinite-volume limit, $\langle |\mathbf{v}|^2 \rangle$ can diverge (the energy integral $\int E(k)\, dk$ may not converge at small $k$), but the structure functions are well-defined because the subtraction removes the infrared divergence.

3. **Scale locality.** The increment at separation $\ell$ probes the velocity fluctuations at scale $\sim \ell$, which is exactly what we need to study the cascade.

---

## 2. The Three Hypotheses

Kolmogorov's 1941 theory rests on three hypotheses about the statistical properties of the velocity field in the limit $\mathrm{Re} \to \infty$. These hypotheses formalize Richardson's qualitative picture of the energy cascade: energy injected at large scales is transferred to successively smaller scales by the nonlinear term, until it reaches the dissipation scale where viscosity converts it to heat.

### 2.1 Hypothesis H1: Local Isotropy and Symmetry Restoration

> **H1.** *In the limit $\mathrm{Re} \to \infty$, all small-scale statistical properties of the turbulent velocity field are uniquely determined by the mean dissipation rate $\varepsilon$ and the viscosity $\nu$. Furthermore, at scales $\ell \ll L_0$, the statistics of velocity increments are homogeneous and isotropic, regardless of any anisotropy or inhomogeneity in the large-scale forcing or boundary conditions.*

**Physical meaning.** The large-scale flow "knows" about the forcing: if the stirring is anisotropic, the large-scale eddies will be anisotropic. But the cascade process --- the successive breaking of large eddies into smaller ones through the nonlinear term --- involves many steps as we move from scale $L_0$ down to scale $\ell$. Each step scrambles the directional information a little. After sufficiently many steps (i.e., for $\ell \ll L_0$), the memory of the large-scale anisotropy is lost, and the small-scale statistics become isotropic. This is analogous to the central limit theorem: many weakly correlated steps produce a universal outcome.

H1 is sometimes decomposed into:
- **Local homogeneity**: the statistics of $\delta \mathbf{v}(\mathbf{r}, \boldsymbol{\ell})$ do not depend on $\mathbf{r}$ for $|\boldsymbol{\ell}| \ll L_0$.
- **Local isotropy**: the statistics depend only on $\ell = |\boldsymbol{\ell}|$, not on the direction of $\boldsymbol{\ell}$.

The hypothesis also asserts *universality*: the only parameters that matter at small scales are $\varepsilon$ and $\nu$. All other details of the forcing and boundary conditions are irrelevant. This is a very strong claim, and as we will see in Section 6, Landau immediately questioned it.

### 2.2 Hypothesis H2: Self-Similarity in the Inertial Range

> **H2.** *In the inertial range $\eta \ll \ell \ll L_0$, the statistics of velocity increments are self-similar with a unique scaling exponent $h$: for any $\lambda \in (0, 1)$,*
> $$\delta v_i(\mathbf{r}, \lambda \boldsymbol{\ell}) \stackrel{\text{law}}{=} \lambda^h\, \delta v_i(\mathbf{r}, \boldsymbol{\ell}),$$
> *where $\stackrel{\text{law}}{=}$ denotes equality in distribution (i.e., all joint probability distributions agree).*

**Physical meaning.** In the inertial range, neither forcing (which acts at scale $L_0$) nor viscosity (which acts at scale $\eta$) is directly relevant. The dynamics is purely inertial: the nonlinear term $v_j \partial_j v_i$ transfers energy from scale $\ell$ to scale $\ell' < \ell$ without any characteristic scale of its own. This suggests that the inertial range is *scale-invariant*: a change of spatial scale $\boldsymbol{\ell} \to \lambda \boldsymbol{\ell}$ can be compensated by a rescaling of the velocity increments $\delta \mathbf{v} \to \lambda^h \delta \mathbf{v}$.

The exponent $h$ is called the **Hurst exponent** or **roughness exponent**. It controls how "rough" the velocity field is: if $h < 1$, the field is Holder continuous with exponent $h$ but not differentiable. As we will see, K41 predicts $h = 1/3$, so the velocity field in fully developed turbulence is extremely rough --- much rougher than, say, Brownian motion ($h = 1/2$).

A direct consequence of H2 is that all structure functions are pure power laws in the inertial range:

$$S_p(\ell) = \langle |\delta v_\|(\ell)|^p \rangle \propto \ell^{ph} = \ell^{\zeta_p},$$

with $\zeta_p = ph$. This is the simplest possible scaling --- a straight line when $\zeta_p$ is plotted against $p$. As we will see, experiments show that $\zeta_p$ is actually a *concave* function of $p$ (anomalous scaling), which means H2 is not exactly correct. But it is an excellent zeroth-order approximation.

### 2.3 Hypothesis H3: Finite Energy Dissipation

> **H3.** *In the limit $\nu \to 0$ (at fixed integral scale $L_0$ and r.m.s. velocity $U$), the mean energy dissipation rate $\varepsilon = \nu \langle |\nabla \mathbf{v}|^2 \rangle$ tends to a finite, nonzero limit.*

**Physical meaning.** This is the most surprising and the most important of the three hypotheses. Naively, one might expect that as $\nu \to 0$, the dissipation $\varepsilon = \nu \langle |\nabla \mathbf{v}|^2 \rangle \to 0$ as well. But this does not happen: as $\nu$ decreases, the velocity gradients $\langle |\nabla \mathbf{v}|^2 \rangle$ increase (the flow develops finer and finer structure), and the product remains finite. The energy injected at large scales must go somewhere, and the cascade delivers it to whatever scale viscosity operates at; reducing $\nu$ simply pushes the dissipation to smaller scales without reducing its rate.

H3 is often called the **zeroth law of turbulence**, by analogy with the zeroth law of thermodynamics. It is the turbulence analogue of the statement that a system in thermal equilibrium has a well-defined temperature independent of the details of the heat bath.

H3 has a mathematical counterpart: the **dissipative anomaly** of the Euler equations. A weak solution $\mathbf{v}$ of the Euler equations ($\nu = 0$) can dissipate energy even without viscosity, provided the velocity field is sufficiently rough (Holder exponent $\leq 1/3$). This is the content of the Onsager conjecture, now a theorem (proved by Isett, 2018; with the sharp $1/3$ threshold by Buckmaster, De Lellis, Szekelyhidi, and Vicol).

**Why H3 is needed.** Without H3, there is no cascade. If $\varepsilon \to 0$ as $\nu \to 0$, the nonlinear term would not transfer energy to small scales, and the inertial-range phenomenology would collapse. H3 provides the dimensional "anchor" that, combined with H2, uniquely determines the scaling exponent $h = 1/3$.

---

## 3. The Four-Fifths Law

The four-fifths law is the crown jewel of turbulence theory: an *exact*, *nontrivial* result derived directly from the Navier-Stokes equations. It is exact in the sense that it involves no closure approximations, no modeling assumptions, and no adjustable parameters. It requires only H3 (finite dissipation) and stationarity/homogeneity/isotropy --- it does *not* require the self-similarity hypothesis H2.

### 3.1 The Two-Point Correlation and Its Evolution

We introduce the shorthand $v_i = v_i(\mathbf{r}, t)$ and $v_i' = v_i(\mathbf{r}', t)$ with $\mathbf{r}' = \mathbf{r} + \boldsymbol{\ell}$. The two-point velocity correlation tensor is

$$R_{ij}(\boldsymbol{\ell}) = \langle v_i\, v_j' \rangle.$$

By homogeneity, this depends only on $\boldsymbol{\ell} = \mathbf{r}' - \mathbf{r}$, not on $\mathbf{r}$ separately. Our goal is to derive the evolution equation for $R_{ij}(\boldsymbol{\ell})$ and then extract from it an equation for the third-order structure function.

**Step 1: The equation for $v_i v_j'$.** We write the Navier-Stokes equation at $\mathbf{r}$ and at $\mathbf{r}'$:

$$\partial_t v_i + v_k \partial_k v_i = -\partial_i p + \nu \Delta v_i + f_i,$$

$$\partial_t v_j' + v_k' \partial_k' v_j' = -\partial_j' p' + \nu \Delta' v_j' + f_j'.$$

Multiply the first by $v_j'$ and the second by $v_i$, then add:

$$\partial_t (v_i v_j') = -v_j' v_k \partial_k v_i - v_i v_k' \partial_k' v_j' - v_j' \partial_i p - v_i \partial_j' p' + \nu(v_j' \Delta v_i + v_i \Delta' v_j') + v_j' f_i + v_i f_j'.$$

**Step 2: Averaging and using homogeneity.** Take $\langle \cdot \rangle$. By homogeneity, $\langle v_j' v_k \partial_k v_i \rangle$ can be rewritten using the identity $\partial_k = -\partial/\partial \ell_k$ (since shifting $\mathbf{r}$ by $d\mathbf{r}$ with $\mathbf{r}'$ fixed changes $\boldsymbol{\ell}$ by $-d\mathbf{r}$; but by homogeneity the average is independent of $\mathbf{r}$, so we can trade the $\mathbf{r}$-derivative for an $\boldsymbol{\ell}$-derivative). Specifically, homogeneity gives:

$$\langle A(\mathbf{r}) \partial_k B(\mathbf{r}) C(\mathbf{r}') \rangle = -\frac{\partial}{\partial \ell_k} \langle A(\mathbf{r}) B(\mathbf{r}) C(\mathbf{r}') \rangle + \langle \partial_k A(\mathbf{r}) \cdot B(\mathbf{r}) C(\mathbf{r}') \rangle$$

but more directly, the key observation is:

$$\frac{\partial}{\partial \ell_k} \langle v_i v_k v_j' \rangle = \langle v_i v_k \partial_k' v_j' \rangle$$

since $\partial/\partial \ell_k$ acts as $\partial/\partial r_k'$ on functions of $\mathbf{r}' = \mathbf{r} + \boldsymbol{\ell}$ when the average removes $\mathbf{r}$-dependence.

Similarly, one can show that the pressure-velocity correlations vanish for homogeneous, incompressible turbulence. This is because $\partial_j' \langle v_i p' \rangle = \langle v_i \partial_j' p' \rangle$ by homogeneity, and the pressure term can be shown to vanish after taking the trace $i = j$ (which is what we need for the energy equation) and using incompressibility.

**Step 3: The trace and the Karman-Howarth-Monin relation.** Set $j = i$ (contract, summing over $i$) to get the equation for $\frac{1}{2}\langle v_i v_i' \rangle = \frac{1}{2}R_{ii}(\boldsymbol{\ell})$. Define the **scale-by-scale energy flux** through scale $\ell$ via the nonlinear term contribution:

$$\varepsilon(\boldsymbol{\ell}) = -\partial_t \left[\tfrac{1}{2} R_{ii}(\boldsymbol{\ell})\right]_{\text{nonlinear}}.$$

After careful bookkeeping (which we sketch rather than reproduce in every detail), one arrives at the **Karman-Howarth-Monin (KHM) relation**:

$$\frac{\partial}{\partial t}\left[\frac{1}{2}\langle v_i v_i'\rangle\right] = \frac{1}{4}\frac{\partial}{\partial \ell_k}\langle (\delta v_k)|\delta \mathbf{v}|^2 \rangle + \nu \frac{\partial^2}{\partial \ell_k \partial \ell_k}\left[\frac{1}{2}\langle v_i v_i'\rangle\right] + \mathcal{F}(\boldsymbol{\ell}),$$

where $\delta v_k = v_k' - v_k$, $|\delta \mathbf{v}|^2 = \delta v_i \delta v_i$, and $\mathcal{F}(\boldsymbol{\ell})$ collects the forcing contributions. We have used the identity (derivable by expanding):

$$\langle v_k v_i v_i' \rangle - \langle v_k' v_i v_i' \rangle = -\frac{1}{2}\langle \delta v_k\, |\delta \mathbf{v}|^2 \rangle$$

which holds by homogeneity, and relates the triple correlation to the third-order structure function.

An equivalent and more transparent form of the KHM relation uses the third-order structure function tensor directly. Rewriting in terms of $|\delta \mathbf{v}|^2$, we get (in the stationary state, $\partial_t = 0$):

$$\boxed{\frac{1}{4}\nabla_{\boldsymbol{\ell}} \cdot \langle |\delta \mathbf{v}|^2\, \delta \mathbf{v} \rangle = -\varepsilon + \nu \Delta_{\boldsymbol{\ell}} \left[\tfrac{1}{2}\langle |\delta \mathbf{v}|^2 \rangle\right] + \mathcal{F}(\boldsymbol{\ell}).}$$

This is exact. No approximations have been made beyond stationarity and homogeneity. The left side is the divergence (in $\boldsymbol{\ell}$-space) of the third-order moment of velocity increments. The right side has the mean dissipation, a viscous correction (which vanishes in the inertial range as $\nu \to 0$), and the forcing (which vanishes for $\ell \ll L_0$, since the forcing is confined to large scales).

### 3.2 The Inertial Range and the Four-Fifths Law

In the inertial range $\eta \ll \ell \ll L_0$:

- The viscous term $\nu \Delta_{\boldsymbol{\ell}}[\cdots]$ is negligible (it is a correction of order $(\eta/\ell)^{4/3}$).
- The forcing term $\mathcal{F}(\boldsymbol{\ell})$ is negligible (it has support at scales $\sim L_0 \gg \ell$).
- Stationarity gives $\partial_t = 0$.

Therefore the KHM relation becomes:

$$\nabla_{\boldsymbol{\ell}} \cdot \langle |\delta \mathbf{v}|^2\, \delta \mathbf{v} \rangle = -4\varepsilon.$$

Now invoke **isotropy** (from H1). In isotropic turbulence, $\langle |\delta \mathbf{v}|^2\, \delta v_k \rangle$ must be proportional to $\ell_k$ (the only available vector), so:

$$\langle |\delta \mathbf{v}|^2\, \delta v_k \rangle = F(\ell)\, \ell_k$$

for some scalar function $F(\ell)$. The divergence is:

$$\nabla_{\boldsymbol{\ell}} \cdot (F(\ell)\, \boldsymbol{\ell}) = F'(\ell)\, \ell + 3\, F(\ell) = \frac{1}{\ell^2}\frac{d}{d\ell}(\ell^3 F(\ell)),$$

where we used $\partial \ell / \partial \ell_k = \ell_k/\ell$ and $\partial \ell_k / \partial \ell_k = 3$. Setting this equal to $-4\varepsilon$:

$$\frac{1}{\ell^2}\frac{d}{d\ell}\left(\ell^3 F(\ell)\right) = -4\varepsilon.$$

Integrate:

$$\ell^3 F(\ell) = -\frac{4}{3}\varepsilon\, \ell^3 + C.$$

Regularity at $\ell = 0$ requires $C = 0$ (since $F(\ell) \ell^3 \to 0$ as $\ell \to 0$). Therefore:

$$F(\ell) = -\frac{4}{3}\varepsilon.$$

Now we extract the longitudinal third-order structure function. Project $\langle |\delta \mathbf{v}|^2 \delta v_k \rangle = F(\ell)\, \ell_k$ onto $\ell_k/\ell$:

$$\langle |\delta \mathbf{v}|^2\, \delta v_\| \rangle = F(\ell)\, \ell = -\frac{4}{3}\varepsilon\, \ell.$$

For isotropic incompressible turbulence, one can show (using the incompressibility constraint $\partial_i \delta v_i = 0$ to relate longitudinal and transverse increments) that:

$$\langle |\delta \mathbf{v}|^2\, \delta v_\| \rangle = \langle (\delta v_\|)^3 \rangle + \langle (\delta v_\|)(\delta v_\perp)^2 \rangle,$$

where $\delta v_\perp^2 = |\delta \mathbf{v}|^2 - (\delta v_\|)^2$ is the transverse contribution. In $d = 3$ dimensions, the isotropy and incompressibility relations between longitudinal and transverse structure functions give:

$$\langle |\delta \mathbf{v}|^2\, \delta v_\| \rangle = \frac{5}{3}\langle (\delta v_\|)^3 \rangle.$$

(This can be derived by writing out the most general isotropic form of $\langle \delta v_i \delta v_j \delta v_k \rangle$ in terms of longitudinal correlations and imposing $\partial/\partial \ell_i$ acting on index $i$ gives zero by incompressibility.) Combining:

$$\frac{5}{3}\langle (\delta v_\|)^3 \rangle = -\frac{4}{3}\varepsilon\, \ell,$$

which gives **Kolmogorov's four-fifths law**:

$$\boxed{\langle (\delta v_\|(\ell))^3 \rangle = -\frac{4}{5}\,\varepsilon\, \ell.}$$

### 3.3 Why the Four-Fifths Law Is Remarkable

The four-fifths law is unique in turbulence theory for several reasons:

1. **Exactness.** It is derived from the Navier-Stokes equations without any closure approximation. In a field plagued by uncontrolled approximations, this is extraordinary.

2. **Minimality of assumptions.** It requires only stationarity, homogeneity, isotropy, and H3 (finite dissipation). It does *not* require the self-similarity hypothesis H2.

3. **Nontriviality.** It relates a *third*-order moment of the velocity to the *first*-order quantity $\varepsilon$. This is not a trivial consequence of Gaussianity (for a Gaussian field, all odd moments vanish). The four-fifths law tells us that turbulence is essentially non-Gaussian.

4. **Negative sign.** The negative sign implies a net energy flux from large to small scales (the direct cascade). The third-order structure function is negative: strong negative velocity increments (convergent flow) are more probable than positive ones of the same magnitude. This is the **skewness** of the velocity increment distribution, and it is a direct signature of the cascade.

5. **Boundary condition for theories.** Any theory of turbulence --- whether K41, multifractal models, or something entirely new --- must reproduce the four-fifths law. It serves as an exact constraint, analogous to a sum rule in quantum field theory.

---

## 4. Main Results of K41

### 4.1 Determination of $h = 1/3$

We now combine H2 (self-similarity) with H3 (finite dissipation) and the four-fifths law to determine the scaling exponent.

From H2, the third-order structure function scales as:

$$S_3(\ell) = \langle (\delta v_\|)^3 \rangle \propto \ell^{3h}.$$

From the four-fifths law:

$$S_3(\ell) = -\frac{4}{5}\varepsilon\, \ell \propto \ell^1.$$

Equating the exponents:

$$3h = 1 \implies \boxed{h = \frac{1}{3}.}$$

**Dimensional analysis perspective.** In the inertial range, the only available dimensional parameter is $\varepsilon$ (with dimensions $[\varepsilon] = L^2 T^{-3}$). A velocity increment at scale $\ell$ must have dimensions of velocity, so:

$$\delta v \sim \varepsilon^a \ell^b.$$

Dimensional analysis gives $L^2 T^{-3}$ for $\varepsilon$ and $L$ for $\ell$, and we need $LT^{-1}$:

$$[L^2 T^{-3}]^a [L]^b = L^{2a+b} T^{-3a} = L T^{-1}.$$

So $3a = 1$ (hence $a = 1/3$) and $2a + b = 1$ (hence $b = 1/3$). Therefore:

$$\delta v(\ell) \sim (\varepsilon \ell)^{1/3},$$

confirming $h = 1/3$. This is the *only* dimensionally consistent value, given that $\varepsilon$ is the sole relevant parameter with dimensions.

### 4.2 Structure Functions: $\zeta_p = p/3$

With $h = 1/3$, H2 immediately gives:

$$\boxed{S_p(\ell) = \langle |\delta v_\|(\ell)|^p \rangle = C_p\, \varepsilon^{p/3}\, \ell^{p/3},}$$

where $C_p$ are dimensionless universal constants. The scaling exponents are:

$$\zeta_p = \frac{p}{3}.$$

This is the K41 prediction: the exponents are a *linear* function of $p$. We will see in Section 6 that experiments show deviations from this (anomalous scaling, intermittency), with $\zeta_p$ being a concave function that falls below $p/3$ for $p > 3$.

For the second-order structure function:

$$S_2(\ell) = C_2\, \varepsilon^{2/3}\, \ell^{2/3},$$

where the constant $C_2$ is experimentally found to be $C_2 \approx 2.0$--$2.2$.

### 4.3 The Kolmogorov-Obukhov Energy Spectrum

The energy spectrum $E(k)$ is defined by

$$\frac{1}{2}\langle |\mathbf{v}|^2 \rangle = \int_0^\infty E(k)\, dk.$$

To relate $E(k)$ to the second-order structure function, we use the Wiener-Khinchin theorem. The velocity correlation $R_{ii}(\ell)$ and the energy spectrum are related by:

$$R_{ii}(\boldsymbol{\ell}) = \int \hat{R}_{ii}(\mathbf{k})\, e^{i\mathbf{k}\cdot\boldsymbol{\ell}}\, d^3\mathbf{k},$$

where $E(k) = \frac{1}{2}\oint_{|\mathbf{k}|=k} \hat{R}_{ii}(\mathbf{k})\, dS(k) = 2\pi k^2 \hat{R}_{ii}(k)$ for isotropic turbulence.

The second-order structure function is:

$$S_2(\ell) = 2[R_{ii}(0) - R_{\|,\|}(\ell)] = 2\int_0^\infty E(k)\left(1 - \frac{\sin k\ell}{k\ell}\right)\frac{dk}{1}\cdot\frac{2}{1}.$$

The precise relation involves geometric factors from the isotropy, but the key point is that $S_2(\ell) \propto \ell^{2/3}$ implies, by a Tauberian-type argument (matching the power-law behaviors in physical and Fourier space):

$$\boxed{E(k) = C_K\, \varepsilon^{2/3}\, k^{-5/3},}$$

where $C_K$ is the **Kolmogorov constant**. Experimentally, $C_K \approx 1.5$--$1.7$.

**Derivation by dimensional analysis.** In the inertial range, $E(k)$ can depend only on $\varepsilon$ and $k$. Since $[E(k)] = L^3 T^{-2}$ (energy per unit mass per unit wavenumber), $[\varepsilon] = L^2 T^{-3}$, and $[k] = L^{-1}$:

$$E(k) = C_K\, \varepsilon^a\, k^b, \quad L^3 T^{-2} = L^{2a} T^{-3a} L^{-b}.$$

From $T$: $3a = 2$, so $a = 2/3$. From $L$: $2a - b = 3$, so $b = 2(2/3) - 3 = -5/3$. Hence $E(k) \propto \varepsilon^{2/3} k^{-5/3}$.

This is the famous **Kolmogorov-Obukhov $k^{-5/3}$ spectrum**, one of the most well-confirmed predictions in all of physics. It has been verified in atmospheric turbulence, wind tunnels, oceanic flows, and numerical simulations over many decades of wavenumber.

### 4.4 The Dissipation Range

K41 also makes predictions about the transition from the inertial range to the dissipation range. In the dissipation range ($\ell \lesssim \eta$ or equivalently $k \gtrsim k_\eta = 1/\eta$), viscosity is important and the energy spectrum falls off rapidly.

Dimensional analysis with both $\varepsilon$ and $\nu$ available gives:

$$E(k) = C_K\, \varepsilon^{2/3}\, k^{-5/3}\, \Phi(k\eta),$$

where $\Phi$ is a universal function with $\Phi(x) \to 1$ for $x \ll 1$ (inertial range) and $\Phi(x) \to 0$ rapidly for $x \gg 1$ (dissipation range). The form of $\Phi$ for large argument is not determined by K41 alone, but empirically it is approximately exponential: $\Phi(x) \sim x^\alpha \exp(-\beta x)$ for some constants $\alpha, \beta$.

Similarly, the structure functions have finite-viscosity corrections. For $S_2$:

$$S_2(\ell) = C_2\, \varepsilon^{2/3}\, \ell^{2/3}\, \Psi(\ell/\eta),$$

where $\Psi(x) \to 1$ for $x \gg 1$ and $\Psi(x) \sim x^{4/3}$ for $x \ll 1$ (so that $S_2(\ell) \propto \ell^2$ in the smooth regime $\ell \ll \eta$, as required for a differentiable velocity field at the dissipation scale).

### 4.5 The Kolmogorov Scales

The dissipation scale $\eta$, the Kolmogorov velocity $u_\eta$, and the Kolmogorov time $\tau_\eta$ are:

$$\eta = \left(\frac{\nu^3}{\varepsilon}\right)^{1/4}, \quad u_\eta = (\nu \varepsilon)^{1/4}, \quad \tau_\eta = \left(\frac{\nu}{\varepsilon}\right)^{1/2}.$$

These are the unique combinations of $\nu$ and $\varepsilon$ with dimensions of length, velocity, and time, respectively. At the Kolmogorov scale, the local Reynolds number $\mathrm{Re}_\eta = u_\eta \eta / \nu = 1$: inertial and viscous forces are in balance.

One can verify consistency: the K41 velocity increment at scale $\eta$ is $\delta v(\eta) \sim (\varepsilon \eta)^{1/3} = (\varepsilon \nu^3/\varepsilon)^{1/12}\cdot\varepsilon^{1/3} = (\nu\varepsilon)^{1/4} = u_\eta$, as expected.

---

## 5. Landau's Objection

### 5.1 The Problem with Universality

Almost immediately after Kolmogorov presented his theory, L.D. Landau raised an objection (reportedly at the seminar where K41 was first discussed, and later formalized in a footnote to *Fluid Mechanics*, Landau & Lifshitz, 1st edition, 1944). The objection strikes at the heart of H1 and H2 and reveals that K41 cannot be exactly correct for moments of order $p \neq 3$.

The K41 prediction for the second-order structure function is:

$$S_2(\ell) = C\, \varepsilon^{2/3}\, \ell^{2/3},$$

where $C$ is supposed to be a *universal* constant (the same for all turbulent flows, independent of the large-scale conditions). But consider the following argument.

### 5.2 Fluctuations of the Dissipation Rate

The mean dissipation rate $\varepsilon$ is an average over the entire flow. But the *local* dissipation rate,

$$\varepsilon(\mathbf{r}, t) = \frac{\nu}{2}\left(\partial_i v_j + \partial_j v_i\right)^2,$$

fluctuates strongly from point to point and from time to time. These fluctuations are not small: experiments show that the probability distribution of $\varepsilon(\mathbf{r}, t)$ is approximately log-normal with a variance that grows with the Reynolds number.

Now suppose that the K41 scaling $S_2(\ell) = C\, \varepsilon_{\text{local}}^{2/3}\, \ell^{2/3}$ holds locally, with $\varepsilon_{\text{local}}$ being the dissipation rate averaged over a region of size $\sim \ell$ around the point in question. To get the globally averaged structure function, we must average over the fluctuations of $\varepsilon_{\text{local}}$:

$$S_2(\ell) = C\, \langle \varepsilon_{\text{local}}^{2/3} \rangle\, \ell^{2/3}.$$

But $\langle \varepsilon_{\text{local}}^{2/3} \rangle \neq \langle \varepsilon_{\text{local}} \rangle^{2/3}$ unless $\varepsilon_{\text{local}}$ is constant (by Jensen's inequality, since $x \mapsto x^{2/3}$ is concave, we have $\langle \varepsilon^{2/3} \rangle \leq \langle \varepsilon \rangle^{2/3}$). So the effective "constant" $C_{\text{eff}} = C \cdot \langle \varepsilon_{\text{local}}^{2/3} \rangle / \langle \varepsilon \rangle^{2/3}$ depends on the statistics of $\varepsilon_{\text{local}}$, which in turn depend on the large-scale flow.

### 5.3 The General Argument for $p \neq 3$

For general order $p$, the K41 prediction is:

$$S_p(\ell) \sim \langle \varepsilon_{\text{local}}^{p/3} \rangle\, \ell^{p/3}.$$

The key observation is:

- For $p = 3$: $\langle \varepsilon_{\text{local}}^1 \rangle = \langle \varepsilon \rangle = \varepsilon$, which is the global mean dissipation rate. This quantity is *not* affected by fluctuations. Hence the four-fifths law $S_3(\ell) = -\frac{4}{5}\varepsilon\, \ell$ is **immune to Landau's objection**. This is not a coincidence --- the four-fifths law is derived from the Navier-Stokes equations without any assumption about the universality of $\varepsilon$.

- For $p \neq 3$: $\langle \varepsilon_{\text{local}}^{p/3} \rangle \neq \langle \varepsilon \rangle^{p/3}$, and the ratio $\langle \varepsilon_{\text{local}}^{p/3} \rangle / \langle \varepsilon \rangle^{p/3}$ depends on the full distribution of $\varepsilon_{\text{local}}$, which is *not* universal.

This means:

- The *exponents* $\zeta_p = p/3$ might still be universal (if the scaling of $\varepsilon_{\text{local}}$ fluctuations with $\ell$ is universal), but the *prefactors* $C_p$ are not.
- Even worse, if $\varepsilon_{\text{local}}$ has its own power-law dependence on $\ell$ (which it does, because the local dissipation averaged over a ball of radius $\ell$ has fluctuations that grow as $\ell$ decreases), then the exponents $\zeta_p$ themselves are modified.

### 5.4 The Modern Formulation

The modern understanding, developed in the 1960s–1990s by Kolmogorov himself (K62), Obukhov, Novikov, Mandelbrot, Parisi, Frisch, and many others, is:

1. The K41 theory is correct at the level of the *mean* dissipation rate (the four-fifths law is exact).
2. For higher-order statistics ($p > 3$), the fluctuations of $\varepsilon_{\text{local}}$ produce **anomalous scaling**: $\zeta_p \neq p/3$, with $\zeta_p < p/3$ for $p > 3$.
3. The deviation $\delta\zeta_p = p/3 - \zeta_p > 0$ is a measure of **intermittency**: the tendency for extreme velocity gradients to be concentrated in small regions of space, rather than uniformly distributed.
4. The scaling exponents $\zeta_p$ are believed to be universal (the same for all turbulent flows at high Re), but the prefactors $C_p$ are not.

The theoretical framework for describing intermittency is the **multifractal model**, in which the velocity field has a spectrum of local Holder exponents $h$ rather than a single value $h = 1/3$. This is the subject of a later tutorial.

---

## 6. Historical Context

### 6.1 Kolmogorov's 1941 Papers

Andrei Nikolaevich Kolmogorov published his theory in two short papers in the *Doklady Akademii Nauk SSSR* (Proceedings of the USSR Academy of Sciences) in 1941:

- **K41a**: "The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers" (Dokl. Akad. Nauk SSSR **30**, 299–303, 1941). This paper states the hypotheses H1–H3 and derives the $\ell^{2/3}$ law for the second-order structure function by dimensional analysis.

- **K41b**: "Dissipation of energy in the locally isotropic turbulence" (Dokl. Akad. Nauk SSSR **32**, 16–18, 1941). This paper derives the four-fifths law.

These papers were written in Russian during World War II and were not widely known in the West until much later. Kolmogorov's work was partly anticipated by independent contributions from Obukhov (who derived the $k^{-5/3}$ spectrum independently) and Onsager (who arrived at similar conclusions from the Fourier-space perspective). The theory is therefore sometimes called the Kolmogorov-Obukhov theory.

### 6.2 Richardson's Cascade

Kolmogorov's theory gives mathematical form to the qualitative picture proposed by Lewis Fry Richardson in 1922, often summarized by his famous verse (a parody of Jonathan Swift):

> *Big whirls have little whirls that feed on their velocity,*
> *and little whirls have lesser whirls and so on to viscosity.*

Richardson envisioned energy being transferred from large eddies to small eddies in a cascade process. Kolmogorov's contribution was to make this precise: the cascade is *local* in scale space (each scale transfers energy primarily to the next smaller scale), the rate of transfer is $\varepsilon$ (independent of scale in the inertial range), and the resulting velocity fluctuations scale as $(\varepsilon \ell)^{1/3}$.

### 6.3 K41 as the Zeroth-Order Theory

Despite Landau's objection and the evidence for intermittency corrections, K41 remains the indispensable starting point for all of turbulence theory. Its status is analogous to that of mean-field theory in statistical mechanics: not exactly correct for fluctuations, but capturing the essential physics and providing the framework within which corrections are understood.

The $k^{-5/3}$ spectrum is experimentally confirmed over many decades of wavenumber in diverse turbulent flows. The four-fifths law is verified to high precision. The deviations from K41 (anomalous exponents) are real but small: $\zeta_2 \approx 0.70$ vs. the K41 prediction of $0.67$, $\zeta_6 \approx 1.78$ vs. $2.0$. The corrections grow with $p$, becoming large only for high-order structure functions.

Every subsequent development in turbulence theory --- the K62 refined similarity hypothesis, the multifractal model, the SLE approach, the conformal invariance program in 2D turbulence, even the rigorous mathematical results on the Euler and Navier-Stokes equations --- takes K41 as its point of departure. Understanding K41 is therefore the prerequisite for understanding everything else.

---

## Summary of Key Results

| Quantity | K41 Prediction | Key Equation |
|---|---|---|
| Scaling exponent | $h = 1/3$ | $\delta v(\ell) \sim (\varepsilon\ell)^{1/3}$ |
| Energy spectrum | $E(k) = C_K \varepsilon^{2/3} k^{-5/3}$ | Kolmogorov-Obukhov law |
| Structure functions | $S_p(\ell) = C_p \varepsilon^{p/3} \ell^{p/3}$ | $\zeta_p = p/3$ |
| Third-order (exact) | $S_3(\ell) = -\frac{4}{5}\varepsilon\,\ell$ | Four-fifths law |
| Dissipation scale | $\eta = (\nu^3/\varepsilon)^{1/4}$ | $\mathrm{Re}_\eta = 1$ |
| Scale separation | $L_0/\eta \sim \mathrm{Re}^{3/4}$ | Inertial range extent |

---

## Further Reading

- U. Frisch, *Turbulence: The Legacy of A.N. Kolmogorov* (Cambridge University Press, 1995). The primary reference for this tutorial; Chapters 5–6 cover K41 in detail.
- A.S. Monin and A.M. Yaglom, *Statistical Fluid Mechanics*, Vol. 2 (MIT Press, 1975; Dover reprint, 2007). The encyclopedic reference.
- A.N. Kolmogorov, "The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers," Dokl. Akad. Nauk SSSR **30**, 299 (1941). Reprinted in *Proc. R. Soc. Lond. A* **434**, 9–13 (1991).
- G.L. Eyink and K.R. Sreenivasan, "Onsager and the theory of hydrodynamic turbulence," *Rev. Mod. Phys.* **78**, 87–135 (2006). Excellent historical and physical review.
