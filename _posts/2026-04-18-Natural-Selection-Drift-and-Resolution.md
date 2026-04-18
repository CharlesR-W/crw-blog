---
title: "Natural Selection: Drift, Neutrality, and Resolution Limits"
date: 2026-04-18
motivation: "The deterministic story of selection (see my post 'Natural Selection: Price to Lande') is clean and beautiful, but real populations are finite.  Finite populations turn selection into a noisy channel: most variation is neutral, the molecular clock ticks, and adaptation has a resolution floor set by $1/(N_e s)$.  The math is a diffusion equation on the simplex, and once you see it the slogans stop sounding like folklore."
background: "Comfortable with basic probability, Fokker-Planck / Kolmogorov forward equations, and the idea of a diffusion limit.  No measure theory required.  Helps to have read the companion seed on Price-to-Lande, but not strictly necessary - the selection side is summarized briefly."
llm: "Claude"
tags: [seed]
math: true
---

# Natural Selection: Drift, Neutrality, and Resolution Limits

## The One-Line Pitch

Finite populations can't resolve fitness differences finer than $1/N_e$.  Below that threshold, drift wins and selection is effectively blind.  Above it, selection is deterministic.  Most of population genetics is figuring out what happens on either side of the line.

This is the second of two seeds on asexual natural selection.  The first, "Natural Selection: Price to Lande" (see my post of the same name), handles the deterministic covariance-of-fitness-with-trait story.  Here I do the stochastic counterpart: Wright-Fisher, the diffusion limit, Kimura's fixation formula, neutral theory, the molecular clock, and the drift barrier on adaptation.

The organizing question: **what is the informational resolution of selection?**  Everything else follows.

## Wright-Fisher and Moran

*Two toy models.  Same continuous limit.  You only need to memorize one.*

Start with a haploid population of constant size $N$.  Consider a single biallelic locus, so each individual has type $A$ (frequency $p$) or $a$ (frequency $1 - p$).  We want to know how $p$ evolves under the combined action of selection and reproductive sampling.

### Wright-Fisher

The Wright-Fisher model says: the next generation is formed by drawing $N$ offspring independently from the parent generation, with replacement, weighted by fitness.  Let $A$-types have fitness $1 + s$ and $a$-types fitness $1$.  Conditional on $p_t$, the probability a given offspring is type $A$ is

$$
\tilde{p}_t = \frac{(1 + s)p_t}{(1 + s) p_t + (1 - p_t)} \approx p_t + s p_t (1 - p_t) \quad \text{(for small } s\text{)}.
$$

The number of $A$-types in the next generation is $\text{Binomial}(N, \tilde{p}_t)$.  So

$$
p_{t+1} \mid p_t \;\sim\; \frac{1}{N} \text{Bin}(N, \tilde{p}_t).
$$

**Mean**: $\mathbb{E}[p_{t+1} \mid p_t] = \tilde{p}_t \approx p_t + sp_t(1-p_t)$.  Deterministic selection plus a drift correction near the boundary.

**Variance**: $\mathrm{Var}(p_{t+1} \mid p_t) = \tilde{p}_t(1 - \tilde{p}_t)/N \approx p_t(1 - p_t)/N$.  The sampling noise.

Two things are happening per generation: a deterministic nudge of size $\sim s$, and a random fluctuation of size $\sim 1/\sqrt{N}$.  Whether selection or drift dominates depends on which is bigger.

### Moran

The Moran model is the continuous-time cousin.  At each infinitesimal timestep, a random individual dies and is replaced by an offspring of a random individual (weighted by fitness).  It's less realistic as a demographic model (populations don't reproduce one-at-a-time) but simpler to analyze because transitions are only $\pm 1/N$.  The scaling is different by a factor of 2 in some places, but the continuous limit is the same diffusion.

I'll stick with Wright-Fisher going forward and just note: **effective population size** $N_e$ is what you get when you match the variance of your actual demographic model to the Wright-Fisher variance $p(1-p)/N$.  $N_e$ is usually smaller than census size because of skewed reproductive success, fluctuating population size, and population structure.  In practice $N_e$ is what you estimate, and the nice formulas below are written in terms of it.

## The Diffusion Limit

*The cleanest form of population genetics.  Everything is a Fokker-Planck equation.*

