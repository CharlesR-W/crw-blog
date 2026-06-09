# Tutorial 5: Intermittency III --- Dissipation-Based Models, Random Cascades & Shell Models

> **Series**: Turbulence & Multifractality
> **Prerequisites**: Tutorials 1–4 (K41, structure functions, multifractal formalism, large deviations)
> **Key insight**: Multiplicative processes produce multifractality *as a theorem*, via large deviations. The Legendre transform is not a modelling choice --- it is Cramér's theorem in disguise.

---

## 1. Kolmogorov's Refined Similarity Hypothesis (1962)

### The flaw in K41

Kolmogorov's 1941 theory assumes that the energy dissipation rate $\varepsilon$ can be replaced by its global mean $\langle \varepsilon \rangle$ throughout the inertial range. This is equivalent to assuming that $\varepsilon$ is spatially homogeneous at inertial-range scales --- an assumption that fails dramatically. Experiments and simulations show that the dissipation field is concentrated on thin, intensely dissipative structures (vortex sheets, filaments) surrounded by quiescent regions. The variance of locally averaged dissipation *grows* as the averaging volume shrinks.

### Local averaging

Define the locally averaged dissipation over a ball of radius $\ell$ centred at $\mathbf{r}$:

$$
\varepsilon_\ell(\mathbf{r}) = \frac{1}{|B_\ell|} \int_{B(\mathbf{r},\,\ell)} \varepsilon(\mathbf{r}')\, d^3 r',
$$

where $|B_\ell| = \frac{4}{3}\pi\ell^3$. This is a coarse-grained version of the dissipation field at scale $\ell$.

### The Refined Similarity Hypothesis (RSH)

Kolmogorov (1962) and Obukhov (1962) independently proposed: replace the global mean $\langle \varepsilon \rangle$ by the local average $\varepsilon_\ell$ in the K41 prediction. The refined statement is:

> **RSH**: The longitudinal velocity increment $\delta v_\|(\ell)$ at scale $\ell$, *conditioned on* $\varepsilon_\ell$, satisfies
> $$\delta v_\|(\ell) \;\overset{d}{\sim}\; (\varepsilon_\ell \cdot \ell)^{1/3},$$
> meaning equality in distribution up to a dimensionless random variable of order unity that is independent of $\ell$ and $\varepsilon_\ell$.

This is a much weaker (and more defensible) claim than K41: K41 asserts a deterministic scaling law; RSH asserts a *distributional* one, with all the intermittency absorbed into the statistics of $\varepsilon_\ell$.

### Structure functions under RSH

Taking the $p$-th moment of the RSH relation:

$$
S_p(\ell) = \langle |\delta v_\|(\ell)|^p \rangle \sim \ell^{p/3}\, \langle \varepsilon_\ell^{p/3} \rangle.
$$

If the locally averaged dissipation has power-law scaling:

$$
\langle \varepsilon_\ell^q \rangle \sim \ell^{\tau_q},
$$

then the velocity structure function exponents are:

$$
\boxed{\zeta_p = \frac{p}{3} + \tau_{p/3}}.
$$

K41 corresponds to $\tau_q = 0$ for all $q$ (no fluctuations in $\varepsilon_\ell$). Any nontrivial $\tau_q$ produces anomalous scaling. The entire intermittency problem is now reduced to characterising the scaling of $\varepsilon_\ell$.

---

## 2. Multifractal Dissipation

### The dissipation measure

In fully developed turbulence, the dissipation field $\varepsilon(\mathbf{r})$ defines a measure $\mu$ on space: for any region $A$,

$$
\mu(A) = \int_A \varepsilon(\mathbf{r})\, d^3 r.
$$

Energy conservation (in the inertial range) means $\mu$ has a fixed total mass proportional to the energy injection rate. This measure is not smooth --- it concentrates on a complicated, scale-dependent set.

### Singularity spectrum of the dissipation

As $\ell \to 0$, the coarse-grained dissipation at a point $\mathbf{r}$ scales as:

$$
\varepsilon_\ell(\mathbf{r}) \sim \ell^{\alpha(\mathbf{r})},
$$

where $\alpha(\mathbf{r})$ is the *local singularity exponent* (or Hölder exponent) of the dissipation measure at $\mathbf{r}$. Note the convention: since $\varepsilon_\ell$ is a density (energy per unit volume per unit time), a uniform distribution gives $\alpha = 0$. Concentrated regions have $\alpha < 0$; depleted regions have $\alpha > 0$.

The set of points sharing exponent $\alpha$ forms a fractal:

$$
\mathcal{S}_\alpha = \{\mathbf{r} : \varepsilon_\ell(\mathbf{r}) \sim \ell^\alpha\},\qquad \dim_H(\mathcal{S}_\alpha) = f(\alpha),
$$

where $f(\alpha)$ is the **singularity spectrum of the dissipation measure**.

### Moment scaling from the singularity spectrum

To compute $\langle \varepsilon_\ell^q \rangle$, partition space into boxes of size $\ell$. In a box where $\varepsilon_\ell \sim \ell^\alpha$, the contribution to the $q$-th moment is $\ell^{q\alpha}$. The number of such boxes scales as $\ell^{-f(\alpha)}$ (from the fractal dimension). Therefore:

$$
\langle \varepsilon_\ell^q \rangle \sim \int \ell^{q\alpha}\, \ell^{-f(\alpha)}\, d\alpha \sim \ell^{\inf_\alpha[q\alpha - f(\alpha) + d]},
$$

where $d = 3$ is the spatial dimension. The integral is dominated by a saddle point (for $\ell \to 0$, the exponent that minimises the power of $\ell$ dominates). Hence:

$$
\boxed{\tau_q = \inf_\alpha \bigl[q\alpha - f(\alpha) + d\bigr] = \inf_\alpha \bigl[q\alpha - f(\alpha)\bigr] + d.}
$$

This is a Legendre–Fenchel transform (up to the additive constant $d$). The inverse transform recovers:

$$
f(\alpha) = \inf_q \bigl[q\alpha - \tau_q\bigr] + d.
$$

### Bridging velocity and dissipation multifractality

From the RSH relation $\zeta_p = p/3 + \tau_{p/3}$, one can relate the velocity singularity spectrum $D(h)$ (from Tutorial 4) to the dissipation singularity spectrum $f(\alpha)$. The velocity increment scales as $\delta v \sim \ell^h$, and by RSH, $\delta v \sim (\varepsilon_\ell \cdot \ell)^{1/3} \sim \ell^{(\alpha + 1)/3}$. Therefore:

$$
h = \frac{\alpha + 1}{3}, \qquad \alpha = 3h - 1.
$$

The Jacobian of this linear transformation is trivial, so:

$$
D(h) = f(3h - 1).
$$

K41 has $h = 1/3$, corresponding to $\alpha = 0$ (uniform dissipation). Intermittency corrections correspond to a spread in both $h$ and $\alpha$ around these values.

---

## 3. Random Cascade Models

The key question is: what kind of process produces a multifractal measure? The answer is **multiplicative cascades** --- and the multifractal formalism emerges from them not as a model but as a *theorem*.

### Construction

Work in one dimension for clarity (the generalisation to $d$ dimensions is straightforward). Start with the interval $[0,1]$ carrying uniform measure. At each stage $n$:

1. Divide each interval of length $r^{n-1}$ into $b = 1/r$ equal sub-intervals of length $r^n$.
2. Multiply the measure in each sub-interval by an independent random weight $W_i \geq 0$, drawn from a common distribution.

After $n$ cascade steps, each interval $I$ at level $n$ carries measure:

$$
\mu_n(I) \propto \prod_{k=1}^{n} W_{i_k},
$$

where $(i_1, i_2, \ldots, i_n)$ labels the hierarchical address of $I$.

### Conservation constraint

For the cascade to conserve total measure (the analogue of energy conservation), we require:

$$
\langle W \rangle = r^d,
$$

where $d$ is the spatial dimension. In one dimension with a binary cascade ($r = 1/2$, $b = 2$), this becomes $\langle W \rangle = 1/2$: the two children of each parent must carry, on average, the full parent measure. More precisely, if $W_1, W_2$ are the weights for the two children, we need $\langle W_1 + W_2 \rangle = 1$.

### Scaling exponents from independence

Since the $W_{i_k}$ are independent:

$$
\langle \mu_n(I)^q \rangle \propto \langle W^q \rangle^n = \bigl(\langle W^q \rangle\bigr)^n.
$$

Writing $n = -\log_r \ell$ (since $\ell = r^n$):

$$
\langle \varepsilon_\ell^q \rangle \sim \ell^{\tau_q},\qquad \tau_q = -\log_r \langle W^q \rangle = \frac{\log \langle W^q \rangle}{\log r}.
$$

The entire function $\tau_q$ is determined by the moment generating function of $\ln W$.

### Specific cascade models

**Binomial cascade** (Mandelbrot, 1974): At each binary split, assign fractions $p$ and $1 - p$ (deterministically or randomly) to the two halves. For the deterministic version:

$$
\tau_q = -\log_2(p^q + (1-p)^q).
$$

The singularity spectrum is:

$$
f(\alpha) = -\frac{\alpha_+\!\log_2 \alpha_+ + \alpha_-\!\log_2 \alpha_-}{(\alpha_+ + \alpha_-)\log_2(\alpha_+ + \alpha_-)},
$$

where $\alpha_\pm = -\log_2 p$ and $-\log_2(1-p)$ define the range $[\alpha_{\min}, \alpha_{\max}]$.

**Lognormal cascade**: Take $\ln W \sim \mathcal{N}(m, \sigma^2)$ with parameters chosen to satisfy conservation. This gives $\tau_q$ quadratic in $q$ (see Section 5 below).

**Log-Poisson cascade** (She–Lévêque, 1994; Dubrulle, 1994): Take $W = A \cdot \beta^{N}$ where $N \sim \text{Poisson}(\lambda)$. This gives:

$$
\tau_q = -q\,\frac{\log A}{\log r} + \frac{\lambda(1 - \beta^q)}{\log r}.
$$

By choosing parameters to match known constraints ($\zeta_3 = 1$, $\tau_0 = 0$), one obtains the She–Lévêque formula:

$$
\zeta_p = \frac{p}{9} + 2\left(1 - \left(\frac{2}{3}\right)^{p/3}\right),
$$

which fits experimental data remarkably well and has the crucial property that $\zeta_p \to \text{const}$ as $p \to \infty$ (no unphysical divergence).

---

## 4. Large Deviations and Multifractality

### Why multifractality is a theorem

The cascade construction makes the coarse-grained dissipation:

$$
\ln \varepsilon_\ell = \sum_{k=1}^{n} \ln W_k + \text{const},
$$

where $n = |\log \ell / \log r|$ is the number of cascade steps. This is a **sum of $n$ iid random variables**. As $\ell \to 0$, $n \to \infty$, and the theory of large deviations applies directly.

### Cramér's theorem

The law of large numbers says $\frac{1}{n}\sum \ln W_k \to \langle \ln W \rangle$ almost surely. Cramér's theorem quantifies the probability of deviations: for $\alpha \neq \langle \ln W \rangle$,

$$
\Pr\!\left(\frac{1}{n}\sum_{k=1}^n \ln W_k \approx \alpha\right) \sim e^{-n\, I(\alpha)},
$$

where the **rate function** is the Legendre–Fenchel transform of the cumulant generating function:

$$
I(\alpha) = \sup_q \bigl[q\alpha - \Lambda(q)\bigr],\qquad \Lambda(q) = \log \langle e^{q \ln W} \rangle = \log \langle W^q \rangle.
$$

### From rate function to singularity spectrum

Since $n \sim |\log \ell|$ and $\varepsilon_\ell \sim \ell^\alpha$ on the set where $\frac{1}{n}\sum \ln W_k \approx \alpha \log r$, the number of boxes with exponent $\alpha$ is:

$$
\mathcal{N}(\alpha, \ell) \sim \ell^{-d} \cdot \ell^{I(\alpha/\log r) \cdot |\log r|} = \ell^{-f(\alpha)},
$$

and the singularity spectrum is:

$$
f(\alpha) = d - \frac{I(\alpha)}{\log(1/r)} = d - \sup_q\!\left[\frac{q\alpha - \log\langle W^q\rangle}{\log(1/r)}\right].
$$

Equivalently, since $\tau_q = -\log_r\langle W^q \rangle$:

$$
\boxed{f(\alpha) = \inf_q [q\alpha - \tau_q] + d.}
$$

This is precisely the Legendre transform encountered in Section 2 --- but now it is not an assumption or a convenient parametrisation. It is a **consequence of Cramér's theorem applied to the multiplicative structure of the cascade**. The Legendre transform relating $\tau_q$ and $f(\alpha)$ is as inevitable as the central limit theorem for additive processes.

### What this means

| Additive process | Multiplicative process |
|:---|:---|
| Sum of iid variables | Product of iid variables |
| CLT $\to$ Gaussian limit | Large deviations $\to$ multifractal spectrum |
| Mean and variance characterise | Full rate function needed |
| Gaussian universality | No universality: $f(\alpha)$ depends on $\text{law}(W)$ |

The lack of universality in the multiplicative case is why different cascade models give different $\zeta_p$. The *form* of the multifractal formalism is universal (it is a theorem); the *content* (the specific function $\tau_q$) is model-dependent.

---

## 5. The Lognormal Model and Its Shortcomings

### Kolmogorov–Obukhov (1962)

The simplest model for dissipation fluctuations: assume $\ln \varepsilon_\ell$ is Gaussian with variance growing logarithmically:

$$
\ln \varepsilon_\ell \sim \mathcal{N}\!\left(\langle \ln \varepsilon_\ell \rangle,\; \mu \ln(L/\ell)\right),
$$

where $\mu > 0$ is the **intermittency parameter** and $L$ is the integral scale. This corresponds to a cascade with lognormal weights.

### Resulting exponents

The moment scaling is:

$$
\langle \varepsilon_\ell^q \rangle \sim \ell^{\tau_q},\qquad \tau_q = -\mu\,\frac{q(q-1)}{2}.
$$

(The linear term in $q$ is fixed by the normalisation $\tau_1 = 0$, i.e., $\langle \varepsilon_\ell \rangle$ is independent of $\ell$.) Via RSH:

$$
\boxed{\zeta_p = \frac{p}{3} - \frac{\mu}{18}\, p(p - 3).}
$$

Note that $\zeta_3 = 1$ exactly (the 4/5 law is preserved). Experimentally, $\mu \approx 0.20 \pm 0.05$.

The singularity spectrum is parabolic:

$$
f(\alpha) = d - \frac{(\alpha - \alpha_0)^2}{2\mu},\qquad \alpha_0 = -\frac{\mu}{2},
$$

peaking at $f(\alpha_0) = d$ with $\alpha_0 < 0$ (the most probable dissipation is slightly concentrated).

### Problem 1: Negative exponents at large $p$

The quadratic formula gives $\zeta_p < 0$ for $p > p^* = 3 + 18/\mu \approx 93$ (for $\mu = 0.2$). But $S_p(\ell) = \langle |\delta v|^p \rangle$ is a positive quantity, and for $\ell$ in the inertial range, $|\delta v| \lesssim v_{\text{rms}}$, so $S_p(\ell) \leq v_{\text{rms}}^p$. Therefore $\zeta_p \geq 0$ is required on physical grounds. The lognormal model violates this for sufficiently high-order moments.

More precisely, there is a rigorous bound: $\zeta_p$ must be a concave, non-decreasing function of $p$ for $p > 0$. The parabolic lognormal formula eventually decreases, violating concavity-implied monotonicity.

### Problem 2: Moment divergence

If $\ln W$ is Gaussian, then $W = e^{\ln W}$ is lognormal, and $\langle W^q \rangle = e^{qm + q^2\sigma^2/2}$. This exists for all $q \in \mathbb{R}$, which seems fine. However, the quadratic growth of $\tau_q$ means $\langle \varepsilon_\ell^q \rangle$ grows super-polynomially in $q$, implying that $\varepsilon_\ell$ does not have a well-defined moment generating function. More fundamentally, $\tau_q \to -\infty$ as $q \to \infty$ means the singularity spectrum $f(\alpha)$ extends to $\alpha \to -\infty$, implying arbitrarily singular concentrations of dissipation --- which is unphysical because pointwise dissipation is bounded by enstrophy.

### Problem 3: Mandelbrot's cascade objection

Mandelbrot (1974) raised a deeper objection: the lognormal distribution is not **stable** under the multiplicative cascade operation. If $W_1, W_2, \ldots$ are iid lognormal and we define $\varepsilon_\ell = \prod_{k=1}^n W_k$, then $\ln \varepsilon_\ell = \sum \ln W_k$ is indeed Gaussian (by closure of Gaussians under addition). So far, so good. But the lognormal is not *infinitely divisible* in the sense required for continuous cascades: one cannot consistently define a lognormal cascade at all scales simultaneously while maintaining positivity and conservation.

More concretely, the issue is that a continuous cascade limit requires the weight distribution to be infinitely divisible on $(\mathbb{R}_+, \times)$, i.e., $\ln W$ must be infinitely divisible on $(\mathbb{R}, +)$. The Gaussian *is* infinitely divisible, so this specific objection is subtle. The real issue, as clarified by Kahane and later by Barral and Mandelbrot, is that the lognormal cascade *does* converge to a non-degenerate limit measure only if $\mu < d$ --- but the resulting measure has *no* finite moments of order $q > q^* = d/\mu + 1$, contradicting the formula $\tau_q = -\mu q(q-1)/2$ which predicts finite moments for all $q$.

### The lesson

The lognormal model is a useful *approximation* for low-order moments ($p \lesssim 10$), where the parabolic formula matches data well. But it cannot be the *exact* theory. Any complete model of turbulent intermittency must produce $\zeta_p$ that is concave, non-decreasing, and bounded --- properties satisfied by log-Poisson and log-stable models, but not by the lognormal.

---

## 6. Shell Models --- Turbulence as ODEs

### Motivation

The Navier–Stokes equations in three dimensions are a nonlinear PDE with $\sim Re^{9/4}$ active degrees of freedom. Direct numerical simulation (DNS) at $Re \sim 10^6$ would require $\sim 10^{13}$ grid points --- far beyond current capability. **Shell models** abandon spatial structure entirely, retaining only the *spectral* cascade dynamics.

### Setup

Discretise wavenumber space into logarithmically spaced shells:

$$
k_n = k_0 \cdot 2^n, \qquad n = 0, 1, 2, \ldots, N.
$$

Assign a single complex velocity variable $u_n(t) \in \mathbb{C}$ to each shell, representing the "typical" velocity fluctuation at scale $k_n^{-1}$. The energy in shell $n$ is $E_n = \tfrac{1}{2}|u_n|^2$.

### The GOY model

The **Gledzer–Ohkitani–Yamada** model (Gledzer 1973, Ohkitani and Yamada 1989) is:

$$
\boxed{\frac{du_n}{dt} = i\bigl(a\, k_n\, u_{n+1}^* u_{n+2}^* + b\, k_{n-1}\, u_{n-1}^* u_{n+1}^* + c\, k_{n-2}\, u_{n-1}^* u_{n-2}^*\bigr) - \nu k_n^2 u_n + f_n.}
$$

The three terms in the nonlinear part represent interactions of triads $(k_{n-2}, k_{n-1}, k_n)$, $(k_{n-1}, k_n, k_{n+1})$, and $(k_n, k_{n+1}, k_{n+2})$ --- the nearest-neighbour triadic interactions in wavenumber space.

The parameters $a$, $b$, $c$ are real constants. The term $-\nu k_n^2 u_n$ is viscous dissipation. The forcing $f_n$ is applied at large scales (typically $n = 1$ or $n = 2$ only).

### Conservation laws

The inviscid, unforced ($\nu = 0$, $f_n = 0$) model must conserve energy:

$$
E = \sum_n \frac{1}{2}|u_n|^2.
$$

Computing $\dot{E} = \sum_n \text{Re}(u_n^* \dot{u}_n)$ and requiring $\dot{E} = 0$ for arbitrary $\{u_n\}$ gives:

$$
a + b + c = 0.
$$

A second conserved quantity exists. For the standard choice $a = 1$, $b = -\delta$, $c = -(1 - \delta)$, the second invariant is:

$$
H = \sum_n (-1)^n k_n^\sigma |u_n|^2,
$$

where $\sigma$ depends on $\delta$. For $\delta = 1/2$, the second invariant resembles helicity ($\sigma = 1$); for $\delta = 5/4$, it resembles enstrophy ($\sigma = 2$), connecting to 2D turbulence. The "canonical" choice for 3D turbulence is $\delta = 1/2$, giving $a = 1$, $b = -1/2$, $c = -1/2$.

### What shell models reproduce

With $N \sim 20$–$30$ shells, GOY model simulations (a system of $\sim 25$ coupled ODEs, trivially integrated on a laptop) reproduce:

- **K41 scaling**: In the inertial range, $|u_n| \sim k_n^{-1/3}$, giving $E(k) \sim k^{-5/3}$.
- **Intermittency corrections**: The structure function exponents $\zeta_p$ measured from $\langle |u_n|^p \rangle \sim k_n^{-\zeta_p}$ deviate from $p/3$ in close quantitative agreement with experimental turbulence data.
- **The energy cascade**: Energy injected at shell 1 cascades through the nonlinear coupling to small scales and is dissipated at the viscous cutoff.
- **Dissipation intermittency**: The dissipation $\varepsilon_n = \nu k_n^2 |u_n|^2$ is highly intermittent, with large bursts separated by quiescent periods --- reproducing the temporal intermittency seen in experiments.
- **Anomalous scaling of the dissipation field**: The locally averaged dissipation exhibits multifractal scaling consistent with random cascade models.

### The Sabra model

A variant of GOY, the **Sabra model** (L'vov, Podivilov, Pomyalov, Procaccia, Vandembroucq 1998), replaces some of the complex conjugates:

$$
\frac{du_n}{dt} = i\bigl(a\, k_n\, u_{n+1} u_{n+2}^* + b\, k_{n-1}\, u_{n-1} u_{n+1}^* + c\, k_{n-2}\, u_{n-1} u_{n-2}\bigr) - \nu k_n^2 u_n + f_n.
$$

The Sabra model has better phase symmetry properties (it is invariant under $u_n \to u_n e^{i\theta}$ simultaneously for all $n$), avoids a period-3 oscillation artefact of GOY, and is now the standard choice for shell-model studies.

### Shell models as "the Ising model of turbulence"

The analogy is instructive:

| Ising model | Shell model |
|:---|:---|
| Captures phase transitions | Captures the energy cascade |
| Wrong on geometry (1D chain vs. 3D lattice) | Wrong on geometry (no spatial structure) |
| Right on universality, exponents | Right on intermittency exponents |
| Minimal model for critical phenomena | Minimal model for turbulent cascades |
| Solvable (Onsager 2D) / tractable (RG) | Tractable (ODE integration, $N \sim 25$) |

Shell models reach effective Reynolds numbers $Re \sim 2^{2N/3}$. With $N = 40$ shells, this gives $Re \sim 10^8$ --- orders of magnitude beyond DNS. They have been used to study:

- Scaling exponents to high order ($p \sim 20$)
- The probability distribution of velocity increments across scales
- Lagrangian intermittency
- Passive scalar transport
- MHD turbulence (with coupled velocity and magnetic field shells)

### What shell models miss

- **Spatial structure**: There is no physical space, hence no vortex tubes, no spatial correlations, no geometry.
- **Isotropy and symmetry**: The Navier–Stokes equations have full rotational symmetry; shell models have no spatial directions at all.
- **Pressure**: The incompressibility constraint and pressure are absent; the divergence-free condition is not imposed.
- **Sweeping**: Large-scale advection of small-scale structures (the "sweeping problem") is absent because there is no space.
- **The 4/5 law**: The exact form of Kolmogorov's $S_3(\ell) = -\frac{4}{5}\langle \varepsilon \rangle \ell$ requires spatial structure. Shell models have an analogue ($\zeta_3 = 1$), but the prefactor is model-dependent.

Despite these limitations, shell models remain the most powerful tool for studying the *generic* properties of nonlinear cascades at extreme scale separations.

---

## Summary: The Logical Chain

$$
\text{RSH: } \delta v \sim (\varepsilon_\ell \cdot \ell)^{1/3}
$$
$$
\Downarrow
$$
$$
\zeta_p = \frac{p}{3} + \tau_{p/3}, \qquad \text{where } \langle \varepsilon_\ell^q \rangle \sim \ell^{\tau_q}
$$
$$
\Downarrow
$$
$$
\text{Cascade: } \varepsilon_\ell = \prod W_k \;\implies\; \tau_q = -\log_r \langle W^q \rangle
$$
$$
\Downarrow
$$
$$
\text{Cramér: } f(\alpha) = \inf_q[q\alpha - \tau_q] + d \quad \textit{(theorem, not model)}
$$
$$
\Downarrow
$$
$$
\text{Choose law}(W): \text{lognormal (quadratic } \tau_q\text{), log-Poisson (She–Lévêque), \ldots}
$$

The mathematical structure is: **multiplicative process $\to$ large deviations $\to$ Legendre transform $\to$ multifractal spectrum**. This chain is rigorous. The only modelling input is the distribution of the cascade weights $W$.

---

## Exercises

1. **Binomial cascade spectrum**. For a deterministic binomial cascade with weights $p = 0.7$ and $1 - p = 0.3$ on $[0,1]$: compute $\tau_q$ analytically, obtain $f(\alpha)$ via Legendre transform, and verify that $f(\alpha_{\min}) = f(\alpha_{\max}) = 0$ and $\max_\alpha f(\alpha) = 1$.

2. **Lognormal breakdown**. Show that the lognormal formula $\zeta_p = p/3 - \mu p(p-3)/18$ gives $\zeta_p = 0$ at $p = 3 + 18/\mu$, and that $\zeta_p$ is not concave for $p$ beyond the inflection point. What is the inflection point?

3. **She–Lévêque derivation**. Starting from a log-Poisson cascade with $W = A\, \beta^N$, $N \sim \text{Poisson}(\lambda)$: (a) compute $\tau_q$; (b) impose $\tau_0 = 0$, $\tau_1 = 0$, and $\zeta_3 = 1$; (c) show that the three constraints fix $A$, $\beta$, $\lambda$ and yield $\zeta_p = p/9 + 2(1 - (2/3)^{p/3})$.

4. **GOY model conservation**. Prove that $a + b + c = 0$ is necessary and sufficient for energy conservation in the inviscid, unforced GOY model. Find the condition on $(a, b, c)$ for the existence of a second quadratic invariant $\sum_n (-1)^n k_n^\sigma |u_n|^2$.

5. **Rate function to spectrum**. Given a cascade weight with $\langle W^q \rangle = e^{q + q^2/2}$ (so $\Lambda(q) = q + q^2/2$): (a) compute the rate function $I(\alpha) = \sup_q[q\alpha - \Lambda(q)]$; (b) compute $f(\alpha)$; (c) identify this as a lognormal cascade and relate the parameters to $\mu$.

---

## References

- A. N. Kolmogorov, "A refinement of previous hypotheses concerning the local structure of turbulence in a viscous incompressible fluid at high Reynolds number," *J. Fluid Mech.* **13**, 82–85 (1962).
- A. M. Obukhov, "Some specific features of atmospheric turbulence," *J. Fluid Mech.* **13**, 77–81 (1962).
- B. B. Mandelbrot, "Intermittent turbulence in self-similar cascades: divergence of high moments and dimension of the carrier," *J. Fluid Mech.* **62**, 331–358 (1974).
- U. Frisch, *Turbulence: The Legacy of A.N. Kolmogorov* (Cambridge University Press, 1995), Chapters 8–9.
- Z.-S. She and E. Lévêque, "Universal scaling laws in fully developed turbulence," *Phys. Rev. Lett.* **72**, 336–339 (1994).
- T. Bohr, M. H. Jensen, G. Paladin, and A. Vulpiani, *Dynamical Systems Approach to Turbulence* (Cambridge University Press, 1998), Chapters 7–9.
- L. Biferale, "Shell models of energy cascade in turbulence," *Annu. Rev. Fluid Mech.* **35**, 441–468 (2003).
- V. S. L'vov *et al.*, "Improved shell model of turbulence," *Phys. Rev. E* **58**, 1811 (1998).
