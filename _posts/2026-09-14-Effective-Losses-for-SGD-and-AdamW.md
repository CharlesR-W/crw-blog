---
title: "Effective Losses for SGD and AdamW: One Fast-Slow Calculation, Six Phenomena"
tags: [notes, ai]
date: 2026-09-14
math: true
---


*Status legend used throughout: **[lit]** = standard result, cited; **[reformulation]** = a literature result rewritten in the notation here; **[extension]** = a small step beyond the literature that I believe is correct but haven't seen stated; **[conjecture]** = flagged guess. References are tiered at the end.*

## 0. What this is

Every "implicit regularizer" I know of for gradient-based training — implicit gradient regularization from finite step size, the SGD batch-noise term, catapults, edge of stability and its continuous-time models (central flow, rod flow), label-noise sharpness reduction, angular equilibrium under normalization plus weight decay, and the momentum / Adam variants of each — comes out of the same calculation. You split the parameter trajectory into a **slow centre** and a **fast fluctuation**, expand the update to second order in the fluctuation, and average. What differs between the phenomena is only the **closure**: what the fast variable is, and what fixes its second moment.

This post does three things.

1. Sets up backward error analysis (BEA) and the fast–slow "master formula" in one notation.
2. Derives each phenomenon as a closure of that formula, at the physics level of rigour.
3. Collects the results into an effective loss $$\mathcal L_{\rm eff}$$ at order $$\eta$$, decomposes it per Hessian mode, and lists the dimensionless numbers that say which term wins in which mode at which time.

Scope: classification with cross-entropy (MSE where the literature uses it), a single global loss $$L(\theta)$$, no attention to what is inside the network. Data enters only through the per-sample gradient covariance and the Hessian's spectral structure (Section 9). I do not treat interactions between the effects beyond what the master formula gives for free; where an interaction needs its own analysis I say so.

### Notation

- Parameters $$\theta \in \mathbb R^P$$, loss $$L(\theta) = \frac1N \sum_{i=1}^N \ell_i(\theta)$$, $$\ell_i = \ell(f(x_i;\theta), y_i)$$.
- $$g = \nabla L$$, $$H = \nabla^2 L$$, $$T = \nabla^3 L$$ (a symmetric 3-tensor). I write $$T[a,b]_j = T_{jkl} a_k b_l$$ and $$T[C]_j = T_{jkl} C_{kl}$$ for a matrix $$C$$.
- Hessian eigenpairs $$H u_k = \lambda_k u_k$$, with $$\lambda_1 \ge \lambda_2 \ge \dots$$; "sharpness" means $$\lambda_1$$. Mode components $$g_k = u_k \cdot g$$, etc.
- Minibatch gradient $$\hat g = g + \xi$$, $$\langle \xi \rangle = 0$$, and its Jacobian $$\hat H = H + \Xi$$ with $$\Xi = \nabla \xi$$. Per-sample gradient covariance $$\Sigma = \frac1N \sum_i (g_i - g)(g_i - g)^\top$$, so a batch of size $$B$$ has $$\langle \xi \xi^\top \rangle \approx \Sigma / B$$. An epoch is $$m = N/B$$ steps.
- Learning rate $$\eta$$, weight decay $$\gamma$$, momentum $$\beta$$ (Adam: $$\beta_1$$, $$\beta_2$$). **Time is measured in steps** throughout; a flow $$d\bar\theta/dt = -\eta(\cdots)$$ advances one step per unit time, matching the central-flow and rod-flow conventions.
- A useful identity I use repeatedly (Hellmann–Feynman): for a non-degenerate eigenvalue, $$\partial_j \lambda_k = u_k^\top (\partial_j H) u_k$$, i.e. $$T[u_k, u_k] = \nabla \lambda_k$$. So the third derivative of $$L$$ contracted with a Hessian eigenvector is the gradient of that eigenvalue.

---

## 1. Backward error analysis in one page **[lit]**

