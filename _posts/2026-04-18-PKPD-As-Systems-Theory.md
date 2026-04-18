---
title: "PKPD as Systems Theory"
date: 2026-04-18
motivation: "Pharmacology reads as chemistry + curve-fitting until you notice it is a small library of canonical dynamical systems templates.  Cascaded filters, saturating nonlinearities, slow-fast integral feedback, opponent processes - the math is generic and transferable, and the concrete pharmacology tells you when each template bites."
background: "Linear systems (Laplace / transfer functions), a little ODE / state-space, comfort with Michaelis-Menten-type saturating nonlinearities.  Pharmacological intuition is not required - drugs are here as worked examples of the math."
llm: "Claude"
tags: [seed]
math: true
---

# PKPD as Systems Theory

Pharmacokinetics-pharmacodynamics (PKPD) gets taught as two disjoint topics joined by a fitting exercise: PK is "what the body does to the drug", PD is "what the drug does to the body", and somewhere a curve is fit.  That framing hides the fact that PKPD is, in its good parts, a small zoo of canonical dynamical-systems templates.  Cascaded first-order LTI filters, Langmuir-type saturating nonlinearities, integral feedback with slow-fast decomposition, a second-order opponent process, multiplicative gain modulation.  Each template is simple enough to carry around in your head, and the pharmacology is mostly useful as a set of sharp worked examples that tell you when the template is load-bearing.

The reframing: **the same molecule is medicine, poison, or recreational drug depending on the shape of the transfer function between ingestion and receptor-level signaling.**  Shape-of-transfer-function is a very general thing to care about, and pharmacology is one of the places where you can actually see all the pieces - input filters, saturating readouts, adaptation loops - mattering at once.

This post walks the zoo.  I'll name each equation by its proper name when it has one, flag when a piece is "just a generic first-order LTI compartment" or "just a generic Hill saturation", and keep concrete drug examples only where they anchor what the math is good for.  The source for a lot of this is a longer PKPD tutorial I wrote for my own use; here I'm pulling out the skeleton.

## 1.  A Drug as an Input-Output System

Call $u(t)$ the rate of drug entering the body (a bolus dose is a $\delta$-function; a slow infusion is a step; an oral pill is something in between).  Call $y(t)$ whatever you actually care about: receptor occupancy, a physiological readout, reinforcement signal, side effect.  Between them sits a chain:

$$
u(t) \xrightarrow{\text{PK}} C_p(t) \xrightarrow{\text{effect-site}} C_e(t) \xrightarrow{\text{binding}} \rho(t) \xrightarrow{\text{transduction}} E(t) \xrightarrow{\text{adaptation}} y(t)
$$

From left to right, the typical character of each block:

- PK is **linear** (first-order LTI compartments, almost always) and gives plasma concentration $C_p$.
- The effect-site step is **another LTI filter** that accounts for the fact that the brain, or wherever the receptor is, lags plasma.
- Binding is a **static saturating nonlinearity** (Langmuir / Hill).
- Transduction can amplify or flatten that nonlinearity (Black-Leff operational model).
- Adaptation is a **slow integral feedback loop** on top of everything else (receptor up/downregulation).

Everything here is generic.  The pharmacology is a rich zoo of cascades of these blocks, in which you can see each block matter in isolation.

## 2.  Linear PK: Compartment Models Are Generic First-Order LTI Cascades

### 2.1  One compartment

The simplest PK model treats the body as one well-mixed volume of apparent size $V_d$ ("volume of distribution" - apparent because drugs that sequester into fat can have $V_d$ larger than the body).  Plasma concentration $C(t)$ after an IV bolus of dose $D$:

$$
\dot C = -k_e C, \qquad C(0) = D/V_d.
$$

This is the generic first-order LTI compartment.  In Laplace:

$$
\frac{C(s)}{U(s)} = \frac{1/V_d}{s + k_e}.
$$

A first-order low-pass with cutoff $k_e$.  The half-life is $t_{1/2} = \ln 2 / k_e$; clearance is $\mathrm{CL} = k_e V_d$ (volume of plasma completely cleared per unit time).

First real prediction this gives you for free: drugs with long half-lives cannot produce sharp concentration transients regardless of route.  A low-pass can't pass a spike.

### 2.2  Oral absorption: two-pole cascade

