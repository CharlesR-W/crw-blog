# Tutorial 4: Intermittency II — From the $\beta$-Model to Multifractals

> *This is the mathematical heart of the turbulence series. The machinery here — Legendre transforms, singularity spectra, large deviations — is the same machinery that appears in statistical mechanics, information theory, and dynamical systems. Master it once and you own it everywhere.*

**Prerequisites:** Tutorial 3 (K41 and the first signs of intermittency). Familiarity with measure theory, Legendre–Fenchel transforms, and the statement of Cramér's theorem.

---

## 1. The $\beta$-Model: A First Step Beyond K41

### 1.1 Modifying the Richardson Cascade

K41 assumes a homogeneous cascade: every eddy at scale $\ell$ transfers energy to *all* daughter eddies at scale $r\ell$ (with $0 < r < 1$, typically $r = 1/2$). The $\beta$-model, introduced by Frisch, Sulem, and Nelkin (1978), makes the simplest possible modification: at each cascade step, only a fraction $\beta \in (0, 1)$ of the daughter eddies are *active*. The remaining $1 - \beta$ fraction is quiescent — it receives no energy.

After $n$ cascade steps, the scale is

$$\ell = \ell_0 \, r^n,$$

and the fraction of space that is active is

$$p_\ell = \beta^n.$$

Since $n = \ln(\ell/\ell_0) / \ln r$, we can write

$$p_\ell = \beta^{\ln(\ell/\ell_0)/\ln r} = \left(\frac{\ell}{\ell_0}\right)^{\ln\beta / \ln r}.$$

Define the exponent

$$3 - D \;=\; -\frac{\ln\beta}{\ln r},$$

so that

$$\boxed{p_\ell = \left(\frac{\ell}{\ell_0}\right)^{3-D}.}$$

The quantity $D$ has a precise geometric meaning: it is the **fractal dimension** (specifically, the Kolmogorov capacity or box-counting dimension) of the set on which the dissipation concentrates.

### 1.2 Geometric Interpretation of $D$

Consider an object $\mathcal{S}$ of fractal dimension $D$ embedded in $\mathbb{R}^3$. Cover space with balls of radius $\ell$. The number of balls needed to cover $\mathcal{S}$ scales as $N(\ell) \sim \ell^{-D}$, while the total number of balls covering the ambient $\mathbb{R}^3$ volume scales as $\ell^{-3}$. The probability that a randomly placed ball of radius $\ell$ intersects $\mathcal{S}$ is therefore

$$p_\ell \;\sim\; \frac{N(\ell) \cdot \ell^3}{\ell_0^3} \;\sim\; \ell^{-D} \cdot \ell^3 \;=\; \ell^{3 - D},$$

up to the normalization by $\ell_0$. This is exactly the scaling of $p_\ell$ in the $\beta$-model. The active eddies live on a fractal of dimension $D < 3$; the cascade "empties out" the complement.

For $D = 3$ ($\beta = r^0 = 1$), all space is active and we recover K41. For $D < 3$, the energy-bearing set is sparse, and the cascade is intermittent.

### 1.3 Velocity Scaling in the $\beta$-Model

On the active set, the energy per unit mass at scale $\ell$ is $E_\ell \sim v_\ell^2$, but this energy is concentrated on a fraction $p_\ell$ of the volume. The energy flux (energy per unit time per unit total mass) must equal the mean dissipation rate $\varepsilon$:

$$\Pi_\ell \;\sim\; \frac{v_\ell^3}{\ell} \cdot p_\ell \;\sim\; \varepsilon.$$

(The factor $v_\ell^3 / \ell$ is the eddy turnover rate on the active set; the factor $p_\ell$ accounts for the fraction of volume participating.)

Solving for $v_\ell$:

$$v_\ell^3 \;\sim\; \varepsilon \, \ell \, p_\ell^{-1} \;\sim\; \varepsilon \, \ell \left(\frac{\ell}{\ell_0}\right)^{-(3-D)},$$

so

$$v_\ell \;\sim\; (\varepsilon \ell_0)^{1/3} \left(\frac{\ell}{\ell_0}\right)^{h}, \qquad h = \frac{1}{3} + \frac{3-D}{3}.$$