Gradient descent is $$\theta_{t+1} = \theta_t - \eta\, g(\theta_t)$$. BEA asks for a *modified* vector field $$f = f_0 + \eta f_1 + \eta^2 f_2 + \dots$$ whose exact time-$$\eta$$ flow reproduces the discrete map order by order. This is the "geometric integration" sense of the phrase ([Hairer, Lubich and Wanner](https://link.springer.com/book/10.1007/3-540-30666-8)), imported into deep learning by [Barrett and Dherin (2021)](https://arxiv.org/abs/2009.11162) and [Smith, Dherin, Barrett and De (2021)](https://arxiv.org/abs/2101.12176).

**Derivation.** Along $$\dot\theta = f(\theta)$$, the Taylor series of the flow is

$$\theta(\eta) = \theta + \eta f + \frac{\eta^2}{2} (\partial f) f + \frac{\eta^3}{6}\big[(\partial f)^2 f + \partial^2 f\,(f,f)\big] + O(\eta^4),$$

using $$\ddot\theta = (\partial f)\dot\theta$$ and $$\dddot\theta = \partial^2 f(\dot\theta,\dot\theta) + (\partial f)\ddot\theta$$. Set this equal to $$\theta - \eta g$$ and match powers of $$\eta$$:

- $$O(\eta)$$: $$f_0 = -g$$.
- $$O(\eta^2)$$: $$f_1 + \frac12 (\partial f_0) f_0 = 0$$. Since $$\partial f_0 = -H$$, $$(\partial f_0)f_0 = Hg$$, so $$f_1 = -\frac12 H g = -\frac14 \nabla \Vert g\Vert ^2$$.
- $$O(\eta^3)$$: $$f_2 + \frac12\big[(\partial f_0) f_1 + (\partial f_1) f_0\big] + \frac16\big[\partial^2 f_0(f_0,f_0) + (\partial f_0)^2 f_0\big] = 0$$. With $$\partial f_1 = -\frac12(T[g] + H^2)$$ (where $$T[g]_{jm} = T_{jml} g_l$$) and $$\partial^2 f_0 = -T$$, the pieces are $$(\partial f_0) f_1 = \frac12 H^2 g$$, $$(\partial f_1) f_0 = \frac12 (T[g,g] + H^2 g)$$, $$\partial^2 f_0(f_0,f_0) = -T[g,g]$$, $$(\partial f_0)^2 f_0 = -H^2 g$$. Collecting: $$f_2 = -\frac13 H^2 g - \frac1{12} T[g,g]$$.

So

$$\boxed{\;\dot\theta = -\nabla\Big(L + \frac{\eta}{4}\Vert \nabla L\Vert ^2\Big) - \eta^2\Big(\tfrac13 H^2 g + \tfrac1{12} T[g,g]\Big) + O(\eta^3).\;}$$

The $$O(\eta)$$ term is **implicit gradient regularization (IGR)**: the discrete iterates follow, to this order, gradient flow on $$\tilde L = L + \frac{\eta}{4}\Vert \nabla L\Vert ^2$$.

**Sanity check on a quadratic mode.** For $$L = \frac12 \lambda \theta^2$$, GD gives $$\theta_{t+1} = (1-\eta\lambda)\theta_t$$, whose exact interpolating flow is $$\dot\theta = \eta^{-1}\ln(1-\eta\lambda)\,\theta$$. Expanding, $$-\eta^{-1}\ln(1-\eta\lambda) = \lambda\big(1 + \frac{\eta\lambda}{2} + \frac{\eta^2\lambda^2}{3} + \dots\big)$$, matching the boxed formula term by term. Two morals:

- **IGR is a per-mode rescaling of the learning rate.** $$\nabla \frac{\eta}{4}\Vert g\Vert ^2 = \frac{\eta}{2} H g$$ exactly, so the modified flow is $$\dot\theta = -(1 + \frac{\eta}{2}H)\nabla L$$: a preconditioned flow whose preconditioner boosts sharp modes by the factor $$(1 + \eta\lambda_k/2)$$. There is no $$\nabla\lambda$$ (flatness-seeking) force in IGR at this order; the "prefers flat minima" story of Barrett and Dherin is about which trajectory you end up on, via $$\Vert \nabla L\Vert ^2 \approx d^\top H^2 d$$ being larger near sharp minima at equal $$L$$.
- **The series has radius of convergence $$\eta\lambda < 1$$.** For $$1 < \eta\lambda < 2$$ the iterates converge but alternate sign; no first-order autonomous ODE interpolates them. For $$\eta\lambda > 2$$ they diverge. BEA on $$\theta$$ itself is a small-$$\eta\lambda$$ tool. This is the obstruction that the central-flow and rod-flow constructions route around ([Regis and Chewi 2026](https://arxiv.org/abs/2602.01480), Appendix A, make this point cleanly).

**Aside: the modified-loss picture is an $$O(\eta)$$ accident.** The $$O(\eta^2)$$ field is $$f_2 = -\frac1{12}\nabla(g^\top H g) - \frac16 H^2 g$$, and $$H^2 g$$ is not a gradient in general: $$\partial_m (H^2 g)_j - \partial_j (H^2 g)_m = [H, T[g]]_{jm}$$, which vanishes only if $$H$$ commutes with $$T[g]$$. So beyond first order the discrete dynamics are not gradient flow on any modified loss. Keep this in mind for Adam (Section 7), where the same issue appears already at first order.

---

## 2. The master formula: split into slow centre and fast spread **[reformulation]**

Every phenomenon below is the same computation. Write the iterate as

$$\theta_t = \bar\theta_t + \delta_t, \qquad \langle \delta_t \rangle = 0,$$

where $$\bar\theta$$ is slow (varies over many steps) and $$\delta$$ is fast (an intra-step interpolant, a noise fluctuation, or a period-2 oscillation), and $$\langle\cdot\rangle$$ averages over whichever fast thing is in play. Let $$C_t = \langle \delta_t \delta_t^\top \rangle$$ be the **spread**. One step of SGD is $$\theta_{t+1} - \theta_t = -\eta\,\hat g_t(\bar\theta_t + \delta_t)$$. Expand the (possibly random) gradient field around the centre:

$$\hat g_t(\bar\theta + \delta) = g + \xi_t + (H + \Xi_t)\,\delta + \tfrac12 (T + \nabla\Xi_t)[\delta,\delta] + O(\delta^3).$$

Average. $$\langle \xi_t \rangle = 0$$, $$\langle H\delta_t\rangle = 0$$, and I drop $$\langle \nabla\Xi_t[\delta,\delta]\rangle$$ (it needs a three-way correlation and is subleading in every closure below). What survives:

$$\boxed{\;\frac{d\bar\theta}{dt} = -\eta\Big[\;\underbrace{\nabla L}_{\text{signal}}\;+\;\underbrace{\langle \Xi_t \delta_t\rangle}_{\text{noise–position correlation}}\;+\;\underbrace{\tfrac12\, T[C_t]}_{\text{curvature-of-curvature}\times\text{spread}}\;\Big]\;+\;(\text{BEA correction of the slow map}).\;}\tag{$\ast$}$$

Three remarks that carry the whole post.

**(i) The third term is a semi-gradient of the excess loss carried by the spread.** The loss averaged over the spread is $$\langle L(\bar\theta+\delta)\rangle = L(\bar\theta) + \frac12\langle H, C\rangle + O(\delta^3)$$. If $$C$$ is diagonal in the Hessian eigenbasis, $$\frac12 T[C] = \frac12\sum_k C_{kk}\, T[u_k,u_k] = \frac12 \sum_k C_{kk} \nabla\lambda_k$$, which is $$\nabla_{\bar\theta}\big[\frac12 \langle H, C\rangle\big]$$ **holding $$C$$ fixed**. So the spread pushes the centre down the gradient of "the sharpness that the spread feels", weighted by how spread out it is. I will call this the **flatness force** and write it as $$\nabla_{\rm semi}$$ to remember that $$C$$ is not differentiated.

**(ii) The second term is a different beast.** It is nonzero only when the Hessian noise $$\Xi_t$$ is correlated with the position noise $$\delta_t$$. For i.i.d. minibatch sampling, $$\Xi_t$$ is independent of the past and the term vanishes. It survives for sampling *without replacement* (Section 4a). For deterministic oscillations it is identically zero.

**(iii) Everything is a closure.** The formula is exact to second order in $$\delta$$; what makes it predictive is a rule for $$C_t$$ (and $$\langle\Xi\delta\rangle$$):

| Phenomenon | Fast variable $$\delta$$ | $$\langle \Xi\delta\rangle$$ | What fixes $$C$$ |
|---|---|---|---|
| Finite step (IGR) | intra-step interpolant | 0 | nothing; it is the BEA correction term |
| SGD, random reshuffling | within-epoch accumulated noise | $$-\frac{1}{4m}\nabla\sum_k\Vert \xi_k\Vert ^2$$ | ballistic (no relaxation) |
| SGD, relaxed fluctuations | Ornstein–Uhlenbeck fluctuation | 0 | discrete Lyapunov (fluctuation–dissipation) |
| Catapult | growing period-2 oscillation | 0 | transient; amplitude ODE |
| Edge of stability / central flow | period-2 oscillation | 0 | constraint $$\lambda_1 = 2/\eta$$ (Lagrange multiplier) |
| Rod flow | half-difference of consecutive iterates | 0 | its own ODE |
| Momentum, Adam | same, in phase space / preconditioned metric | 0 | same closures, different thresholds |

The flatness force is **linear in $$C$$**, so independent sources of spread add at this order: $$C = C_{\rm noise} + C_{\rm osc}$$. The interactions live in the closures (Section 8).

---

## 3. Finite step size: IGR as the BEA of the slow map **[lit]**

Already done in Section 1. In the language of $$(\ast)$$: with no noise and no oscillation, $$\delta$$ is the intra-step interpolant, $$C = O(\eta^2)$$ contributes only at $$O(\eta^3)$$, and the entire $$O(\eta^2)$$-per-step correction is the BEA term $$-\frac{\eta^2}{2}Hg$$. Result:

$$\mathcal L^{(1)} = \frac{\eta}{4}\Vert \nabla L\Vert ^2, \qquad \text{per-mode strength } \frac{\eta\lambda_k}{2}.$$

For SGD, the per-step version of this is the BEA of the *minibatch* map, giving $$\frac{\eta}{4}\Vert \nabla \hat L_t\Vert ^2$$ step by step; averaging over an epoch is what produces the next term.

---

## 4. SGD batch noise: two closures, one quantity

### 4a. Random reshuffling: the epoch-level BEA of Smith et al. **[lit]**

Take one epoch of $$m = N/B$$ minibatch steps in a random order, with minibatch gradients $$\hat g_k = g + \xi_k$$, $$\sum_k \xi_k = 0$$ (the batches partition the data). Compose the $$m$$ Euler steps and expand each gradient about $$\theta_0$$:

$$\theta_m = \theta_0 - \eta\sum_{k=1}^m \hat g_k(\theta_{k-1}) = \theta_0 - \eta m g + \eta^2 \sum_{k=1}^{m}\hat H_k \sum_{j<k}\hat g_j + O(\eta^3).$$

Compare with the time-$$m\eta$$ flow of a candidate modified loss $$\tilde L = L + \eta R$$:

$$\theta(m\eta) = \theta_0 - m\eta g - m\eta^2 \nabla R + \frac{(m\eta)^2}{2} H g + O(\eta^3).$$

Matching the $$\eta^2$$ terms requires $$\frac{m^2}{2}Hg - m\nabla R = \sum_k \hat H_k \sum_{j<k}\hat g_j$$. Now average over the random order. Using $$\sum_{j,k}\hat H_k \hat g_j = m^2 Hg$$ and symmetry between $$j<k$$ and $$j>k$$,

$$\Big\langle \sum_k \hat H_k \sum_{j<k}\hat g_j\Big\rangle = \frac12\Big(m^2 Hg - \sum_k \hat H_k \hat g_k\Big) = \frac{m^2}{2}Hg - \frac14 \nabla\sum_k \Vert \hat g_k\Vert ^2,$$

since $$\hat H_k \hat g_k = \frac12 \nabla\Vert \hat g_k\Vert ^2$$. Therefore $$\nabla R = \frac{1}{4m}\nabla\sum_k\Vert \hat g_k\Vert ^2$$ and

$$\boxed{\;\tilde L_{\rm SGD} = L + \frac{\eta}{4m}\sum_{k=1}^m \Vert \nabla \hat L_k\Vert ^2 = L + \frac{\eta}{4}\Vert \nabla L\Vert ^2 + \frac{\eta}{4m}\sum_{k=1}^m\Vert \nabla\hat L_k - \nabla L\Vert ^2,\;}$$

the cross term vanishing because $$\sum_k \xi_k = 0$$. This is the result of [Smith, Dherin, Barrett and De (2021)](https://arxiv.org/abs/2101.12176). For $$B \ll N$$, $$\frac1m\sum_k\Vert \xi_k\Vert ^2 \approx \frac{1}{B}\,{\rm tr}\,\Sigma$$ (finite-population factor $$\frac{N-B}{N-1}$$ if you want it), so

$$\mathcal L^{(2)} = \frac{\eta}{4B}\,{\rm tr}\,\Sigma .$$

This is the term Charles had in mind: a penalty on the per-sample gradient *variance*, with the famous $$\eta/B$$ scaling.

**Where it sits in $$(\ast)$$, and a subtlety.** Redo the derivation with $$\hat g_k = g + \xi_k$$, $$\hat H_k = H + \Xi_k$$. The only surviving non-trivial average is $$\langle \sum_{j<k}\Xi_k \xi_j\rangle$$. Under random reshuffling, for $$j \ne k$$, $$\langle \Xi_{\pi(k)}\xi_{\pi(j)}\rangle = -\frac{1}{m(m-1)}\sum_a \Xi_a\xi_a$$, because the batches within an epoch are **anticorrelated** (they sum to the full gradient). Multiply by the $$m(m-1)/2$$ pairs: the term is $$-\frac12\sum_a\Xi_a\xi_a = -\frac14\nabla\sum_a\Vert \xi_a\Vert ^2$$. In the language of $$(\ast)$$ this is the noise–position correlation $$\langle\Xi\delta\rangle$$ with $$\delta_{k-1} = -\eta\sum_{j<k}\xi_j$$ accumulated ballistically. **With i.i.d. (with-replacement) sampling the same average is $$\langle\Xi_k\rangle\langle\xi_j\rangle = 0$$ and the noise term disappears from the expected epoch map.** The $$\eta/B$$ regularizer of Smith et al. is the imprint of reshuffling, not of noise per se. Noise still matters for i.i.d. sampling, but through the other closure.

**Validity.** The expansion drops terms like $$\eta^3 m^3 H^2 g$$, so it needs $$m\,\eta\lambda_1 \ll 1$$: the *whole epoch* must be shorter than the fastest relaxation time. That is violated in practice for the top modes, which motivates:

### 4b. Relaxed fluctuations: the Ornstein–Uhlenbeck closure **[lit, reformulated]**

Now let the noise act for long enough that the fast modes relax. Linearize $$(\ast)$$ for the fluctuation in Hessian mode $$k$$, assuming $$\Sigma$$ is approximately co-diagonal with $$H$$ (empirically decent: [Wu, Wang and Su 2022](https://arxiv.org/abs/2207.02628), [Thomas et al. 2020](https://arxiv.org/abs/1906.07774)):

$$\delta^{(k)}_{t+1} = (1 - \eta\lambda_k)\,\delta^{(k)}_t - \eta\,\xi^{(k)}_t, \qquad \langle \xi^{(k)2}\rangle = \Sigma_{kk}/B .$$

Stationary variance from $$C_{kk} = (1-\eta\lambda_k)^2 C_{kk} + \eta^2\Sigma_{kk}/B$$:

$$\boxed{\;C_{kk} = \frac{\eta\,\Sigma_{kk}}{B\,\lambda_k\,(2 - \eta\lambda_k)}\;\xrightarrow{\;\eta\lambda_k\ll 1\;}\;\frac{\eta\,\Sigma_{kk}}{2B\lambda_k},\;}\qquad \tau_k = \frac{-1}{\ln\vert 1-\eta\lambda_k\vert }\approx \frac{1}{\eta\lambda_k}.$$

This is the discrete fluctuation–dissipation relation. It is the same object as the stationary covariance of the stochastic modified equation of [Li, Tai and E (2017)](https://arxiv.org/abs/1511.06251), $$d\theta = -\nabla(L + \frac\eta4\Vert \nabla L\Vert ^2)\,dt + \sqrt{\eta}\,\Sigma_B^{1/2}\,dW$$, whose drift — note — contains only the IGR term, consistent with 4a for i.i.d. sampling.

Plug into the flatness force:

$$\frac{d\bar\theta}{dt}\Big\vert _{\rm noise} = -\frac{\eta}{2}\sum_k C_{kk}\nabla\lambda_k = -\frac{\eta^2}{2B}\sum_k \frac{\Sigma_{kk}}{\lambda_k(2-\eta\lambda_k)}\nabla\lambda_k .$$

Three special cases:

- **Label noise / aligned noise, $$\Sigma = \sigma^2 H$$.** For MSE at interpolation with label noise of variance $$\sigma^2$$, the per-sample gradient is $$-\epsilon_i J_i^\top$$, so $$\Sigma = \sigma^2 \frac1N\sum_i J_i^\top J_i = \sigma^2 H$$ exactly. Then $$C_{kk} \approx \frac{\eta\sigma^2}{2B}$$ (equal for every mode!) and the drift is $$-\eta\nabla\big[\frac{\eta\sigma^2}{4B}{\rm tr}\,H\big]$$. This is the result of [Blanc et al. (2020)](https://arxiv.org/abs/1904.09080) and [Damian, Ma and Lee (2021)](https://arxiv.org/abs/2106.06530): label-noise SGD near the zero-loss manifold minimizes $${\rm tr}\,H$$ on it. [Li, Wang and Arora (2022)](https://arxiv.org/abs/2110.06914) give the general slow-manifold SDE for arbitrary $$\Sigma$$; in the co-diagonal approximation it reduces to the display above.
- **Isotropic noise, $$\Sigma_{kk} = \sigma^2$$.** $$C_{kk} = \frac{\eta\sigma^2}{2B\lambda_k}$$ and the semi-gradient is of $$\frac{\eta\sigma^2}{4B}\sum_k\log\lambda_k$$: a log-determinant penalty over the thermalized modes.
- **Generic SGD.** Empirically $$\Sigma \approx \sigma^2(t) H$$ up to a scalar (the "alignment property"), so the $${\rm tr}\,H$$ form is the practically relevant one, with $$\sigma^2(t)$$ shrinking as the residuals shrink (Section 9).

**One quantity, three guises.** The excess loss carried by a thermalized mode is

$$\tfrac12\lambda_k C_{kk} = \frac{\eta\,\Sigma_{kk}}{2B(2-\eta\lambda_k)}\;\to\;\frac{\eta\,\Sigma_{kk}}{4B}.$$

Summed over modes this is exactly the Smith et al. term $$\frac{\eta}{4B}{\rm tr}\,\Sigma$$. So the same number is (a) the reshuffling regularizer, (b) the stationary excess loss of the thermal bath — a discrete-time equipartition, $$\frac{\eta\Sigma_{kk}}{4B}$$ per mode — and (c) the object whose semi-gradient (at fixed $$C$$) is the label-noise flatness force. They are different derivatives of the same functional: 4a differentiates $$\Sigma$$ at fixed geometry; 4b differentiates $$\lambda_k$$ at fixed $$\Sigma$$. **[extension]** as a statement; each piece is standard. Note also that the thermal excess loss diverges as $$\eta\lambda_k \to 2$$: the noise-side of the edge of stability. [Wu, Ma and E (2018)](https://arxiv.org/abs/1803.00195) turn this into a linear-stability criterion for SGD that includes the noise, which is why SGD's sharpness sits *below* $$2/\eta$$ by an amount growing with $$\eta/B$$.

---

## 5. Instability: catapult, edge of stability, central flow, rod flow

### 5a. The linear picture and the cubic fix **[lit]**

In mode $$k$$ the fluctuation obeys $$\delta^{(k)}_{t+1} = (1-\eta\lambda_k)\delta^{(k)}_t$$. For $$\eta\lambda_k > 2$$ it grows with alternating sign: a period-2 oscillation along $$u_k$$. On a quadratic this diverges; on a real loss it does not, because of the third derivative. Expand the gradient at $$\bar\theta + x u$$ for the top eigenvector $$u$$:

$$g(\bar\theta + xu) = g + x\lambda u + \tfrac12 x^2\, T[u,u] + O(x^3) = g + x\lambda u + \tfrac12 x^2\,\nabla\lambda + O(x^3),$$

by Hellmann–Feynman. Average over the two-cycle $$x = \pm a$$: the mean step is $$-\eta\big(g + \frac{a^2}{2}\nabla\lambda\big)$$, i.e. $$(\ast)$$ with $$C = a^2 uu^\top$$. The oscillation pushes the centre down $$\nabla\lambda$$ at a rate proportional to its variance. This is the **self-stabilization** mechanism of [Damian, Nichani and Lee (2023)](https://arxiv.org/abs/2209.15594): sharpness above $$2/\eta$$ grows the oscillation, the oscillation lowers the sharpness, the sharpness drops below $$2/\eta$$, the oscillation shrinks, progressive sharpening raises it again. The empirical regularity that full-batch GD spends most of training with $$\lambda_1 \approx 2/\eta$$, with non-monotone loss, is [Cohen, Kaur, Li, Kolter and Talwalkar (2021)](https://arxiv.org/abs/2103.00065); the sharpening itself is only partly explained (quadratic-regression models: [Agarwala, Pedregosa and Pennington 2023](https://arxiv.org/abs/2210.04860)).

Two closures for $$a^2$$ have been proposed, plus the transient case.

### 5b. Central flow: closure by constraint **[lit]**

[Cohen, Damian, Talwalkar, Kolter and Lee (2025)](https://arxiv.org/abs/2410.24206) close $$(\ast)$$ by demanding that the sharpness stay pinned. Rank-one case: $$\frac{d\lambda}{dt} = \nabla\lambda\cdot\frac{d\bar\theta}{dt} = -\eta\big(\nabla\lambda\cdot g + \frac{\sigma^2}{2}\Vert \nabla\lambda\Vert ^2\big) = 0$$ gives

$$\sigma^2 = \frac{-2\,\nabla\lambda\cdot\nabla L}{\Vert \nabla\lambda\Vert ^2}\quad(\ge 0\text{ exactly when gradient flow would sharpen}),\qquad \frac{d\bar\theta}{dt} = -\eta\Big[\nabla L + \frac{\sigma^2}{2}\nabla\lambda\Big].$$

Read as projected gradient flow: minimize $$L$$ subject to $$\lambda_1 \le 2/\eta$$, with $$\frac{\eta}{2}\sigma^2$$ the Lagrange multiplier. In the multi-mode case $$\Sigma = U\Omega U^\top$$ lives in the critical subspace and $$\Omega$$ solves a semidefinite complementarity problem (oscillation and slack cannot coexist in a direction). The loss the *iterates* see is $$L(\bar\theta) + \frac12\lambda\sigma^2 = L(\bar\theta) + \sigma^2/\eta$$, above the loss at the centre. The paper also treats scalar and per-coordinate RMSProp with the preconditioner as a slow variable (Section 7).

### 5c. Rod flow: closure by an ODE **[lit]**

[Regis and Chewi (2026)](https://arxiv.org/abs/2602.01480) avoid the constraint by tracking the *centre and half-difference of consecutive iterates* $$\bar w_t = \frac12(w_{t+1}+w_t)$$, $$\delta_t = \frac12(w_{t+1}-w_t) = -\frac\eta2\nabla L(w_t)$$. Because $$w_t = \bar w_t - \delta_t$$ and $$w_{t+1} = \bar w_t + \delta_t$$, the GD recursion gives *exact* difference equations

$$\bar w_{t+1} - \bar w_t = -\frac{\eta}{2}\big[\nabla L_+ + \nabla L_-\big],\qquad \delta_{t+1}\otimes\delta_{t+1} - \delta_t\otimes\delta_t = \frac{\eta^2}{4}\big[\nabla L_+\otimes\nabla L_+ + \nabla L_-\otimes\nabla L_-\big] - 2\,\delta_t\otimes\delta_t ,$$

with $$L_\pm = L(\bar w \pm \delta)$$. Both are smooth even when $$\delta$$ flips sign every step, because the extent $$\delta\otimes\delta$$ is sign-blind. Promoting to ODEs (with one BEA correction on the centre) gives the rod flow

$$\frac{d\bar w}{dt} = -\frac{\eta}{2}\big[\nabla L_+ + \nabla L_-\big] - \frac{\eta^2}{8}\big[\nabla^2 L_+ + \nabla^2 L_-\big]\big[\nabla L_+ + \nabla L_-\big],\qquad \frac{d\Sigma}{dt} = \frac{\eta^2}{4}\big[\nabla L_+\otimes\nabla L_+ + \nabla L_-\otimes\nabla L_-\big] - 2\Sigma .$$

Two checks. On a quadratic with sharpness $$S$$, at $$\bar w = 0$$: $$\dot\Sigma = (\frac{\eta^2S^2}{2} - 2)\Sigma$$, unstable exactly when $$S > 2/\eta$$. On the quartic $$L = \frac{S}{2}w^2 - \frac{Q}{4}w^4$$ the stable nonzero fixed point is $$\Sigma^* = \frac{S}{Q} - \frac{2}{\eta Q}$$, which exists iff $$S > 2/\eta$$: the rod stretches until its endpoints sit where the local curvature has dropped to the stability threshold. Taylor-expanding $$\nabla L_\pm$$ to second order in $$\delta$$ recovers the central-flow centre equation, $$\dot{\bar w} \approx -\eta\nabla L - \frac{\eta}{2}\nabla^3 L[\delta,\delta]$$, i.e. $$(\ast)$$ again; the difference is that rod flow evaluates the landscape *at the endpoints* rather than Taylor-expanding at the centre, and lets $$\Sigma$$ relax on its own $$O(1)$$-step timescale instead of solving a constraint. A June 2026 follow-up, [Edge Flow](https://arxiv.org/abs/2606.18080), argues rod flow does not pin the sharpness at exactly $$2/\eta$$ over long runs and proposes explicit direction/amplitude variables; I have not worked through it.

### 5d. Catapult: the transient closure **[lit]**

[Lewkowycz, Bahri, Dyer, Sohl-Dickstein and Gur-Ari (2020)](https://arxiv.org/abs/2003.02218): start GD with $$\eta > 2/\lambda_0$$. The loss first grows exponentially, then the sharpness collapses and the loss converges to a region with $$\lambda < 2/\eta$$. Their solvable model is one hidden layer, one datapoint, $$f = \frac{1}{\sqrt n} v^\top u$$, $$L = \frac12 f^2$$, NTK $$\lambda = \frac1n(\Vert u\Vert ^2 + \Vert v\Vert ^2) = \Vert \nabla f\Vert ^2$$. One GD step gives exactly

$$f_{t+1} = f_t\Big(1 - \eta\lambda_t + \frac{\eta^2 f_t^2}{n}\Big),\qquad \lambda_{t+1} = \lambda_t + \frac{\eta f_t^2}{n}\big(\eta\lambda_t - 4\big).$$

For $$2 < \eta\lambda < 4$$: $$\vert f\vert $$ grows (linear instability) while $$\lambda$$ falls (the second equation), until $$\eta\lambda < 2$$, after which $$\vert f\vert $$ decays and $$\lambda$$ freezes below $$2/\eta$$. For $$\eta\lambda > 4$$ both diverge. Since the $$\lambda$$-update is $$O(f^2/n)$$, the loss must reach $$O(n)$$ before the curvature moves — in NTK scaling the catapult is a large excursion. The second equation is nothing but $$\lambda(\theta - \eta g) - \lambda(\theta) = -\eta\nabla\lambda\cdot g + \frac{\eta^2}{2}g^\top(\nabla^2\lambda)g$$ with $$\nabla\lambda\cdot g = \frac{4f^2}{n}$$ and $$\nabla^2\lambda = \frac{2}{n}I$$: the sharpness moves because of where the *endpoint* of the step lands, exactly the rod-flow logic with the rod's extent equal to the step itself. Catapult and edge of stability are the same mechanism with different boundary conditions: a transient with a single large oscillation that overshoots and freezes, versus a steady state maintained by progressive sharpening. Rod flow's Phase 2 (repeated small catapults at the onset of EoS) interpolates.

---

## 6. Scale invariance and weight decay: the radial/angular split **[lit, reformulated]**

For a parameter block $$w$$ followed by a normalization layer, $$L(cw) = L(w)$$. Differentiating in $$c$$: $$w\cdot\nabla_w L = 0$$ and $$\nabla L(cw) = c^{-1}\nabla L(w)$$. Differentiating the first identity again, $$H w = -\nabla L$$, so $$w^\top H w = 0$$: the radial direction carries no curvature. This is a fast–slow split handed to us by symmetry. Write $$r = \Vert w\Vert $$, $$\hat w = w/r$$, and $$\hat G = \Vert \nabla_{\hat w} L\Vert ^2$$ for the gradient norm squared at unit norm, so $$\Vert \nabla_w L\Vert ^2 = \hat G/r^2$$.

**Norm dynamics (slow).** SGD with weight decay, $$w_{t+1} = (1-\eta\gamma)w_t - \eta g_t$$, and $$g\perp w$$:

$$r_{t+1}^2 = (1-\eta\gamma)^2 r_t^2 + \eta^2\frac{\hat G_t}{r_t^2}.$$

Fixed point: $$(2\eta\gamma - \eta^2\gamma^2) r_\ast^2 = \eta^2\hat G/r_\ast^2$$, i.e.

$$r_\ast^4 = \frac{\eta\,\hat G}{\gamma(2-\eta\gamma)}\approx\frac{\eta\hat G}{2\gamma}.$$

Linearizing $$x = r^2$$ about $$x_\ast$$: $$\partial_x[-2\eta\gamma x + \eta^2\hat G/x] = -2\eta\gamma - \eta^2\hat G/x_\ast^2 = -4\eta\gamma$$, so the norm relaxes in $$\tau_{\rm norm} = 1/(4\eta\gamma)$$ steps (for an Adam-like update whose norm does not depend on $$r$$, the second contribution is absent and $$\tau_{\rm norm} = 1/(2\eta\gamma)$$).

**Angular dynamics (fast).** The direction moves by $$\tan\Delta\phi = \frac{\eta\Vert g\Vert }{(1-\eta\gamma)r}\approx \frac{\eta\sqrt{\hat G}}{r^2}$$, which at equilibrium is

$$\boxed{\;\Delta\phi_* = \sqrt{2\eta\gamma}\;\text{ per step, independent of }\hat G,\qquad \eta_{\rm eff} := \frac{\eta}{r_\ast^2} = \sqrt{\frac{2\eta\gamma}{\hat G}}.\;}$$

The effective learning rate on the sphere is set by the *intrinsic* rate $$\eta\gamma$$ ([Li, Lyu and Arora 2020](https://arxiv.org/abs/2010.02916)), the per-step rotation is universal ([Wan et al. 2020](https://arxiv.org/abs/2006.08419), "spherical motion dynamics"; [Kosson, Messmer and Jaggi 2024](https://arxiv.org/abs/2305.17212), "rotational equilibrium", who extend it to AdamW and Lion and use it to explain why AdamW beats Adam with $$L^2$$). The angular motion is just GD on the sphere with a slowly varying learning rate $$\eta_{\rm eff}(t) = \eta/r_t^2$$; everything in Sections 3–5 applies on the sphere with $$\eta \to \eta_{\rm eff}$$ and $$H \to$$ the spherical Hessian $$r^2 H\vert_{\perp w}$$.

**Time asymptotics of angular progress.** If successive angular steps are uncorrelated (noise-dominated), $$\langle\phi^2(t)\rangle \approx 2\eta\gamma\,t$$, so the direction decorrelates from its initialization after $$t \sim 1/(2\eta\gamma)$$ steps, the same order as $$\tau_{\rm norm}$$. If they are coherent, $$\phi \approx \sqrt{2\eta\gamma}\,t$$. The dimensionless clock for a normalized block is $$\eta\gamma t$$.

**The link to EoS.** Without weight decay $$r$$ grows, $$\eta_{\rm eff}$$ shrinks, and the spherical dynamics cool. With weight decay $$\eta_{\rm eff}$$ rises toward its equilibrium value, and the spherical sharpness rises by progressive sharpening, until $$\eta_{\rm eff}\lambda^{\rm sph}_1 = 2$$. [Lyu, Li and Arora (2022)](https://arxiv.org/abs/2206.07085) show that GD plus weight decay on a scale-invariant loss then follows a *spherical sharpness-reduction* flow near the minimizer manifold: angular equilibrium is an edge-of-stability state, and the flatness force of Section 5 is what the normalization plus weight decay buys you.

---

## 7. Momentum and Adam(W): is there still an effective loss?

I use Adam's EMA convention throughout: $$m_{t+1} = \beta m_t + (1-\beta)g_t$$, $$\theta_{t+1} = \theta_t - \eta\, m_{t+1}$$. Polyak's form has $$\eta_{\rm P} = \eta(1-\beta)$$.

### 7a. Heavy-ball momentum: three regimes per mode **[lit + reformulation]**

On a quadratic mode, eliminating $$m$$ gives the two-step recursion $$\theta_{t+1} = (1+\beta-\eta_{\rm P}\lambda)\theta_t - \beta\theta_{t-1}$$ with characteristic equation $$\mu^2 - (1+\beta - \eta_{\rm P}\lambda)\mu + \beta = 0$$.

**Overdamped: effective loss with amplified IGR.** For small $$\eta_{\rm P}\lambda$$ expand the slow root $$\mu = 1 - a\epsilon - b\epsilon^2$$, $$\epsilon = \eta_{\rm P}\lambda$$. Order $$\epsilon$$: $$a(\beta-1) = -1$$, so $$a = \frac{1}{1-\beta}$$ (the familiar effective LR $$\eta_{\rm P}/(1-\beta) = \eta$$). Order $$\epsilon^2$$: $$b(\beta-1) = a - a^2$$, so $$b = \frac{\beta}{(1-\beta)^3}$$. The interpolating rate $$\tilde\lambda = -\eta^{-1}\ln\mu$$ is then

$$\tilde\lambda = \lambda\Big[1 + \frac{\eta\lambda}{2}\cdot\frac{1+\beta}{1-\beta} + O(\eta^2\lambda^2)\Big],$$

so the modified loss is

$$\boxed{\;\tilde L_{\rm HB} = L + \frac{\eta}{4}\cdot\frac{1+\beta}{1-\beta}\,\Vert \nabla L\Vert ^2,\;}$$

the result of [Ghosh, Lyu, Zhang and Wang (2023)](https://arxiv.org/abs/2302.00849): momentum amplifies IGR by $$\frac{1+\beta}{1-\beta}$$ ($$=19$$ at $$\beta = 0.9$$) at fixed effective learning rate. Validity: after the momentum transient ($$t \gg 1/(1-\beta)$$), and only while the roots are real.

**Underdamped: no first-order effective loss for that mode.** The roots go complex when $$(1+\beta-\eta_{\rm P}\lambda)^2 < 4\beta$$, i.e.

$$\eta\lambda > \frac{1-\sqrt\beta}{1+\sqrt\beta}\;\approx\;\frac{1-\beta}{4}\qquad(=0.026\text{ at }\beta=0.9).$$

Above this the mode is a damped oscillator with $$\vert \mu\vert  = \sqrt\beta$$: it relaxes in $$\tau = 1/(1-\sqrt\beta) \approx 2/(1-\beta)$$ steps ($$\approx 20$$ at $$\beta = 0.9$$) **regardless of $$\lambda$$**, while ringing at frequency $$\sim\sqrt{\eta_{\rm P}\lambda}$$. Momentum thus equalizes the relaxation time across the whole band $$\frac{1-\beta}{4} \lesssim \eta\lambda \lesssim 2\frac{1+\beta}{1-\beta}$$, which is most of the spectrum that matters. In this band the mode is not a first-order flow, which I think is the "spatial filtering" feeling: the gradient is temporally low-passed, and along a trajectory a temporal filter is a spatial one. The envelope of the oscillation is still slow, and the fluctuation *variance* is unchanged — for white noise driving, the continuum limit is an underdamped Langevin equation with damping $$1-\beta$$, frequency$$^2$$ $$\eta_{\rm P}\lambda$$ and diffusion $$\frac12\eta_{\rm P}^2\sigma^2$$, whose stationary position variance is $$\frac{\eta_{\rm P}\sigma^2}{2\lambda(1-\beta)} = \frac{\eta\sigma^2}{2\lambda}$$, identical to SGD at the effective learning rate ([Wang, Malladi et al. 2023](https://arxiv.org/abs/2307.15196) make this rigorous in the small-LR regime). So for the *closures* in Sections 4–5, momentum enters through $$\eta$$ and through the relaxation time; the flatness force is unchanged.

**Unstable.** Beyond $$\vert \mu\vert  = 1$$, i.e.

$$\eta\lambda > 2\,\frac{1+\beta}{1-\beta}\qquad(=38\text{ at }\beta = 0.9),$$

the mode goes to the edge of stability. This is the threshold measured by [Cohen et al. (2022)](https://arxiv.org/abs/2207.14484) for momentum methods, and in phase space $$(w, m)$$ the period-2 oscillation of $$w$$ and $$m$$ is a single rod ([Regis and Chewi 2026b](https://arxiv.org/abs/2605.06821)).

### 7b. Adam: three timescales, and what closes **[lit + reformulation]**

Adam is $$m \leftarrow \beta_1 m + (1-\beta_1)g$$, $$\nu \leftarrow \beta_2\nu + (1-\beta_2)g^{\odot 2}$$, $$\theta \leftarrow \theta - \eta\,m/(\sqrt\nu + \epsilon)$$; write $$P = {\rm diag}(\sqrt\nu) + \epsilon I$$. The timescales are

$$2\ \text{(EoS oscillation)}\;\ll\;\frac{1}{1-\beta_1}\sim 10\;\ll\;\frac{1}{1-\beta_2}\sim 10^3\;\lesssim\;\frac{1}{2\eta\gamma}\ \text{(AdamW norm equilibration)}\;\ll\;T_{\rm total}.$$

To Charles's question: yes, the standard $$\beta_1 = 0.9$$, $$\beta_2 = 0.999$$ is a timescale separation, and every analysis I know exploits it. $$\nu$$ is treated as a *smooth, slow, non-oscillating* variable — squaring kills sign flips — so it needs no rod of its own and can be frozen over any window shorter than $$1/(1-\beta_2)$$. Momentum is either eliminated (small-LR, overdamped regime) or lifted into phase space (EoS regime).

**Frozen-$$\nu$$ BEA.** With $$P$$ constant, one step is Euler for $$\dot\theta = -P^{-1}\nabla L$$, and Section 1 gives $$f_1 = -\frac12(\partial f_0)f_0 = -\frac12 P^{-1}HP^{-1}g = -P^{-1}\nabla\big[\frac14 g^\top P^{-1}g\big]$$. So

$$\dot\theta = -P^{-1}\nabla\Big[L + \frac{\eta}{4}\cdot\frac{1+\beta_1}{1-\beta_1}\,\Vert \nabla L\Vert ^2_{P^{-1}}\Big],\qquad \Vert g\Vert ^2_{P^{-1}} = \sum_j \frac{g_j^2}{\sqrt{\nu_j}+\epsilon},$$

a $$P$$-gradient flow of a modified loss (momentum factor from 7a). In the signal-dominated regime $$\nu_j \approx g_j^2$$ and $$\Vert g\Vert ^2_{P^{-1}} \to \Vert \nabla L\Vert _1$$ — the "perturbed one-norm" of [Cattaneo, Klusowski and Shigida (2024)](https://arxiv.org/abs/2309.00079). **But** they show that once the lag of $$\nu$$ behind $$g^2$$ is accounted for, the coefficient's sign depends on $$\beta_1$$, $$\beta_2$$ and the training stage, and that the *anti*-penalizing sign is typical. The frozen-$$\nu$$ picture is the exceptional case. The intuition: if $$\nu$$ tracked $$g^2$$ instantaneously the update would be $${\rm sign}(g)$$, whose Jacobian vanishes, so there is no IGR at all; the finite lag then produces a term of either sign. This is the first place where "effective loss" genuinely fails for Adam: the failure is not momentum, it is the preconditioner's dependence on the trajectory, and it appears already at $$O(\eta)$$ (compare the aside in Section 1, where GD only fails at $$O(\eta^2)$$).

**Noise-dominated $$\nu$$: Adam whitens the noise.** With minibatch noise, $$\nu_j \approx g_j^2 + \Sigma_{jj}/B$$ ([Malladi et al. 2022](https://arxiv.org/abs/2205.10287) give the SDE and scaling rules). When $$g_j^2 \ll \Sigma_{jj}/B$$, $$P_j^{-1} \approx \sqrt{B/\Sigma_{jj}}$$ and the per-step noise in coordinate $$j$$ is $$\eta P_j^{-1}\xi_j$$ with variance $$\eta^2$$: **uniform across coordinates**. Adam in the noise-dominated regime is SGD with a per-coordinate learning rate $$\eta\sqrt{B/\Sigma_{jj}}$$ and a coordinate-isotropic bath of temperature $$\eta^2$$.

Now run the OU closure of Section 4b in the preconditioned dynamics $$\theta \leftarrow \theta - \eta P^{-1}(g + \xi)$$. The stationary spread solves $$P^{-1}HC + CHP^{-1} = \eta P^{-1}\Sigma P^{-1}$$. For aligned noise $$\Sigma = \sigma^2 H$$ the solution is $$C = \frac{\eta\sigma^2}{2}P^{-1}$$ (check: $$P^{-1}H\cdot\frac{\eta\sigma^2}{2}P^{-1} + \frac{\eta\sigma^2}{2}P^{-1}\cdot HP^{-1} = \eta\sigma^2 P^{-1}HP^{-1}$$). The flatness force is the $$P$$-semi-gradient of $$\frac12\langle H, C\rangle = \frac{\eta\sigma^2}{4}{\rm tr}(HP^{-1}) = \frac{\eta\sigma^2}{4}\sum_j H_{jj}/\sqrt{\nu_j}$$, and with $$\nu_j \approx \Sigma_{jj} = \sigma^2 H_{jj}$$ this is

$$\Phi_{\rm Adam} = \frac{\eta\sigma}{4}\,{\rm tr}\big({\rm Diag}(H)^{1/2}\big),$$

versus $$\Phi_{\rm SGD} = \frac{\eta\sigma^2}{4B}{\rm tr}\,H$$. This is the result of [Li, Wen and Lyu (2025)](https://arxiv.org/abs/2511.02773): label-noise Adam takes semi-gradients of $${\rm tr}({\rm Diag}(H)^{1/2})$$ near the minimizer manifold (they also cover RMSProp, Adam-mini, Adalayer, Shampoo). That the master formula reproduces their sharpness measure in three lines, with "semi-gradient" appearing as "hold $$C$$ and $$\nu$$ fixed", is the best evidence I have that $$(\ast)$$ is the right organizing object. **[reformulation]**

**Adam at the edge of stability.** The linearized step in the top mode is $$\delta \to (1 - \eta\lambda^P)\delta$$ with $$\lambda^P = \lambda_{\max}(P^{-1/2}HP^{-1/2})$$, so the stability number is the *preconditioned* sharpness, and with momentum the threshold is $$\eta\lambda^P = 2\frac{1+\beta_1}{1-\beta_1}$$ — the $$38/\eta$$ of [Cohen et al. (2022)](https://arxiv.org/abs/2207.14484). The central flow for RMSProp ([Cohen et al. 2025](https://arxiv.org/abs/2410.24206)) and the rod flow for Adam ([Regis and Chewi 2026b](https://arxiv.org/abs/2605.06821)) both treat $$\nu$$ as a smooth auxiliary with its own ODE, $$\dot{\bar\nu} = (1-\beta_2)\big[\frac12(\nabla L_+^{\odot 2} + \nabla L_-^{\odot 2}) - \bar\nu\big]$$, and the rod as a phase-space object $$(w, m)$$. What is new relative to GD is a **second channel** for relieving excess sharpness: an oscillation along $$u$$ inflates $$\nu_j$$ on the coordinates where $$u_j$$ is large, which raises $$P$$ and lowers $$\lambda^P$$ without the oscillation amplitude having to grow as far. Cohen et al. call this "acceleration via regularization"; the price is a smaller effective step $$\eta/\sqrt\nu$$ on those coordinates. The flatness force is still $$(\ast)$$ in the $$P$$-metric, but the closure for $$C$$ now involves $$\nu$$'s response, on the $$1/(1-\beta_2)$$ timescale.

**AdamW.** Decoupled decay $$\theta \leftarrow (1-\eta\gamma)\theta - \eta\,m/\sqrt\nu$$ on a scale-invariant block gives the Section 6 equilibrium with an update norm $$\Vert u\Vert $$ that does not depend on $$r$$: $$r_\ast = \sqrt{\eta/(2\gamma)}\,\Vert u\Vert $$, rotation $$\sqrt{2\eta\gamma}$$ per step, $$\tau_{\rm norm} = 1/(2\eta\gamma)$$. For white-noise gradients each coordinate of $$u = m/\sqrt\nu$$ has variance $$\frac{1-\beta_1}{1+\beta_1}$$, for coherent gradients it is $$\pm1$$, so $$\Vert u\Vert ^2 \in [\frac{1-\beta_1}{1+\beta_1}d,\ d]$$ for a block of $$d$$ parameters. This is Kosson et al.'s rotational equilibrium; the universality of $$\sqrt{2\eta\gamma}$$ across optimizers is why AdamW's $$(\eta,\gamma)$$ pair, rather than either alone, is the thing to tune.

**Summary of the answer.** Adam *is* an effective-loss story in the window: after the momentum transient, in the overdamped band, on windows short compared to $$1/(1-\beta_2)$$, and away from EoS — a $$P$$-gradient flow of $$L + \frac{\eta}{4}\frac{1+\beta_1}{1-\beta_1}\Vert \nabla L\Vert ^2_{P^{-1}}$$ plus the whitened-noise flatness force. It stops being one (a) in the underdamped band, where modes ring; (b) when $$\nu$$'s lag matters, which flips the sign of the IGR-like term; (c) at EoS, where you need the phase-space rod and $$\nu$$'s response. All three are timescale statements, which is why the $$\beta_1 \ll \beta_2$$ (in $$1-\beta$$) convention is not just a heuristic.

---

## 8. Collecting the effects at order $$\eta$$ (plain SGD) **[reformulation]**

For SGD without momentum, in step-time, everything above assembles into

$$\frac{d\bar\theta}{dt} = -\eta\,\nabla_{\rm semi}\,\mathcal L_{\rm eff},\qquad \mathcal L_{\rm eff} = L + \underbrace{\frac{\eta}{4}\Vert \nabla L\Vert ^2}_{\text{IGR}} + \underbrace{\frac{\eta}{4B}{\rm tr}\,\Sigma}_{\text{reshuffle}} + \underbrace{\tfrac12\langle H, C_{\rm noise}\rangle}_{\text{thermal flatness}} + \underbrace{\tfrac12\langle H, C_{\rm osc}\rangle}_{\text{EoS flatness}} + \frac{\gamma}{2}\Vert \theta\Vert ^2 ,$$

with the closures

$$C_{\rm noise} = \sum_k \frac{\eta\Sigma_{kk}}{B\lambda_k(2-\eta\lambda_k)}\,u_ku_k^\top\ (\text{relaxed modes}),\qquad C_{\rm osc} = \sum_{k:\ \eta\lambda_k = 2}\sigma_k^2\,u_ku_k^\top\ (\text{constraint or rod ODE}),$$

and $$\nabla_{\rm semi}$$ meaning: differentiate $$L$$, $$\Vert \nabla L\Vert ^2$$, $${\rm tr}\,\Sigma$$ and $$\Vert \theta\Vert ^2$$ fully, but differentiate $$\langle H, C\rangle$$ only through $$H$$. Which terms are honest gradients: the first three and the last. The two flatness terms are semi-gradients; the EoS one is a constraint force (Lagrangian $$L + \mu(\lambda_1 - 2/\eta)$$ with $$\mu = \frac{\sigma^2}{2}$$), and the thermal one is a gradient only in special cases ($${\rm tr}\,H$$ for aligned noise, $$\log\det H$$ for isotropic noise). Momentum: multiply the IGR term by $$\frac{1+\beta}{1-\beta}$$ and use the underdamped relaxation time in the closures. Adam: replace $$\Vert \cdot\Vert ^2$$ by $$\Vert \cdot\Vert ^2_{P^{-1}}$$, $$\Sigma$$ by $$P^{-1}\Sigma P^{-1}$$, and read the whole thing in the $$P$$-metric.

**Interactions.** Because the flatness force is linear in $$C$$, noise and oscillation add at this order — *if the closures are computed independently*. They are not independent in one place: the thermal closure has $$C_{kk} \propto (2-\eta\lambda_k)^{-1}$$, which diverges exactly where the oscillation closure switches on. A mode near $$\eta\lambda_k = 2$$ has its spread set jointly by noise injection, linear (in)stability and cubic self-stabilization; this is the regime where SGD sits below $$2/\eta$$ by a batch-size-dependent gap (Cohen et al. 2021 observe it; Wu, Ma and E 2018 give the linear-stability criterion). I do not know a closed-form closure for it; a rod flow driven by noise would be the natural object. Everything else is additive at order $$\eta$$.

---

## 9. Per-mode catalogue of characteristic scales

Work in the Hessian eigenbasis. (Why Hessian and not GGN: stability and relaxation are properties of the discrete map, which linearizes with $$H$$; but signal, noise and spikes are built from Jacobians and live in $$G$$. They agree near interpolation, where $$H_{\rm res} = H - G \to 0$$; they disagree early, which is exactly when catapults happen and where negative curvature lives. Practical compromise: use $$H$$'s eigenbasis and track the GGN fraction $$u_k^\top G u_k/\lambda_k$$ per mode.)

Per mode $$k$$ define $$g_k$$, $$\lambda_k$$, $$\Sigma_{kk}$$, and the **curvature length** $$\ell_k = \lambda_k/\Vert \nabla\lambda_k\Vert $$ (distance over which the mode's sharpness changes by order one).

| Number | Definition | Meaning / thresholds |
|---|---|---|
| $$\epsilon_k = \eta\lambda_k$$ | stability & discretization | $$<\frac{1-\sqrt\beta}{1+\sqrt\beta}$$: overdamped (HB); $$<1$$: BEA converges; $$=2$$: EoS; $$= 2\frac{1+\beta}{1-\beta}$$: EoS with momentum. Relaxation $$\tau_k \approx 1/\epsilon_k$$, or $$\approx 2/(1-\beta)$$ if underdamped. IGR strength $$\epsilon_k/2$$. |
| $${\rm SNR}_k = B g_k^2/\Sigma_{kk}$$ | per-step signal-to-noise | $$>1$$: mean step exceeds noise step in this mode. |
| $$R_k = {\rm SNR}_k\,\dfrac{2-\epsilon_k}{\epsilon_k}$$ | **resolution** | ratio of (distance to the mode's minimum)$$^2 = g_k^2/\lambda_k^2$$ to the equilibrium spread $$C_{kk}$$. $$R_k \gg 1$$: mode is deterministically resolved; $$R_k \ll 1$$: thermalized. |
| $$\frac{\eta\Sigma_{kk}}{2B(2-\epsilon_k)}$$ | thermal loss floor of mode $$k$$ | sums to $$\frac{\eta}{4B}{\rm tr}\Sigma$$; diverges at EoS. |
| $$F_k = \dfrac{C_{kk}\Vert \nabla\lambda_k\Vert }{2\Vert \nabla L\Vert }$$ | flatness force / loss force | thermal: $$\dfrac{\eta\Sigma_{kk}}{2B\,\ell_k\Vert \nabla L\Vert (2-\epsilon_k)}$$; EoS (central flow): $$\vert \cos\angle(\nabla\lambda_k,\nabla L)\vert $$. |
| $$A_k = \sqrt{C_{kk}}/\ell_k$$ | spread vs curvature length | $$\ll1$$: Taylor expansion at the centre (central flow) is fine; $$\sim1$$: need endpoint evaluation (rod flow), catapult regime. |
| $$m\,\eta\lambda_k$$ | epoch vs relaxation | $$\ll1$$: Smith term in full force; $$\gg1$$: mode relaxes within an epoch, reshuffling anticorrelation is averaged out (see companion notes). |
| $${\rm SNR}^{\rm coord}_j = Bg_j^2/\Sigma_{jj}$$ | Adam's preconditioner regime | $$\gg1$$: sign-descent-like, $$\Vert \cdot\Vert _1$$ IGR; $$\ll1$$: whitened noise, temperature $$\eta^2$$. |
| $$\eta\gamma$$ | intrinsic LR (normalized blocks) | $$\tau_{\rm norm} = 1/(4\eta\gamma)$$; rotation $$\sqrt{2\eta\gamma}$$/step; $$\eta_{\rm eff}\lambda^{\rm sph}$$ vs 2. |
| $$u_k^\top G u_k/\lambda_k$$ | GGN fraction | $$\to1$$ at interpolation; $$<1$$ or $$<0$$ where $$H_{\rm res}$$ dominates. |

Timescales, in steps: $$2$$ (EoS oscillation); $$1/(1-\beta_1)$$; $$1/(\eta\lambda_k)$$ per mode; $$1/(1-\beta_2)$$; $$m = N/B$$; $$1/(4\eta\gamma)$$ and $$1/(2\eta\gamma)$$; the sharpness-drift time $$\lambda_k/(\eta\, C_{kk}\Vert \nabla\lambda_k\Vert ^2) = \ell_k^2/(\eta\lambda_k A_k^2)$$; the spike-emergence time of Section 10 (data-dependent; I don't have a formula).

---

## 10. Data structure: Papyan, spikes, bulk, and what "fitting the spikes" would mean **[lit + conjecture]**

For a $$C$$-class network with logits $$f(x_i)$$ and softmax $$p_i$$, the Gauss–Newton part of the Hessian is $$G = \frac1N\sum_i J_i^\top A_i J_i$$ with $$J_i = \partial f(x_i)/\partial\theta$$ and $$A_i = {\rm diag}(p_i) - p_ip_i^\top$$ (MSE: $$A_i = I$$), and the remainder is

$$H_{\rm res} = H - G = \frac1N\sum_i\sum_c r_{ic}\,\nabla^2_\theta f_c(x_i),\qquad r_{ic} = p_{ic} - y_{ic}.$$

Per-sample gradients are $$g_i = J_i^\top r_i$$, so $$\Sigma$$, $$g$$ and $$G$$ are all built from the same Jacobians, weighted by residuals: schematically $$g \sim \rho$$, $$G \sim \rho$$, $$\Sigma \sim \rho^2$$, $$H_{\rm res} \sim \rho$$ as the residual scale $$\rho \to 0$$.

**Spikes and bulk.** [Sagun et al. (2017)](https://arxiv.org/abs/1706.04454) observed $$\approx C$$ outliers plus a bulk; [Papyan (2019)](https://arxiv.org/abs/1901.08244), [Papyan (2020)](https://arxiv.org/abs/2008.11865) explained the outliers by decomposing the $$NC$$ vectors $$\{A_i^{1/2}J_i\}$$ (the "backpropagated errors" that build $$G$$) hierarchically into a global mean, class means, class–cross-class means, and within-class residuals. The between-class part is rank $$\le C$$ and produces the $$C$$ spikes; the cross-class part a secondary cluster of order $$C^2$$ eigenvalues; the residuals the bulk. In RMT terms $$G$$ is a sample covariance of $$NC$$ vectors in $$P$$ dimensions with a low-rank mean structure: Marchenko–Pastur-like bulk from the residuals, spikes from the means via the usual spiked-covariance (BBP-type) mechanism. $$H_{\rm res}$$ is a residual-weighted sum of $$NC$$ symmetric matrices with weights of both signs, so its spectrum is roughly symmetric about zero and its width scales with the residuals; it is where the negative eigenvalues come from, and they shrink over training ([Ghorbani, Krishnan and Xiao 2019](https://arxiv.org/abs/1901.10159)). [Singh, Bachmann and Hofmann (2021)](https://arxiv.org/abs/2106.16225) give its exact rank and $$\pm$$-paired structure for deep linear networks; [Liao and Mahoney (2021)](https://arxiv.org/abs/2103.01519) compute the full Hessian spectrum for generalized linear models with RMT, including this term.

**Dynamics.** [Papyan (2018)](https://arxiv.org/abs/1811.07062) shows the outliers *emerge* from the bulk during training — they are not there at initialization; this is progressive sharpening confined to the between-class subspace, and it is the same object as the class-mean separation of neural collapse. [Gur-Ari, Roberts and Dyer (2018)](https://arxiv.org/abs/1812.04754) show the gradient lives in the top-$$C$$ subspace after an early phase. In the thermal picture this is what you expect: the minibatch gradient power in mode $$k$$ is $$\lambda_k^2 C_{kk} + \Sigma_{kk}/B \propto \lambda_k\Sigma_{kk}$$, largest exactly where both curvature and noise are largest, and $$\Sigma \approx \sigma^2 H$$ puts both in the spikes.

**Basin commitment.** The empirical facts: two children forked from a checkpoint become linearly mode-connected after a small fraction of training ([Frankle, Dziugaite, Roy and Carbin 2020](https://arxiv.org/abs/1912.05671)); the NTK and loss geometry change rapidly and then stabilize early ([Fort et al. 2020](https://arxiv.org/abs/2010.15110)); the early learning rate sets the curvature and noise scale the trajectory will live with ([Jastrzebski et al. 2020](https://arxiv.org/abs/2002.09572), "break-even point"). **[conjecture]** In the language of Section 9, "having fitted the spikes" means two things have happened: the spike directions $$u_1,\dots,u_C$$ (the class-mean geometry) have stopped rotating, and the spike modes have reached quasi-equilibrium, $$g_k^2/\lambda_k^2 \lesssim C_{kk}$$ for $$k \le C$$ — they were resolved ($$R_k \gg 1$$, relaxation time $$1/\eta\lambda_k$$ short) and are now fitted. After that, two children forked from the same checkpoint differ only in bulk coordinates, where the spread is small compared to the curvature length ($$A_k \ll 1$$) and the landscape between them is quadratic enough for the segment to stay in the basin: linear mode connectivity. The spike-emergence time is the data-dependent clock I would most like a formula for.

**Late-time cross-entropy.** On separable data GD drives $$\Vert w\Vert  \sim \log t$$, $$L \sim 1/t$$, direction converging to max-margin at rate $$1/\log t$$ ([Soudry et al. 2018](https://arxiv.org/abs/1710.10345); homogeneous networks: [Lyu and Li 2020](https://arxiv.org/abs/1906.05890)). In residual language everything scales with $$\rho \sim e^{-{\rm margin}}$$: $$\epsilon_k \to 0$$ (the dynamics cool below every threshold), $${\rm SNR}$$ is pinned by the support vectors, and $$R_k \sim 1/\rho \to \infty$$ (see companion notes). Weight decay or normalization stops $$\rho$$ from vanishing and pins the block at the Section 6 equilibrium instead.

---

## 11. Open questions

1. A noisy rod flow: the closure for $$C_{kk}$$ near $$\eta\lambda_k = 2$$ with minibatch noise, and the resulting batch-size-dependent gap below $$2/\eta$$.
2. Progressive sharpening itself: the sign of $$\nabla\lambda\cdot\nabla L$$ is an input to every EoS closure and is not derived here.
3. The sign of Adam's IGR-like term as a function of $$(1-\beta_1)/(1-\beta_2)$$ and the local timescale of $$g^2$$; whether there is a clean fast–slow statement that reproduces Cattaneo et al.
4. A formula for the spike-emergence time in terms of the class-mean geometry of the data, and whether it coincides with the LMC commitment time.
5. Whether the per-block version of $$(\ast)$$ — restricting $$C$$ and $$\Sigma$$ to a layer and treating its input/output statistics as slowly varying — is a usable "free-body diagram" for a layer. The third-derivative coupling between blocks is a product of input activations and output sensitivities, so it looks tractable.
6. Text: with $$d_{\rm vocab}$$ classes and Zipfian class frequencies the spike/bulk separation presumably becomes a power-law tail; none of Section 10 has been checked there.

---

## References

Tiers: **[A]** fetched or verified during drafting; **[B]** confident from memory, identifiers should be right; **[C]** from memory, check identifier before publishing.

**BEA and implicit regularization**
- [A] Barrett, Dherin. *Implicit gradient regularization.* ICLR 2021. https://arxiv.org/abs/2009.11162
- [A] Smith, Dherin, Barrett, De. *On the origin of implicit regularization in stochastic gradient descent.* ICLR 2021. https://arxiv.org/abs/2101.12176
- [B] Hairer, Lubich, Wanner. *Geometric Numerical Integration.* Springer 2006. https://link.springer.com/book/10.1007/3-540-30666-8
- [B] Li, Tai, E. *Stochastic modified equations and adaptive stochastic gradient algorithms.* ICML 2017. https://arxiv.org/abs/1511.06251
- [A] Ghosh, Lyu, Zhang, Wang. *Implicit regularization in heavy-ball momentum accelerated stochastic gradient descent.* ICLR 2023. https://arxiv.org/abs/2302.00849
- [A] Cattaneo, Klusowski, Shigida. *On the implicit bias of Adam.* ICML 2024. https://arxiv.org/abs/2309.00079
- [B] Wang, Malladi, Wang, Lyu, Li. *The marginal value of momentum for small learning rate SGD.* 2023. https://arxiv.org/abs/2307.15196
- [B] Malladi, Lyu, Panigrahi, Arora. *On the SDEs and scaling rules for adaptive gradient algorithms.* NeurIPS 2022. https://arxiv.org/abs/2205.10287

**SGD noise and sharpness**
- [B] Blanc, Gupta, Valiant, Valiant. *Implicit regularization for deep neural networks driven by an Ornstein–Uhlenbeck like process.* COLT 2020. https://arxiv.org/abs/1904.09080
- [B] Damian, Ma, Lee. *Label noise SGD provably prefers flat global minimizers.* NeurIPS 2021. https://arxiv.org/abs/2106.06530
- [B] Li, Wang, Arora. *What happens after SGD reaches zero loss? A mathematical framework.* ICLR 2022. https://arxiv.org/abs/2110.06914
- [A] Li, Wen, Lyu. *Adam reduces a unique form of sharpness: theoretical insights near the minimizer manifold.* NeurIPS 2025. https://arxiv.org/abs/2511.02773
- [B] Wu, Wang, Su. *The alignment property of SGD noise and how it helps select flat minima.* NeurIPS 2022. https://arxiv.org/abs/2207.02628
- [C] Thomas et al. *On the interplay between noise and curvature and its effect on optimization and generalization.* AISTATS 2020. https://arxiv.org/abs/1906.07774
- [C] Wu, Ma, E. *How SGD selects the global minima in over-parameterized learning: a dynamical stability perspective.* NeurIPS 2018. https://arxiv.org/abs/1803.00195

**Edge of stability, catapult, flows**
- [A] Cohen, Kaur, Li, Kolter, Talwalkar. *Gradient descent on neural networks typically occurs at the edge of stability.* ICLR 2021. https://arxiv.org/abs/2103.00065
- [B] Cohen et al. *Adaptive gradient methods at the edge of stability.* 2022. https://arxiv.org/abs/2207.14484
- [B] Damian, Nichani, Lee. *Self-stabilization: the implicit bias of gradient descent at the edge of stability.* ICLR 2023. https://arxiv.org/abs/2209.15594
- [B] Cohen, Damian, Talwalkar, Kolter, Lee. *Understanding optimization in deep learning with central flows.* ICLR 2025. https://arxiv.org/abs/2410.24206
- [A] Regis, Chewi. *Rod Flow: a continuous-time model for gradient descent at the edge of stability.* 2026. https://arxiv.org/abs/2602.01480
- [A] Regis, Chewi. *A Rod Flow model for Adam at the edge of stability.* 2026. https://arxiv.org/abs/2605.06821
- [A] *Edge Flow: a tractable and predictive continuous-time model for gradient descent at the edge of stability.* 2026. https://arxiv.org/abs/2606.18080 (authors not checked)
- [A] Lewkowycz, Bahri, Dyer, Sohl-Dickstein, Gur-Ari. *The large learning rate phase of deep learning: the catapult mechanism.* 2020. https://arxiv.org/abs/2003.02218
- [C] Agarwala, Pedregosa, Pennington. *Second-order regression models exhibit progressive sharpening to the edge of stability.* ICML 2023. https://arxiv.org/abs/2210.04860

**Scale invariance and weight decay**
- [B] Li, Lyu, Arora. *Reconciling modern deep learning with traditional optimization analyses: the intrinsic learning rate.* NeurIPS 2020. https://arxiv.org/abs/2010.02916
- [B] Wan, Zhu, Zhang, Sun. *Spherical motion dynamics: learning dynamics of normalized neural network using SGD and weight decay.* NeurIPS 2021. https://arxiv.org/abs/2006.08419
- [A] Kosson, Messmer, Jaggi. *Rotational equilibrium: how weight decay balances learning across neural networks.* ICML 2024. https://arxiv.org/abs/2305.17212
- [B] Lyu, Li, Arora. *Understanding the generalization benefit of normalization layers: sharpness reduction.* NeurIPS 2022. https://arxiv.org/abs/2206.07085

**Hessian structure and data**
- [B] Sagun, Evci, Guney, Dauphin, Bottou. *Empirical analysis of the Hessian of over-parametrized neural networks.* 2017. https://arxiv.org/abs/1706.04454
- [B] Papyan. *The full spectrum of deepnet Hessians at scale: dynamics with SGD training and sample size.* 2018. https://arxiv.org/abs/1811.07062
- [B] Papyan. *Measurements of three-level hierarchical structure in the outliers in the spectrum of deepnet Hessians.* ICML 2019. https://arxiv.org/abs/1901.08244
- [B] Papyan. *Traces of class/cross-class structure pervade deep learning spectra.* JMLR 2020. https://arxiv.org/abs/2008.11865
- [B] Gur-Ari, Roberts, Dyer. *Gradient descent happens in a tiny subspace.* 2018. https://arxiv.org/abs/1812.04754
- [B] Ghorbani, Krishnan, Xiao. *An investigation into neural net optimization via Hessian eigenvalue density.* ICML 2019. https://arxiv.org/abs/1901.10159
- [C] Singh, Bachmann, Hofmann. *Analytic insights into structure and rank of neural network Hessian maps.* NeurIPS 2021. https://arxiv.org/abs/2106.16225
- [C] Liao, Mahoney. *Hessian eigenspectra of more realistic nonlinear models.* NeurIPS 2021. https://arxiv.org/abs/2103.01519
- [B] Frankle, Dziugaite, Roy, Carbin. *Linear mode connectivity and the lottery ticket hypothesis.* ICML 2020. https://arxiv.org/abs/1912.05671
- [B] Fort et al. *Deep learning versus kernel learning: an empirical study of loss landscape geometry and the time evolution of the NTK.* NeurIPS 2020. https://arxiv.org/abs/2010.15110
- [B] Jastrzebski et al. *The break-even point on optimization trajectories of deep neural networks.* ICLR 2020. https://arxiv.org/abs/2002.09572
- [B] Soudry, Hoffer, Nacson, Gunasekar, Srebro. *The implicit bias of gradient descent on separable data.* JMLR 2018. https://arxiv.org/abs/1710.10345
- [B] Lyu, Li. *Gradient descent maximizes the margin of homogeneous neural networks.* ICLR 2020. https://arxiv.org/abs/1906.05890

*Written with Claude.*
