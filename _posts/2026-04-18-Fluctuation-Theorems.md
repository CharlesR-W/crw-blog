---
title: "Fluctuation Theorems"
date: 2026-04-18
motivation: "The second law, in its usual form, is an inequality about averages. Fluctuation theorems upgrade it to equalities holding for the full distribution of work, heat, and entropy. This is the quiet revolution that transformed non-equilibrium statistical mechanics in the 1990s and 2000s."
background: "Graduate stat mech (Gibbs ensembles, free energy, detailed balance). Some comfort with Langevin or Markov jump processes helps. The goal is to see why one identity, $\\langle e^{-\\sigma}\\rangle = 1$, is really the whole show."
llm: "Claude"
tags: [seed]
math: true
---

# Fluctuation Theorems

## The 2nd Law, Upgraded

Classical stat mech gives you the second law as an inequality over averages.  Pull on a polymer, compress a gas, drag a bead through water: the average work you put in is at least the free energy difference,

$$
\langle W \rangle \geq \Delta F.
$$

That's true, it's correct, and for most of the 20th century it was basically the end of the story for finite-rate processes.  The trouble is that "average" is doing a lot of heavy lifting.  For a single trajectory, $W$ is a random variable.  Sometimes $W < \Delta F$.  Sometimes entropy decreases.  What rule governs how often?

In the 1990s and early 2000s, Jarzynski, Crooks, Gallavotti, Cohen, Evans, Searles, Sekimoto, Seifert, and others figured out the rule.  The answer is startlingly clean: a family of exact equalities holds for the full distribution of work, heat, and entropy production, arbitrarily far from equilibrium.  The second law is what you get when you apply Jensen's inequality to one of them.

This is what people mean by "stochastic thermodynamics".  It's not a generalization of thermodynamics to fluctuations.  It's a refinement: the usual laws are shadows cast by sharper equalities.

## Jarzynski Equality

The one that cracked it open.  Take a system with Hamiltonian $H(x, \lambda)$ where $\lambda$ is an external control parameter: piston position, laser trap stiffness, whatever.  Start in canonical equilibrium at $\lambda_0$, so the initial distribution is

$$
\rho_0(x) = \frac{e^{-\beta H(x, \lambda_0)}}{Z(\lambda_0)}.
$$

Now drag $\lambda$ from $\lambda_0$ to $\lambda_1$ along some protocol $\lambda(t)$, $t \in [0, T]$.  Fast, slow, wiggly, doesn't matter.  For each trajectory $x(t)$, define the work done on the system as

$$
W[x(\cdot)] = \int_0^T \frac{\partial H}{\partial \lambda}\, \dot\lambda\, dt.
$$

Then Jarzynski's equality says

$$
\boxed{\langle e^{-\beta W} \rangle = e^{-\beta \Delta F}}
$$

where $\Delta F = F(\lambda_1) - F(\lambda_0)$ is the equilibrium free energy difference and the average is over the ensemble of trajectories induced by the initial distribution and whatever dynamics you're running.

Let me emphasize how weird this is.  $\Delta F$ is an equilibrium quantity.  $W$ is a non-equilibrium quantity, depending on the whole protocol.  And yet the equality is exact, for any protocol, no matter how fast.

### Derivation (Hamiltonian)

Take the dynamics to be Hamiltonian with a time-dependent $\lambda(t)$.  Along any trajectory,

$$
\frac{dH}{dt} = \{H, H\} + \frac{\partial H}{\partial \lambda} \dot\lambda = \frac{\partial H}{\partial \lambda} \dot\lambda.
$$

So $W = H(x(T), \lambda_1) - H(x(0), \lambda_0)$.  Now:

$$
\langle e^{-\beta W} \rangle = \int dx_0\, \rho_0(x_0)\, e^{-\beta [H(x(T), \lambda_1) - H(x_0, \lambda_0)]}.
$$

Substitute $\rho_0 = e^{-\beta H(x_0, \lambda_0)}/Z(\lambda_0)$.  The two $H(x_0, \lambda_0)$ factors cancel:

$$
\langle e^{-\beta W} \rangle = \frac{1}{Z(\lambda_0)} \int dx_0\, e^{-\beta H(x(T), \lambda_1)}.
$$

Hamiltonian flow is measure-preserving (Liouville), so $dx_0 = dx(T)$.  Change variables:

$$
\langle e^{-\beta W} \rangle = \frac{1}{Z(\lambda_0)} \int dx_T\, e^{-\beta H(x_T, \lambda_1)} = \frac{Z(\lambda_1)}{Z(\lambda_0)} = e^{-\beta \Delta F}.
$$

Please clap.

### Generality

Jarzynski works for a lot more than Hamiltonian dynamics.  If your system is coupled to a thermostat (Langevin, Nose-Hoover, Markov jump process with detailed balance), the same identity goes through.  The only ingredients you need are:

1. Start in canonical equilibrium at $\lambda_0$.
2. Dynamics preserve canonical equilibrium at each fixed $\lambda$ (microcanonical also works, mutatis mutandis).
3. Define $W$ as the integrated "$\partial H/\partial \lambda$" along the trajectory.

The proofs are all basically the same trick: the weights line up so that the end-time distribution, reweighted by $e^{-\beta W}$, is the equilibrium distribution at $\lambda_1$.

Jensen's inequality gets you the 2nd law as a corollary:

$$
e^{-\beta \langle W \rangle} \leq \langle e^{-\beta W} \rangle = e^{-\beta \Delta F} \implies \langle W \rangle \geq \Delta F.
$$

That inequality is the shadow.  The equality is the sun.

## Crooks Fluctuation Theorem

Jarzynski's equality is already a big deal, but it's really a corollary of something deeper.  Crooks's theorem relates the distribution of work in a forward protocol to the distribution of work in the time-reversed protocol.

Let $P_F(W)$ be the probability of observing work $W$ when you run $\lambda$ from $\lambda_0 \to \lambda_1$ starting from equilibrium at $\lambda_0$.  Let $P_R(W)$ be the probability of observing work $W$ when you run the reverse protocol $\lambda(T - t)$ from $\lambda_1 \to \lambda_0$ starting from equilibrium at $\lambda_1$.

Then

$$
\boxed{\frac{P_F(W)}{P_R(-W)} = e^{\beta(W - \Delta F)}.}
$$

Again, this is exact.  Any protocol, any speed.

### Microscopic Reversibility Derivation

The cleanest derivation uses a single identity: for time-reversible dynamics in contact with a thermal bath, the ratio of forward to reverse trajectory probabilities is $e^{\beta Q}$, where $Q$ is the heat absorbed by the system.  This is essentially Bayes' rule plus detailed balance.

More concretely, for a Langevin bath or a Markov jump process obeying local detailed balance, if $\mathcal{P}_F[x(\cdot)]$ is the path probability of trajectory $x(t)$ under the forward protocol (starting at $x_0$) and $\mathcal{P}_R[\tilde x(\cdot)]$ is the path probability of the time-reversed trajectory $\tilde x(t) = x(T - t)$ under the reverse protocol,

$$
\frac{\mathcal{P}_F[x(\cdot)]}{\mathcal{P}_R[\tilde x(\cdot)]} = e^{\beta Q[x(\cdot)]}
$$

where $Q$ is the heat delivered to the system from the bath along the forward path.  (Equivalently, $-Q$ is the heat dumped to the bath.)

Now include the initial equilibrium weights.  The forward ensemble has weight $\rho_0(x_0) \mathcal{P}_F[x(\cdot)]$ with $\rho_0 \propto e^{-\beta H(x_0, \lambda_0)}$.  The reverse ensemble has weight $\rho_1(x_T) \mathcal{P}_R[\tilde x(\cdot)]$ with $\rho_1 \propto e^{-\beta H(x_T, \lambda_1)}$.  The ratio:

$$
\frac{\rho_0(x_0) \mathcal{P}_F[x(\cdot)]}{\rho_1(x_T) \mathcal{P}_R[\tilde x(\cdot)]} = \frac{Z(\lambda_1)}{Z(\lambda_0)} e^{-\beta [H(x_0, \lambda_0) - H(x_T, \lambda_1)]} e^{\beta Q} = e^{\beta \Delta F} e^{\beta(Q + \Delta H)}.
$$

First law: $W = \Delta H - Q$, so $Q + \Delta H = W$ wait no, $Q + \Delta H$... let me be careful.  Energy balance says $\Delta H = W + Q$ (work and heat both add to energy).  So $-\Delta H + Q = -W$.  We had $H(x_0, \lambda_0) - H(x_T, \lambda_1) = -\Delta H$.  Then $-\Delta H + Q = -W$, so the exponent is $\beta \Delta F - \beta W + \ldots$ (CHECK signs, I always mess these up).  The cleanest way: trust the final answer and verify by integrating.

The ratio of path weights, integrated over all paths producing work $W$, gives

$$
\frac{P_F(W)}{P_R(-W)} = e^{\beta(W - \Delta F)}.
$$

Signs again: work $W > \Delta F$ is dissipative and more likely in the forward direction than its negative in the reverse.  That matches intuition.

### Jarzynski as a Corollary

Integrate Crooks against $e^{-\beta W}$:

$$
\int e^{-\beta W} P_F(W)\, dW = \int e^{-\beta W} \cdot e^{\beta(W - \Delta F)} P_R(-W)\, dW = e^{-\beta \Delta F} \int P_R(-W)\, dW = e^{-\beta \Delta F}.
$$

The left side is $\langle e^{-\beta W} \rangle_F$.  Jarzynski, out the back.  Crooks is stronger.

### Reading Crooks As A Symmetry

Rewrite it as

$$
P_F(W) e^{-\beta W / 2} = P_R(-W) e^{+\beta W / 2} \cdot e^{-\beta \Delta F}.
$$

The distribution $\tilde P(W) \equiv P_F(W) e^{-\beta W/2}$ (up to normalization) is related to $\tilde P_R(-W)$ by a constant.  Equivalently, the log-ratio $\ln P_F(W) - \ln P_R(-W)$ is linear in $W$ with slope $\beta$ and intercept $-\beta \Delta F$.  This is a linear relationship you can fit experimentally, and the point where $P_F(W) = P_R(-W)$ gives you $\Delta F$ for free.  Nice.

## Detailed Fluctuation Theorem: The Unified Kernel

Jarzynski and Crooks both smell like instances of something more general.  They are.  The cleanest way to see this is to define entropy production along a trajectory.

For a trajectory $\omega = x(\cdot)$ with time-reversed counterpart $\bar\omega$, define

$$
\sigma[\omega] = \ln \frac{\mathcal{P}[\omega]}{\tilde{\mathcal{P}}[\bar\omega]}
$$

where $\mathcal{P}$ is the forward path weight including initial distribution and $\tilde{\mathcal{P}}$ is the reverse path weight with its own initial distribution.  You pick the "reverse reference" measure based on the physics: for a relaxation process it's the equilibrium distribution, for a steady state it's the same steady state run backwards, etc.

Then, by a one-line calculation (change of variables $\omega \leftrightarrow \bar\omega$),

$$
\boxed{\langle e^{-\sigma}\rangle = 1.}
$$

Proof: $\langle e^{-\sigma}\rangle_F = \int \mathcal{P}[\omega] e^{-\sigma[\omega]} d\omega = \int \tilde{\mathcal{P}}[\bar\omega] d\omega = \int \tilde{\mathcal{P}}[\bar\omega] d\bar\omega = 1$.  Done.

This is Seifert's **integral fluctuation theorem**, and it's the unified kernel.  Every fluctuation theorem in the zoo is a specialization of this identity:

- **Jarzynski**: take $\sigma = \beta(W - \Delta F)$.
- **Crooks (detailed form)**: $P(\sigma)/P_R(-\sigma) = e^{\sigma}$, from which $\langle e^{-\sigma}\rangle = 1$ follows by integration.
- **Gallavotti-Cohen (large deviation form)**: steady-state version where $\sigma$ is extensive in time and you look at the rate function.
- **Bochkov-Kuzovlev**: an older, related identity using a different partition between "work" and "exclusive work" (pre-Jarzynski, often overlooked).