Rescale time by $N_e$: one unit of rescaled time equals $N_e$ generations.  For large $N_e$ the per-generation change is small, and the discrete chain converges to a continuous-time Markov process $p(\tau)$ on $[0, 1]$ with infinitesimal mean and variance

$$
\mu(p) = s \cdot p(1 - p), \qquad \sigma^2(p) = \frac{p(1-p)}{N_e}.
$$

Here I've reverted to the "per-generation" scaling, where time is counted in generations rather than units of $N_e$ generations; this is the convention most papers use.  The density $P(p, t)$ satisfies the **Kolmogorov forward equation** (Fokker-Planck):

$$
\frac{\partial P}{\partial t} = -\frac{\partial}{\partial p}\!\big[\,\mu(p)\, P\,\big] + \frac{1}{2} \frac{\partial^2}{\partial p^2}\!\big[\,\sigma^2(p)\, P\,\big].
$$

Plug in the selection and drift terms:

$$
\boxed{\;\frac{\partial P}{\partial t} = -\frac{\partial}{\partial p}\big[s\, p(1-p)\, P\big] + \frac{1}{2 N_e}\frac{\partial^2}{\partial p^2}\big[p(1-p)\, P\big].\;}
$$

This is the master equation of population genetics.  Kimura turned this into a substantial industry in the 1950s and 1960s; much of what's worth knowing comes from exact solutions to special cases.

### The one dimensionless number

Nondimensionalize.  The relative size of the drift and selection terms is

$$
\frac{\text{drift}}{\text{selection}} \sim \frac{p(1-p)/N_e}{s p(1-p)} = \frac{1}{N_e s}.
$$

So the entire behavior is controlled by the single scaled quantity $N_e s$ (sometimes written $\gamma = 2 N_e s$ for diploids, with a factor-of-2 convention).  Three regimes.

- $\lvert N_e s \rvert \gg 1$: selection dominates.  The deterministic ODE $\dot p = sp(1-p)$ is a good approximation except near the boundaries.
- $\lvert N_e s \rvert \ll 1$: drift dominates.  The allele is effectively neutral.
- $\lvert N_e s \rvert \sim 1$: both matter.  Nearly-neutral regime (more below).

The slogan "$N_e s \gtrsim 1$ for selection to be effective" is just the statement that the deterministic drift and the stochastic diffusion have the same magnitude at this threshold.  It's the SNR threshold of the selection-as-noisy-channel picture from my "Selection As Noisy Channel" post.

## Fixation Probability

*Kimura's formula.  One of the few exact closed-form results in the whole theory.*

