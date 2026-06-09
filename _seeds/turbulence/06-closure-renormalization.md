# Tutorial 6: Closure, Functional Methods & Renormalization in Turbulence

> *The problem of turbulence is the only one in physics where we know the equations exactly, and yet we cannot solve them.* — Attributed to various, expressing a shared frustration

This tutorial covers the analytical machinery that has been developed to extract predictions from the Navier-Stokes equations without direct numerical simulation. The programme is essentially the field theory of turbulence: perturbation expansions, diagrammatic resummations, self-consistent closures, and renormalization group methods. For readers trained in QFT and statistical mechanics, most of the structural ideas will be familiar. What is unfamiliar — and what makes the problem genuinely hard — is the absence of a small parameter. Turbulence is strongly coupled, and everything follows from that.

---

## The Closure Problem

### The Moment Hierarchy

The Navier-Stokes equations for an incompressible fluid are:

$$\partial_t v_i + v_j \partial_j v_i = -\partial_i p + \nu \nabla^2 v_i + f_i, \qquad \partial_i v_i = 0,$$

where $f_i$ is a random external force. The velocity field $v_i(\mathbf{x}, t)$ is a random variable, and we want its statistical properties — moments, correlations, spectra.

Take the ensemble average of the equation for $v_i v_j$. The quadratic nonlinearity $v_j \partial_j v_i$ generates a cubic term when multiplied by another velocity factor:

$$\frac{\partial}{\partial t} \langle v_i v_j \rangle + \cdots = \cdots + \text{terms involving } \langle v_i v_j v_k \rangle.$$

Now write the equation for $\langle v_i v_j v_k \rangle$. The nonlinearity generates terms involving $\langle v_i v_j v_k v_l \rangle$. And so on. The equation for the $n$-th moment involves the $(n+1)$-th moment. We have an **infinite hierarchy of coupled equations** — each equation is exact, but none is closed.

This is directly analogous to the **BBGKY hierarchy** in kinetic theory, where the equation for the one-particle distribution function involves the two-particle function, which involves the three-particle function, and so on. In kinetic theory, the hierarchy can be truncated because interactions are weak (the Boltzmann limit: dilute gas, binary collisions dominate). The resulting Boltzmann equation is an enormously successful closure.

In turbulence, no such small parameter exists. The nonlinearity is $O(1)$ at all inertial-range scales — that is what it means for the Reynolds number to be large. The moment hierarchy has no natural truncation point. This is the **closure problem**, and it has driven most of the analytical theory of turbulence since the 1950s.

### Why Gaussianity Doesn't Help (Much)

If the velocity field were Gaussian, all odd moments would vanish and all even moments would factor into products of second moments (Wick's theorem / Isserlis' theorem). The hierarchy would close at second order. But a Gaussian velocity field has identically zero energy transfer — the triple correlations that drive the cascade vanish. Turbulence is essentially non-Gaussian precisely because it cascades.

The quasi-normal approximation (Millionshchikov, 1941) assumes the fourth-order cumulant vanishes — i.e., the fourth moment is expressed in terms of second moments via the Gaussian factorisation. This closes the hierarchy but yields equations that are **unstable**: the energy spectrum develops negative values at certain wavenumbers. The failure is instructive. It shows that the non-Gaussian corrections (cumulants) are not small perturbations but play a stabilising, dynamically essential role.

---

## The Hopf Equation

### The Characteristic Functional

Rather than working with the moment hierarchy level by level, one can encode all moments simultaneously in a single generating object. Define the **characteristic functional**:

$$Z[\mathbf{k}] = \left\langle \exp\!\left(i \int \mathbf{k}(\mathbf{x}) \cdot \mathbf{v}(\mathbf{x}) \, d^3x \right) \right\rangle,$$

where $\mathbf{k}(\mathbf{x})$ is an arbitrary test vector field. This is the infinite-dimensional analogue of the characteristic function $\langle e^{i \mathbf{k} \cdot \mathbf{X}} \rangle$ of a random vector $\mathbf{X}$.

The functional $Z[\mathbf{k}]$ encodes **all** statistical information about the velocity field. Functional derivatives of $Z$ generate all moments:

$$\left. \frac{\delta^n Z}{\delta(ik_{i_1}(\mathbf{x}_1)) \cdots \delta(ik_{i_n}(\mathbf{x}_n))} \right|_{\mathbf{k}=0} = \langle v_{i_1}(\mathbf{x}_1) \cdots v_{i_n}(\mathbf{x}_n) \rangle.$$

The logarithm $W[\mathbf{k}] = \ln Z[\mathbf{k}]$ generates the connected correlations (cumulants), exactly as in quantum field theory.