Swallowed drugs pass through a gut compartment first:

$$
\dot C_g = -k_a C_g, \qquad \dot C = \tfrac{k_a F}{V_d} C_g - k_e C,
$$

where $k_a$ is absorption rate and $F \in [0,1]$ is **bioavailability** (the fraction surviving first-pass hepatic metabolism).  The transfer function from dose input to plasma is

$$
H(s) = \frac{F k_a / V_d}{(s + k_a)(s + k_e)},
$$

a two-pole cascade whose impulse response is a difference of exponentials (the **Bateman function**):

$$
C(t) = \frac{F D k_a}{V_d (k_a - k_e)} \bigl(e^{-k_e t} - e^{-k_a t}\bigr).
$$

This is just a generic two-stage first-order cascade; you meet it in pharmacokinetics, radioactive decay chains, consecutive first-order chemical reactions, and compartmental tracer kinetics in PET.

The pharmacology bite: **route is a choice of input filter.**  Same molecule, same $k_e$, same receptor - but IV, intranasal, oral, slow-release all look like convolving a fixed impulse response with a different input kernel, so they produce radically different $dC_p/dt$.  When we get to §7 we'll see that $dC_e/dt$ (not $C_e$) is what the reinforcement-learning system actually sees, which is the quantitative way to say "rate of onset determines abuse potential".

### 2.3  Two-compartment: state-space distribution

Many drugs don't stay in plasma; they partition into tissue.  Central compartment $C_1$ (plasma, volume $V_1$), peripheral $C_2$ (tissue, $V_2$):

$$
\frac{d}{dt}\begin{pmatrix} C_1 \\ C_2 \end{pmatrix}
= \begin{pmatrix} -(k_{12}+k_e) & k_{21} \\ k_{12} & -k_{21} \end{pmatrix}
\begin{pmatrix} C_1 \\ C_2 \end{pmatrix}
+ \begin{pmatrix} u/V_1 \\ 0 \end{pmatrix}.
$$

Two negative eigenvalues $\alpha > \beta > 0$, so after a bolus you see biexponential decay: fast $\alpha$-phase is distribution into tissue, slow $\beta$-phase is true elimination.  Terminal half-life is $t_{1/2,\beta} = \ln 2 / \beta$.

This is exactly the same math as a two-tank linear mixing model, or any two-state Markov chain with a drain.  Nothing pharmacological is required to write it down; it's the generic second-order linear compartmental system.

### 2.4  Repeated dosing: steady state and accumulation

Under repeated oral dosing at interval $\tau$, the steady-state trough is

$$
C_{ss,\min} = \frac{FD}{V_d}\cdot\frac{e^{-k_e\tau}}{1 - e^{-k_e\tau}},
$$

with accumulation ratio $R = 1/(1 - e^{-k_e\tau})$.  Time to reach steady state is $\sim 4$-$5$ half-lives, independent of the dose and dosing frequency.  (This is a generic fact about first-order systems driven by periodic inputs, not a PK fact.)

tl;dr of linear PK: **every standard PK textbook picture is a cascade of generic first-order LTI compartments driven by different input shapes.**  You can read off time-to-steady-state, accumulation, and peak-trough swing without any pharmacology-specific content.

## 3.  Receptor Binding: Generic Saturating Nonlinearity

### 3.1  Langmuir / Clark / Michaelis-Menten

Drug $D$ binds receptor $R$ with on/off rates $k_\text{on}, k_\text{off}$.  Equilibrium occupancy fraction:

$$
\rho = \frac{[D]}{[D] + K_d}, \qquad K_d = \frac{k_\text{off}}{k_\text{on}}.
$$

This is the **Langmuir isotherm**, identical in form to **Michaelis-Menten** enzyme kinetics.  $K_d$ is the **dissociation constant** - the concentration at which half the receptors are occupied.

Cooperativity (or downstream sharpening) promotes this to the **Hill equation**:

$$
\rho = \frac{[D]^n}{[D]^n + K_d^n}.
$$

$n$ is the **Hill coefficient**.  $n=1$ is the plain hyperbola; $n \gtrsim 2$ is a sigmoid, a soft switch around $K_d$.  This is just the generic saturating nonlinearity you meet everywhere in kinetics and in logistic models of activation.

Two things to take from this block:

- **$K_d$ is thermodynamic, not behavioral.**  It tells you how many receptors are bound at equilibrium.  It says nothing about what happens when the receptor is bound.
- **Hill $n$ sets where you're sensitive.**  Steep $n$ means small changes in $[D]$ near $K_d$ swing occupancy hard, and nothing much happens far from $K_d$.  This is why dose-response curves have a therapeutic window: the steep part of the sigmoid.

### 3.2  Affinity vs. efficacy: the Black-Leff operational model

The original Clark picture assumed effect was proportional to occupancy, $E = E_\text{max}\rho$.  This is wrong.  Different ligands at the same receptor, even at full occupancy, produce different maximal responses.  The cleanest way to handle this is the **Black-Leff operational model** (1983), which introduces a **transducer ratio** $\tau = [R_t]/K_E$ (receptor density divided by a transducer constant).  Substituting $\rho = [D]/([D] + K_d)$:

$$
E = \frac{E_\text{max}\,\tau [D]}{K_d + [D](1+\tau)}.
$$

Still a hyperbolic response curve, but with two modifications worth naming:

- **Apparent $\mathrm{EC}_{50} = K_d / (1+\tau)$**, strictly less than $K_d$.  So you can reach 50% of maximal response with $<50\%$ of receptors occupied.  The surplus is called **receptor reserve** or "spare receptors".
- **Apparent $E_\text{max} = E_\text{max}\tau / (1+\tau)$**, approaching $E_\text{max}$ only as $\tau \to \infty$.

A full agonist has large $\tau$.  A partial agonist has small $\tau$ - the response curve sits lower no matter how much you push $[D]$.  This is the minimal model that separates **affinity** (binding tightness, $K_d$) from **efficacy** (signaling coupling, $\tau$), and it's the whole reason "binds it tightly" and "activates it strongly" are independent design axes in drug discovery.

A nice consequence: because $\tau \propto [R_t]$, the same molecule can be a full agonist in a tissue with lots of receptors and a partial agonist in a tissue with few.  "Partial agonism" is not a property of the molecule alone - it's joint with the system.

One concrete pharmacology anchor where this distinction is load-bearing: **benzodiazepines vs. barbiturates at $\text{GABA}_A$**.  Benzos are positive allosteric modulators (PAMs) - they only amplify endogenous GABA signaling, so they have a ceiling set by how much GABA is actually around.  Barbiturates bind a different site and can drive the channel directly.  Same receptor, same downstream effect class, but "amplifier with ceiling" vs. "direct driver" is the difference between "hard to overdose on" and "easy to die from".  The operational model plus the PAM-vs-agonist distinction is the minimal apparatus that makes this cleanly visible.

## 4.  Effect Compartment: Hysteresis as Phase Lag

If you plot effect $E(t)$ against plasma concentration $C_p(t)$ parametrically in $t$, you often trace out a **loop** rather than a curve - effect lags plasma on the way up and persists on the way down.  This is hysteresis, and it has (at least) two distinct sources:

- Distribution lag: the drug takes time to cross blood-brain barrier or otherwise reach the effect site.
- Mechanism lag: the receptor-triggered effect needs downstream machinery (second messengers, gene expression) that has its own time constants.