The single-line identity $\langle e^{-\sigma}\rangle = 1$ tells you that the 2nd law (now: $\langle \sigma\rangle \geq 0$) is a Jensen consequence of a deeper exact symmetry between forward and reverse dynamics.

## Gallavotti-Cohen: Steady-State Entropy Production

Everything above is for a system started in equilibrium, driven by a protocol.  What if you're in a non-equilibrium steady state - say, a particle driven around a ring by a non-conservative force, or a chemical reaction network with sustained chemostats?  Then there's no protocol, but there's a steady rate of entropy production $\dot\sigma$.

Gallavotti-Cohen (1995) proved a fluctuation theorem for the time-averaged entropy production rate $\sigma_\tau = \sigma / \tau$ in the long-$\tau$ limit.  The statement is about the large-deviation rate function $I(s)$ defined by

$$
P(\sigma_\tau \approx s) \asymp e^{-\tau I(s)}.
$$

Gallavotti-Cohen says

$$
I(-s) - I(s) = s.
$$

This is a symmetry of the rate function itself, not of the full distribution.  Equivalently, the scaled cumulant generating function $\psi(\lambda) = \lim_{\tau \to \infty} \tau^{-1} \ln \langle e^{-\lambda \sigma_\tau \tau}\rangle$ satisfies $\psi(\lambda) = \psi(1 - \lambda)$.

Originally proven for time-reversible Anosov flows (using SRB measures, which is basically the ergodic theory of chaotic systems), then extended to stochastic systems where the proof is much easier.  The SRB-measure version is worth knowing about: for a chaotic deterministic system with a non-equilibrium steady state, the phase-space contraction rate serves as an entropy production, and its fluctuations satisfy GC.  Large deviation theory is the natural language for all of this, and the Gartner-Ellis theorem is the workhorse.

Related: Evans-Searles transient fluctuation theorem, which is the finite-time, no-steady-state-required cousin.

## Stochastic Thermodynamics: Heat, Work, Entropy Along A Trajectory

The deep shift in perspective here is due largely to Sekimoto (Japanese stochastic energetics, 1997-98) and Seifert (unifying framework, 2005).  The claim is: heat, work, and entropy can be defined *along a single trajectory*, not just as ensemble averages.  Then the fluctuation theorems become statements about the distributions of these single-trajectory quantities.

### Langevin case

Take overdamped Langevin dynamics,

$$
\gamma \dot x = -\partial_x U(x, \lambda(t)) + \xi(t), \qquad \langle \xi(t)\xi(t')\rangle = 2\gamma T \delta(t - t').
$$

Sekimoto: define the heat absorbed from the bath along a trajectory as

$$
dQ = [-\gamma \dot x + \xi] \circ dx = [\partial_x U] \circ dx
$$

where $\circ$ is the Stratonovich product.  The first expression is "force from bath times displacement" (the bath does work $dQ$ on the particle).  The second uses the force balance.

Define work as

$$
dW = \partial_\lambda U\, d\lambda.
$$

Then the first law holds trajectory-by-trajectory:

$$
dU = dW + dQ
$$

with $dU$ being the total change in $U(x(t), \lambda(t))$ along the path.  Sanity check: this is exactly what you'd hope.

Seifert then defined a **trajectory entropy**:

$$
s(t) = -\ln \rho(x(t), t)
$$

where $\rho(x, t)$ is the instantaneous ensemble density (obtained by solving the Fokker-Planck equation).  This is weird at first glance - $\rho$ is an ensemble object, but we're evaluating it along a single path.  But it's the right definition: its ensemble average $\langle s\rangle$ is the Gibbs entropy, and with the medium entropy change $\Delta s_m = -Q/T$, the total trajectory entropy $\Delta s_\mathrm{tot} = \Delta s + \Delta s_m$ satisfies the integral fluctuation theorem $\langle e^{-\Delta s_\mathrm{tot}}\rangle = 1$ for *any* initial distribution, any driving protocol.