Start with an allele at frequency $p_0$.  What is the probability it eventually reaches $p = 1$ (fixation) rather than $p = 0$ (loss)?  Both $p = 0$ and $p = 1$ are **absorbing states** (once you lose, you can't get it back without mutation; same for fixation).  Drift eventually pushes to one or the other.

### The derivation in one paragraph

Let $u(p)$ be the fixation probability starting from frequency $p$.  By the strong Markov property, $u(p)$ satisfies the **backward equation** (adjoint of the forward equation):

$$
\mu(p)\, u'(p) + \tfrac{1}{2} \sigma^2(p)\, u''(p) = 0.
$$

With boundary conditions $u(0) = 0$, $u(1) = 1$.  Plug in $\mu = s p(1-p)$, $\sigma^2 = p(1-p)/N_e$:

$$
s\, u'(p) + \frac{1}{2 N_e} u''(p) = 0.
$$

The $p(1-p)$ factored out.  Solution: $u''/u' = -2 N_e s$, so $u'(p) = C e^{-2 N_e s p}$, and integrating with boundary conditions:

$$
\boxed{\;u(p_0) = \frac{1 - e^{-2 N_e s \, p_0}}{1 - e^{-2 N_e s}}.\;}
$$

This is **Kimura's fixation formula** (Kimura 1962).  Note: I'm using the haploid convention.  For diploids with $2N$ alleles per locus, factors of $2N$ become $4N$; you'll see both versions in the literature.

### Limiting cases

**Neutral** ($N_e s \to 0$): expand the exponentials.  $u(p_0) \to p_0$.  A neutral allele fixes with probability equal to its current frequency.  This is the simplest possible result and it's exactly right.  For a new mutation ($p_0 = 1/N$) this is $u = 1/N$ (or $1/2N$ for diploids).

**Strongly favored** ($N_e s \gg 1$, $p_0$ small): $u \approx 1 - e^{-2 N_e s p_0}$.  For a single new copy ($p_0 = 1/N$), $u \approx 2s$ (for $s > 0$, $N_e \approx N$).  Even a very favorable allele is lost most of the time when it's new - drift kills the stochastic wave before selection can grab hold.  The factor of $2$ is from the haploid convention; it's famously $2s$ in Haldane's original paper for diploids in the weak-selection limit.

**Strongly disfavored** ($N_e s \ll -1$): $u \approx e^{-2 N_e \lvert s \rvert}$ for $p_0 = 1/N$.  Exponentially small.  Bad alleles basically never fix unless the population is tiny.

The shape of $u(p_0)$ as a function of $N_e s$ is the most important single picture in the subject: it's essentially a sigmoid in $N_e s$, steepest around $N_e s = 0$.  It quantifies the SNR threshold I keep harping on.

## Neutral Theory

*Kimura's move: most molecular variation is effectively neutral, drift is the dominant evolutionary force at the molecular level, and the substitution rate is independent of population size.*

### The claim

At the molecular level (DNA / protein sequences), most variation is either neutral or nearly so.  Strongly deleterious mutations are purged; strongly advantageous ones are rare.  What remains is a sea of near-neutral variants whose dynamics are dominated by drift, not selection.

This is Kimura's 1968 [neutral theory](https://www.nature.com/articles/217624a0).  It was controversial for decades and is now close to consensus for most of the genome, with important exceptions for coding regions under purifying selection.

### The arithmetic of substitution

Consider a haploid population of size $N$ with per-site mutation rate $\mu$ per generation.

- **New neutral mutations per generation**: each of $N$ individuals produces mutations at rate $\mu$ per site, so new mutations per generation is $N \mu$ per site.
- **Fixation probability of a neutral allele**: $1/N$ (it starts at frequency $1/N$ and, being neutral, fixes with probability equal to its frequency).
- **Substitution rate**: $N \mu \times 1/N = \mu$.

$$
\boxed{\;\text{substitution rate (neutral)} = \mu.\;}
$$

The population size cancels.  This is the **molecular clock**: neutral substitutions accumulate at a rate equal to the per-generation mutation rate, independent of $N$.

(For diploids the arithmetic is $2N\mu \times 1/(2N) = \mu$.  Same cancellation.)

### The molecular clock

If the mutation rate $\mu$ is constant across species and time, then neutral substitutions accumulate linearly with time.  The genetic distance between two species is then proportional to the time since their common ancestor - this is the **molecular clock** (Zuckerkandl and Pauling 1962, reinterpreted by Kimura).

Given two species with per-site divergence $d$ and mutation rate $\mu$ per generation, the time since divergence (in generations) is

$$
T \approx \frac{d}{2 \mu}
$$

(factor of 2 because divergence accumulates on both lineages).  For mammals this gives a mutation rate of $\sim 10^{-8}$ per site per generation, and divergence times that roughly match the fossil record.  It basically worked.

### When the clock breaks

The clock is a useful null, not a law.  It breaks in identifiable ways.

- **Selection**: coding regions and regulatory elements evolve slower than the neutral rate (purifying selection).  Some sites evolve faster (positive selection).  You can test for this by comparing synonymous (usually neutral) to nonsynonymous (usually selected) substitution rates: the $dN/dS$ or $K_a/K_s$ test.
- **Generation-time effects**: the clock ticks per generation, but we usually want a clock per year.  Species with short generation times accumulate substitutions faster per year.  Mice vs. elephants.
- **Mutation rate variation**: different species have different $\mu$.  Thermophiles, for example, have higher $\mu$ because DNA repair is harder at high temperatures.
- **Demographic fluctuations**: $N_e$ bottlenecks and expansions change which mutations are "effectively neutral" (see below), which distorts the clock at the margin.

The modern genomic clock is calibrated lineage-by-lineage and site-class-by-site-class.  "Neutral" is a model, not a fact.

### Ohta's nearly neutral theory

Kimura's original theory has a sharp boundary: alleles are either neutral ($\lvert N_e s \rvert \ll 1$) or selected ($\lvert N_e s \rvert \gg 1$).  In reality there's a continuum.  [Ohta's nearly neutral theory](https://www.nature.com/articles/246096a0) (1973, refined 1992) takes this seriously: many mutations have $\lvert N_e s \rvert \sim 1$, so their fate depends sensitively on $N_e$.

The key prediction: in **small populations** (small $N_e$), nearly neutral *deleterious* mutations are more likely to fix.  Small populations accumulate mildly deleterious mutations at a higher rate than large ones.  This predicts that the molecular clock is *faster* in species with small $N_e$, at least for functional sites - which is what's observed in, e.g., great apes (smaller $N_e$ than rodents) for coding sequences.

This matters for the error catastrophe / drift barrier story below.  If $N_e$ drops, your accumulated mutational load creeps up, and there's a hard limit below which a population can't maintain complex function.

## The Drift Barrier

*Selection can't refine what it can't resolve.  Adaptation has a floor at $1/N_e$.*

### The basic argument

Suppose you want to evolve a trait to its optimum.  Selection acts with effective strength $s$, drift with magnitude $1/N_e$.  For selection to "see" a refinement of size $\delta s$, you need $N_e \delta s \gtrsim 1$, i.e.

$$
\delta s_{\min} \sim \frac{1}{N_e}.
$$

Features of a phenotype that require selective differences smaller than this can't be resolved.  The organism looks "good enough" but not perfect: you expect $O(1/N_e)$ deviations from optimality.

The **drift barrier** is the resulting floor on how precisely natural selection can tune any quantitative feature.  In large populations (bacteria, $N_e \sim 10^9$) the barrier is very low; in small populations (mammals, $N_e \sim 10^4$) it's substantial.  Empirically, this predicts that bacteria have more "polished" molecular machinery than mammals, and at the level of codon usage, protein thermostability, and translational accuracy this seems to be true ([Lynch 2007](https://www.pnas.org/doi/10.1073/pnas.0701985104)).

### Mutational meltdown and error catastrophe

If $N_e$ is small enough *and* the deleterious mutation rate is high enough, mildly deleterious mutations fix faster than beneficial compensations can remove them.  The fitness of the population deteriorates stochastically - **Muller's ratchet**, in asexuals.  In the sexual case, recombination can reverse this; in asexuals, the ratchet is one-way.

Taken to an extreme (very high mutation rate, or $N_e$ too small), this causes **mutational meltdown**: the population fitness decreases until the population goes extinct.  This is the evolutionary version of [Eigen's error catastrophe](https://link.springer.com/article/10.1007/BF00623322) - above a critical mutation rate the "master sequence" can't be maintained by selection and the population disintegrates into a quasispecies cloud.

Both are instances of the same underlying fact: **selection has a finite informational throughput, and above a certain load it can't maintain structure**.  The drift barrier, Muller's ratchet, and Eigen's error catastrophe are the same phenomenon viewed through different parameters.

### Nonadaptive null hypothesis for complexity

Lynch has a provocative thesis: a lot of eukaryotic genomic complexity (introns, expanded gene regulatory networks, complex protein architectures) is the *consequence* of small $N_e$, not its cause.  In large-$N_e$ populations, selection strips away weakly deleterious architectural features as "bloat".  In small-$N_e$ populations, the drift barrier allows this bloat to persist and sometimes become co-opted into useful structure.

So complexity isn't necessarily adaptive; it can be neutral elaboration that later gets selected on.  This flips the usual "complexity is the product of selection" story on its head.  Whether you buy the full thesis or not, the drift barrier gives a specific, quantitative prediction for what complexity *looks* nonadaptive.

## Diffusion Stationary Distribution

*With mutation holding the fort against the absorbing boundaries, selection and drift settle into a characteristic equilibrium.*

Without mutation, every locus eventually hits $p = 0$ or $p = 1$ and stays there - the stationary distribution is a pair of delta functions at the absorbing boundaries.  Uninteresting.

Add **symmetric mutation** at rate $\mu$ per generation (both $A \to a$ and $a \to A$).  Now the boundaries aren't absorbing; there's a steady-state distribution of allele frequencies.  Working out the stationary solution to the Fokker-Planck equation (set $\partial_t P = 0$ and solve) gives [Wright's formula](https://www.genetics.org/content/16/2/97):

$$
P_{\text{stat}}(p) \propto e^{2 N_e s p}\, p^{4 N_e \mu - 1} (1 - p)^{4 N_e \mu - 1}.
$$

The exponential prefactor tilts toward the favored allele (selection); the power-law factors pile up probability near the boundaries for $4 N_e \mu < 1$ and near $p = 1/2$ for $4 N_e \mu > 1$.

For $4 N_e \mu \ll 1$ (low-mutation, typical of many eukaryotes), the stationary distribution is bimodal: most of the time the population is near-fixed for one allele or the other, with brief transitions between them.  Polymorphism is the exception.

For $4 N_e \mu \gg 1$ (high-mutation, typical of RNA viruses or very large populations), the distribution is centered and unimodal.  Polymorphism is the rule.

The quantity $\theta = 4 N_e \mu$ (or $2 N_e \mu$ for haploids) is called the **population-scaled mutation rate** and is the core parameter of coalescent theory.  The expected number of polymorphic sites in a sample scales linearly with $\theta$.  You can estimate $\theta$ from sequence data even when $N_e$ and $\mu$ are individually hard to pin down.

## Selection as Bayesian Update, Again

*Reweighting by fitness is Bayes.  Drift is the finite-sample version of that update.*

Briefly, to tie back to my other posts.

In the infinite-population limit, selection is Bayes:
$$
p_i' = \frac{p_i w_i}{\bar{w}}.
$$
(See "Natural Selection: Price to Lande" and "Probability as Operators" for more.)

In a finite population, you can't implement the posterior exactly - you can only draw $N_e$ samples from it.  So each generation you update the "ideal" posterior $q_i = p_i w_i / \bar{w}$, then approximate it with an empirical distribution built from $N_e$ draws:

$$
p_i^{(t+1)} = \frac{1}{N_e} \sum_{k=1}^{N_e} \mathbb{1}[\text{individual } k \text{ is type } i], \qquad \text{individuals drawn from } q.
$$

This is **sequential Monte Carlo on the simplex**, with Bayesian importance-reweighting as the correction step and multinomial resampling as the propagation step.  Drift is just the variance of the resampling estimator.

The Kimura diffusion equation is the continuum limit of this particle filter when $N_e$ is large and $s$ is small.  Saying "population genetics is a particle filter" isn't just cute; it's literally the algorithm being run by the biology.

## Everything Is Price, Including the Noise

*The Price equation survives the jump to finite populations.  It just has a stochastic residual.*

Here's a slogan I like: **the Price equation is still true, you just have to be careful about expectations**.

In a finite population, let $\mathbb{E}_{\text{drift}}$ be the expectation over the sampling step (Wright-Fisher variance).  Then the expected change in mean trait is

$$
\mathbb{E}_{\text{drift}}[\Delta \bar{z}] = \frac{\mathrm{Cov}(w, z)}{\bar{w}} + \frac{\mathbb{E}[w \Delta z]}{\bar{w}},
$$

exactly the Price equation, because sampling is unbiased in expectation.  The *realized* $\Delta \bar{z}$ has an additional stochastic component with variance

$$
\mathrm{Var}_{\text{drift}}(\Delta \bar{z}) = \frac{\mathrm{Var}_q(z)}{N_e}
$$

where $q$ is the post-selection distribution and $\mathrm{Var}_q(z) = \sum_i q_i z_i^2 - (\sum_i q_i z_i)^2$.  So finite-population evolution is deterministic Price plus a Gaussian noise term of width $\sqrt{\mathrm{Var}_q(z) / N_e}$ per generation.

This decomposition matters.  In Fisher-style arguments you often want to separate "what selection is trying to do" from "what drift is undoing".  The Price equation gives you the former for free; the variance formula above gives you the latter.

## Synthesis: The Informational Resolution of Selection

*All the results above are aspects of one fact: $N_e$ is the bandwidth, $1/(N_e s)$ is the resolution.*

### The information-theoretic frame

The channel capacity view of finite-population selection (developed in my "Selection As Noisy Channel" post) says:

$$
C \approx \tfrac{1}{2} \ln(1 + N_e \cdot \mathrm{Var}(\ln w)) \quad \text{nats per generation}.
$$

This is the per-generation throughput of selection as a communication channel from environment to population.  Everything in this post is a consequence.

- **Neutral theory**: when $N_e \cdot \mathrm{Var}(\ln w) \lesssim 1$, the channel is below capacity and noise (drift) dominates.  Substitutions that do happen go through at the mutation rate, independent of $N$.
- **Molecular clock**: the channel noise floor is $1/N_e$, so variation that falls below this floor accumulates deterministically at rate $\mu$.
- **Drift barrier**: features of a phenotype that require adaptive resolution finer than $1/N_e$ can't be maintained.  Adaptation has a floor.
- **Haldane's cost**: per substitution, you pay $-\ln p_0$ nats of information (from the companion seed).  Total rate of adaptive substitution is capacity / cost-per-sub.  Population size buys you bandwidth, not rate directly.
- **Error catastrophe**: if the per-generation mutational load exceeds capacity, selection can't maintain the existing information state.  Population disintegrates.

Read this way, the central dogma of population genetics is just Shannon's theorem with a specific channel model.  This is the spirit of [Frank's papers](https://arxiv.org/abs/1211.4037) on information-theoretic evolution; I think it's the right way to teach the subject.

### The scale $1/(N_e s)$ is fundamental

The dimensionless quantity $N_e s$ is the one scaled parameter of the diffusion theory; $1/(N_e s)$ is its inverse, the *resolution*.  Concrete slogans:

- Fitness differences smaller than $1/N_e$ are invisible.
- Alleles whose scaled advantage $N_e s$ exceeds $\sim 1$ are on the selective side of the ledger; those below are effectively neutral.
- Adaptations with per-step selective benefit $< 1/N_e$ can't climb.
- The stationary variance of frequencies under mutation-drift-selection is governed by $4 N_e \mu$ (polymorphism) and $2 N_e s$ (selection bias).

Every empirically interesting question reduces to "where does this sit relative to $1/N_e$?"

### When drift "resolves"

The word "resolves" cuts both ways.

From the selection side: drift *destroys* resolution.  Selection would like to refine arbitrarily; drift washes out refinements smaller than $1/N_e$.

From the state side: drift *resolves* polymorphism.  Without mutation input, drift drives each locus toward fixation - $p \to 0$ or $p \to 1$.  In this sense drift is a resolution mechanism too, it just picks the fixation state stochastically.  [Ewens sampling formula](https://doi.org/10.1016/0040-5809(72)90035-4) and the coalescent are the exact theory of this "resolution by drift".

These are two sides of the same coin.  Drift is stochastic fluctuation that both blurs selective refinement and collapses polymorphism toward absorbing states.  The combined effect is that finite populations can only maintain information at scales above $1/N_e$, and the steady-state "informational repertoire" of the population is bounded.

## What's Next

Pointers beyond.

- **Coalescent theory**: the backward-time dual of Wright-Fisher.  Genealogies of samples from a population, with branch lengths scaling as $N_e$.  The generator of half of modern population genetics and the natural framework for statistical inference from sequence data.  [Kingman 1982](https://doi.org/10.1016/0304-4149(82)90011-4) is the original; Wakeley's textbook is the standard reference.
- **Diffusion on the full simplex**: with $n > 2$ alleles, the state space is the simplex, the diffusion is the Wright-Fisher diffusion in multiple dimensions, and the geometry is (again) Fisher / Shahshahani.  The replicator equation with stochasticity is the natural continuous limit of multi-allele selection-drift.
- **Spatial and structured populations**: once you add spatial structure, $N_e$ becomes an effective quantity that depends on migration rates.  "Effective population size" is a pragmatic concept, and there are many ways to measure it (inbreeding, variance, coalescent, etc.) that all agree in simple cases but can diverge.
- **Multilevel selection and the evolution of evolvability**: how the architecture of variation itself evolves.  The $G$-matrix in the Lande framework is not fixed; on long timescales it responds to persistent directional selection and to the drift-mutation balance.  See [Pavlicev and Hansen](https://onlinelibrary.wiley.com/doi/10.1111/j.1558-5646.2011.01258.x) and references therein.
- **Selectionist theories of learning**: much of my interest in all this is whether selectionist dynamics can model how structured computation emerges in neural networks.  The drift barrier analog for a learner would be something like a minimum SNR for SGD to resolve a structural feature - a compute vs. data vs. model-capacity trade-off.  I'm still working this out.

Please clap.

*Written with Claude.*