For pure distributional lag, the **Sheiner effect compartment** model postulates a virtual compartment with negligible volume (so it doesn't contaminate PK) and equilibration rate $k_{e0}$:

$$
\dot C_e = k_{e0}(C_p - C_e), \qquad \frac{C_e(s)}{C_p(s)} = \frac{k_{e0}}{s + k_{e0}}.
$$

Yet another generic first-order LTI low-pass, cascaded onto the PK transfer function.  Apply your PD model (Hill, operational) to $C_e$ instead of $C_p$ and the hysteresis loop collapses into a single curve.

The general fact: **hysteresis between two signals in a causal system is phase lag.**  If you introduce the right lagged intermediate variable, the loop in the $(C_p, E)$ plane straightens out into a curve in $(C_e, E)$.  This is exactly what phasors do for sinusoidal steady state, and it's the same idea here.  (Mechanism-level hysteresis, where the shape of $E(\cdot)$ itself drifts with exposure history, is a different beast and gets its own section.)

## 5.  Receptor Dynamics as Integral Feedback - Slow-Fast Decomposition

The number of functional receptors is not fixed.  Cells adjust it based on the time-integrated activation history - classic **integral feedback control**.  In a minimal model, let $R(t)$ be functional receptor density and $\sigma(t)$ be a leaky-integrator proxy for cumulative agonist signal:

$$
\dot R = k_\text{syn} - k_\text{deg} R - k_\text{down}\sigma R,
$$

$$
\dot\sigma = C_e - k_\sigma \sigma.
$$

The steady state with no drug is $R_0 = k_\text{syn}/k_\text{deg}$.  Under chronic agonist, $R$ decreases - **tolerance**.  Upon sudden withdrawal, $\sigma$ takes its own timescale to decay while $R$ relaxes back toward $R_0$; during the mismatch, the system is hypersensitive - **rebound**.

This is structurally a generic slow-fast adaptation model, and it has exact analogues in sensory adaptation (retinal light adaptation, olfactory desensitization), in bacterial chemotaxis (the methylation state of the receptor serves as $\sigma$), and in any control loop that tries to cancel persistent DC error via an integrator.

Concrete pharmacology anchor: **$\beta$-blocker withdrawal causes rebound tachycardia** because chronic antagonism upregulates $\beta$-adrenergic receptors (the "low input, crank the gain" mode); **benzodiazepine withdrawal produces hyperexcitability** because chronic PAM use downregulates $\text{GABA}_A$ function.  Same block of math, opposite signs.  The severity of withdrawal is set by (a) how far from $R_0$ chronic use pushed the receptor pool, (b) the timescale separation between $R$ dynamics and $\sigma$ dynamics, and (c) whether the resulting transient crosses a stability boundary of the larger circuit (see §9).

## 6.  Irreversible Inhibition: Effect Outlives PK

Not every drug plays by Langmuir rules.  **Mechanism-based inhibitors** form covalent bonds with their targets: the off-rate is effectively zero.  Once a target molecule is hit, the only way to recover function is to **synthesize a new one**.

The generic model for a covalent inhibitor hitting an enzyme $E$ (not to be confused with "effect" from earlier - conflict of notation is unavoidable here):

$$
\dot {[E]} = k_\text{syn} - k_\text{deg}[E] - k_\text{inact}[D][E],
$$

with steady-state active-enzyme level under chronic drug

$$
[E]_{ss} = \frac{k_\text{syn}}{k_\text{deg} + k_\text{inact}[D]},
\qquad
f_\text{inhib} = \frac{k_\text{inact}[D]}{k_\text{deg} + k_\text{inact}[D]}.
$$

That looks like a Michaelis-Menten curve, but the apparent "$K_d$" is $k_\text{deg}/k_\text{inact}$ - the ratio of **enzyme turnover rate** to **inactivation rate**.  This is not a thermodynamic binding constant.  It's a steady-state ratio between a synthesis process and an attack rate.

The real kicker: **the duration of pharmacological effect is set by the target's resynthesis timescale, not by the drug's own PK half-life.**

The canonical example is **selegiline**, a selective irreversible inhibitor of monoamine oxidase B (MAO-B).  Selegiline itself clears with half-life $\sim 10$ hours.  But once it has attached itself to MAO-B, the enzyme is permanently dead, and the MAO-B pool recovers over 2-6 weeks as new enzyme is synthesized.  So the *drug* is gone in a day and the *effect* lasts weeks.  This is a qualitatively different regime from reversible competitive inhibitors (say, bupropion's DAT/NET inhibition), where effect tracks plasma within a few half-lives.

The general lesson: whenever your "drug" forms a stoichiometric, non-recoverable modification of its target, **the target's resynthesis rate - not the drug's elimination rate - is the slow variable**, and that's the timescale of interest.  This is a specific, non-generic insight that the linear-cascade picture does not give you: it's the one place in this zoo where the PK half-life genuinely misleads you.

## 7.  Opponent Process as a Generic Second-Order System

Solomon and Corbit's **opponent process theory** of motivation proposes that every hedonic process (the "$a$-process") triggers a slower compensatory opponent (the "$b$-process"), and observed affect is their difference.  Minimally:

$$
\dot a = -a/\tau_a + u(t), \qquad \dot b = -b/\tau_b + \kappa a, \qquad y = a - b.
$$

With $\tau_b \gg \tau_a$, this is a generic second-order system with overshoot and afterimage: stimulus onset $\Rightarrow$ $a$ rises fast while $b$ lags $\Rightarrow$ positive $y$; stimulus offset $\Rightarrow$ $a$ drops fast while $b$ is still elevated $\Rightarrow$ negative $y$ (the withdrawal "afterimage").

This is isomorphic to a cascade of two first-order filters with opposite signs summed at the output.  In control-theory language, it's a classic lag-lead arrangement with a sign inversion - the reason it has overshoot is just that the two timescales differ.

Koob's **allostatic extension** says the $b$-process doesn't just transiently track $a$, it also **ratchets up its setpoint** under repeated stimulation.  In notation:

$$
\dot b_0 = \eta \max(b - b_0, 0) - \mu b_0, \qquad \eta \gg \mu.
$$

Asymmetric gain on $b_0$: the setpoint drifts upward much faster than it recovers.  This makes the opponent process **allostatic** - the regulator is itself modified by what it regulates.  Generic instance of the same idea: any slowly-varying parameter in a homeostat that is driven by an asymmetric rectifier of the regulated variable will drift, and the drift is where long-term "wear" lives.

Pharmacology anchor: this is one cartoon of the addiction trajectory - fast hedonic gain, slow build of opponent tone, and a slowly drifting opponent setpoint that doesn't fully reset.  The "dark side" of addiction (dysphoria in the absence of drug) shows up as the $b_0$ term failing to come back down.

## 8.  Gain Modulation and the Inverted U

At the circuit level, neuromodulators (dopamine, serotonin, norepinephrine) aren't primarily excitatory or inhibitory - they are **multiplicative gain knobs** on input-output functions of neural populations.  If a population has activity $r = f(I)$, a gain-modulated version looks like

$$
r = f\bigl(g(m) \cdot I\bigr),
$$

where $m$ is the modulator concentration and $g$ is some gain function.  For prefrontal dopamine (Arnsten's inverted-U), the empirical shape is something like

$$
g(m) \sim m^\gamma e^{-m/m^*},
$$

with an interior optimum at $m^*$.  Low $m$ → weak gain, signal buried in noise; very high $m$ → gain collapses, past-peak nonlinearity, representations destabilize.  This is a **non-monotonic** dose-response on the output even if every individual piece (binding, transduction) is monotonic.  It's the cleanest structural answer to "why is the dose-response for cognitive drugs inverted-U?": it's not about the molecule, it's about where on the gain curve you started.

The broader circuit in which $g(m)$ lives is often a **Wilson-Cowan** E/I pair:

$$
\tau_E \dot E = -E + f_E(w_{EE} E - w_{IE} I + h_E),
$$

$$
\tau_I \dot I = -I + f_I(w_{EI} E - w_{II} I + h_I),
$$

with sigmoidal $f_E, f_I$.  This generic two-population model supports fixed points, oscillations, bistability, and winner-take-all depending on the weights.  Neuromodulators slide its parameters around: dopamine in PFC tunes $w_{EE}$ and the slope of $f_E$ (sharpens working-memory attractors, but past a point makes them too stable - perseveration, hallucination); serotonin shifts E/I balance toward $I$ (behavioral inhibition, and part of the story for SSRIs in OCD and anxiety).

Nothing here is pharmacology-specific.  Gain modulation of sigmoidal input-output functions is a generic move - it's what multiplicative attention does in neural networks, what adaptive control does for sensor gain, and what any hormonal homeostat does when it rescales a tissue's responsiveness.

## 9.  Rate of Rise and Reinforcement Learning

The whole cascade finally cashes out at behavior.  For drugs that act through phasic dopamine, the reinforcement-learning system cares about the **reward prediction error**, and phasic DA encodes something like

$$
\delta(t) \propto \left(\frac{dC_e}{dt}\right)_+,
$$

the positive part of the rate of change of effect-site concentration.  RPE neurons encode surprise - departure from expected baseline - so a slow rise gets predicted away and elicits little RPE, while a sharp spike fires the system before the prediction can catch up.

For a DAT inhibitor with effect-compartment kinetics $C_e(t) = h(t) * C_p(t)$, differentiating and bounding gives

$$
\max \frac{dC_e}{dt} \lesssim k_{e0}\,\max C_p(t).
$$

So the reinforcement signal is bounded by the product of peak plasma concentration and effect-site equilibration rate.  Cocaine (fast intranasal $k_a$, high $k_{e0}$, $\sim 60$-$80\%$ DAT occupancy) wins this product by roughly an order of magnitude over bupropion (slow oral $k_a$, moderate $k_{e0}$, $\sim 25\%$ DAT occupancy).  Both inhibit the same target with similar mechanism - the difference between "antidepressant" and "drug of abuse" shows up as a quantitative bound on $dC_e/dt$.

**The structural lesson** is the one I care about.  The system response depends on the **derivative** of the effect-site signal, not the signal itself.  If you rewrite your block diagram as a low-pass cascade followed by a derivative followed by a rectifier, the "abuse potential" question is just "what's the max output of this operator chain for a physically realizable input?"  That's a completely generic signal-processing question - and the answer is that an aggressive input filter (fast $k_a$) + an aggressive effect-site filter (fast $k_{e0}$) maximize the derivative, which maximizes the RPE signal, which maximizes the reinforcement.  You can make any drug more addictive by making the transfer function between dose and effect-site faster, without changing the molecule at all.  That's why formulation matters.

## 10.  The Library

Compressed, the zoo is small:

| Block | Math | What it buys you |
|-------|------|------------------|
| PK compartment | $\dot C = -k_e C$ | Generic first-order LTI low-pass |
| Oral absorption | Two poles, Bateman | Cascaded low-pass, route = input filter |
| Two-compartment | Biexponential | State-space distribution, two timescales |
| Langmuir / Hill | $\rho = C^n/(C^n+K_d^n)$ | Generic saturating nonlinearity |
| Black-Leff operational | $E = E_\text{max}\tau\rho / (1+\tau\rho)$ | Separates affinity from efficacy |
| Effect compartment | Extra LP with $k_{e0}$ | Makes hysteresis go away |
| Receptor regulation | $\dot R = k_\text{syn} - k_\text{deg} R - k_\text{down}\sigma R$ | Integral feedback $\Rightarrow$ tolerance + rebound |
| Irreversible inhibition | $\dot E = k_\text{syn} - k_\text{deg} E - k_\text{inact} D E$ | Effect timescale = target resynthesis, not PK |
| Opponent process | $\dot a,\dot b$ with $\tau_b\gg\tau_a$ | Generic 2nd-order with overshoot; allostatic if $b_0$ drifts |
| Gain modulation | $r=f(g(m)\cdot I)$ | Non-monotonic dose-response from monotonic pieces |
| RPE $\times$ kinetics | $\delta \propto (dC_e/dt)_+$ | Rate of rise sets reinforcement |

Each block is generic; each concrete drug is some particular choice of parameters and a particular cascade of these blocks.  The art of PKPD reasoning is knowing which block is rate-limiting for the question you're asking.

## 11.  One-Line Pointers

Things that deserve their own posts but belong on the map:

- **Biased agonism:** operational $\tau$ is not scalar but different per downstream pathway at the same receptor.  Lets you design ligands that hit G-protein but not $\beta$-arrestin, etc.
- **Chronopharmacology:** circadian modulation of PK parameters ($k_e$, $V_d$, $F$) and receptor densities.  Same dose at 8am vs. 10pm can be meaningfully different drugs.
- **Population PK / NONMEM:** the parameters above are not scalars but draws from distributions across the population, and the whole pipeline is a mixed-effects model.  This is where PK meets statistics for real.
- **Dose individualization:** once you have population-level distributions on $(k_e, V_d, k_a, F, k_{e0}, \tau, K_d)$, Bayesian updating on plasma measurements gives per-patient posterior estimates and optimal individualized schedules.

None of these change the zoo.  They just dress the same blocks in more distributional machinery.

## Coda

The thing I actually want the reader to take away is independent of pharmacology: there's a small library of canonical dynamical-systems blocks - cascaded first-order filters, saturating nonlinearities, integral feedback with slow-fast decomposition, multiplicative gain, opponent processes - that compose to describe a genuinely hard domain (what a drug actually does to a person) with surprisingly little pharmacology-specific structure.  The pharmacology is where you get to watch each block matter in isolation, which makes it an unreasonably good training ground for input-output reasoning in general.

If you want a one-sentence slogan: **PKPD is a control-theory problem in disguise, and the disguise is mostly just a vocabulary.**

Written with Claude.
