# Tutorial 3 — Intermittency I: From Experiments to Exact Constraints

> **Series**: Turbulence Theory
> **Prerequisites**: K41 theory (Tutorial 1), four-fifths law (Tutorial 2)
> **Key references**: Frisch, *Turbulence* (1995), Ch. 8; Anselmet, Gagne, Hopfinger & Antonia (1984)

---

Kolmogorov's 1941 theory (K41) predicts that velocity increments in the inertial range are self-similar with exponent $h = 1/3$. This is elegant, universal, and wrong — or at least incomplete. The failure has a name: **intermittency**. This tutorial develops the concept, shows how experiments expose it, and derives the rigorous constraints that any correction to K41 must satisfy.


## What Is Intermittency?

### Self-similar vs. intermittent signals

A random function $v(t)$ is **self-similar** if zooming in on any sub-interval produces, statistically, a rescaled copy of the whole. The prototype is fractional Brownian motion $B_h(t)$ with Hurst exponent $h$: the increments $B_h(t+\tau) - B_h(t)$ have the same law as $\lambda^h [B_h(t+\tau/\lambda) - B_h(t)]$ for any $\lambda > 0$. At every scale, the signal "looks the same" — the active regions fill space uniformly.

An **intermittent** signal is fundamentally different. As you zoom into finer scales, the activity concentrates on a progressively smaller fraction of the domain. The canonical mathematical example is the **Devil's staircase** (the Cantor function): a continuous, monotonically non-decreasing function whose derivative is zero almost everywhere, yet which increases from 0 to 1. All the "action" lives on a fractal set of measure zero.

The physical picture for turbulence: at small scales, intense velocity gradients are not spread uniformly through the flow. They concentrate in thin filaments and sheets — isolated bursts of extreme activity, separated by quiescent regions. This spatial and temporal spottiness is intermittency.

### Flatness: an operational diagnostic

Given a stationary signal $v(t)$, apply a high-pass filter at frequency $\Omega$ to extract the small-scale component $v^>_\Omega(t)$. Define the **flatness** (or kurtosis):

$$F(\Omega) = \frac{\langle (v^>_\Omega)^4 \rangle}{\langle (v^>_\Omega)^2 \rangle^2}.$$

This is a scale-dependent measure of how "peaked" the distribution of small-scale fluctuations is:

- **Gaussian signal**: $F = 3$ at all $\Omega$, independent of scale.
- **Self-similar signal**: $F$ is constant (though not necessarily 3) — the shape of the distribution does not change with scale.
- **Intermittent signal**: $F(\Omega) \to \infty$ as $\Omega \to \infty$. The distribution develops heavier and heavier tails at smaller scales.

A growing flatness is the signature of intermittency: the small-scale fluctuations are increasingly dominated by rare, extreme events.

### A toy model: the "chopped" signal

To build intuition, consider a simple model: a signal $v(t)$ that is "on" (drawn from some distribution) for a fraction $\gamma$ of the time, and zero otherwise. If the non-zero part has flatness $F_0 = \langle v^4 \rangle / \langle v^2 \rangle^2$, then for the full signal:

$$\langle v^4 \rangle_{\text{full}} = \gamma \langle v^4 \rangle, \qquad \langle v^2 \rangle_{\text{full}} = \gamma \langle v^2 \rangle,$$

so the flatness of the chopped signal is:

$$F_\gamma = \frac{\gamma \langle v^4 \rangle}{(\gamma \langle v^2 \rangle)^2} = \frac{1}{\gamma} \cdot \frac{\langle v^4 \rangle}{\langle v^2 \rangle^2} = \frac{F_0}{\gamma}.$$

As $\gamma \to 0$, the flatness diverges: concentrating activity onto a smaller fraction of the domain drives up the flatness. If the active fraction $\gamma(\Omega)$ decreases with frequency (finer scales), the flatness grows — precisely the intermittency diagnostic.


## Self-Similar Scaling and Its Consequence

### Why self-similarity kills intermittency

Suppose $v(t)$ has self-similar increments with exponent $h$. Then the high-pass filtered signal satisfies

$$v^>_{\lambda\Omega} \stackrel{\text{law}}{=} \lambda^{-h}\, v^>_\Omega$$

for any rescaling factor $\lambda > 0$. Substituting into the flatness:

$$F(\lambda\Omega) = \frac{\langle (v^>_{\lambda\Omega})^4 \rangle}{\langle (v^>_{\lambda\Omega})^2 \rangle^2} = \frac{\langle (\lambda^{-h} v^>_\Omega)^4 \rangle}{\langle (\lambda^{-h} v^>_\Omega)^2 \rangle^2} = \frac{\lambda^{-4h} \langle (v^>_\Omega)^4 \rangle}{\lambda^{-4h} \langle (v^>_\Omega)^2 \rangle^2} = F(\Omega).$$