### The Hopf Functional Equation

Hopf (1952) showed that applying the Navier-Stokes equation under the ensemble average yields a single **functional partial differential equation** for $Z$:

$$\frac{\partial Z}{\partial t} = \left[ \nu \nabla_x^2 \frac{\delta}{\delta(ik_i(\mathbf{x}))} + \frac{\delta^2}{\delta(ik_j(\mathbf{x})) \, \delta(ik_i(\mathbf{x}))} \partial_j^{(x)} + F_i[\mathbf{k}, \mathbf{x}] \right] Z,$$

where the second term (involving the second functional derivative and a spatial derivative) encodes the nonlinearity, and $F_i$ encodes the forcing statistics.

This equation is exact. It is also a single equation — the infinite moment hierarchy has been compressed into one object. But the price is high: it is a **functional PDE**, an equation for a function of infinitely many variables. The moment hierarchy was an infinite system of equations for finitely many variables (the $n$-point functions); the Hopf equation is a single equation for an infinite-dimensional object. We have traded one kind of intractability for another.

The Hopf equation has never been solved for any realistic turbulence problem. Its value is conceptual and structural: it provides a rigorous starting point for formal manipulations (functional integrals, perturbation theory, symmetry arguments) even when explicit solutions are out of reach.

---

## Functional and Diagrammatic Methods

### The Martin-Siggia-Rose / Janssen-De Dominicis Formalism

To apply the full machinery of field theory, we reformulate the problem as a functional integral. The Navier-Stokes equation with random forcing can be written schematically as:

$$L[v] = f,$$

where $L$ is the (nonlinear) Navier-Stokes operator and $f$ is Gaussian random with correlation $\langle f_i(\mathbf{x},t) f_j(\mathbf{x}',t') \rangle = D_{ij}(\mathbf{x}-\mathbf{x}', t-t')$.

Using the Martin-Siggia-Rose (MSR) formalism (1973) — the classical stochastic analogue of the Schwinger-Keldysh formalism in quantum mechanics — one introduces an auxiliary "response" field $\hat{v}_i$ and writes the generating functional as:

$$Z[J, \hat{J}] = \int \mathcal{D}v \, \mathcal{D}\hat{v} \; \exp\!\Big(-S[v, \hat{v}] + J \cdot v + \hat{J} \cdot \hat{v}\Big),$$

where the action is:

$$S[v, \hat{v}] = \int \hat{v}_i \Big(\partial_t v_i + v_j \partial_j v_i - \nu \nabla^2 v_i\Big) - \frac{1}{2} \int \hat{v}_i \, D_{ij} \, \hat{v}_j.$$

The first term enforces the equation of motion (the $\hat{v}$ integration produces a delta functional $\delta[L[v] - f]$, and the $f$-average over the Gaussian forcing gives the second term). This is structurally identical to the field-theory path integral, with $S$ playing the role of the Euclidean action.

### Propagators and Vertices

Expanding around the linear theory ($v_j \partial_j v_i = 0$), the free (Gaussian) part of the action gives two propagators:

- **The bare response function (retarded propagator):**

$$G_0(k, \omega) = \frac{1}{-i\omega + \nu k^2}.$$

This is the Green's function of the linearised Navier-Stokes equation — the response of the fluid to an infinitesimal perturbation. In Fourier space, it has a single pole at $\omega = -i\nu k^2$ (a purely damped mode, no oscillation).

- **The bare correlation function:**

$$C_0(k, \omega) = G_0(k, \omega) \, D(k, \omega) \, G_0^*(k, \omega) = \frac{D(k, \omega)}{|\omega|^2 + \nu^2 k^4},$$

where $D(k, \omega)$ is the force spectrum. The correlation function encodes the statistics of the velocity field itself — it is the quantity whose equal-time, $k$-space version gives the energy spectrum $E(k)$.

The nonlinearity $v_j \partial_j v_i$ produces a **cubic vertex** coupling one $\hat{v}$ field to two $v$ fields. In Fourier space, the vertex factor is:

$$V_{ijk}(\mathbf{k}, \mathbf{p}, \mathbf{q}) = \frac{i}{2} \Big( k_j P_{ik}(\mathbf{q}) + k_k P_{ij}(\mathbf{p}) \Big) \, \delta(\mathbf{k} - \mathbf{p} - \mathbf{q}),$$

where $P_{ij}(\mathbf{k}) = \delta_{ij} - k_i k_j / k^2$ is the transverse projector (enforcing incompressibility).

### Diagrammatic Rules and the Wyld Expansion

With these ingredients, one can write down Feynman-diagram-like rules for turbulence:

- **Solid directed line**: bare propagator $G_0(k, \omega)$
- **Dashed line or wavy line**: bare correlation $C_0(k, \omega)$ (often drawn as two solid lines joined at a force-correlation blob)
- **Three-point vertex**: the nonlinear coupling $V_{ijk}$

The perturbation expansion in powers of the vertex generates a diagrammatic series for the full (renormalised) propagator and correlation function. This is the **Wyld diagram expansion** (Wyld, 1961), the turbulence analogue of Feynman diagrams.

There is a crucial structural difference from QFT. In quantum field theory, the "free" theory is a system of non-interacting fields, and the perturbation parameter is the coupling constant. In turbulence, the "free" theory already has nontrivial statistics — the Gaussian random forcing gives a nontrivial $C_0$. We are not expanding around vacuum; we are expanding around a state with prescribed random input. The perturbation parameter is the strength of the nonlinearity relative to viscous damping — essentially the Reynolds number, which is large. This is why the perturbation series is not useful as a convergent expansion, but only as the starting point for resummation.

---

## The Direct Interaction Approximation (DIA)

### Kraichnan's Self-Consistent Closure

Robert Kraichnan's Direct Interaction Approximation (1959) is the most celebrated analytical closure for turbulence. The idea is beautifully simple in retrospect, and readers familiar with condensed matter will recognise it immediately: it is the **self-consistent Born approximation** (or, equivalently, the Hartree-Fock / large-$N$ / self-consistent one-loop approximation) applied to the turbulence Wyld expansion.

The DIA defines a **renormalised response function** $G(k, \omega)$ and a **renormalised correlation function** $C(k, \omega)$ via Dyson equations:

$$G^{-1}(k, \omega) = G_0^{-1}(k, \omega) - \Sigma(k, \omega),$$
$$C(k, \omega) = G(k, \omega) \left[ D(k, \omega) + F(k, \omega) \right] G^*(k, \omega),$$

where $\Sigma$ is the self-energy (response renormalisation) and $F$ is the nonlinear contribution to the correlation. The DIA approximation consists of evaluating $\Sigma$ and $F$ at the one-loop level but using the **full** (renormalised) $G$ and $C$ inside the loop, rather than the bare ones. This produces a closed, self-consistent system of integral equations.

Explicitly, in the time domain (suppressing indices and wavevector arguments for clarity):