Wait — let us be more careful. Writing $v_\ell \sim (\ell/\ell_0)^h$ and substituting into the flux condition:

$$\left(\frac{\ell}{\ell_0}\right)^{3h} \cdot \frac{1}{\ell} \cdot \left(\frac{\ell}{\ell_0}\right)^{3-D} \sim \text{const},$$

which requires $3h + 1 + (3-D) - 1 = 0$ ... let me redo this cleanly.

The flux condition is $v_\ell^3 \cdot p_\ell / \ell = \varepsilon$, i.e.,

$$v_\ell^3 \sim \varepsilon \, \ell \, p_\ell^{-1} = \varepsilon \, \ell \left(\frac{\ell}{\ell_0}\right)^{-(3-D)}.$$

Thus

$$v_\ell \sim \varepsilon^{1/3} \ell_0^{(3-D)/3} \, \ell^{[1-(3-D)]/3} \cdot \ell_0^{-1/3} \cdot \ell_0^{(3-D)/3}.$$

More directly: write $v_\ell \sim (\ell/\ell_0)^h$ with appropriate prefactors. Then $v_\ell^3 \sim (\ell/\ell_0)^{3h}$ and we need

$$\left(\frac{\ell}{\ell_0}\right)^{3h} \cdot \left(\frac{\ell}{\ell_0}\right)^{-(3-D)} \cdot \frac{\ell_0}{\ell_0} \sim \frac{\varepsilon \ell}{\varepsilon \ell_0} = \frac{\ell}{\ell_0}.$$

So $3h - (3-D) = 1$, giving

$$\boxed{h = \frac{1}{3} + \frac{3-D}{3} = \frac{4-D}{3}.}$$

Hmm, but this doesn't reduce to $h = 1/3$ when $D = 3$. Let us be even more careful.

**Correct derivation.** The mean dissipation is $\varepsilon$. On the active set (fraction $p_\ell$ of volume), the *local* dissipation rate is $\varepsilon_\ell^{\text{local}} = \varepsilon / p_\ell$ (since the total dissipation is carried by the active fraction). The local velocity scaling satisfies the K41-like relation on the active set:

$$v_\ell \sim (\varepsilon_\ell^{\text{local}} \, \ell)^{1/3} = \left(\frac{\varepsilon}{p_\ell} \cdot \ell\right)^{1/3}.$$

Therefore

$$v_\ell \sim (\varepsilon \ell)^{1/3} \, p_\ell^{-1/3} \sim v_0 \left(\frac{\ell}{\ell_0}\right)^{1/3} \left(\frac{\ell}{\ell_0}\right)^{-(3-D)/3},$$

giving the local Hölder exponent

$$\boxed{h = \frac{1}{3} - \frac{3-D}{3}.}$$

Now $D = 3 \Rightarrow h = 1/3$ (K41), and $D < 3 \Rightarrow h > 1/3$... no. We have $h = 1/3 - (3-D)/3 = (D-2)/3$. For $D < 3$, $h < 1/3$: the velocity increments are *more* singular on the active set than K41 predicts. This makes physical sense — the energy is packed into a smaller volume, so the local gradients must be steeper.

### 1.4 Structure Functions in the $\beta$-Model

The $p$-th order structure function $S_p(\ell) = \langle |\delta v(\ell)|^p \rangle$ involves an average over *all* positions, but only the active fraction contributes nontrivially. Thus

$$S_p(\ell) \sim v_\ell^p \cdot p_\ell \sim \left(\frac{\ell}{\ell_0}\right)^{ph} \cdot \left(\frac{\ell}{\ell_0}\right)^{3-D} = \left(\frac{\ell}{\ell_0}\right)^{\zeta_p},$$

with

$$\boxed{\zeta_p = ph + (3 - D), \qquad h = \frac{1}{3} - \frac{3-D}{3}.}$$

Substituting:

$$\zeta_p = p\left[\frac{1}{3} - \frac{3-D}{3}\right] + (3-D) = \frac{p}{3} - \frac{p(3-D)}{3} + (3-D) = \frac{p}{3} + (3-D)\left(1 - \frac{p}{3}\right).$$

**Check:** $\zeta_3 = 1 + (3-D)(1 - 1) = 1$. The four-fifths law is respected. Good.

**The key observation:** $\zeta_p$ is **linear in $p$**. The $\beta$-model introduces intermittency — the dissipation is concentrated on a fractal — but the structure function exponents remain a straight line. It is a *monofractal* model: there is a single scaling exponent $h$, and the only new parameter beyond K41 is the codimension $3 - D$.

The $\beta$-model predicts the **intermittency parameter** $\mu = 2 - \zeta_6$:

$$\zeta_6 = 2 + (3-D)(1-2) = 2 - (3-D), \qquad \mu = 3-D.$$

Experimentally, $\mu \approx 0.2$–$0.25$, giving $D \approx 2.75$–$2.80$, which is reasonable but the linear $\zeta_p$ is inconsistent with experiments showing clear curvature.

---

## 2. The Bifractal Model

### 2.1 Two Exponents Are Better Than One

The next logical step: allow **two** distinct scaling exponents. Suppose the velocity field has:

- exponent $h_1$ on a set of dimension $D_1$ (e.g., space-filling: $D_1 = 3$),
- exponent $h_2$ on a set of dimension $D_2 < D_1$ (a more singular, sparser structure).

Then

$$S_p(\ell) \sim \ell^{p h_1 + 3 - D_1} + \ell^{p h_2 + 3 - D_2}.$$

As $\ell \to 0$, the dominant term is the one with the *smaller* exponent of $\ell$:

$$\zeta_p = \min\bigl(p h_1 + 3 - D_1,\; p h_2 + 3 - D_2\bigr).$$

This is the minimum of two linear functions of $p$, hence **piecewise linear** with a kink at the crossover

$$p^* = \frac{(D_1 - D_2)}{h_1 - h_2}.$$

For $p < p^*$, the space-filling component dominates (low-order moments are insensitive to rare, intense events); for $p > p^*$, the concentrated component dominates (high-order moments feel the most singular structures).

### 2.2 Assessment

The bifractal model captures a qualitative truth — different moment orders "see" different parts of the flow — but the sharp kink in $\zeta_p$ is not observed experimentally. Real turbulence has smooth, continuously curving $\zeta_p$. We need not two exponents, but a **continuum**.

---

## 3. The Multifractal Model

### 3.1 A Continuous Family of Exponents

The multifractal model (Parisi and Frisch, 1985) is the natural generalization: for each value of the Hölder exponent $h$, the set of points where $\delta v(\ell, \mathbf{x}) \sim \ell^h$ has fractal dimension $D(h)$.

The function $D(h)$ is called the **singularity spectrum** (or **multifractal spectrum**). It tells you "how much room" in physical space is occupied by each type of singularity.