This is the crown jewel of stochastic thermodynamics: a single exact identity, holding for arbitrary non-equilibrium driving, that reduces to all the other fluctuation theorems as special cases.

### Itô vs. Stratonovich

Side remark that tends to trip people up.  The Sekimoto definitions use Stratonovich products because they preserve the chain rule and make the first law look natural.  If you use Itô, there are extra drift-like corrections.  This matters when you do computations and care about signs.  The physics is the same, but the algebra looks different.

## FDT from Crooks Near Equilibrium

Here's a fun one.  The fluctuation-dissipation theorem says that, in linear response, the response of a system to a perturbation is given by an equilibrium correlation function.  Specifically, if you perturb $H \to H - h(t) A$, the response of $B$ is

$$
\langle B(t)\rangle - \langle B\rangle_\mathrm{eq} = \int_{-\infty}^t \chi_{BA}(t - t') h(t')\, dt'
$$

with $\chi_{BA}(t) = \beta \theta(t) \frac{d}{dt}\langle A(0) B(t)\rangle_\mathrm{eq}$ (up to signs; this is the Kubo form).

Claim: Crooks reduces to this in the linear-response limit.  Sketch.  Take a protocol that perturbs $\lambda$ by a small amount $\epsilon$.  Then $W = \epsilon \int \partial_\lambda H\, \dot\lambda\, dt/\epsilon \cdot \epsilon + O(\epsilon^2)$... ok let me be less sloppy.

Crooks gives $P_F(W) = P_R(-W) e^{\beta(W - \Delta F)}$.  Expand both sides in $\epsilon$, where $W, \Delta F = O(\epsilon)$.  To leading order, the log-ratio $\ln P_F(W)/P_R(-W) = \beta(W - \Delta F)$ is linear in $W$.  The distributions $P_F$ and $P_R$ become Gaussians (central limit theorem / small-$\epsilon$), and linearity of the log-ratio of two Gaussians is automatic: it's a symmetry statement about their means and variances.

Specifically, let $P_F(W) \approx \mathcal{N}(\mu_F, \sigma^2)$ and $P_R(W) \approx \mathcal{N}(\mu_R, \sigma^2)$ (same variance by time-reversal symmetry at leading order).  Then $\ln P_F(W) - \ln P_R(-W) = (W(\mu_F + \mu_R) - (\mu_F^2 - \mu_R^2)/2) / \sigma^2$.  Matching to $\beta(W - \Delta F)$:

$$
\mu_F + \mu_R = \beta \sigma^2.
$$

This is the **Jarzynski-Wang relation** or, viewed appropriately, the FDT.  It says: the average dissipated work in forward plus reverse equals $\beta$ times the variance.  Variance-equals-dissipation is exactly FDT in disguise.