The $\lambda$-dependence cancels exactly. **A self-similar signal has scale-independent flatness: it is not intermittent.**

### The K41 prediction

K41 asserts self-similar scaling of velocity increments with exponent $h = 1/3$, inherited from the dimensional constraint $\delta v \sim (\varepsilon \ell)^{1/3}$. This predicts:

- The flatness of inertial-range velocity fluctuations should be constant.
- The probability distribution of $\delta v_\ell / \ell^{1/3}$ should be independent of $\ell$.

**But experiments show the flatness grows with frequency in the inertial range.** The distributions of velocity increments develop increasingly heavy tails at smaller scales. K41 is therefore incomplete: the real turbulent velocity field is intermittent, not self-similar.


## Experimental Evidence

### Structure function exponents

The central observable is the longitudinal velocity structure function of order $p$:

$$S_p(\ell) = \langle |\delta v_\|(\ell)|^p \rangle,$$

where $\delta v_\|(\ell) = [\mathbf{v}(\mathbf{x} + \boldsymbol{\ell}) - \mathbf{v}(\mathbf{x})] \cdot \hat{\boldsymbol{\ell}}$ is the longitudinal velocity increment over separation $\ell$. In the inertial range, one assumes power-law scaling:

$$S_p(\ell) \propto \ell^{\zeta_p}.$$

K41 predicts $\zeta_p = p/3$, a straight line through the origin. Intermittency means the actual $\zeta_p$ deviates from this line.

### The measurements

The landmark experiments are those of **Anselmet, Gagne, Hopfinger & Antonia (1984)** in a jet at $R_\lambda \approx 500{-}850$, with further refinements by **Gagne (1987)**. Measured exponents include:

| $p$ | $\zeta_p$ (K41) | $\zeta_p$ (measured) |
|-----|:---:|:---:|
| 2 | 0.667 | $\approx 0.70$ |
| 3 | 1.000 | $\approx 1.00$ |
| 4 | 1.333 | $\approx 1.28$ |
| 6 | 2.000 | $\approx 1.78$ |
| 8 | 2.667 | $\approx 2.33$ |

Several features stand out:

1. **$\zeta_2 \approx 0.70$**, close to but slightly above the K41 value of $2/3$. The energy spectrum exponent $E(k) \sim k^{-\beta}$ with $\beta = 1 + \zeta_2$ is thus slightly steeper than $-5/3$.

2. **$\zeta_3 = 1$ exactly.** This is not a fitting parameter — it is guaranteed by the four-fifths law (Tutorial 2), the one exact result in turbulence theory. It provides a crucial anchor point.

3. **$\zeta_6 \approx 1.78$**, significantly below K41's prediction of 2. The **intermittency parameter** $\mu$ is conventionally defined as

$$\mu \equiv 2 - \zeta_6 \approx 0.2.$$

This single number quantifies the deviation from K41 at sixth order. It is related to the scaling of the dissipation correlation: $\langle \varepsilon(\mathbf{x})\, \varepsilon(\mathbf{x}+\boldsymbol{\ell}) \rangle \sim \ell^{-\mu}$.

4. The full curve $\zeta_p$ vs. $p$ is **concave** and lies **below the K41 line** $p/3$ for all $p > 3$.

### Extended Self-Similarity (ESS)

Direct measurement of $\zeta_p$ from log-log plots of $S_p(\ell)$ vs. $\ell$ is difficult: the inertial range is often narrow (barely a decade even at $R_\lambda \sim 1000$), and the scaling is contaminated by crossovers to dissipation and large-scale ranges.