Properties of $D(h)$:
- $D(h) \leq 3$ (the sets live in $\mathbb{R}^3$),
- $D(h)$ is typically a smooth, concave function of $h$,
- $D(h) = -\infty$ for $h$ outside the support (those exponents don't occur),
- The maximum of $D(h)$ corresponds to the "most probable" scaling exponent.

### 3.2 Derivation of the Structure Function Exponents

Consider the $p$-th order structure function:

$$S_p(\ell) = \langle |\delta v(\ell)|^p \rangle = \int |\delta v|^p \, \mathrm{d}\mu(\mathbf{x}).$$

Decompose by Hölder exponent. The set of points with exponent in $[h, h + dh]$ contributes:

- **Velocity scaling:** $|\delta v| \sim \ell^h$ on this set,
- **Probability weight:** a randomly placed ball of radius $\ell$ hits this set with probability $\sim \ell^{3 - D(h)}$ (by the covering argument of Section 1.2).

Therefore

$$S_p(\ell) \sim \int \ell^{ph} \cdot \ell^{3 - D(h)} \, dh = \int \ell^{ph + 3 - D(h)} \, dh.$$

Write $f(h) = ph + 3 - D(h)$. As $\ell \to 0$ (i.e., $\ln \ell \to -\infty$), the integral is dominated by the value of $h$ that **minimizes** $f(h)$ — this is a **saddle-point** (Laplace method) evaluation:

$$S_p(\ell) \sim \ell^{\inf_h f(h)} = \ell^{\inf_h [ph + 3 - D(h)]}.$$

Hence

$$\boxed{\zeta_p = \inf_h \bigl[ph + 3 - D(h)\bigr].}$$

This is the **fundamental formula of the multifractal model**.

### 3.3 Recovering the Special Cases

**K41.** If $D(h) = 3$ only at $h = 1/3$ and $D(h) = -\infty$ elsewhere (a delta function in the multifractal language), the infimum is achieved at $h = 1/3$:

$$\zeta_p = p \cdot \frac{1}{3} + 3 - 3 = \frac{p}{3}.$$

This is exactly K41.

**$\beta$-model.** If $D(h) = D$ at the single point $h = 1/3 - (3-D)/3$ and $D(h) = -\infty$ elsewhere:

$$\zeta_p = p\left[\frac{1}{3} - \frac{3-D}{3}\right] + 3 - D = \frac{p}{3} + (3-D)\left(1 - \frac{p}{3}\right),$$

which is linear in $p$. The $\beta$-model is a **monofractal** — its singularity spectrum is a single point.

**Bifractal.** $D(h)$ supported on two points: the infimum selects one or the other depending on $p$, giving the piecewise-linear $\zeta_p$ of Section 2.

**True multifractal.** When $D(h)$ is a smooth, strictly concave function on an interval $[h_{\min}, h_{\max}]$, the infimum traces out a smooth curve, and $\zeta_p$ is a smooth, **concave** function of $p$ — *anomalous scaling*.

---

## 4. The Legendre Transform Structure in Detail

### 4.1 Making the Legendre Structure Explicit

Define $C(h) = D(h) - 3$, so that $C(h) \leq 0$ and the formula reads

$$\zeta_p = \inf_h \bigl[ph - C(h)\bigr] = \sup_h \bigl[C(h) - ph\bigr] \cdot (-1).$$

More precisely, writing $\zeta_p = \inf_h [ph - C(h)]$, we recognize this as the **Legendre–Fenchel transform** of $C(h)$:

$$\zeta_p = C^*(p),$$

where $C^*(p) = \sup_h [ph - C(h)]$... let me be precise about signs.

The cleanest convention: define

$$\tau(p) = \zeta_p - 3.$$

Then

$$\tau(p) = \inf_h \bigl[ph - D(h)\bigr].$$

Now $\tau(p)$ and $D(h)$ are related by a **Legendre–Fenchel transform pair** (up to a sign):

$$\tau(p) = \inf_h \bigl[ph - D(h)\bigr] = -\sup_h \bigl[D(h) - ph\bigr],$$

so $-\tau(p) = \sup_h [D(h) - ph]$, which is the concave conjugate of $D$.

If $D(h)$ is smooth and strictly concave, the **inverse transform** recovers $D$:

$$\boxed{D(h) = \inf_p \bigl[ph - \tau(p)\bigr] = \inf_p \bigl[ph - \zeta_p + 3\bigr].}$$

### 4.2 Saddle-Point Conditions

At the saddle point (the $h$ that achieves the infimum for a given $p$):

$$\frac{d}{dh}\bigl[ph + 3 - D(h)\bigr] = 0 \quad \Longrightarrow \quad p = D'(h).$$

That is, the slope of the singularity spectrum at the relevant $h$ equals the moment order $p$. Equivalently, the value of $h$ selected by the $p$-th moment is

$$h(p) = \frac{d\zeta_p}{dp} = \zeta_p'.$$

And at this saddle point,

$$D(h(p)) = ph(p) - \zeta_p + 3.$$

This pair of relations — $h = \zeta_p'$ and $D = ph - \zeta_p + 3$ — is the operational recipe for going from measured $\zeta_p$ to the singularity spectrum $D(h)$.

### 4.3 The Thermodynamic Analogy

The Legendre transform relating $D(h)$ and $\zeta_p$ has exactly the same structure as the transforms of equilibrium thermodynamics:

| Turbulence | Thermodynamics | Large Deviations |
|---|---|---|
| $h$ (Hölder exponent) | $E$ (energy) | outcome variable |
| $p$ (moment order) | $\beta = 1/k_B T$ (inverse temperature) | tilting parameter |
| $D(h)$ (singularity spectrum) | $S(E)$ (entropy) | negative rate function |
| $\tau(p) = \zeta_p - 3$ | $-\beta F$ (neg. free energy) | log-moment generating function |

The passage from the microcanonical description ($D(h)$: "how many configurations have exponent $h$?") to the canonical description ($\zeta_p$: "what is the $p$-th moment?") is the same Legendre transform in all three settings. The saddle-point equation $p = D'(h)$ corresponds to the thermodynamic relation $\beta = S'(E)$ — the moment order plays the role of inverse temperature, and the Hölder exponent plays the role of energy.

---

## 5. Connection to Large Deviations Theory

### 5.1 The Scaling Exponent as a Random Variable

Fix a point $\mathbf{x}$ and define the *local scaling exponent* at scale $\ell$:

$$h_\ell(\mathbf{x}) = \frac{\ln |\delta v(\ell, \mathbf{x})|}{\ln(\ell / \ell_0)}.$$

As $\ell \to 0$, $h_\ell$ converges (in some sense) to the true Hölder exponent $h(\mathbf{x})$. But we can also think of $h_\ell$ as a **random variable** (random over the choice of $\mathbf{x}$, or equivalently, over realizations of the turbulent field).

The multifractal formalism asserts that the distribution of $h_\ell$ satisfies a **large deviation principle** as $\ell \to 0$:

$$\boxed{\mathrm{Prob}\bigl(h_\ell \in [h, h+dh]\bigr) \;\sim\; \left(\frac{\ell}{\ell_0}\right)^{3 - D(h)} dh.}$$

Here $3 - D(h) \geq 0$ is the **rate function**: the probability of observing a "rare" exponent $h$ far from the most probable value $h^*$ (where $D(h^*) = 3$) decays as a power law in $\ell$, with exponent $3 - D(h)$.

Compare with the standard large deviations setup: if $X_n$ is a sequence of random variables with rate function $I(x)$, then $\mathrm{Prob}(X_n \approx x) \sim e^{-n I(x)}$. Here the role of $n$ is played by $-\ln(\ell/\ell_0)$ (the number of cascade steps), and we write

$$\mathrm{Prob}(h_\ell \approx h) \sim e^{-[3-D(h)] \cdot |\ln(\ell/\ell_0)|} = \left(\frac{\ell}{\ell_0}\right)^{3-D(h)}.$$

So $I(h) = 3 - D(h)$ is literally the rate function, and the singularity spectrum $D(h) = 3 - I(h)$ is the "complement" of the rate function relative to the ambient dimension.

### 5.2 Cramér's Theorem and Multiplicative Cascades

The large deviations perspective becomes especially powerful when we model the cascade as a **multiplicative process**. At each cascade step, the velocity multiplier is an iid random variable $W$:

$$\delta v(\ell) = \delta v(\ell_0) \cdot W_1 \cdot W_2 \cdots W_n,$$

so the Hölder exponent is

$$h_\ell = \frac{1}{n} \sum_{i=1}^n \ln W_i \cdot \frac{1}{\ln r} + \text{const}.$$

This is a **sample mean** of iid random variables. By **Cramér's theorem**, the rate function for the sample mean is the Legendre–Fenchel transform of the log-moment generating function:

$$I(h) = \sup_p \bigl[ph - \Lambda(p)\bigr], \qquad \Lambda(p) = \ln \mathbb{E}[W^p] / |\ln r|.$$

Since $I(h) = 3 - D(h)$ and $\Lambda(p) = -\tau(p) / |\ln r| \cdot |\ln r| = 3 - \zeta_p$... let's be precise. Identifying the rate function:

$$3 - D(h) = \sup_p \bigl[ph - \Lambda(p)\bigr],$$

where $\Lambda(p)$ is the cumulant generating function of the multiplier in the appropriate scaling. Taking the Legendre dual:

$$\Lambda(p) = \sup_h \bigl[ph - (3 - D(h))\bigr] = \sup_h \bigl[ph - 3 + D(h)\bigr] = -\inf_h[ph + 3 - D(h)] + \text{...}$$

The key point is that $\tau(p) = \zeta_p - 3$ is (up to normalization) the cumulant generating function $\Lambda(p)$, and $D(h)$ is recovered from it via the Legendre transform. **Cramér's theorem provides the rigorous justification for the saddle-point evaluation** we did heuristically in Section 3.2.

This also explains *why* $D(h)$ should be concave: rate functions arising from Cramér's theorem are always convex, so $I(h) = 3 - D(h)$ is convex, hence $D(h)$ is concave.

### 5.3 The Cascade as a Branching Random Walk

There is an even deeper connection. In the multiplicative cascade, the logarithmic multipliers $\ln W_i$ execute a **random walk** along the branches of the cascade tree. The multifractal spectrum $D(h)$ encodes the "population" of branches that arrive at a given average step size $h$ after $n$ steps. This is precisely the setting of the **branching random walk**, and the singularity spectrum is related to the free energy of the associated directed polymer on a tree.

This connection to branching random walks and directed polymers is one of the deep structural reasons why the multifractal formalism appears in so many seemingly unrelated contexts: turbulence, financial time series, random matrices, quantum gravity.

---

## 6. Probabilistic Reformulation

### 6.1 From Geometry to Probability

The geometric language — "the set of points with exponent $h$ has dimension $D(h)$" — is vivid but can be misleading. Computing fractal dimensions rigorously requires delicate limit procedures, and the "sets" in question may not be well-defined for a single realization of a random field.

The modern reformulation avoids these issues by working directly with probability. Define the **partition function** at scale $\ell$:

$$Z_p(\ell) = \sum_i |\delta v_i(\ell)|^p,$$

where the sum is over a partition of the domain into cells of size $\ell$, and $\delta v_i(\ell)$ is the velocity increment in cell $i$. Then

$$Z_p(\ell) \sim \ell^{\tau(p) + 3}, \qquad \tau(p) = \zeta_p - 3.$$

The scaling exponents $\tau(p)$ are defined purely in terms of moments — no fractal geometry needed. The singularity spectrum $D(h)$ is then *defined* as the Legendre transform of $\tau(p)$:

$$D(h) = \inf_p [ph - \tau(p)].$$

This is a theorem (under appropriate regularity conditions), not an assumption. The geometric interpretation of $D(h)$ as a fractal dimension is then a *consequence*, not a starting point.

### 6.2 Advantages of the Probabilistic Viewpoint

1. **Rigorous:** No need to define or compute fractal dimensions of random sets.
2. **Statistical:** $\tau(p)$ can be estimated directly from data via log-log regression of $Z_p(\ell)$ versus $\ell$.
3. **General:** Applies to any random field with power-law scaling, not just velocity fields.
4. **Connection to statistical mechanics** is more transparent: $Z_p(\ell)$ is literally a partition function, $p$ is the inverse temperature, $\tau(p)$ is the free energy.

---

## 7. Comparison with Experimental Data

### 7.1 Measured Scaling Exponents

High-Reynolds-number experiments and DNS (direct numerical simulations) have measured $\zeta_p$ up to $p \approx 8$–$12$. Key values:

| $p$ | K41 ($p/3$) | $\beta$-model ($D = 2.8$) | Experiment |
|-----|-------------|---------------------------|------------|
| 1 | 0.333 | 0.400 | $\approx 0.37$ |
| 2 | 0.667 | 0.733 | $\approx 0.70$ |
| 3 | 1.000 | 1.000 | $1.000$ (exact) |
| 4 | 1.333 | 1.267 | $\approx 1.28$ |
| 5 | 1.667 | 1.533 | $\approx 1.54$ |
| 6 | 2.000 | 1.800 | $\approx 1.77$ |
| 8 | 2.667 | 2.333 | $\approx 2.21$ |

The experimental values show clear **concave** curvature — $\zeta_p$ grows slower than $p/3$ for large $p$. The $\beta$-model (any monofractal) gives a straight line, which deviates from the data at both low and high $p$. Only a multifractal model can capture the curvature.

### 7.2 The She–Lévêque Formula

She and Lévêque (1994) proposed a formula derived from a log-Poisson model for the cascade:

$$\boxed{\zeta_p = \frac{p}{9} + 2\left[1 - \left(\frac{2}{3}\right)^{p/3}\right].}$$

**Check:**
- $\zeta_3 = 1/3 + 2(1 - 2/3) = 1/3 + 2/3 = 1$. Exact.
- $\zeta_6 = 2/3 + 2(1 - 4/9) = 2/3 + 10/9 = 16/9 \approx 1.78$.
- $\zeta_2 = 2/9 + 2(1 - (2/3)^{2/3}) \approx 0.222 + 2(1 - 0.763) \approx 0.696$.

These match the experimental data remarkably well. The physical assumptions behind She–Lévêque are:

1. The most singular structures are **one-dimensional** (vortex filaments), so $D(h_{\min}) = 1$, i.e., $\text{codim} = 2$.
2. The cascade multipliers follow a **log-Poisson** distribution (as opposed to log-normal), which yields the specific functional form $(2/3)^{p/3}$.

The corresponding singularity spectrum $D(h)$ can be computed via the Legendre transform of the She–Lévêque $\zeta_p$. It is a smooth concave curve with:
- Maximum at $D(h^*) = 3$ (the most probable exponent),
- $D(h_{\min}) = 1$ at the most singular end (filamentary structures),
- $h$ ranging over an interval roughly $[0.16, 0.69]$.

### 7.3 The Singularity Spectrum from Data

Given measured $\zeta_p$ (typically for integer or half-integer $p$), one computes $D(h)$ by:

1. Fit a smooth interpolant to $\zeta_p$ (e.g., polynomial or the She–Lévêque form),
2. Compute $h(p) = d\zeta_p / dp$,
3. Compute $D(h(p)) = ph(p) - \zeta_p + 3$.

Plotting $D$ vs. $h$ gives the singularity spectrum. For real turbulence, this is an inverted parabola-like curve, peaked at $h^* \approx 0.33$–$0.36$ (near the K41 value) with $D(h^*) \approx 3$.

---

## Summary and Key Takeaways

The progression from K41 to multifractals is a progression in the *complexity of the scaling description*:

| Model | # of exponents | $\zeta_p$ | $D(h)$ |
|-------|----------------|-----------|--------|
| K41 | 1 ($h = 1/3$) | Linear: $p/3$ | Delta function at $h = 1/3$ |
| $\beta$-model | 1 ($h, D$) | Linear: $ph + (3-D)$ | Single point $(h, D)$ |
| Bifractal | 2 | Piecewise linear | Two points |
| Multifractal | $\infty$ | Smooth, concave | Smooth, concave curve |

The **Legendre transform** is the unifying mathematical structure:

$$\zeta_p = \inf_h [ph + 3 - D(h)], \qquad D(h) = \inf_p [ph - \zeta_p + 3].$$

This is the same duality that appears in:
- **Thermodynamics:** entropy $\leftrightarrow$ free energy,
- **Large deviations:** rate function $\leftrightarrow$ cumulant generating function,
- **Convex analysis:** a function $\leftrightarrow$ its Legendre–Fenchel conjugate.

The practical upshot: to characterize intermittency in turbulence (or any multiscaling phenomenon), you need either $\zeta_p$ for all $p$ or $D(h)$ for all $h$ — they carry the same information, connected by a Legendre transform. The She–Lévêque formula provides a one-parameter family that fits the data well and has a physical interpretation in terms of filamentary vortex structures.

---

**Next:** Tutorial 5 will discuss specific cascade models (random $\beta$-model, $p$-model, log-normal, log-Poisson) and their predictions for $D(h)$.