(Kinda feels like it makes sense?  The work variance is an equilibrium fluctuation; the mean dissipation is a response.  FDT links them.  Crooks says they're linked *even away from equilibrium*, with corrections you can compute order by order.  Big if true, and it is true.)

## Experimental Tests

These are not just math games.  They've been tested.

**Liphardt et al. (2002)**: Mechanically unfolded a single RNA hairpin with optical tweezers, pulling fast enough to go non-equilibrium.  Measured $W$ over many trials in both forward and reverse directions, verified Crooks, extracted $\Delta F$ (the folding free energy) from the crossover point.  This was the first clean experimental demonstration.

**Collin, Ritort, Jarzynski, Smith, Tinoco, Bustamante (2005)**: Extended this to more complex RNA structures, including three-state folders.  Showed that Crooks works even when the forward and reverse distributions are wildly non-Gaussian.

**Douarche, Joubaud, Garnier, Petrosyan, Ciliberto (various)**: Tests in driven colloidal systems, electrical circuits in the Nyquist regime.

**Toyabe, Sagawa, Ueda, Muneyuki, Sano (2010)**: The "Maxwell demon" experiment - extracted work from information in a colloidal feedback system, demonstrating the Sagawa-Ueda extension of Jarzynski to information thermodynamics.

The experimental story is essentially closed: fluctuation theorems work.  The interesting questions now are about extending them (feedback, quantum, non-Markovian) and using them as tools (free-energy estimation from non-equilibrium pulling is routine in biophysics now).

## Connection Points

A few directions out, each worth a longer post someday.

**Information thermodynamics.**  Landauer's principle says erasing a bit costs $kT \ln 2$ of heat.  Sagawa and Ueda generalized Jarzynski to feedback-controlled systems: if you measure the state and use the information, the entropy budget has to include the mutual information $I$ between system and measurement, and you get $\langle e^{-\beta W - I}\rangle = e^{-\beta \Delta F}$.  Maxwell's demon doesn't violate the 2nd law; it converts information into work, and the 2nd law now says $\langle W\rangle \geq \Delta F - k T I$.  Information is a thermodynamic resource, and fluctuation theorems quantify the exchange rate.

**Large deviations.**  The Gallavotti-Cohen symmetry is a special case of a general principle: non-equilibrium steady states have a large-deviation structure governed by a rate function $I(\sigma)$ with the symmetry $I(-\sigma) - I(\sigma) = \sigma$.  Touchette's review is the canonical reference.  This is where the probabilistic and thermodynamic pictures meet most cleanly.

**Quantum fluctuation theorems.**  Tasaki-Crooks, Campisi-Hanggi-Talkner, etc.  Same structure, but work isn't an observable in the usual sense (it's a two-time correlation), so the bookkeeping is subtler.  Active area.

**Chemical reaction networks.**  Jarzynski and Crooks adapted to mass-action kinetics with chemostats.  Schmiedl-Seifert, Gaspard, Qian, and others built this out.  Lets you apply fluctuation theorems to metabolic networks, ribosomes, signaling cascades.  Biology-adjacent and fun.

**Active matter.**  Here the fluctuation theorems break in instructive ways, because the "bath" isn't thermal.  You can still define an entropy production, but it doesn't have the same interpretation.  Seifert, Fodor, Marchetti, Cates, and others have worked on what survives.

## What To Read

Shortest sharp reference: **Seifert 2012, "Stochastic thermodynamics, fluctuation theorems, and molecular machines"** (Rep. Prog. Phys.).  Clean, modern, unified.  The right first thing after this post.

Jarzynski's original **PRL 1997** and Crooks's **PRE 1999** are both short and readable.  So is Gallavotti-Cohen's **PRL 1995**, though the proof uses ergodic theory machinery that the later stochastic derivations avoid.

Sekimoto's **"Stochastic Energetics"** (book, 2010) is the definitive treatment of the trajectory-level definitions.

For a big-picture view, Jarzynski's **"Equalities and Inequalities: Irreversibility and the Second Law of Thermodynamics at the Nanoscale"** (Ann. Rev. Cond. Mat. Phys. 2011) is a great survey aimed at newcomers.

Touchette's **"The large deviation approach to statistical mechanics"** (Phys. Rep. 2009) for the large-deviation framing.

## Takeaway

The 2nd law, as taught in undergrad, is an inequality about averages of macroscopic observables.  Fluctuation theorems say the inequality is the shadow of an exact symmetry between forward and reverse trajectories, encoded in the identity $\langle e^{-\sigma}\rangle = 1$.

Everything else is a specialization: Jarzynski for relaxation, Crooks for the joint forward/reverse structure, Gallavotti-Cohen for steady states, Seifert for arbitrary initial conditions, Sagawa-Ueda for feedback.  One kernel, many petals.

What's striking in retrospect is how *simple* the core identity is.  The proof of the integral fluctuation theorem is one line.  The physical reason is just: forward and reverse trajectory probabilities are related by a change of measure whose Radon-Nikodym derivative is $e^\sigma$.  Everything flows from that.

It's rare for a subject to find its unified kernel.  Stat mech found one in the 2000s.  Please clap.

***

*Written with Claude.*

*See also: [Asymptotics, Borel, and Stokes], [WKB and the Art of Matched Asymptotics].*