**Benzi, Ciliberto, Tripiccione, Baudet, Massaioli & Succi (1993)** introduced a powerful trick: **Extended Self-Similarity (ESS)**. Instead of plotting $S_p(\ell)$ against $\ell$, plot $S_p(\ell)$ against $S_{p'}(\ell)$ on a log-log scale, for some reference order $p'$ (typically $p' = 3$, exploiting $\zeta_3 = 1$). The resulting curve:

$$\log S_p \quad \text{vs.} \quad \log S_3$$

gives a slope equal to the **ratio** $\zeta_p / \zeta_3 = \zeta_p$, and this scaling extends far beyond the inertial range — often spanning three decades or more, even in moderate-Reynolds-number flows.

The physical reason ESS works so well is not fully understood, but the practical consequence is dramatic: relative exponents $\zeta_p / \zeta_3$ can be measured with much higher precision. ESS has become a standard tool in the field.


## Exact Results on the Exponents $\zeta_p$

We now turn from measurement to rigorous constraints. Assuming that the even-order structure functions have power-law scaling in the inertial range,

$$S_{2p}(\ell) \sim A_{2p} \left(\frac{\ell}{\ell_0}\right)^{\zeta_{2p}}, \qquad \ell_d \ll \ell \ll \ell_0,$$

where $\ell_0$ is the integral scale and $\ell_d$ the dissipation scale, what can we prove about $\zeta_{2p}$?

The following results are due to Frisch (1995, Section 8.4). They are not models — they are mathematical consequences of the assumed scaling form plus elementary inequalities.

### P1 — Concavity of $\zeta_{2p}$

**Theorem.** The function $p \mapsto \zeta_{2p}$ is concave.

**Proof.** Take three values $p_1 < p_2 < p_3$ and set $X = |\delta v_\|(\ell)|^2$. Holder's inequality for random variables states: for $\alpha, \beta > 1$ with $1/\alpha + 1/\beta = 1$,

$$\langle |Y Z| \rangle \leq \langle |Y|^\alpha \rangle^{1/\alpha} \langle |Z|^\beta \rangle^{1/\beta}.$$

Applying this (or equivalently, the log-convexity of $L^p$ norms), one obtains the interpolation inequality:

$$\langle X^{p_2} \rangle^{(p_3 - p_1)} \leq \langle X^{p_1} \rangle^{(p_3 - p_2)} \langle X^{p_3} \rangle^{(p_2 - p_1)}.$$

This is a standard consequence of Holder's inequality. Taking $X = |\delta v_\|(\ell)|^2$ so that $\langle X^p \rangle = S_{2p}(\ell)$, and substituting the assumed scaling $S_{2p}(\ell) \sim A_{2p} (\ell/\ell_0)^{\zeta_{2p}}$, we get:

$$A_{2p_2}^{p_3 - p_1} \left(\frac{\ell}{\ell_0}\right)^{\zeta_{2p_2}(p_3 - p_1)} \leq A_{2p_1}^{p_3 - p_2} A_{2p_3}^{p_2 - p_1} \left(\frac{\ell}{\ell_0}\right)^{\zeta_{2p_1}(p_3 - p_2) + \zeta_{2p_3}(p_2 - p_1)}.$$

For this to hold at all inertial-range scales $\ell$ (in particular as $\ell/\ell_0 \to 0$), the exponent on the left must be at least as large as the exponent on the right:

$$\zeta_{2p_2}(p_3 - p_1) \geq \zeta_{2p_1}(p_3 - p_2) + \zeta_{2p_3}(p_2 - p_1).$$

This is exactly the condition that $\zeta_{2p}$ is a **concave** function of $p$. $\square$

**Remark.** Concavity of $\zeta_p$ (extended to all real $p$) is a purely kinematic statement — it follows from Holder's inequality alone, requiring no dynamics.

### P2 — Unbounded velocity implies $\zeta_{2p}$ is non-decreasing

**Theorem.** If $\zeta_{2p} < \zeta_{2p+2}$ fails for some $p$ — that is, if the exponents eventually decrease — then the velocity field cannot be bounded.

**Proof.** Suppose the velocity field is bounded: $|\mathbf{v}(\mathbf{x})| \leq U_{\max}$ everywhere. Then the longitudinal increment satisfies $|\delta v_\|(\ell)| \leq 2U_{\max}$, and therefore:

$$S_{2p+2}(\ell) = \langle |\delta v_\|(\ell)|^{2p+2} \rangle \leq (2U_{\max})^2 \langle |\delta v_\|(\ell)|^{2p} \rangle = (2U_{\max})^2\, S_{2p}(\ell).$$

Using the assumed scaling:

$$A_{2p+2} \left(\frac{\ell}{\ell_0}\right)^{\zeta_{2p+2}} \leq (2U_{\max})^2 A_{2p} \left(\frac{\ell}{\ell_0}\right)^{\zeta_{2p}}.$$

If $\zeta_{2p+2} < \zeta_{2p}$, then as $\ell \to 0$ the left side grows faster than the right (since $\ell/\ell_0 < 1$ and $\zeta_{2p+2} < \zeta_{2p}$ means the left exponent is more negative). The inequality is eventually violated, contradicting the boundedness assumption.

More precisely: rearranging,

$$\frac{A_{2p+2}}{(2U_{\max})^2 A_{2p}} \leq \left(\frac{\ell}{\ell_0}\right)^{\zeta_{2p} - \zeta_{2p+2}}.$$

If $\zeta_{2p} - \zeta_{2p+2} > 0$, the right side goes to zero as $\ell \to 0$, while the left side is a positive constant — contradiction. $\square$

**Consequence.** For a bounded velocity field (as physically expected), $\zeta_{2p}$ must be **non-decreasing**. Combined with concavity (P1), the exponents must flatten out: $\zeta_{2p}$ approaches a finite limit as $p \to \infty$.

### P3 — Growing Mach number and the incompressibility tension

**Theorem.** If $\zeta_{2p}$ eventually decreases (violating P2), then increasing the Reynolds number at fixed large-scale velocity $v_0$ forces the maximum velocity $U_{\max}$ to grow without bound.

The argument runs as follows. In a turbulent flow, the Reynolds number is $\operatorname{Re} = v_0 \ell_0 / \nu$. At fixed $v_0$ and $\ell_0$, increasing Re means decreasing $\nu$. But the structure function scaling

$$S_{2p}(\ell) \sim A_{2p} (\ell/\ell_0)^{\zeta_{2p}}$$

extends down to the dissipation scale $\ell_d \sim \ell_0 \operatorname{Re}^{-3/4}$ (in K41 estimation). From P2, if $\zeta_{2p}$ decreases, then the velocity field is unbounded. More carefully: the ratio $U_{\max}/v_0$ must grow with Re, meaning the maximum Mach number $U_{\max}/c_s$ grows without bound — contradicting the assumption of incompressible Navier-Stokes, which requires low Mach number throughout the domain.

**Physical meaning.** Strong intermittency (a $\zeta_p$ curve that eventually turns over) would produce velocity spikes so extreme that they violate incompressibility. This places a physical bound on how "wild" the exponent curve can be.


## What the Four-Fifths Law Anchors

The four-fifths law (derived in Tutorial 2) is the unique exact result for inertial-range scaling. It fixes:

$$\zeta_3 = 1.$$

This is not a measurement — it is a theorem, valid in the limit $\operatorname{Re} \to \infty$ for homogeneous isotropic turbulence with finite, non-zero mean dissipation. Combined with the concavity constraint (P1), it has powerful consequences.

### Bounding the exponents

Since $\zeta_p$ is concave and passes through the origin ($\zeta_0 = 0$) and the anchor point $\zeta_3 = 1$, elementary geometry of concave functions gives:

$$\boxed{\zeta_p \leq \frac{p}{3} \quad \text{for } p \geq 3, \qquad \zeta_p \geq \frac{p}{3} \quad \text{for } 0 \leq p \leq 3.}$$

The K41 line $\zeta_p = p/3$ is a tangent line at $p = 3$. Any intermittency (non-linearity of $\zeta_p$) pushes $\zeta_p$ below the K41 prediction for high orders and above it for low orders. This is exactly what experiments show.

### A consistency check

The experimental values satisfy these bounds:

- $\zeta_2 \approx 0.70 \geq 2/3 \approx 0.667$ (above K41, as required for $p < 3$). Check.
- $\zeta_6 \approx 1.78 \leq 2.0$ (below K41, as required for $p > 3$). Check.
- $\zeta_3 = 1.00$ (exactly on the K41 line). Anchored by theorem.


## Summary: The Constraints Any Model Must Satisfy

We are now in a position to state what any intermittency model (the subject of Tutorial 4) must deliver:

1. **$\zeta_3 = 1$ exactly** — anchored by the four-fifths law.
2. **$\zeta_p$ is concave** — from Holder's inequality (P1).
3. **$\zeta_p$ is non-decreasing** — from boundedness of velocity (P2), consistent with incompressibility (P3).
4. **$\zeta_p \leq p/3$ for $p \geq 3$** and **$\zeta_p \geq p/3$ for $p \leq 3$** — from concavity plus the anchor.
5. **$\mu = 2 - \zeta_6 \approx 0.2$** — the intermittency parameter, a key quantitative target.
6. **The $\zeta_p$ curve matches the full set of experimental values**, not just a few low-order moments.

The message is sharp: K41 gives the correct answer at $p = 3$ (guaranteed by an exact theorem) and good approximations at low $p$, but it fails progressively for higher-order statistics. Intermittency is real, experimentally robust, and mathematically constrained. The question is no longer *whether* to go beyond K41, but *how* — subject to these exact constraints.

---

> **Next**: Tutorial 4 — Intermittency II: Models (multifractal formalism, log-normal and log-Poisson models, She-Leveque)