$$\Sigma(k; t, t') = \int \frac{d^3p}{(2\pi)^3} \, |V(k,p,q)|^2 \, G(p; t, t') \, C(q; t, t'),$$

$$F(k; t, t') = \int \frac{d^3p}{(2\pi)^3} \, |V(k,p,q)|^2 \, C(p; t, t') \, C(q; t, t'),$$

with $\mathbf{q} = \mathbf{k} - \mathbf{p}$. These are coupled nonlinear integral equations for $G$ and $C$ — the turbulence analogues of the gap equation in BCS theory or the Schwinger-Dyson equations in QFT.

### What DIA Gets Right

The DIA is a remarkable achievement:

- It is **realisable**: the energy spectrum it predicts is guaranteed non-negative (unlike the quasi-normal approximation).
- It conserves energy in the inviscid limit.
- It correctly predicts the **existence** of an inertial range with a power-law energy spectrum.
- It captures the qualitative physics of the energy cascade.

### What DIA Gets Wrong

DIA predicts an inertial-range spectrum:

$$E(k) \sim k^{-3/2}$$

instead of the observed (and dimensionally required) Kolmogorov spectrum $E(k) \sim k^{-5/3}$.

The error has a precise and instructive origin: **DIA is not Galilean invariant in the Eulerian frame**. In Eulerian coordinates, the velocity field at a fixed point in space is strongly affected by the sweeping of small eddies past the observation point by the large-scale mean flow. The sweeping contributes to the two-time statistics (the decorrelation rate of $C(k; t, t')$) but does not contribute to the energy transfer. DIA conflates these two effects: it allows the sweeping by large eddies to enter the self-energy $\Sigma$, which artificially enhances the decorrelation rate at small scales and steepens the spectrum.

In the language of field theory: the DIA self-energy is contaminated by contributions from Galilean boosts, which are gauge artifacts of the Eulerian frame. The theory does not properly separate the "physical" interactions (straining) from the "gauge" interactions (sweeping).

### Kraichnan's Fix: Lagrangian Coordinates

Kraichnan himself identified this problem and proposed the remedy: reformulate the theory in **Lagrangian coordinates**, where the velocity is measured following individual fluid particles. In this frame, uniform sweeping produces no decorrelation — a uniformly translating fluid looks stationary to a co-moving particle. The Lagrangian-History DIA (LHDIA, 1965) is Galilean invariant by construction and recovers $E(k) \sim k^{-5/3}$.

The cost is substantial: the Lagrangian formulation introduces a dependence on two times *and* two spatial positions (the initial and current positions of the fluid particle), making the equations far more complex. The Lagrangian DIA has never been widely used as a practical tool, though it demonstrated that the self-consistent closure approach is not inherently incompatible with the correct scaling.

The **Abridged Lagrangian-History DIA** and the **test-field model** (Kraichnan, 1971) are simplified versions that retain Galilean invariance while reducing the computational burden. These form the basis for practical closure calculations.

---

## Closures and Their Shortcomings

### EDQNM: A Practical Compromise

The **Eddy-Damped Quasi-Normal Markovian (EDQNM)** closure (Orszag, 1970; Leith, 1971; André and Lesieur, 1977) is the workhorse of analytical turbulence modelling. It starts from the quasi-normal approximation (Gaussian factorisation of fourth-order moments) and patches its two known failures:

1. **Eddy damping**: a phenomenological damping rate $\mu_k \sim \left(\int_0^k p^2 E(p) \, dp \right)^{1/2}$ is added to stabilise the equations (preventing the negative-energy catastrophe of the raw quasi-normal approximation).

2. **Markovianisation**: the memory integrals in the time domain are replaced by their Markovian (instantaneous) limits, assuming that the turbulence decorrelates quickly compared to the evolution of the spectrum.

The result is a closed integro-differential equation for the energy spectrum $E(k, t)$:

$$\frac{\partial E(k, t)}{\partial t} = T(k, t) - 2\nu k^2 E(k, t) + F(k, t),$$

where the nonlinear transfer $T(k, t)$ is expressed as an integral over triadic interactions involving $E(p, t)$ and $E(q, t)$ with $\mathbf{k} = \mathbf{p} + \mathbf{q}$:

$$T(k, t) = \int \int_{\Delta_k} \theta_{kpq} \, b(k, p, q) \left[ k^2 p \, E(p) E(q) - p^3 E(q) E(k) \right] dp \, dq,$$

with $\theta_{kpq} = (\mu_k + \mu_p + \mu_q)^{-1}$ being the triad relaxation time and $b(k,p,q)$ a geometric factor from the incompressibility projection.

EDQNM correctly predicts:
- The $k^{-5/3}$ inertial-range spectrum
- The Kolmogorov constant $C_K \approx 1.4$ (close to the experimental value $\approx 1.5$)
- Reasonable behaviour of spectral transfer and energy flux
- Correct qualitative behaviour of decaying turbulence

EDQNM is widely used in engineering and geophysical applications for spectral modelling. It is computationally cheap compared to DNS and captures the essential energetics well.

### The Common Failing: Gaussianity

All closures in this family — DIA, LHDIA, EDQNM, test-field model — share a deep structural limitation. They are built on the assumption that the velocity field is **nearly Gaussian**, with the non-Gaussianity treated as a perturbative correction driven by the nonlinearity. The closures resum certain classes of diagrams to all orders (typically the "ring" or "bubble" diagrams — the one-loop self-energy), but they neglect higher-order cumulants or treat them as slaved to the second-order statistics.

This means that all such closures are fundamentally **mean-field theories** in the statistical mechanics sense. They capture the behaviour of average quantities (the mean energy spectrum, the mean transfer rate) but miss the fluctuations around those averages.

The consequence is stark: closures **cannot capture intermittency**. The anomalous scaling exponents $\zeta_n$ of the structure functions $S_n(\ell) = \langle |\delta v(\ell)|^n \rangle \sim \ell^{\zeta_n}$, which deviate from the K41 prediction $\zeta_n = n/3$ due to non-Gaussian fluctuations of the dissipation rate, are invisible to any Gaussian-based closure. All closures predict $\zeta_n = n/3$ exactly.

This is not a technical limitation that could be overcome by resumming more diagrams. It is a consequence of the fact that the anomalous exponents arise from rare, intense events in the velocity field — the "fat tails" of the probability distribution — which are precisely what Gaussian-based methods average away. In the language of critical phenomena, intermittency is a fluctuation effect, and closures are mean-field theories that sit above the upper critical dimension.

---

## Eddy Viscosity

### The Oldest Idea

Long before functional integrals and Dyson equations, Boussinesq (1877) proposed the simplest possible closure: the effect of small-scale turbulence on the large-scale flow is analogous to the effect of molecular viscosity. Just as molecular viscosity arises from the random thermal motion of molecules transporting momentum, turbulent eddies transport momentum by their random convective motion.

The **eddy viscosity hypothesis** writes the Reynolds stress (the averaged effect of the fluctuating velocity on the mean flow) as:

$$\langle v_i' v_j' \rangle \approx -\nu_{\text{eddy}} \left( \partial_j \bar{v}_i + \partial_i \bar{v}_j \right),$$

in direct analogy to the Newtonian viscous stress. The eddy viscosity $\nu_{\text{eddy}}$ is estimated dimensionally from the velocity scale $v_\ell$ and length scale $\ell$ of the dominant eddies:

$$\nu_{\text{eddy}} \sim v_\ell \cdot \ell.$$

For the inertial range, using $v_\ell \sim (\varepsilon \ell)^{1/3}$:

$$\nu_{\text{eddy}}(\ell) \sim \varepsilon^{1/3} \ell^{4/3}.$$

This is enormously larger than the molecular viscosity $\nu$. For atmospheric turbulence at $\ell \sim 100$ m, $\nu_{\text{eddy}} \sim 10 \; \text{m}^2/\text{s}$, compared to $\nu \sim 10^{-5} \; \text{m}^2/\text{s}$ — a factor of $10^6$.

### Formal Derivation

The eddy viscosity can be derived more systematically via a **multiscale expansion**. Decompose the velocity field into large-scale (resolved) and small-scale (unresolved) components:

$$v_i = \bar{v}_i + v_i',$$

where $\bar{v}_i$ varies on scales $\geq \ell_c$ (the cutoff) and $v_i'$ varies on scales $< \ell_c$. Substitute into Navier-Stokes, average over the small scales (assuming they are in a statistically steady state determined by the local large-scale strain rate), and expand in powers of the scale ratio $\ell' / \ell_c$.

At leading order, the averaged effect of $v'$ on $\bar{v}$ is indeed a viscosity-like term:

$$\text{Effect of } v' \text{ on } \bar{v} \approx \nu_{\text{eddy}}(k_c) \, \nabla^2 \bar{v}_i + \cdots$$

where $k_c = 2\pi / \ell_c$ is the cutoff wavenumber and:

$$\nu_{\text{eddy}}(k_c) \sim \varepsilon^{1/3} k_c^{-4/3}.$$

This is the formal justification for large-eddy simulation (LES): resolve the large scales on a grid, model the effect of the unresolved small scales as an eddy viscosity.

### Why Eddy Viscosity Is Not Enough

The eddy viscosity concept, while practically useful, is theoretically unsatisfying for several reasons:

1. **It is not a scalar.** The turbulent transport of momentum is anisotropic; the eddy viscosity is properly a fourth-rank tensor $\nu_{ijkl}$, not a single number. Reducing it to a scalar requires the assumption of local isotropy, which fails near boundaries, in shear flows, and in rotating or stratified turbulence.

2. **It is not always positive.** There are flow configurations where the small scales transfer energy *to* the large scales (backscatter), corresponding to a negative eddy viscosity. This occurs in two-dimensional turbulence (where the energy cascade is inverse) and in certain three-dimensional configurations. A negative viscosity makes the equations ill-posed.

3. **It is not local.** The eddy viscosity at a point depends on the turbulence intensity in a neighbourhood, not just at that point. It is a spatially non-local functional of the flow.

4. **It depends on the cutoff.** The value of $\nu_{\text{eddy}}$ depends on where you place the separation between "large" and "small" scales. It is not a property of the turbulence alone but of the turbulence-plus-observation-scheme.

These problems are familiar from condensed matter: the eddy viscosity is a **transport coefficient** of a non-equilibrium system, and it inherits all the subtleties of non-equilibrium transport theory.

---

## Multiscale Methods

### Systematic Scale Elimination

The multiscale approach formalises and extends the eddy viscosity idea. Decompose the velocity field using a sharp spectral cutoff at wavenumber $\Lambda$:

$$v_i(\mathbf{x}, t) = v_i^<(\mathbf{x}, t) + v_i^>(\mathbf{x}, t),$$

where $v^<$ contains Fourier modes with $|\mathbf{k}| < \Lambda$ and $v^>$ contains modes with $|\mathbf{k}| > \Lambda$. The Navier-Stokes equations split into coupled equations for $v^<$ and $v^>$:

$$\partial_t v_i^< + \text{P}^<\left[ (v^< + v^>) \cdot \nabla (v^< + v^>) \right] = \nu \nabla^2 v_i^< + f_i^<,$$
$$\partial_t v_i^> + \text{P}^>\left[ (v^< + v^>) \cdot \nabla (v^< + v^>) \right] = \nu \nabla^2 v_i^> + f_i^>,$$

where $\text{P}^<$ and $\text{P}^>$ are projections onto the low- and high-wavenumber sectors.

The goal is to **integrate out** $v^>$ — solve for $v^>$ as a functional of $v^<$ (perturbatively in the interaction terms) and substitute back into the $v^<$ equation. This yields an effective equation for the large-scale field alone:

$$\partial_t v_i^< = \nu \nabla^2 v_i^< + \text{P}^<\left[ v^< \cdot \nabla v^< \right] + \text{correction terms from } v^>.$$

### Order-by-Order Results

Expanding the correction terms in powers of the interaction between $v^<$ and $v^>$:

**Zeroth order:** No correction. The large scales evolve as if the small scales did not exist.

**First order:** The leading correction is the eddy viscosity:

$$\Delta \nu(k) \, k^2 v_i^<(k),$$

where $\Delta \nu$ is an integral over the small-scale energy spectrum in the shell $\Lambda < |\mathbf{k}| < k_{\max}$. This is the formal derivation of the result quoted in the eddy viscosity section.

**Second order:** Two new effects appear:

- **Eddy noise**: the small scales act as an additional random force on the large scales, with a calculable correlation spectrum. This is the **fluctuation-dissipation** partner of the eddy viscosity — just as molecular viscosity is accompanied by thermal noise (Langevin equation), eddy viscosity is accompanied by eddy noise.

- **Non-local (in scale) corrections**: the effective equation for $v^<$ acquires terms that couple wavenumbers that are not direct triad partners, mediated by the eliminated small scales.

**Higher orders:** increasingly complex non-local and non-Markovian terms. The expansion is asymptotic, not convergent — the effective description becomes more accurate as the scale separation $\ell_c / \eta$ increases, but the series does not converge.

### Connection to Wilson's Renormalization Group

The multiscale elimination procedure is structurally identical to **Wilson's momentum-shell RG** in statistical mechanics. In both cases:

1. Decompose the field into slow (IR) and fast (UV) modes.
2. Integrate out the fast modes perturbatively.
3. Absorb the effect into renormalised parameters of the slow-mode equation.
4. Rescale to restore the original form of the equation.

The analogy is not merely formal. In both turbulence and critical phenomena, the procedure yields:

- **Relevant operators** (eddy viscosity: the leading correction)
- **Marginal operators** (logarithmic corrections, anomalous dimensions)
- **Irrelevant operators** (higher-order terms that vanish under rescaling)

The key question, as always, is whether the procedure has a **fixed point** — a self-similar effective equation that is invariant under further scale elimination. If it does, the fixed-point equation describes the universal properties of the inertial range, independent of the details of forcing and dissipation.

---

## Renormalization Group Methods

### The Forster-Nelson-Stephen (FNS) Theory

The first rigorous application of the RG to turbulence was by Forster, Nelson, and Stephen (1977). They considered a randomly stirred fluid with forcing correlation:

$$D(k) \sim D_0 \, k^{4-d-2\epsilon},$$

where $d$ is the spatial dimension and $\epsilon$ is a control parameter analogous to the $4 - d$ expansion parameter $\epsilon$ in the Wilson-Fisher theory of critical phenomena.

The choice of this forcing spectrum is not arbitrary — it is designed so that the problem has a **marginal** perturbation at $\epsilon = 0$ (Gaussian fixed point is marginally stable), allowing a controlled perturbative RG. The physical picture is:

- $\epsilon = 0$: the forcing is concentrated at the largest scales ($k \to 0$), and the nonlinearity is irrelevant. The velocity field is essentially Gaussian (linear response to forcing).
- $\epsilon > 0$: the forcing extends to smaller scales, making the nonlinearity relevant. A nontrivial fixed point emerges at $O(\epsilon)$.
- $\epsilon = 2$ (in $d = 3$): the forcing spectrum is $\sim k^{-2}$, corresponding to equipartition forcing. Real turbulence corresponds to $\epsilon \approx 2$ in $d = 3$.

### The $\epsilon$-Expansion for Turbulence

The FNS RG proceeds in exact analogy to the Wilson-Fisher calculation:

1. **Integrate out** a thin shell of high-wavenumber modes $\Lambda / b < k < \Lambda$.
2. **Compute** the one-loop corrections to the viscosity $\nu$ and forcing amplitude $D_0$.
3. **Rescale** momenta and fields to restore the cutoff: $k \to bk$, $\omega \to b^z \omega$, $v \to b^\chi v$.

The one-loop RG flow equations have a nontrivial fixed point at:

$$\nu^* \sim \left( \frac{D_0}{\epsilon} \right)^{1/2} k^{-\epsilon/3 + O(\epsilon^2)},$$

and the dynamic exponent at the fixed point is:

$$z = 2 - \frac{2\epsilon}{3} + O(\epsilon^2).$$

The energy spectrum at the fixed point scales as:

$$E(k) \sim k^{1 - 2\epsilon/3}.$$

For $\epsilon = 2$ (the value that gives $E(k)$ consistent with the Kolmogorov spectrum), this yields:

$$E(k) \sim k^{-5/3}.$$

This is a striking result: the RG, applied to a randomly stirred fluid, recovers the Kolmogorov spectrum as a scaling prediction associated with a fixed point.

### The Catch

The result is beautiful but must be treated with extreme caution. The $\epsilon$-expansion is controlled only for $\epsilon \ll 1$, where the forcing is nearly concentrated at the largest scales and the nonlinearity is weak. The physically relevant regime is $\epsilon \approx 2$ (or $\epsilon = 4$ in the notation where the forcing spectrum is $k^{4-d-2\epsilon}$ with $d = 3$ and a different convention for the exponent). This is **far** from the perturbative regime.

The situation is analogous to using the $\epsilon$-expansion in $4 - \epsilon$ dimensions to predict critical exponents in $d = 3$ (where $\epsilon = 1$). In critical phenomena, the $\epsilon$-expansion works surprisingly well at $\epsilon = 1$ due to Borel summability and the existence of only one relevant coupling. In turbulence, the evidence is far less encouraging:

- The one-loop result gives $k^{-5/3}$ at $\epsilon = 2$, but this may be an accident — the exponent $-5/3$ is already dictated by dimensional analysis and constant energy flux (the Kolmogorov argument), so the RG is not predicting something new but rather confirming a consistency.
- Higher-loop corrections have been computed (two-loop, three-loop), and they do not show convincing convergence at $\epsilon = 2$.
- The RG fixed point at small $\epsilon$ describes a regime of **long-range correlated forcing**, not the inertial range driven by a cascade from large-scale forcing. Whether the fixed point survives in the physically relevant limit is unknown.

### The Yakhot-Orszag Theory

In 1986, Yakhot and Orszag proposed a more ambitious RG calculation that attempted to go beyond perturbation theory. Their approach eliminated thin wavenumber shells iteratively while introducing two key modifications:

1. A **distant interaction approximation**: the dominant contributions come from triads where one wavenumber is much smaller than the other two.
2. A **recursion relation** for the eddy viscosity that can be integrated nonperturbatively.

The Yakhot-Orszag theory predicts:

- $E(k) \sim k^{-5/3}$ (by construction, essentially)
- The Kolmogorov constant $C_K \approx 1.617$
- Various turbulence modelling constants (the $k$-$\varepsilon$ model coefficients) from first principles

The theory is **controversial**. Its critics point out that:

- The distant interaction approximation is not justified — the interactions are known to be local (Tutorial 2).
- The theory introduces uncontrolled approximations that are hard to assess systematically.
- Several of the "predictions" involve adjustable assumptions whose effect on the output is unclear.

Despite the controversy, the Yakhot-Orszag theory has been influential, particularly in turbulence modelling, where it provides a theoretical basis (however approximate) for the empirical constants used in RANS models.

### The Deep Lesson

The fundamental difficulty with RG methods in turbulence can be stated precisely: **turbulence may not have a useful small parameter**.

In critical phenomena, the RG is powerful because:
- There is a perturbative fixed point (the Gaussian fixed point) that can be reached by tuning $\epsilon \to 0$.
- The physical fixed point is smoothly connected to the perturbative one.
- The number of relevant couplings is small (typically one or two).

In turbulence:
- The perturbative fixed point exists only for long-range forcing, not for the physically relevant case of large-scale forcing + cascade.
- The "coupling constant" (the Reynolds number) is effectively infinite in the inertial range.
- The number of relevant operators may be large (the full velocity PDF, not just a few couplings).

This is the same obstruction encountered in strongly coupled quantum field theories (QCD at low energies, quantum gravity) and in spin glasses. The absence of a small parameter is not a technical inconvenience but a reflection of the genuine complexity of the problem.

---

## The Big Picture

### What the Analytical Methods Achieve

The closure/DIA/RG programme is powerful for **two-point statistics** — the energy spectrum $E(k)$, the response function, the spectral transfer rate. For these quantities:

- DIA and EDQNM give quantitatively useful predictions.
- The RG provides a formal (if uncontrolled) framework connecting turbulence to the universality concepts of critical phenomena.
- Eddy viscosity and multiscale methods provide practical tools for modelling (LES, RANS).

These methods correctly predict the Kolmogorov $k^{-5/3}$ spectrum, the Kolmogorov constant, the spectral transfer function, and the general features of decaying and forced turbulence. For many engineering and geophysical applications, this is sufficient.

### What They Miss

All of these methods are **blind to intermittency**. The anomalous scaling exponents, the non-Gaussian tails of the velocity gradient distribution, the multifractal structure of the dissipation field, the statistics of extreme events — none of these are captured by any known closure or RG calculation.

This is a precise statement, not a vague complaint. The anomalous exponents $\zeta_n \neq n/3$ are non-perturbative in the same sense that instantons are non-perturbative in quantum mechanics: they arise from rare, localised configurations (intense vortex tubes, dissipation sheets) that are invisible to any diagrammatic expansion around the Gaussian.

The multifractal models (Parisi-Frisch, She-Leveque, log-Poisson) covered in previous tutorials capture intermittency but are **phenomenological** — they introduce the multifractal structure by hand, without deriving it from Navier-Stokes. The field remains caught between:

- **Analytical methods** (closures, RG): systematic and derivable but limited to Gaussian (mean-field) physics.
- **Phenomenological models** (multifractal, shell models): capture the non-Gaussian physics but are not derived from first principles.

### Open Connections

The turbulence closure problem connects to several other major unsolved problems in theoretical physics:

- **Strongly coupled QFT**: the inability to compute non-perturbatively in turbulence is structurally identical to the inability to compute at strong coupling in QCD. The Dyson-Schwinger equations of QCD have the same self-consistent structure as the DIA equations, and they face the same truncation problem.

- **Spin glasses**: disordered systems with quenched randomness and frustration share the feature of complex energy landscapes and the failure of mean-field (replica-symmetric) solutions. The Parisi replica-symmetry breaking solution of the Sherrington-Kirkpatrick model has been suggested as an analogy for the multiscale organisation of turbulence, though no concrete mapping exists.

- **Out-of-equilibrium statistical mechanics**: turbulence is a driven-dissipative system far from equilibrium. There is no free energy to minimise, no detailed balance, no fluctuation-dissipation theorem (except in a modified form for certain closures). The tools of equilibrium statistical mechanics are available only by analogy, not by right.

- **Conformal field theory and integrability**: in two-dimensional turbulence (and in the Kraichnan model of passive scalar advection — one of the few exactly solvable turbulence problems), there are hints of conformal symmetry and integrable structures. Whether any of this extends to the three-dimensional problem is unknown.

The honest assessment is that the fully developed turbulence problem — computing the velocity PDF and all scaling exponents from Navier-Stokes — remains open. Sixty years of sophisticated analytical work have produced powerful tools for second-order statistics and a clear understanding of why higher-order statistics are hard. The gap between what we can compute and what we observe is one of the sharpest in all of theoretical physics.

---

## Summary

| Method | Key idea | Predicts $E(k)$? | Captures intermittency? | Status |
|--------|----------|-------------------|------------------------|--------|
| Moment hierarchy | Exact equations, no truncation | N/A (unclosed) | In principle, yes | Exact but intractable |
| Hopf equation | Characteristic functional | N/A (unsolved) | In principle, yes | Exact but intractable |
| Quasi-normal | Gaussian factorisation of 4th cumulant | Unstable | No | Failed |
| DIA (Kraichnan) | Self-consistent one-loop | $k^{-3/2}$ (wrong) | No | Historically important |
| LHDIA | DIA in Lagrangian frame | $k^{-5/3}$ | No | Correct but impractical |
| EDQNM | Eddy-damped quasi-normal Markovian | $k^{-5/3}$ | No | Widely used |
| Eddy viscosity | Small scales $\approx$ enhanced $\nu$ | $k^{-5/3}$ (input) | No | Practical (LES/RANS) |
| FNS RG | $\epsilon$-expansion for stirred fluid | $k^{-5/3}$ at $\epsilon = 2$ | No | Controlled only at $\epsilon \ll 1$ |
| Yakhot-Orszag RG | Non-perturbative RG attempt | $k^{-5/3}$ | No | Controversial |

The recurring theme: two-point statistics are tractable; higher-order statistics are not. The Kolmogorov spectrum is robust (recoverable by many methods) because it is dictated by dimensional analysis and conservation laws. The anomalous exponents are fragile because they encode the full non-Gaussian structure of the turbulent velocity field — and that structure has resisted every analytical attack to date.

---

*Next: Tutorial 7 will turn to passive scalar turbulence and the Kraichnan model — one of the rare cases where the closure programme can be carried to completion and anomalous scaling exponents can be computed exactly.*

---

*Written with Claude (Anthropic)*
